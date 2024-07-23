[![PyPI version fury.io](https://badge.fury.io/py/swisslandstats-geopy.svg)](https://pypi.python.org/pypi/swisslandstats-geopy/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/swisslandstats-geopy.svg)](https://anaconda.org/conda-forge/swisslandstats-geopy)
[![Documentation Status](https://readthedocs.org/projects/swisslandstats-geopy/badge/?version=latest)](https://swisslandstats-geopy.readthedocs.io/en/latest/?badge=latest)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/martibosch/swisslandstats-geopy/main.svg)](https://results.pre-commit.ci/latest/github/martibosch/swisslandstats-geopy/main)
[![tests](https://github.com/martibosch/swisslandstats-geopy/actions/workflows/tests.yml/badge.svg)](https://github.com/martibosch/swisslandstats-geopy/blob/main/.github/workflows/tests.yml)
[![codecov](https://codecov.io/gh/martibosch/swisslandstats-geopy/branch/main/graph/badge.svg)](https://codecov.io/gh/martibosch/swisslandstats-geopy)
[![GitHub license](https://img.shields.io/github/license/martibosch/swisslandstats-geopy.svg)](https://github.com/martibosch/swisslandstats-geopy/blob/main/LICENSE.txt)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/martibosch/swisslandstats-geopy/main?filepath=examples/overview.ipynb)
[![status](http://joss.theoj.org/papers/b6de0f096382d4dcd5d137a3f1edcb30/status.svg)](http://joss.theoj.org/papers/b6de0f096382d4dcd5d137a3f1edcb30)
[![DOI](https://zenodo.org/badge/151926572.svg)](https://zenodo.org/badge/latestdoi/151926572)

# swisslandstats-geopy

Extended pandas-like interface for the [Swiss Federal Statistics Geodata (GEOSTAT)](https://www.bfs.admin.ch/bfs/en/home/services/geostat/swiss-federal-statistics-geodata.html).

**Citation**: Bosch M. 2019. "swisslandstats-geopy: Python tools for the land statistics datasets from the Swiss Federal Statistical Office". The Journal Open Source Software 4(40), 1511. https://doi.org/10.21105.joss.01511

Many datasets of the GEOSTAT inventory are provided in a relational database format which allows storing a coolection of variables into a single CSV file, nevertheless, libraries to process geographical raster data aree rarely capable of processing such format. Therefore, the aim of `swisslandstats-geopy` is to provide an extended pandas `DataFrame` interface to such inventory (see [the "Features" section below](#features)).

The target audience of `swisslandstats-geopy` is researchers and developers in environmental sciences and GIS, who intend to produce repeatable and reproducible computational workflows that make use of the geodata inventory provided by the SFSO.

## Features

- Automatically read CSV files from the GEOSTAT inventory into dataframes
- Export columns into `numpy` arrays and `GeoTIFF` files
- Clip dataframes by vector geometries
- Plot information as raster maps

```python
import swisslandstats as sls

ldf = sls.from_url()
ldf.plot("LU09_4", cmap=sls.noas04_4_cmap, legend=True)
```

![landstats](examples/landstats.png)

```python
vaud_ldf = ldf.clip_by_nominatim("Vaud, Switzerland")
vaud_ldf.plot("LU09_4", cmap=sls.noas04_4_cmap, legend=True)
```

![landstats-vaud](examples/landstats_vaud.png)

See the [example notebook](https://github.com/martibosch/swisslandstats-geopy/tree/main/examples/overview.ipynb) for a more thorough overview and example uses with the [land use statistics](https://www.bfs.admin.ch/bfs/en/home/services/geostat/swiss-federal-statistics-geodata/land-use-cover-suitability/swiss-land-use-statistics.html) and [population and household statistics](https://www.bfs.admin.ch/bfs/en/home/services/geostat/swiss-federal-statistics-geodata/population-buildings-dwellings-persons/population-housholds-from-2010.html). You might click the Binder badge above to execute it interactively in your browser.

Examples of applications of the library in the academic literature include:

- The assessment of the carbon sequestration for the canton of Vaud (see [the dedicated GitHub repository](https://github.com/martibosch/carbon-sequestration-vaud) with the materials necessary to reproduce the results)
- The evaluation of the spatio-temporal patterns of LULC change in the urban agglomerations of Zurich, Bern and Lausanne (see [the dedicated GitHub repository](https://github.com/martibosch/swiss-urbanization) with the materials necessary to reproduce the results).

## Installation

### With conda

The easiest way to install `swisslandstats-geopy` is with conda as in:

```bash
conda install -c conda-forge swisslandstats-geopy
```

### With pip

If you want to be able to clip dataframes by vector geometries, you will need [geopandas](https://github.com/geopandas/geopandas) (and [osmnx](https://github.com/gboeing/osmnx) to clip dataframes from place names e.g., "Zurich, Switzerland"). The easiest way to install such requirements is via conda as in:

```bash
conda install -c conda-forge geopandas osmnx rasterio
```

Although [rasterio](https://github.com/mapbox/rasterio) can be installed via pip, it is recommended to install it via conda to avoid potential issues with GDAL (such as the support of the Swiss EPSG coordinate reference systems).

Then you can install `swisslandstats-geopy` via pip as in:

```bash
pip install swisslandstats-geopy
```

## TODO

- Add missing colormaps
  - Automatically assign columns to cmaps when plotting
- Exceptions for no land use/land cover columns
- Implement methods to merge DataFrames from multiple csv files
