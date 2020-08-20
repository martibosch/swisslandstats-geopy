# coding=utf-8

from setuptools import setup

long_description = """
Python tools for the Swiss Land Statistics datasets from the Swiss Federal
Statistical Office. The current features are:
* Automatically transform files from the Swiss Federal Statistical Office into
  dataframes
* Transform categorical land use/land cover information into numpy arrays and
  GeoTIFF files
* Plot categorical land use/land cover information with legend and the
  appropriate color map
* Clip dataframes by vector geometries
"""


def _get_requirements_from_files(groups_files):
    groups_reqlist = {}

    for k, v in groups_files.items():
        with open(v, 'r') as f:
            pkg_list = f.read().splitlines()
            groups_reqlist[k] = pkg_list

    return groups_reqlist


def setup_package():
    reqs = _get_requirements_from_files({
        'base': 'requirements.txt',
        'geo': 'requirements-geo.txt'
    })
    install_reqs = reqs.pop('base')

    # Extra dependences for geometric operations
    geo_reqs = reqs.pop('geo')

    # yapf: disable
    setup(
        name='swisslandstats-geopy',
        version='0.8.0',
        description='Python for the land statistics datasets from the SFSO',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/martibosch/swisslandstats-geopy',
        author='Martí Bosch',
        author_email='marti.bosch@epfl.ch',
        license='GPL-3.0',
        packages=['swisslandstats'],
        install_requires=install_reqs,
        extras_require={'geo': geo_reqs},
        zip_safe=False
    )
    # yapf: enable


if __name__ == '__main__':
    setup_package()
