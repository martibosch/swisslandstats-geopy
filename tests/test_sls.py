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
    import matplotlib.pyplot as plt
    plt.switch_backend('agg')  # only for testing purposes
    import numpy as np
    import pandas as pd

    ldf = sls.read_csv('tests/input_data/dataset.csv')

    assert np.all(
        ldf.to_ndarray('AS09_4') == np.arange(4, dtype=np.uint8).reshape(2, 2))
    ldf.to_geotiff(tempfile.TemporaryFile(), 'AS09_4')

    assert isinstance(
        ldf.plot('AS09_4', cmap=sls.noas04_4_cmap, legend=True), plt.Axes)

    assert type(ldf[[ldf.x_column, ldf.y_column,
                     'AS09_4']]) == sls.LandDataFrame
    assert type(ldf[[ldf.x_column, 'AS09_4']]) == pd.DataFrame
    assert type(ldf['AS09_4']) == pd.Series


def test_geometry():
    from shapely.geometry import Polygon

    ldf = sls.read_csv('tests/input_data/dataset.csv')
    geometry = Polygon([(0, 0), (0, 150), (150, 150), (150, 0)])

    clipped_ldf = ldf.clip_by_geometry(geometry)
    assert len(clipped_ldf) == 1

    clipped_ldf = ldf.clip_by_nominatim('Lausanne, Switzerland')
    assert len(clipped_ldf) == 0
