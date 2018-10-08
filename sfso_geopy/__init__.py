from __future__ import division

import numpy as np
import pandas as pd
import rasterio

from rasterio.transform import from_origin


class SFSOGeoDataFrame(pd.DataFrame):
    """Documentation for SFSOGeoDataFrame

    """

    def __init__(self, xres=100, yres=100, crs={'init': 'epsg:21781'}):
        super(SFSOGeoDataFrame, self).__init__()
        self.xres = xres
        self.yres = yres
        self.crs = crs

    def to_geotiff(self, filename, col_name, nodata=0, dtype=rasterio.uint8):
        x = self['X'].values
        y = self['Y'].values
        z = self[col_name].values

        i = (y - min(y)) // self.yres
        j = (x - min(x)) // self.xres

        z_arr = np.nan * np.empty((len(set(i)), len(set(j))))
        z_arr[-i, j] = z
        x_origin = min(x) - self.xres // 2
        y_origin = max(y) + self.yres // 2
        self.transform = from_origin(x_origin, y_origin, self.xres, self.yres)

        z_arr[np.isnan(z_arr)] = nodata

        with rasterio.open(
                filename,
                'w',
                driver='GTiff',
                height=z_arr.shape[0],
                width=z_arr.shape[1],
                count=1,
                dtype=str(dtype),
                nodata=0,
                crs=self.crs,
                transform=self.transform) as raster:
            raster.write(z_arr.astype(dtype), 1)
