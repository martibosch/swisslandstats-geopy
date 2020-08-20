import logging

from . import settings

try:
    import geopandas as gpd

    from shapely.geometry import Point
    from shapely.ops import transform
except ImportError:
    gpd = None

try:
    import osmnx as ox
except ImportError:
    ox = None

__all__ = [
    'get_geoseries', 'to_geodataframe', 'clip_by_geometry', 'clip_by_nominatim'
]

_gpd_warning_msg = """
The geometry module requires the geopandas package. For better performance, we
strongly suggest that you install its cythonized version via conda-forge as in:
conda install -c conda-forge/label/dev geopandas
See https://github.com/geopandas/geopandas for more information about
installing geopandas
"""

_get_geoseries_doc = """
Get the geometry of the LandDataFrame as a geopandas GeoSeries%s

Returns
----------
result : geopandas GeoSeries
"""

_to_geodataframe_doc = """
Transform the LandDataFrame to a geopandas GeoDataFrame with the points
represented by the x and y columns as geometry

Parameters
----------%s
drop_xy_columns : boolean, default True
    whether the LandDataFrame x and y columns should be deleted from the
    geopandas GeoDataFrame

Returns
----------
result : geopandas GeoDataFrame
"""

_clip_by_geometry_doc = """
Clip a LandDataFrame by a geometry

Parameters
----------%s
geometry : shapely Polygon or MultiPolygon
    the geometry used to clip the dataframe
geometry_crs : dict, optional
    the starting coordinate reference system of the passed-in geometry.
    If not given, it will take the default crs from the settings.

Returns
-------
result : LandDataFrame
"""

_clip_by_nominatim_doc = """
Clip a LandDataFrame by a single place name query to Nominatim. See also the
documentation for `osmnx.gdf_from_place`

Parameters
----------%s
query : string or dict
    query string or structured query dict to geocode/download
which_result : int
    max number of results to return and which to process upon receipt

Returns
-------
result : LandDataFrame
"""


def get_geoseries(ldf):
    if gpd:
        return gpd.GeoSeries(
            map(Point, ldf[[ldf.x_column, ldf.y_column]].values),
            index=ldf.index, crs=ldf.crs)
    else:
        logging.warning(_gpd_warning_msg)


get_geoseries.__doc__ = _get_geoseries_doc % \
                        '\n\nParameters\n----------\nldf : LandDataFrame'


def to_geodataframe(ldf, drop_xy_columns=True):
    gser = get_geoseries(ldf)

    # if geometry is None, geopandas is not installed and the corresponding
    # warning has already been logged by get_geoseries
    if not gser.empty:
        _ldf = ldf
        if drop_xy_columns:
            _ldf = ldf.drop(labels=[ldf.x_column, ldf.y_column], axis=1)

        return gpd.GeoDataFrame(_ldf, crs=gser.crs, geometry=gser)


to_geodataframe.__doc__ = _to_geodataframe_doc % '\nldf : LandDataFrame'


def clip_by_geometry(ldf, geometry, geometry_crs=None):
    if geometry_crs is None:
        geometry_crs = settings.DEFAULT_CRS

    if gpd:
        # TODO: it'd be cool to 'cache' the GeoSeries (maybe as an
        # attribute of LandDataFrame)

        gdf = gpd.GeoDataFrame({'geometry': [geometry]}, crs=geometry_crs)
        if geometry_crs != ldf.crs:
            # alternative with osmnx (slower):
            # geometry = ox.project_geometry(geometry, to_crs=ls_ldf.crs)
            # alternative without geopandas (faster but less ):
            # geometry = transform(
            #     partial(pyproj.transform, pyproj.Proj(**geometry_crs),
            #             pyproj.Proj(**ldf.crs)), geometry)
            gdf = gdf.to_crs(ldf.crs)

        return ldf.loc[gpd.sjoin(
            gpd.GeoDataFrame(
                geometry=gpd.points_from_xy(ldf[ldf.x_column],
                                            ldf[ldf.y_column], crs=ldf.crs),
                index=ldf.index), gdf, how='inner', op='within').index]

    else:
        # warn about missing dependences
        # TODO: warn also if using non-cythonized geopandas?
        logging.warning(_gpd_warning_msg)


clip_by_geometry.__doc__ = _clip_by_geometry_doc % '\nldf : LandDataFrame'


def clip_by_nominatim(ldf, query, **gdf_from_place_kws):
    if ox:
        try:
            geometry = ox.gdf_from_place(
                query, **gdf_from_place_kws)['geometry'].iloc[0]
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


clip_by_nominatim.__doc__ = _clip_by_nominatim_doc % '\nldf : LandDataFrame'
