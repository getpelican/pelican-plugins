# -*- coding: utf-8 -*-

from setuptools import setup
from os import path
import io


HERE = path.abspath(path.dirname(__file__))

with io.open(path.join(HERE, 'Readme.rst'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='pelican-neighbors',
    version='1.0.0',
    keywords='text filter html generator pelican',
    description='Pelican plugin to add next_article (newer) and/or prev_article (older) variables to article context',
    long_description=long_description,
    author='Pelican Team',
    url='https://github.com/getpelican/pelican-plugins',
    py_modules=['neighbors'],
    install_requires=['pelican'],
    license='GNU Affero General Public License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'License :: OSI Approved :: GNU Affero General Public License v3'])
