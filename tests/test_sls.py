"""swisslandstats tests."""

import logging as lg
import tempfile
import unittest
from os import path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pooch
import pytest
import responses
import xarray as xr
from rasterio.crs import CRS

import swisslandstats as sls
from swisslandstats import settings, utils

MOCK_DATASET_DIR = "tests/input_data"
MOCK_EXT_DICT = {
    "sls": "csv",
    "bds": "zip",
    "statent": "zip",
}
MOCK_KNOWN_HASH_DICT = {
    "sls": "4f7a0cb33fbde048ed20d7bf7259d8c9658c1c2e9e4956f203a87487df106eb2",
    "bds": "e6732e7c972dc0905e419470d81aa92532f9467488b6bf70c3e756234f5827f9",
    "statent": "b8e0931d1ff547fdbf8a7d2fd6777b0c5711136855f1b79c18f19f5937dcd30d",
}
plt.switch_backend("agg")  # only for testing purposes


class TestSwissLandStats(unittest.TestCase):
    def setUp(self):
        self.dataset_dict = settings.DATASET_DICT.copy()

    def _test_dataset(self, dataset_key):
        dataset_latest = self.dataset_dict[dataset_key]["latest"]
        dataset_item = self.dataset_dict[dataset_key][dataset_latest]
        retrieve_kwargs = {
            "known_hash": dataset_item["known_hash"],
        }
        if dataset_item["zip"]:
            retrieve_kwargs["processor"] = pooch.Unzip(
                members=[dataset_item["members"]]
            )
            which_member = dataset_item["which_member"]
        else:
            which_member = None

        # test instantiation
        for ldf in [
            sls.load_dataset(dataset_key),
            sls.load_dataset(dataset_key=dataset_key),
            sls.load_dataset(dataset_key=dataset_key, year=dataset_latest),
            sls.load_dataset(
                url=dataset_item["url"],
                retrieve_kwargs=retrieve_kwargs,
                which_member=which_member,
                **dataset_item["read_csv_kwargs"],
            ),
        ]:
            assert isinstance(ldf, sls.LandDataFrame)
            # test crs
            assert isinstance(ldf.crs, CRS)

        # try that setting an inexistent column as index should not raise a KeyError
        # because it is caught, but it can raise a ValueError if the dataset has
        # a non-empty default "columns" arg
        if "columns" in dataset_item["read_csv_kwargs"]:
            with pytest.raises(ValueError):
                sls.load_dataset(dataset_key, index_column="inexistent_column")
        else:
            # the KeyError is caught and a warning is issued in the logs
            sls.load_dataset(dataset_key, index_column="inexistent_column")

        # try that filtering columns returns at most the same number of columns
        assert (
            sls.load_dataset(
                dataset_key,
                columns=[settings.DEFAULT_INDEX_COLUMN]
                + [
                    dataset_item["read_csv_kwargs"].get(coord_col, default)
                    for coord_col, default in zip(
                        ["x_column", "y_column"],
                        [settings.DEFAULT_X_COLUMN, settings.DEFAULT_Y_COLUMN],
                    )
                ],
            ).shape[1]
            <= ldf.shape[1]
        )

        # now test geometry
        # geopandas exports
        gser = ldf.get_geoseries()
        assert isinstance(gser, gpd.GeoSeries)
        assert len(ldf) == len(gser)
        assert ldf.crs == gser.crs

        gdf = ldf.to_geodataframe()
        assert isinstance(gdf, gpd.GeoDataFrame)
        assert len(ldf) == len(gdf)
        assert ldf.x_column not in gdf.columns and ldf.y_column not in gdf.columns
        assert ldf.crs == gdf.crs

        return ldf

    def test_statpop(self):
        # test that calling `load_dataset` without a dataset key raises an error
        with pytest.raises(ValueError):
            sls.load_dataset()

        # test loading the actual dataset (no mocking) for statpop only (smaller)
        ldf = self._test_dataset("statpop")

        # only test clipping with nominatim here because (i) we are not mocking requests
        # (ii) it is an actual dataset so we will clip something
        clipped_ldf = ldf.clip_by_nominatim("Lausanne, Switzerland")
        assert len(clipped_ldf) > 0

    @responses.activate
    def test_others(self):
        other_datasets = set(self.dataset_dict.keys()) - {"statpop"}
        # configure request mocking except for statpop
        for dataset_key in other_datasets:
            _latest_sls_key = self.dataset_dict[dataset_key]["latest"]
            with open(
                path.join(
                    MOCK_DATASET_DIR, f"{dataset_key}.{MOCK_EXT_DICT[dataset_key]}"
                ),
                "rb",
            ) as src:
                responses.add(
                    responses.GET,
                    self.dataset_dict[dataset_key][_latest_sls_key]["url"],
                    body=src.read(),
                    status=200,
                    stream=True,
                )
            self.dataset_dict[dataset_key][_latest_sls_key]["known_hash"] = (
                MOCK_KNOWN_HASH_DICT[dataset_key]
            )

        # test all the other datasets
        for dataset_key in other_datasets:
            _ = self._test_dataset(dataset_key)

        # now test basic features and pandas-like transformations with the SLS dataset
        # only test it with SLS because of the specific land use columns
        ldf = sls.load_dataset(dataset_key="sls")
        # assert np.all(
        #     ldf.to_ndarray("LU09_4") == np.arange(4, dtype=np.uint8).reshape(2, 2)
        # )
        ldf.to_geotiff(tempfile.TemporaryFile(), "LU09_4")

        # test plots
        assert isinstance(
            ldf.plot("LU09_4", cmap=sls.noas04_4_cmap, legend=True), plt.Axes
        )
        # test noas04_4_cmap. TODO: DRY this test??
        # arr = ldf.to_ndarray("LU18_4")
        # if we do not use the `norm` arg and there is no "nodata" value in our land
        # data frame, the "nodata" color will actually be assigned to an actual valid
        # color
        ldf.plot("LU18_4", cmap=sls.noas04_4_cmap)
        # instead, when we use the `norm` arg, the colors are properly assigned
        ldf.plot("LU18_4", cmap=sls.noas04_4_cmap, norm=sls.noas04_4_norm)

        # test data frame types
        assert isinstance(
            ldf[[ldf.x_column, ldf.y_column, "LU09_4"]], sls.LandDataFrame
        )
        assert isinstance(ldf[[ldf.x_column, "LU09_4"]], pd.DataFrame)
        assert isinstance(ldf["LU09_4"], pd.Series)

        # create dataframe with another dummy land statistics column, but with one
        # row less and test merge (should fill the missing row with a nan)
        ldf2 = ldf.copy()
        ldf2["LU00"] = pd.Series(1, index=ldf.index[:-1], name="LU00")
        # ldf2 = ldf2.drop("LU85_4", axis=1)
        merged_ldf = ldf.merge(ldf2)

        assert "LU00" in merged_ldf.columns.difference(ldf.columns)
        # to test for the presence of nan: merged_ldf['LU85_4'].isna().any()
        assert np.sum(merged_ldf["LU00"].isna()) == 1

        # test that `get_transform` returns a different transform if, e.g., we
        # change the min x or max y value
        assert ldf.get_transform() != ldf.iloc[:2].get_transform()

        # test export to xarray
        # ldf = sls.read_csv(path.join(MOCK_DATASET_DIR, "sls.csv"))
        ldf["LU85_4"] = pd.Series(1, index=ldf.index[:-1], name="LU85_4")
        columns = ["LU85_4", "LU09_4"]
        assert isinstance(ldf.to_xarray(columns), xr.DataArray)
        # test that columns are the outermost dimension
        assert ldf.to_xarray(columns).shape[0] == len(columns)
        num_cols = 1
        assert ldf.to_xarray(columns[:num_cols]).shape[0] == num_cols
        # test that the name of the outermost dimension is set
        dim_name = "survey"
        da = ldf.to_xarray(columns, dim_name=dim_name)
        assert dim_name in da.dims
        assert np.all(da.coords[dim_name] == columns)
        # test that the data array metadata is set
        nodata = 255
        attrs = ldf.to_xarray(columns, nodata=nodata).attrs
        assert attrs["nodata"] == nodata
        assert "pyproj_srs" in attrs
        # test that the data array has the proper dtype
        dtype = "uint16"
        assert ldf.to_xarray(columns, dtype=dtype).dtype == dtype


def test_logging():
    # enable logging to both console and file to bump test coverage
    settings.LOG_CONSOLE = True
    settings.LOG_FILE = True

    utils.log("test a fake default message")
    utils.log("test a fake debug", level=lg.DEBUG)
    utils.log("test a fake info", level=lg.INFO)
    utils.log("test a fake warning", level=lg.WARNING)
    utils.log("test a fake error", level=lg.ERROR)

    utils.ts(style="iso8601")
    utils.ts(style="date")
    utils.ts(style="time")
