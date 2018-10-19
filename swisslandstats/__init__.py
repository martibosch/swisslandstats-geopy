from __future__ import division

import numpy as np
import pandas as pd
import rasterio

from rasterio.transform import from_origin

from . import geometry
from . import plotting
from . import settings


class SLSDataFrame(pd.DataFrame):

    # so that pandas can allow setting this class attributes
    _metadata = ['crs', 'res']

    index_column = settings.DEFAULT_INDEX_COLUMN
    x_column = settings.DEFAULT_X_COLUMN
    y_column = settings.DEFAULT_Y_COLUMN

    def __init__(self, *args, **kwargs):
        crs = kwargs.pop('crs', settings.DEFAULT_CRS)
        res = kwargs.pop('res', settings.DEFAULT_RES)
        super(SLSDataFrame, self).__init__(*args, **kwargs)
        if self.index.name != self.index_column:
            self.set_index(self.index_column, inplace=True)
        self.crs = crs
        self.res = res

    def to_ndarray(self, column, nodata=0, dtype=np.uint8):
        x = self[self.x_column].values
        y = self[self.y_column].values
        z = self[column].values

        xres, yres = self.res
        i = (y - min(y)) // yres
        j = (x - min(x)) // xres

        lulc_arr = np.nan * np.empty((len(set(i)), len(set(j))))
        lulc_arr[-i, j] = z
        x_origin = min(x) - xres // 2
        y_origin = max(y) + yres // 2
        self.transform = from_origin(x_origin, y_origin, xres, yres)

        lulc_arr[np.isnan(lulc_arr)] = nodata

        return lulc_arr.astype(dtype)

    def to_geotiff(self, fp, column, nodata=0, dtype=rasterio.uint8):
        lulc_arr = self.to_ndarray(column, nodata, dtype)

        with rasterio.open(fp, 'w', driver='GTiff', height=lulc_arr.shape[0],
                           width=lulc_arr.shape[1], count=1, dtype=str(dtype),
                           nodata=0, crs=self.crs,
                           transform=self.transform) as raster:

            raster.write(lulc_arr.astype(dtype), 1)

    def plot(self, column, cmap=None, *args, **kwargs):
        # TODO: automatically assign cmaps according to columns
        lulc_arr = self.to_ndarray(column)
        return plotting.plot_ndarray(lulc_arr, cmap=cmap, *args, **kwargs)

    def __getitem__(self, key):
        result = super(SLSDataFrame, self).__getitem__(key)
        if isinstance(result, pd.DataFrame):
            # TODO: check that there is at least one column of land statistics
            if self.x_column in result and self.y_column in result:
                result.__class__ = SLSDataFrame
                result.crs = self.crs
                result.res = self.res
            else:
                result.__class__ = pd.DataFrame
        return result

    @property
    def _constructor(self):
        return SLSDataFrame


def read_csv(filepath_or_buffer, crs=None, res=None, *args, **kwargs):
    if crs:
        kwargs['crs'] = crs
    if res:
        kwargs['res'] = res
    df = pd.read_csv(filepath_or_buffer, *args, **kwargs)
    return SLSDataFrame(df, *args, **kwargs)
