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

* tests
* add missing colormaps
  * automatically assign columns to cmaps when plotting
* exceptions for no land use/land cover columns
* cache colum ndarrays as class attributes?
* clip by nominatim query via `osmnx`
