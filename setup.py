#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='chembl_clippy',
    version='0.1.0',
    scripts=['chembl_clippy/clippy_all.py'],
    author='George Papadatos',
    author_email='georgep@ebi.ac.uk',
    description='A cross-platform chemical structure rendering desktop app.',
    url='https://www.ebi.ac.uk/chembl/',
    license='MIT',
    packages=['chembl_clippy'],
    long_description=open('README.md').read(),
    install_requires=['chembl_beaker',],
    package_data={
        'chembl_beaker': ['art/*'],
        },
    include_package_data=False,
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: MacOS X',
                 'Environment :: Win32 (MS Windows)',
                 'Environment :: X11 Applications',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: MacOS',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Scientific/Engineering :: Chemistry'],
    zip_safe=False,
)
