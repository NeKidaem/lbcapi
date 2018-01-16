#!/usr/bin/env python
import os
from setuptools import setup

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'lbcapi',
    version = '1.0.3',
    packages = ['lbcapi'],
    include_package_data = True,
    license = 'MIT License',
    description = 'Make API calls to LocalBitcoins API.',
    author = 'MarcoRacer',
    url = 'https://github.com/marcoracer/lbcapi',
    install_requires=[
        'requests',
    ],
)
