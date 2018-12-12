#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="lib-py-insightly",
    version="0.0.3",

    description='Python wrapper around the Insightly API',
    long_description=open('README.md').read(),
    author='Henry Marment',
    author_email='henrymarment@gmail.com',
    url='',
    keywords='python',
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
)