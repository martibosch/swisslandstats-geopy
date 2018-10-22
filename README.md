[![Build Status](https://travis-ci.com/martibosch/swisslandstats-geopy.svg?token=AdqNpn2z1w9P1qtcys7B&branch=master)](https://travis-ci.com/martibosch/swisslandstats-geopy)

# swisslandstats-geopy

Python tools for the [Swiss Land Statistics datasets from the Swiss Federal Statistical Office](https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie.html) (link in French)

## Features

* Automatically transforms csv files form the Swiss Federal Statistical Office into DataFrames
* Transforms categorical land use/land cover information into `numpy` arrays and `GeoTIFF` files
* Plots categorical land use/land cover information with legend and the appropriate color map

## Description of the datasets

More information can be found in the [Swiss Federal Statistical Office page](https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie.html) (in German and French)

* [Standard nomenclature](https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie/nomenclature-standard.html) `NOAS04` with 72 base categories that combine information on land cover and land use
* [Land cover nomenclature](https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie/occupation-sol.html) `NOLC04` with 27 categories of land cover
* [Land use nomenclature](https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie/utilisation-sol.html) `NOLU04` with 46 categories of land use


## TODO

* add missing colormaps
  * automatically assign columns to cmaps when plotting
* exceptions for no land use/land cover columns
* cache colum ndarrays as class attributes?
* implement methods to merge DataFrames from multiple csv files
