from __future__ import division

import numpy as np
import pandas as pd
import rasterio

from rasterio.transform import from_origin

DEFAULT_INDEX_COLUMN = 'RELI'
DEFAULT_CRS = {'init': 'epsg:21781'}
DEFAULT_RES = (100, 100)


class SFSOGeoDataFrame(pd.DataFrame):
    """Documentation for SFSOGeoDataFrame

    """

    # so that pandas can allow setting this class attributes
    _metadata = ['crs', 'res']

    def __init__(self, *args, **kwargs):
        crs = kwargs.pop('crs', DEFAULT_CRS)
        res = kwargs.pop('res', DEFAULT_RES)
        super(SFSOGeoDataFrame, self).__init__(*args, **kwargs)
        self.set_index(DEFAULT_INDEX_COLUMN, inplace=True)
        self.crs = crs
        self.res = res

    def to_ndarray(self, column, nodata=0, dtype=np.uint8):
        x = self['X'].values
        y = self['Y'].values
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


def read_csv(filepath_or_buffer, crs=None, res=None, *args, **kwargs):
    if crs:
        kwargs['crs'] = crs
    if res:
        kwargs['res'] = res
    df = pd.read_csv(filepath_or_buffer, *args, **kwargs)
    return SFSOGeoDataFrame(df, *args, **kwargs)
