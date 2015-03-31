#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess

PLUGINS = ['liquid_tags',
           'series']

if __name__ == "__main__":
    for plugin in PLUGINS:
        print('Running test for {} plugin'.format(plugin))
        subprocess.call('{}/runtests.py'.format(plugin))
