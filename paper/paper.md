---
title: swisslandstats-geopy: Python tools for the land statistics datasets from the Swiss Federal Statistical Office
tags:
  - Python
  - land use
  - land cover
  - GIS
  - raster
authors:
 - name: Martí Bosch
   orcid: 0000-0001-8735-9144
   affiliation: 1
affiliations:
 - name: Urban and Regional Planning Community (CEAT), École Polytechnique Fédérale de Lausanne (EPFL), Switzerland
   index: 1
date: 17 May 2019
bibliography: paper.bib
---

# Summary

The Swiss Land Statistics inventory by the Swiss Federal Statistical Office (SFSO) [@sfso2017statistique] provides land use/land cover (LULC) datasets at the Swiss national extent for a sequence of four survey periods in 1979/85, 1992/97, 2004/09 and 2013/18. The data is stored in a relational database format, where each row corresponds to one of the hectometric pixels that configure the Swiss territory, and features three groups of columns:

* Firstly, the `E` and `N` columns denote the coordinates of the pixel's centroid in the LV95 coordinate reference system (or alternatively `X` and `Y` in LV03). 
* Secondly, the `FJ85`, `FJ97`, `FJ09` and `FJ18` columns denote the exact years when the observations for each of the four survey periods were taken. For instance, the first dataset was produced between 1979 and 1985. Accordingly, for each row/pixel, the `FJ85` column will denote the exact year where its LULC category attribution was made (it can be any year within the 1979/85 period, depending on the part of Switzerland).
* Thirdly, the LULC data is provided in three different nomenclatures: the *standard nomenclature*, which feature 72 categories that combine land use and land cover information; the *land cover* nomenclature and the *land use nomenclature*. Accordingly, the LULC information for each pixel is stored in columns of the form `LC85_27`, where `LC` denotes the *land cover nomenclature*, `85` the survey period 1979/85 and `27` the number of categories considered. 

The inventory for each nomenclature can be downloaded as a comma-separated value (CSV) file. For instance, the *standard nomenclature* aggregated to 17 categories can be download freely, and is of the form:

E       |  N      | FJ85 | ... | FJ18 | AS85_17 | ... | AS18_17 |
------- | ------- | ---- | --- | ---- | :-----: | --- | :-----: |
2485500 | 1109700 | 1980 | ... | 2012 |      10 | ... |      10 |
2485500 | 1109800 | 1980 | ... | 2012 |      10 | ... |      10 |

The aim of the proposed library, `swisslandstats-geopy` is to provide an extended pandas *DataFrame* interface [@mckinney2010data] to the table-like LULC inventory provided by the SFSO. 

* Automatically read CSV files from the SFSO into dataframes
* Export categorical land use/land cover columns into `numpy` arrays and `GeoTIFF` files
* Clip dataframes by vector geometries
* Plot categorical land use/land cover information

# Availability

The source code of `swisslandstats-geopy` is fully available at [a GitHub repository](https://github.com/martibosch/swisslandstats-geopy). A dedicated Python package has been created and is hosted at the [Python Package Index (PyPI)](https://pypi.org/project/swisslandstats-geopy/). While there is no documentation site for the library, all the methods are documented by means of Python docstrings [@goodger2001docstrings], and an example notebook with the overview of the `swisslandstats-geopy`'s features with the free tier
