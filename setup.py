# coding=utf-8

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

    setup(
        name='sfso_geopy',
        version='0.1',
        description='foo',
        url='https://github.com/martibosch/sfso_geopy',
        author='Martí Bosch',
        author_email='marti.bosch@epfl.ch',
        licence='BSD',
        packages=['sfso_geopy'],
        install_requires=install_reqs,
        zip_safe=False)


if __name__ == '__main__':
    setup_package()
