#!/usr/bin/env python

import os
from setuptools import setup, find_packages

# Utility function to read the README file.

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md')) as fp:
    README = fp.read()

setup(
    name='genius_lyrics',
    version='v0.2',
    description='The Python genius.com command line lyric searcher.',
    long_description=README,
    url='https://github.com/donniebishop/genius_lyrics',
    author='Donnie Bishop',
    author_email='donnie.a.bishop@gmail.com',
    license='MIT',
    packages=find_packages(),
    keywords='Genius lyrics api music CLI rap',
)
