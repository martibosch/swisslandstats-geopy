"""Land data frame."""

import io

import numpy as np
import pandas as pd
import rasterio as rio
import requests
import requests_cache
import xarray as xr
from rasterio import transform
from rasterio.crs import CRS

from . import geometry as sls_geometry
from . import plotting, settings, utils

__all__ = ["LandDataFrame", "merge", "read_csv", "from_url"]

_merge_doc = """
Merges LandDataFrame objects.

The default parameter values will do an outer join using the indices of both dataframes
as join keys, and will avoid duplicating columns. See also the documentation for
`pandas.merge`

Parameters
----------%s
right : LandDataFrame
duplicate_columns : boolean, default False
how : {'left', 'right', 'outer', 'inner'}, default 'outer'
    parameter passed to `pandas.merge`
left_index : boolean, default True
    parameter passed to `pandas.merge`
right_index : boolean, default True
    parameter passed to `pandas.merge`
**kwargs : additional kewyord arguments passed to `pandas.merge`

Returns
-------
result : LandDataFrame
"""


class LandDataFrame(pd.DataFrame):
    """
    Land data frame.

    A LandDataFrame object is a pandas.DataFrame extended to deal with the land
    statistics files provided by the Swiss Federal Statistical Office (SFSO). Each row
    of a LandDataFrame represents a pixel of a raster landscape, with the 'x' and 'y'
    that depict the centroid of the pixel, as well as a set of data columns.
    """

    # so that pandas can allow setting this class attributes
    _metadata = ["x_column", "y_column", "crs", "res"]

    # index_column = settings.DEFAULT_INDEX_COLUMN

    def __init__(
        self,
        data,
        *,
        index_column=None,
        x_column=None,
        y_column=None,
        crs=None,
        res=None,
        **df_init_kwargs,
    ):
        """
        Initialize the land data frame instance.

        The default parameters are defined to work with SFSO data out-of-the-box, but
        they can be modified through the following keyword arguments:

        Parameters
        ----------
        data : ndarray (structured or homogeneous), Iterable, dict or DataFrame
            Data that will be passed to the initialization method of `pd.DataFrame`.
        index_column : str, optional
            Label of the index column. If `None` is provided, the value set in
            `settings.DEFAULT_INDEX_COLUMN` will be taken.
        x_column : str, optional
            Label of the x-coordinates column. If `None` is provided, the value set in
            `settings.DEFAULT_X_COLUMN` will be taken.
        y_column : str, optional
            Label of the y-coordinates column. If `None` is provided, the value set in
            `settings.DEFAULT_Y_COLUMN` will be taken.
        crs : str or rasterio CRS, optional
            Coordinate reference system, as string or as rasterio CRS object. If a
            string is provided, it will be passed to `rasterio.crs.CRS.from_string` to
            instantiatie a rasterio CRS object. If `None` is provided, the value set in
            `settings.DEFAULT_CRS` will be taken.
        res : tuple, optional
            The (x, y) resolution of the dataset. If `None` is provided, the value set
            in `settings.DEFAULT_RES` will be taken.
        df_init_kwargs : dict-like
            Keyword arguments to be passed to `pandas.DataFrame.__init__`.
        """
        # init the pandas dataframe
        super().__init__(data, **df_init_kwargs)

        # set the index
        if index_column is None:
            index_column = settings.DEFAULT_INDEX_COLUMN
        if self.index.name != index_column:
            try:
                self.index = self[index_column]
                self.drop(columns=index_column, inplace=True)
            except KeyError:
                utils.log(
                    "Ignoring attempt to set non-existent "
                    f"{index_column} column as index",
                )

        # set the rest of attributes
        if x_column is None:
            x_column = settings.DEFAULT_X_COLUMN
        if y_column is None:
            y_column = settings.DEFAULT_Y_COLUMN
        if crs is None:
            crs = CRS.from_string(settings.DEFAULT_CRS)
        elif isinstance(crs, str):
            crs = CRS.from_string(crs)
        if res is None:
            res = settings.DEFAULT_RES

        self.x_column = x_column
        self.y_column = y_column
        self.crs = crs
        self.res = res

    def get_transform(self):
        """
        Get the affine transform of the current land data frame.

        Returns
        -------
        transform : Affine
        """
        x = self[self.x_column].values
        y = self[self.y_column].values

        xres, yres = self.res

        x_origin = min(x) - xres // 2
        y_origin = max(y) + yres // 2
        return transform.from_origin(x_origin, y_origin, xres, yres)

    def _to_ndarray(self, column, i, j, nodata, dtype):
        arr = np.full((i.max() + 1, j.max() + 1), nodata, dtype=dtype)
        arr[-i, j] = np.where(self[column].isna(), nodata, self[column])
        return arr

    def to_ndarray(self, column, *, nodata=0, dtype="uint8"):
        """
        Convert a data column to a numpy array.

        Parameters
        ----------
        column : str
            name of the data column.
        nodata : numeric, default 0
            value to be assigned to pixels with no data.
        dtype : str or numpy dtype, default uint8
            the data type.

        Returns
        -------
        arr : np.ndarray
            A raster array.
        """
        x = self[self.x_column].values
        y = self[self.y_column].values

        xres, yres = self.res
        i = (y - min(y)) // yres
        j = (x - min(x)) // xres

        return self._to_ndarray(column, i, j, nodata, dtype)

    def to_xarray(self, columns, *, dim_name="time", nodata=0, dtype="uint8"):
        """
        Convert a data column to a xarray data array.

        Parameters
        ----------
        columns : str or list of str
            name or names of the data columns.
        dim_name : str, default time
            name of the outermost dimension set by the `columns` argument.
        nodata : numeric, default 0
            value to be assigned to pixels with no data.
        dtype : str or numpy dtype, default uint8
            the data type.

        Returns
        -------
        da : xr.DataArray
            A xarray data array.
        """
        x = self[self.x_column].values
        y = self[self.y_column].values

        xres, yres = self.res
        i = (y - min(y)) // yres
        j = (x - min(x)) // xres

        # ensure that `columns` is a list
        if isinstance(columns, str):
            columns = [columns]
        # use a head-tail iteration pattern to get the array shape and prepare
        # the pixel coordinates
        arr = self._to_ndarray(columns[0], i, j, nodata, dtype)
        num_rows, num_cols = arr.shape
        _transform = self.get_transform()
        cols = np.arange(num_cols)
        rows = np.arange(num_rows)
        x_coords, _ = transform.xy(_transform, cols, cols)
        _, y_coords = transform.xy(_transform, rows, rows)

        return xr.DataArray(
            [arr]
            + [self._to_ndarray(column, i, j, nodata, dtype) for column in columns[1:]],
            dims=[dim_name, self.y_column, self.x_column],
            coords={
                self.x_column: x_coords,
                self.y_column: y_coords,
                dim_name: columns,
            },
            attrs=dict(nodata=nodata, pyproj_srs=f"epsg:{self.crs.to_epsg()}"),
        )

    def to_geotiff(self, fp, column, *, nodata=0, dtype="uint8"):
        """
        Export a data column to a GeoTIFF file.

        Parameters
        ----------
        fp : str, file object or pathlib.Path object
            A filename or URL, a file object opened in binary ('rb') mode, or a Path
            object.
        column : str
            name of the data column.
        nodata : numeric, default 0
            value to be assigned to pixels with no data.
        dtype : str or numpy dtype, default
            the data type.
        """
        arr = self.to_ndarray(column, nodata=nodata, dtype=dtype)

        with rio.open(
            fp,
            "w",
            driver="GTiff",
            height=arr.shape[0],
            width=arr.shape[1],
            count=1,
            dtype=str(dtype),
            nodata=0,
            crs=self.crs,
            transform=self.get_transform(),
        ) as raster:
            raster.write(arr.astype(dtype), 1)

    def plot(  # noqa: D102
        self,
        column,
        *,
        cmap=None,
        legend=False,
        figsize=None,
        ax=None,
        **show_kwargs,
    ):
        # TODO: automatically assign cmaps according to columns
        arr = self.to_ndarray(column)
        return plotting.plot_ndarray(
            arr,
            transform=self.get_transform(),
            cmap=cmap,
            legend=legend,
            figsize=figsize,
            ax=ax,
            **show_kwargs,
        )

    plot.__doc__ = plotting._plot_ndarray_doc % (
        "column",
        "\ncolumn : str\n    data column to display",
    )

    def clip_by_geometry(self, geometry, *, geometry_crs=None):  # noqa: D102
        return sls_geometry.clip_by_geometry(self, geometry, geometry_crs=geometry_crs)

    clip_by_geometry.__doc__ = sls_geometry._clip_by_geometry_doc % ""

    def clip_by_nominatim(self, query, *, which_result=1):  # noqa: D102
        return sls_geometry.clip_by_nominatim(self, query, which_result=which_result)

    clip_by_nominatim.__doc__ = sls_geometry._clip_by_nominatim_doc % ""

    # pandas methods
    def __getitem__(self, key):  # noqa: D105
        result = super().__getitem__(key)
        if isinstance(result, pd.DataFrame):
            # TODO: check that there is at least one column of land statistics
            if self.x_column in result and self.y_column in result:
                result.__class__ = LandDataFrame
                result.crs = self.crs
                result.res = self.res
            else:
                result.__class__ = pd.DataFrame
        return result

    def merge(  # noqa: D102
        self,
        right,
        *,
        duplicate_columns=False,
        how="outer",
        left_index=True,
        right_index=True,
        **kwargs,
    ):
        return merge(
            self,
            right,
            duplicate_columns=duplicate_columns,
            how=how,
            left_index=left_index,
            right_index=right_index,
            **kwargs,
        )

    merge.__doc__ = _merge_doc % ""

    @property
    def _constructor(self):
        return LandDataFrame

    # geopandas
    def get_geoseries(self):
        """Get geometry as geopandas geo-series.

        Returns
        -------
        geoseries : geopandas.GeoSeries
        """
        return sls_geometry.get_geoseries(self)

    get_geoseries.__doc__ = sls_geometry._get_geoseries_doc % ""

    def to_geodataframe(self, *, drop_xy_columns=True):
        """Convert to geopandas geo-dataframe.

        Parameters
        ----------
        drop_xy_columns : bool, default True
            whether the LandDataFrame x and y columns should be deleted from the
            geopandas GeoDataFrame.

        Returns
        -------
        geodataframe : geopandas.GeoDataFrame
        """
        return sls_geometry.to_geodataframe(self, drop_xy_columns=drop_xy_columns)

    to_geodataframe.__doc__ = sls_geometry._to_geodataframe_doc % ""


def merge(  # noqa: D103
    left,
    right,
    *,
    duplicate_columns=False,
    how="outer",
    left_index=True,
    right_index=True,
    **kwargs,
):
    if duplicate_columns:
        _right = right
    else:
        _right = right[right.columns.difference(left.columns)]

    return pd.merge(
        left,
        _right,
        how=how,
        left_index=left_index,
        right_index=right_index,
        **kwargs,
    )


merge.__doc__ = _merge_doc % "\nleft : LandDataFrame"


def read_csv(
    filepath_or_buffer,
    *,
    index_column=None,
    x_column=None,
    y_column=None,
    sep=None,
    crs=None,
    res=None,
    read_csv_kwargs=None,
    df_init_kwargs=None,
):
    """
    Read a CSV file into a LandDataFrame.

    See also the documentation for `pandas.read_csv`.

    Parameters
    ----------
    filepath_or_buffer : str, pathlib.Path, py._path.local.LocalPath or any \
    object with a read() method (such as a file handle or StringIO)
        The string could be a URL. Valid URL schemes include http, ftp, s3, and
        file. For file URLs, a host is expected. For instance, a local file
        could be file://localhost/path/to/table.csv
    index_column : str, optional
        Label of the index column. If `None` is provided, the value set in
        `settings.DEFAULT_INDEX_COLUMN` will be taken.
    x_column : str, optional
        Label of the x-coordinates column. If `None` is provided, the value
        set in `settings.DEFAULT_X_COLUMN` will be taken.
    y_column : str, optional
        Label of the y-coordinates column. If `None` is provided, the value
        set in `settings.DEFAULT_Y_COLUMN` will be taken.
    sep: str, optional
        Delimiter to use. If `None` is provided, the value set in `settings.DEFAULT_SEP`
        will be taken.
    crs : rasterio CRS, optional
        Coordinate reference system, as a rasterio CRS object. If `None` is
        provided, the value set in `settings.DEFAULT_CRS` will be taken.
    res : tuple, optional
        The (x, y) resolution of the dataset. If `None` is provided, the value
        set in `settings.DEFAULT_RES` will be taken.
    read_csv_kwargs : dict-like, optional
        Keyword arguments to be passed to `pandas.read_csv`, except `sep`.
    df_init_kwargs : dict-like, optional
        Keyword arguments to be passed to `LandDataFrame.__init__`

    Returns
    -------
    result : LandDataFrame
    """
    if read_csv_kwargs is None:
        read_csv_kwargs = {}
    # remove the `sep` parameter from the kwargs
    _read_csv_kwargs = read_csv_kwargs.copy()
    _read_csv_kwargs.pop("sep", None)
    if sep is None:
        sep = settings.DEFAULT_SEP
    df = pd.read_csv(filepath_or_buffer, sep=sep, **read_csv_kwargs)

    if df_init_kwargs is None:
        df_init_kwargs = {}
    return LandDataFrame(
        df,
        crs=crs,
        res=res,
        index_column=index_column,
        x_column=x_column,
        y_column=y_column,
        **df_init_kwargs,
    )


def from_url(*, url=None, **read_csv_kwargs):
    """
    Read a CSV file from a URL into a LandDataFrame.

    Parameters
    ----------
    url : str, optional
        The URL of the file. If `None` is provided, the value set in `settings.SLS_URL`
        will be taken.
    **read_csv_kwargs : dict-like
        Keyword arguments to be passed to `pandas.read_csv`.

    Returns
    -------
    ldf : LandDataFrame
    """
    if url is None:
        url = settings.LATEST_SLS_URL
    if read_csv_kwargs is None:
        read_csv_kwargs = {}
    if settings.USE_CACHE:
        session = requests_cache.CachedSession(
            cache_name=settings.CACHE_NAME,
            backend=settings.CACHE_BACKEND,
            expire_after=settings.CACHE_EXPIRE,
        )
    else:
        session = requests.Session()

    response = session.get(url)
    return read_csv(
        io.StringIO(response.content.decode(response.encoding)), **read_csv_kwargs
    )
