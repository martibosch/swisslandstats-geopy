from __future__ import division

import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_origin

from . import geometry as sls_geometry
from . import plotting, settings

__all__ = ['LandDataFrame', 'merge', 'read_csv']

_merge_doc = """
Merges LandDataFrame objects
The default parameter values will do an outer join using the indices of both
dataframes as join keys, and will avoid duplicating columns.
See also the documentation for `pandas.merge`

Parameters
----------%s
right : LandDataFrame
duplicate_columns : boolean, default True
how : {'left', 'right', 'outer', 'inner'}, default 'outer'
    parameter passed to `pandas.merge`
left_index : boolean, default True
    parameter passed to `pandas.merge`
right_index : boolean, default True
    parameter passed to `pandas.merge`
**kwargs : additional keyord arguments passed to `pandas.merge`

Returns
-------
result : LandDataFrame
"""


class LandDataFrame(pd.DataFrame):
    """
    A LandDataFrame object is a pandas.DataFrame extended to deal with the land
    statistics files provided by the Swiss Federal Statistical Office (SFSO).
    Each row of a SLSDataFrame represents a pixel of a raster landscape, with
    the 'x' and 'y' that depict the centroid of the pixel, as well as a set of
    land use/land cover (LULC) information columns.

    The default parameters are defined to work with SFSO data out-of-the-box,
    but they can be modified through the following keyword arguments:

    Parameters
    ----------
    data : ndarray (structured or homogeneous), Iterable, dict or DataFrame
        Data that will be passed to the initialization method of `pd.DataFrame`
    index_column : str, optional
        Label of the index column. If `None` is provided, the value set in
        `settings.DEFAULT_INDEX_COLUMN` will be taken.    
    x_column : str, optional
        Label of the x-coordinates column. If `None` is provided, the value
        set in `settings.DEFAULT_X_COLUMN` will be taken.    
    y_column : str, optional
        Label of the y-coordinates column. If `None` is provided, the value
        set in `settings.DEFAULT_Y_COLUMN` will be taken.    
    crs : rasterio CRS, optional
        Coordinate reference system, as a rasterio CRS object. If `None` is
        provided, the value set in `settings.DEFAULT_CRS` will be taken.
    res : tuple, optional
        The (x, y) resolution of the dataset. If `None` is provided, the value
        set in `settings.DEFAULT_RES` will be taken.
    """

    # so that pandas can allow setting this class attributes
    _metadata = ['x_column', 'y_column', 'crs', 'res']

    # index_column = settings.DEFAULT_INDEX_COLUMN

    def __init__(self, data, index_column=None, x_column=None, y_column=None,
                 crs=None, res=None, **df_init_kws):
        # init the pandas dataframe
        super(LandDataFrame, self).__init__(data, **df_init_kws)

        # set the index
        if index_column is None:
            index_column = settings.DEFAULT_INDEX_COLUMN
        if self.index.name != index_column:
            self.set_index(index_column, inplace=True)

        # set the rest of attributes
        if x_column is None:
            x_column = settings.DEFAULT_X_COLUMN
        if y_column is None:
            y_column = settings.DEFAULT_Y_COLUMN
        if crs is None:
            crs = settings.DEFAULT_CRS
        if res is None:
            res = settings.DEFAULT_RES

        self.x_column = x_column
        self.y_column = y_column
        self.crs = crs
        self.res = res

    def get_transform(self):
        x = self[self.x_column].values
        y = self[self.y_column].values

        xres, yres = self.res

        x_origin = min(x) - xres // 2
        y_origin = max(y) + yres // 2
        return from_origin(x_origin, y_origin, xres, yres)

    def to_ndarray(self, column, nodata=0, dtype=np.uint8):
        """
        Convert a LULC column to a numpy array

        Parameters
        ----------
        column : str
            name of the LULC column
        nodata : numeric
            value to be assigned to pixels with no data
        dtype : str or numpy dtype
            the data type

        Returns
        -------
        lulc_arr : np.ndarray
            A LULC array
        """
        x = self[self.x_column].values
        y = self[self.y_column].values
        z = self[column].values

        xres, yres = self.res
        i = (y - min(y)) // yres
        j = (x - min(x)) // xres

        lulc_arr = np.full((i.max() + 1, j.max() + 1), np.nan)
        lulc_arr[-i, j] = z
        lulc_arr[np.isnan(lulc_arr)] = nodata

        return lulc_arr.astype(dtype)

    def to_geotiff(self, fp, column, nodata=0, dtype=rasterio.uint8):
        """
        Export a LULC column to a GeoTIFF file

        Parameters
        ----------
        fp : str, file object or pathlib.Path object
            A filename or URL, a file object opened in binary ('rb') mode,
            or a Path object.
        column : str
            name of the LULC column
        nodata : numeric
            value to be assigned to pixels with no data
        dtype : str or numpy dtype
            the data type
        """
        lulc_arr = self.to_ndarray(column, nodata, dtype)

        with rasterio.open(fp, 'w', driver='GTiff', height=lulc_arr.shape[0],
                           width=lulc_arr.shape[1], count=1, dtype=str(dtype),
                           nodata=0, crs=self.crs,
                           transform=self.get_transform()) as raster:
            raster.write(lulc_arr.astype(dtype), 1)

    def plot(self, column, cmap=None, legend=False, figsize=None, ax=None,
             **show_kws):
        # TODO: automatically assign cmaps according to columns
        lulc_arr = self.to_ndarray(column)
        return plotting.plot_ndarray(lulc_arr, transform=self.get_transform(),
                                     cmap=cmap, legend=legend, figsize=figsize,
                                     ax=ax, **show_kws)

    plot.__doc__ = plotting._plot_ndarray_doc % (
        'column', '\ncolumn : str\n    data column to display')

    def clip_by_geometry(self, geometry, geometry_crs=None):
        return sls_geometry.clip_by_geometry(self, geometry,
                                             geometry_crs=geometry_crs)

    clip_by_geometry.__doc__ = sls_geometry._clip_by_geometry_doc % ''

    def clip_by_nominatim(self, query, which_result=1):
        return sls_geometry.clip_by_nominatim(self, query,
                                              which_result=which_result)

    clip_by_nominatim.__doc__ = sls_geometry._clip_by_nominatim_doc % ''

    # pandas methods
    def __getitem__(self, key):
        result = super(LandDataFrame, self).__getitem__(key)
        if isinstance(result, pd.DataFrame):
            # TODO: check that there is at least one column of land statistics
            if self.x_column in result and self.y_column in result:
                result.__class__ = LandDataFrame
                result.crs = self.crs
                result.res = self.res
            else:
                result.__class__ = pd.DataFrame
        return result

    def merge(self, right, duplicate_columns=False, how='outer',
              left_index=True, right_index=True, **kwargs):
        return merge(self, right, **kwargs)

    merge.__doc__ = _merge_doc % ''

    @property
    def _constructor(self):
        return LandDataFrame

    # geopandas
    def get_geoseries(self):
        return sls_geometry.get_geoseries(self)

    get_geoseries.__doc__ = sls_geometry._get_geoseries_doc % ''

    def to_geodataframe(self, drop_xy_columns=True):
        return sls_geometry.to_geodataframe(self,
                                            drop_xy_columns=drop_xy_columns)

    to_geodataframe.__doc__ = sls_geometry._to_geodataframe_doc % ''


def merge(left, right, duplicate_columns=False, how='outer', left_index=True,
          right_index=True, **kwargs):

    if duplicate_columns:
        _right = right
    else:
        _right = right[right.columns.difference(left.columns)]

    return pd.merge(left, _right, how=how, left_index=left_index,
                    right_index=right_index, **kwargs)


merge.__doc__ = _merge_doc % '\nleft : LandDataFrame'


def read_csv(filepath_or_buffer, index_column=None, x_column=None,
             y_column=None, crs=None, res=None, read_csv_kws=None,
             df_init_kws=None):
    """
    Convert a LULC column to a numpy array. See also the documentation for
    `pandas.read_csv`.

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
    crs : rasterio CRS, optional
        Coordinate reference system, as a rasterio CRS object. If `None` is
        provided, the value set in `settings.DEFAULT_CRS` will be taken.
    res : tuple, optional
        The (x, y) resolution of the dataset. If `None` is provided, the value
        set in `settings.DEFAULT_RES` will be taken.
    read_csv_kws : dict-like, optional
        Keyword arguments to be passed to `pandas.read_csv`
    df_init_kws : dict-like, optional
        Keyword arguments to be passed to `pandas.read_csv`

    Returns
    -------
    result : LandDataFrame
    """
    if read_csv_kws is None:
        read_csv_kws = {}
    df = pd.read_csv(filepath_or_buffer, **read_csv_kws)

    if df_init_kws is None:
        df_init_kws = {}
    return LandDataFrame(df, crs=crs, res=res, index_column=index_column,
                         x_column=x_column, y_column=y_column, **df_init_kws)
