try:
    import geopandas as gpd
    import pyproj

    from functools import partial
    from shapely.geometry import Point
    from shapely.ops import transform
except ImportError:
    import logging
    gpd = None

from . import settings


def clip_by_geometry(sdf, geometry, geometry_crs=settings.DEFAULT_CRS):
    if gpd:
        # TODO: it'd be cool to 'cache' the GeoSeries (maybe as an
        # attribute of SLSDataFrame)

        # alternative with osmnx (slower though):
        # geometry = ox.project_geometry(geometry, to_crs=ls_sdf.crs)
        if geometry_crs != sdf.crs:
            geometry = transform(
                partial(pyproj.transform, pyproj.Proj(**geometry_crs),
                        pyproj.Proj(**sdf.crs)), geometry)

        # first clip by polygon bounds without geopandas
        xmin, ymin, xmax, ymax = geometry.bounds
        x_column, y_column = sdf.x_column, sdf.y_column
        bounds_sdf = sdf[(sdf[x_column] > xmin) & (sdf[x_column] < xmax) &
                         (sdf[y_column] > ymin) & (sdf[y_column] < ymax)]

        gser = gpd.GeoSeries(
            map(Point, bounds_sdf[[x_column, y_column]].values),
            index=bounds_sdf.index)

        return bounds_sdf[gser.within(geometry)]

    else:
        # warn about missing dependences
        # TODO: warn also if using non-cythonized geopandas?
        logging.warning(
            "The geometry module requires the geopandas package. "
            "For better performance, we strongly suggest that you install its "
            "cythonized version via conda-forge as in\n"
            "conda install -c conda-forge/label/dev geopandas"
            "See https://github.com/geopandas/geopandas for more information "
            "about installing geopandas")
