"""swisslandstats setup script."""
# coding=utf-8

from setuptools import setup

long_description = """
Python tools for the Swiss Federal Statistics Geodata (GEOSTAT). The current
features are:
* Automatically read CSV files from the GEOSTAT inventory into dataframes
* Export columns into `numpy` arrays and `GeoTIFF` files
* Clip dataframes by vector geometries
* Plot information as raster maps
"""


def _get_requirements_from_files(groups_files):
    groups_reqlist = {}

    for k, v in groups_files.items():
        with open(v, "r") as f:
            pkg_list = f.read().splitlines()
            groups_reqlist[k] = pkg_list

    return groups_reqlist


reqs = _get_requirements_from_files(
    {"base": "requirements.txt", "geo": "requirements-geo.txt"}
)
install_reqs = reqs.pop("base")

# Extra dependences for geometric operations
geo_reqs = reqs.pop("geo")

setup(
    name="swisslandstats-geopy",
    version="0.10.0",
    description="Python for the Swiss Federal Statistics Geodata",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/martibosch/swisslandstats-geopy",
    author="Martí Bosch",
    author_email="marti.bosch@epfl.ch",
    license="GPL-3.0",
    packages=["swisslandstats"],
    install_requires=install_reqs,
    extras_require={"geo": geo_reqs},
    zip_safe=False,
)
