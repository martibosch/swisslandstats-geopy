swisslandstats-geopy documentation
==================================

Extended pandas-like interface for the `Swiss Land Statistics datasets from the Swiss Federal Statistical Office <https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie.html>`_ (link in French)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   swisslandstats

Features
--------

* Automatically read CSV files from the SFSO into dataframes
* Export categorical land use/land cover columns into ``numpy`` arrays and ``GeoTIFF`` files
* Clip dataframes by vector geometries
* Plot categorical land use/land cover information

See the `swisslandstats-notebooks <https://github.com/martibosch/swisslandstats-notebooks)>`_ repository for a more thorough overview.  
  
Installation
------------

If you want to be able to clip dataframes by vector geometries, you will need `geopandas <https://github.com/geopandas/geopandas>`_ (and `osmnx <https://github.com/gboeing/osmnx>`_ to clip dataframes from place names e.g., "Zurich, Switzerland"). The easiest way to install such requirements is via conda as in:

.. code-block:: bash

   # install the cythonized geopandas
   $ conda install -c conda-forge/label/dev geopandas
   $ conda install -c conda-forge osmnx

Then you might install ``swisslandstats-geopy`` as in
.. code-block:: bash

   $ pip install swisslandstats-geopy

**Important notes**:

* The `cythonized geopandas <https://jorisvandenbossche.github.io/blog/2017/09/19/geopandas-cython/>`_ can give you vast speed-ups when clipping dataframes e.g., 32.7 ms instead of 51.8 s (x1584) to clip by the dataframe by canton of Vaud. However, `the cythonized geopandas is not production code yet <https://github.com/geopandas/geopandas/issues/473>`_. If other libraries of your environment depend on geopandas, it might be better to install its (slower) stable version as in ``conda install -c conda-forge geopandas``.
* Depending on your environment, you might get an ``error while loading shared libraries: libncurses.so.6``. You might solve it by ``conda install -c conda-forge ncurses``

Description of the datasets
---------------------------

More information can be found in the `Swiss Federal Statistical Office page <https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie.html>`_ (in German and French)

* `Standard nomenclature <https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie/nomenclature-standard.html>`_ ``NOAS04`` with 72 base categories that combine information on land cover and land use
* `Land cover nomenclature <https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie/occupation-sol.html>`_ ``NOLC04`` with 27 categories of land cover
* `Land use nomenclature <https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie/utilisation-sol.html>`_ ``NOLU04`` with 46 categories of land use
   
   
Indices and tables
==================
* :ref:`genindex`
