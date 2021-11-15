"""swisslandstats tests."""

import swisslandstats as sls


def test_base_imports():
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import rasterio
    import xarray as xr
    from matplotlib import colors
    from rasterio import transform
    from rasterio.crs import CRS


def test_geo_imports():
    from functools import partial

    import geopandas as gpd
    import osmnx as ox
    import pyproj
    from shapely.geometry import Point
    from shapely.ops import transform


def test_slsdataframe():
    import tempfile

    import matplotlib.pyplot as plt
    import numpy as np
    import osmnx as ox
    import pandas as pd
    import xarray as xr
    from rasterio.crs import CRS

    plt.switch_backend("agg")  # only for testing purposes

    # test instantiation
    for crs in [None, "epsg:2056", CRS.from_string("epsg:2056")]:
        assert isinstance(sls.read_csv("tests/input_data/dataset.csv").crs, CRS)

    # test basic features and pandas-like transformations
    ldf = sls.read_csv("tests/input_data/dataset.csv")
    assert np.all(
        ldf.to_ndarray("AS09_4") == np.arange(4, dtype=np.uint8).reshape(2, 2)
    )
    ldf.to_geotiff(tempfile.TemporaryFile(), "AS09_4")

    # test plots
    assert isinstance(ldf.plot("AS09_4", cmap=sls.noas04_4_cmap, legend=True), plt.Axes)
    # test noas04_4_cmap. TODO: DRY this test??
    arr = ldf.to_ndarray("AS18_4")
    # if we do not use the `norm` arg and there is no "nodata" value in our land data
    # frame, the "nodata" color will actually be assigned to an actual valid color
    ax_no_norm = ldf.plot("AS18_4", cmap=sls.noas04_4_cmap)
    im_no_norm = ax_no_norm.get_images()[0]
    assert np.all(
        im_no_norm.cmap(im_no_norm.norm(np.unique(arr)))[0]
        == sls.plotting._nodata_color
    )
    # instead, when we use the `norm` arg, the colors are properly assigned
    ax_norm = ldf.plot("AS18_4", cmap=sls.noas04_4_cmap, norm=sls.noas04_4_norm)
    im_norm = ax_norm.get_images()[0]
    assert np.all(
        im_norm.cmap(im_norm.norm(np.unique(arr)))[0] != sls.plotting._nodata_color
    )

    # test data frame types
    assert type(ldf[[ldf.x_column, ldf.y_column, "AS09_4"]]) == sls.LandDataFrame
    assert type(ldf[[ldf.x_column, "AS09_4"]]) == pd.DataFrame
    assert type(ldf["AS09_4"]) == pd.Series

    # create dataframe with another dummy land statistics column, but with one
    # row less and test merge (should fill the missing row with a nan)
    ldf2 = ldf.copy()
    ldf2["AS85_4"] = pd.Series(1, index=ldf.index[:-1], name="AS85_4")
    ldf2 = ldf2.drop("AS09_4", axis=1)
    merged_ldf = ldf.merge(ldf2)

    assert "AS85_4" in merged_ldf.columns.difference(ldf.columns)
    # to test for the presence of nan: merged_ldf['AS85_4'].isna().any()
    assert np.sum(merged_ldf["AS85_4"].isna()) == 1

    # test that `get_transform` returns a different transform if, e.g., we
    # change the min x or max y value
    assert ldf.get_transform() != ldf.iloc[:2].get_transform()

    # test export to xarray
    ldf = sls.read_csv("tests/input_data/dataset.csv")
    ldf["AS85_4"] = pd.Series(1, index=ldf.index[:-1], name="AS85_4")
    columns = ["AS85_4", "AS09_4"]
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


def test_geometry():
    import geopandas as gpd
    from shapely.geometry import Polygon

    ldf = sls.read_csv("tests/input_data/dataset.csv")

    # geopandas exports
    gser = ldf.get_geoseries()
    assert type(gser) == gpd.GeoSeries
    assert len(ldf) == len(gser)
    assert ldf.crs == gser.crs

    gdf = ldf.to_geodataframe()
    assert type(gdf) == gpd.GeoDataFrame
    assert len(ldf) == len(gdf)
    assert ldf.x_column not in gdf.columns and ldf.y_column not in gdf.columns
    assert ldf.crs == gdf.crs

    # clip methods
    geometry = Polygon([(0, 0), (0, 150), (150, 150), (150, 0)])

    clipped_ldf = ldf.clip_by_geometry(geometry)
    assert len(clipped_ldf) == 1

    clipped_ldf = ldf.clip_by_nominatim("Lausanne, Switzerland")
    assert len(clipped_ldf) == 0
