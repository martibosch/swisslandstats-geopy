import logging

try:
    import geopandas as gpd
    import pyproj

    from functools import partial
    from shapely.geometry import Point
    from shapely.ops import transform
except ImportError:
    gpd = None

try:
    import osmnx as ox
except ImportError:
    ox = None

from . import settings

__all__ = ['clip_by_geometry', 'clip_by_nominatim']


def clip_by_geometry(ldf, geometry, geometry_crs=None):
    """
    Clip a LandDataFrame by a geometry

    Parameters
    ----------
    ldf : LandDataFrame
        landscape statistics dataframe
    geometry : shapely Polygon or MultiPolygon
        the geometry used to clip the dataframe
    crs : dict, optional
        the starting coordinate reference system of the passed-in geometry.
        If not given, it will take the default crs from the settings.

    Returns
    -------
    result : LandDataFrame
    """
    if geometry_crs is None:
        geometry_crs = settings.DEFAULT_CRS

    if gpd:
        # TODO: it'd be cool to 'cache' the GeoSeries (maybe as an
        # attribute of LandDataFrame)

        # alternative with osmnx (slower though):
        # geometry = ox.project_geometry(geometry, to_crs=ls_ldf.crs)
        if geometry_crs != ldf.crs:
            geometry = transform(
                partial(pyproj.transform, pyproj.Proj(**geometry_crs),
                        pyproj.Proj(**ldf.crs)), geometry)

        # first clip by polygon bounds without geopandas
        xmin, ymin, xmax, ymax = geometry.bounds
        x_column, y_column = ldf.x_column, ldf.y_column
        bounds_ldf = ldf[(ldf[x_column] > xmin) & (ldf[x_column] < xmax) &
                         (ldf[y_column] > ymin) & (ldf[y_column] < ymax)]

        gser = gpd.GeoSeries(
            map(Point, bounds_ldf[[x_column, y_column]].values),
            index=bounds_ldf.index)

        return bounds_ldf[gser.within(geometry)]

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


def clip_by_nominatim(ldf, query, which_result=1):
    """
    Clip a LandDataFrame by a single place name query to Nominatim. See also
    the documentation for `osmnx.gdf_from_place`

    Parameters
    ----------
    ldf : LandDataFrame
        landscape statistics dataframe
    query : string or dict
        query string or structured query dict to geocode/download
    which_result : int
        max number of results to return and which to process upon receipt

    Returns
    -------
    result : LandDataFrame
    """
    if ox:
        try:
            geometry = ox.gdf_from_place(
                query, which_result=which_result)['geometry'].iloc[0]
            return clip_by_geometry(ldf, geometry,
                                    geometry_crs=ox.settings.default_crs)

        except KeyError:
            logging.warning(
                'OSM returned no results (or fewer than which_result) for '
                'query "{}".\n Returning empty SLSDataFrame'.format(query))
            return ldf[0:0]

    else:
        # warn about missing dependences
        logging.warning(
            "The clip_by_nominatim module requires the osmnx package. "
            "The easiest wayto install it is as in\n"
            "conda install -c conda-forge osmnx"
            "See https://github.com/gboeing/osmnx for more information "
            "about installing osmnx")
