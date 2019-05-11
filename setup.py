#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher-example: setup.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE and WARRANTY for details.
"""Setuptools module."""
from os import path
try:  # pip version 9
    from pip.req import parse_requirements
except ImportError:
    from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

INSTALL_REQS = parse_requirements('requirements.txt', session='hack')

setup(
    name='pacifica-dispatcher-example',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='An example Pacifica Dispatcher',
    url='https://github.com/pacifica/pacifica-dispatcher-example/',
    long_description=open(path.join(
        path.abspath(path.dirname(__file__)),
        'README.md')).read(),
    long_description_content_type='text/markdown',
    author='Mark Borkum',
    author_email='mark.borkum@pnnl.gov',
    packages=find_packages(),
    namespace_packages=['pacifica'],
    include_package_data=True,
    package_data={'': ['*.txt']},
    entry_points={
        'console_scripts': [
            'pacifica-dispatcher-example=pacifica.dispatcher_example.__main__:main',
        ],
    },
    install_requires=[str(ir.req) for ir in INSTALL_REQS]
)
