from setuptools import setup


def _get_requirements_from_files(groups_files):
    groups_reqlist = {}

    for k, v in groups_files.items():
        with open(v, 'r') as f:
            pkg_list = f.read().splitlines()
            groups_reqlist[k] = pkg_list

    return groups_reqlist


def setup_package():
    reqs = _get_requirements_from_files({'base': 'requirements.txt'})
    install_reqs = reqs.pop('base')

    # Extra dependences for geometric operations
    geo = ["geopandas"]

    # yapf: disable
    setup(
        name='swisslandstats-geopy',
        version='0.1',
        description='Python for the land statistics datasets from the SFSO',
        url='https://github.com/martibosch/swisslandstats-geopy',
        author='Martí Bosch',
        author_email='marti.bosch@epfl.ch',
        licence='BSD',
        packages=['swisslandstats'],
        install_requires=install_reqs,
        extras_require={'geo': geo},
        zip_safe=False
    )
    # yapf: enable


if __name__ == '__main__':
    setup_package()
