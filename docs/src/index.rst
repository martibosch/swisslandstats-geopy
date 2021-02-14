swisslandstats-geopy documentation
==================================

Extended pandas-like interface for the `Swiss Federal Statistics Geodata (GEOSTAT) <https://www.bfs.admin.ch/bfs/en/home/services/geostat/swiss-federal-statistics-geodata.html>`_.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   swisslandstats

The target audience of `swisslandstats-geopy` is researchers and developers in environmental sciences and GIS, who intend to produce repeatable and reproducible computational workflows that make use of the geodata inventory provided by the SFSO. 
   
Features
--------

* Automatically read CSV files from the GEOSTAT inventory into dataframes
* Export columns into `numpy` arrays and `GeoTIFF` files
* Clip dataframes by vector geometries
* Plot information as raster maps

See the `example notebook <https://github.com/martibosch/swisslandstats-geopy/tree/master/examples/overview.ipynb>`_ for a more thorough overview and example uses with the `land use statistics <https://www.bfs.admin.ch/bfs/en/home/services/geostat/swiss-federal-statistics-geodata/land-use-cover-suitability/swiss-land-use-statistics.html>`_ and `population and household statistics <https://www.bfs.admin.ch/bfs/en/home/services/geostat/swiss-federal-statistics-geodata/population-buildings-dwellings-persons/population-housholds-from-2010.html>`_. You might click the Binder badge above to execute it interactively in your browser.

Examples of applications of the library in the academic literature include:

* The assessment of the carbon sequestration for the canton of Vaud (see `the dedicated GitHub repository <https://github.com/martibosch/carbon-sequestration-vaud>`_ with the materials necessary to reproduce the results)
* The evaluation of the spatio-temporal patterns of LULC change in the urban agglomerations of Zurich, Bern and Lausanne (see `the dedicated GitHub repository <https://github.com/martibosch/swiss-urbanization>`_ with the materials necessary to reproduce the results).

  
Installation
------------

With conda
^^^^^^^^^^

The easiest way to install `swisslandstats-geopy` is with conda as in:

    $ conda install -c conda-forge swisslandstats-geopy


With pip
^^^^^^^^

If you want to be able to clip dataframes by vector geometries, you will need `geopandas <https://github.com/geopandas/geopandas>`_ (and `osmnx <https://github.com/gboeing/osmnx>`_ to clip dataframes from place names e.g., "Zurich, Switzerland"). The easiest way to install such requirements is via conda as in:

    $ conda install -c conda-forge geopandas osmnx rasterio 

Although `rasterio <https://github.com/mapbox/rasterio>`_ can be installed via pip, it is recommended to install it via conda to avoid potential issues with GDAL (such as the support of the Swiss EPSG coordinate reference systems). 

Then you can install `swisslandstats-geopy` via pip as in:

    $ pip install swisslandstats-geopy

Additionally, you might consider `installing pygeos to drastically improve the performance <https://geopandas.readthedocs.io/en/latest/install.html#using-the-optional-pygeos-dependency>`_ of the `clip_by_geometry` method (and by extension the `clip_by_nominatim` method too). For example, in my laptop, clipping the whole Swiss land use/land cover database to the extent of the Canton of Vaud takes 3.78s when using `pygeos` instead of 197s (speed-up of x50).
   
   
Indices and tables
==================
* :ref:`genindex`
