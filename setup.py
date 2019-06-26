#!/usr/bin/env python
import os

from distutils.core import setup
from setuptools import find_packages

__author__ = 'Aleksandar Savkov'


# allow setup.py to be run from any path
this_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(os.path.normpath(this_dir))

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()[1:]

with open('README.md') as fh:
    description = fh.read()

setup(
    name='bioeval',
    version='1.1.2.dev0',
    description='BIO and BEISO evaluation library',
    author='Sasho Savkov',
    author_email='me@sasho.io',
    url='https://github.com/savkov/bioeval',
    packages=find_packages(exclude=('tests', 'prl', 'res')),
    zip_safe=True,
    include_package_data=True,
    license='MIT',
    long_description=description,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: Unix',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering'
    ]
)
