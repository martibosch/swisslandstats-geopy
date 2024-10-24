# Change log

## \[v0.11.0\] - 2024-10-24

### :boom: BREAKING CHANGES

- due to [`8b44edc`](https://github.com/martibosch/swisslandstats-geopy/commit/8b44edc3980b2a7274ed16deca866bb8ffeebe63) - using kws->kwargs, use keyword-only arguments *(commit by [@martibosch](https://github.com/martibosch))*:

  using kws->kwargs, use keyword-only arguments

- due to [`3173730`](https://github.com/martibosch/swisslandstats-geopy/commit/31737303f82341eea5b99d02329a60f201d7be5a) - change default x/y columns in settings *(commit by [@martibosch](https://github.com/martibosch))*:

  change default x/y columns in settings

- due to [`b450a62`](https://github.com/martibosch/swisslandstats-geopy/commit/b450a627df7764822820406e74e582344adffdee) - dedicated sep kwarg for read_csv with default in settings *(commit by [@martibosch](https://github.com/martibosch))*:

  dedicated sep kwarg for read_csv with default in settings

- due to [`9147fcf`](https://github.com/martibosch/swisslandstats-geopy/commit/9147fcfd899e822a570b8363bb556fcd329215a9) - only set index column if exists, otherwise log info msg *(commit by [@martibosch](https://github.com/martibosch))*:

  only set index column if exists, otherwise log info msg

### :sparkles: New Features

- [`3173730`](https://github.com/martibosch/swisslandstats-geopy/commit/31737303f82341eea5b99d02329a60f201d7be5a) - change default x/y columns in settings *(commit by [@martibosch](https://github.com/martibosch))*
- [`b450a62`](https://github.com/martibosch/swisslandstats-geopy/commit/b450a627df7764822820406e74e582344adffdee) - dedicated sep kwarg for read_csv with default in settings *(commit by [@martibosch](https://github.com/martibosch))*
- [`96f621e`](https://github.com/martibosch/swisslandstats-geopy/commit/96f621ecdca45ad624a9a2f51ba370c557e596ef) - use requests_cache *(commit by [@martibosch](https://github.com/martibosch))*
- [`9147fcf`](https://github.com/martibosch/swisslandstats-geopy/commit/9147fcfd899e822a570b8363bb556fcd329215a9) - only set index column if exists, otherwise log info msg *(commit by [@martibosch](https://github.com/martibosch))*
- [`af7f8b3`](https://github.com/martibosch/swisslandstats-geopy/commit/af7f8b308cab593c9351e0a7061afdfe36ece2f1) - replace nan with nodata before `to_ndarray` *(commit by [@martibosch](https://github.com/martibosch))*

### :recycle: Refactors

- [`8b44edc`](https://github.com/martibosch/swisslandstats-geopy/commit/8b44edc3980b2a7274ed16deca866bb8ffeebe63) - using kws->kwargs, use keyword-only arguments *(commit by [@martibosch](https://github.com/martibosch))*

### :white_check_mark: Tests

- [`acdd0d6`](https://github.com/martibosch/swisslandstats-geopy/commit/acdd0d6133446cc04ca0a25758d93912f418ee14) - update test data; mock requests with getsentry/responses *(commit by [@martibosch](https://github.com/martibosch))*
- [`87f08f3`](https://github.com/martibosch/swisslandstats-geopy/commit/87f08f32efdcc5eb522f0fff3d5ff8e1d1dadacf) - use isinstance instead of type() + == *(commit by [@martibosch](https://github.com/martibosch))*

## 0.10.0 (17/11/2021)

- dropped support for Python 3.6
- GitHub Actions tests in develop branch too
- added nbstripout and nbqa pre-commit hooks, black/isort toml config
- added noas04_4_norm for noas04_4_cmap
- fix missing osmnx in test_geo_imports

## 0.9.0 (30/09/2021)

- updated to pre-commit, black, pydocstyle, github actions, codecov
- added `to_xarray` method
- init `LandDataFrame.crs` from settings as rasterio CRS
- str as default `dtype` arg
- updated to osmnx>=1

## 0.8.0 (20/08/2020)

- corrected init of `lulc_arr` in `to_ndarray` method
- install rasterio from conda-forge in travis to avoid CRS errors
- use `gpd.sjoin` in `clip_by_geometry`
- index/x/y columns as instance attrs, updated init/read_csv args

## 0.7.3 (17/01/2020)

- updated CRS in settings to `'<authority>:<code>'` syntax

## 0.7.2 (05/09/2019)

- updated README and JOSS paper
- moved overview notebook from separate repo to examples directory

## 0.7.1 (09/07/2019)

- fix: deleted reqs-dev from setup.py (not included in MANIFEST)

## 0.7.0 (09/07/2019)

- plotting with an affine transform via rasterio.plot.show
- fix wrong indent of crs and res setting in LandDataFrame's init

## 0.6.1 (17/05/2019)

- fix: included requirements in MANIFEST

## 0.6.0 (17/05/2019)

- kwargs for external methods
- default lv95 (instead of lv03)
- geopandas instead of pyproj to reproject geom in `clip_by_geometry`

## 0.5.1 (08/04/2019)

- changed `affine_transform` property for `get_transform` method

## 0.5.0 (07/04/2019)

- affine_transform as instance property

## 0.4.1 (07/11/2018)

- fix `to_geodataframe` method
- auto extract crs from geoseries

## 0.4.0 (07/11/2018)

- added to_geopandas methods

## 0.3.0 (07/11/2018)

- added merge class method and module function

## 0.2.0 (06/11/2018)

- geometry clip functions as LandDataFrame class methods
- fix colormap and legend bug

## 0.1 (25/10/2018)

- initial release
  \[v0.11.0\]: https://github.com/martibosch/swisslandstats-geopy/compare/v0.10.0...v0.11.0
