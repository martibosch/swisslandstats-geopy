# Change log

## 0.7.1 (09/07/2019)

* fix: deleted reqs-dev from setup.py (not included in MANIFEST)

## 0.7.0 (09/07/2019)

* plotting with an affine transform via rasterio.plot.show
* fix wrong indent of crs and res setting in LandDataFrame's init

## 0.6.1 (17/05/2019)

* fix: included requirements in MANIFEST

## 0.6.0 (17/05/2019)

* kwargs for external methods
* default lv95 (instead of lv03)
* geopandas instead of pyproj to reproject geom in `clip_by_geometry`

## 0.5.1 (08/04/2019)

* changed `affine_transform` property for `get_transform` method

## 0.5.0 (07/04/2019)

* affine_transform as instance property

## 0.4.1 (07/11/2018)

* fix `to_geodataframe` method
* auto extract crs from geoseries

## 0.4.0 (07/11/2018)

* added to_geopandas methods

## 0.3.0 (07/11/2018)

* added merge class method and module function

## 0.2.0 (06/11/2018)

* geometry clip functions as LandDataFrame class methods
* fix colormap and legend bug

## 0.1 (25/10/2018)

* initial release
