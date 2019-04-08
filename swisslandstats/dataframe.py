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

    Keyword Arguments
    -----------------
    crs : dict
        Coordinate system. The default is ``{'init': 'epsg:21781'}``
    res : tuple
        The (x, y) resolution of the dataset. The default is ``(100, 100)``
    """

    # so that pandas can allow setting this class attributes
    _metadata = ['crs', 'res']

    index_column = settings.DEFAULT_INDEX_COLUMN
    x_column = settings.DEFAULT_X_COLUMN
    y_column = settings.DEFAULT_Y_COLUMN

    def __init__(self, *args, **kwargs):
        crs = kwargs.pop('crs', settings.DEFAULT_CRS)
        res = kwargs.pop('res', settings.DEFAULT_RES)
        super(LandDataFrame, self).__init__(*args, **kwargs)
        if self.index.name != self.index_column:
            self.set_index(self.index_column, inplace=True)
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

        lulc_arr = np.nan * np.empty((len(set(i)), len(set(j))))
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

    def plot(self, column, cmap=None, *args, **kwargs):
        # TODO: automatically assign cmaps according to columns
        lulc_arr = self.to_ndarray(column)
        return plotting.plot_ndarray(lulc_arr, cmap=cmap, *args, **kwargs)

    plot.__doc__ = plotting._plot_ndarray_doc % \
        '\ncolumn : str\n    data column to display'

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


def read_csv(filepath_or_buffer, crs=None, res=None, *args, **kwargs):
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
    crs : str
        Coordinate system. The default is ``'epsg:21781'``
    res : tuple
        The (x, y) resolution of the dataset. The default is ``(100, 100)``

    Returns
    -------
    result : LandDataFrame
    """
    if crs:
        kwargs['crs'] = crs
    if res:
        kwargs['res'] = res
    df = pd.read_csv(filepath_or_buffer, *args, **kwargs)
    return LandDataFrame(df, *args, **kwargs)
