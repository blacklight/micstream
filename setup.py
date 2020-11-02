#!/usr/bin/env python
import os

from setuptools import setup, find_packages


def path(fname=''):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fname))


def readfile(fname):
    with open(path(fname)) as f:
        return f.read()


setup(
    name="micstream",
    version="0.1",
    author="Fabio Manganiello",
    author_email="info@fabiomanganiello.com",
    description="Stream an audio source as mp3 over HTTP",
    license="MIT",
    python_requires='>= 3.6',
    keywords="mp3 stream http",
    url="https://github.com/BlackLight/micstream",
    packages=find_packages(),
    include_package_data=True,
    long_description=readfile('README.md'),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'micstream=micstream.__main__:main',
        ],
    },
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
    ],
)
