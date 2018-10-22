import swisslandstats as sls


def test_base_imports():
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import rasterio

    from matplotlib import colors
    from rasterio.transform import from_origin


def test_geo_imports():
    import geopandas as gpd
    import pyproj

    from functools import partial
    from shapely.geometry import Point
    from shapely.ops import transform


def test_slsdataframe():
    import tempfile
    import numpy as np
    import pandas as pd

    sdf = sls.read_csv('tests/input_data/dataset.csv')

    assert np.all(
        sdf.to_ndarray('AS09_4') == np.arange(4, dtype=np.uint8).reshape(2, 2))
    sdf.to_geotiff(tempfile.TemporaryFile(), 'AS09_4')

    assert type(sdf[[sdf.x_column, sdf.y_column,
                     'AS09_4']]) == sls.LandDataFrame
    assert type(sdf[[sdf.x_column, 'AS09_4']]) == pd.DataFrame
    assert type(sdf['AS09_4']) == pd.Series


def test_geometry():
    from shapely.geometry import Polygon

    sdf = sls.read_csv('tests/input_data/dataset.csv')
    geometry = Polygon([(0, 0), (0, 150), (150, 150), (150, 0)])

    clipped_sdf = sls.clip_by_geometry(sdf, geometry)
    assert len(clipped_sdf) == 1

    clipped_sdf = sls.clip_by_nominatim(sdf, 'Lausanne, Switzerland')
    assert len(clipped_sdf) == 0
