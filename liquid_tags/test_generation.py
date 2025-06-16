# -*- coding: utf-8 -*-
from __future__ import print_function

import filecmp
import logging
import os
import unittest
from shutil import rmtree
from tempfile import mkdtemp

import pytest
from pelican import Pelican
from pelican.settings import read_settings

from .notebook import IPYTHON_VERSION

PLUGIN_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(PLUGIN_DIR, 'test_data')


class TestFullRun(unittest.TestCase):
    '''Test running Pelican with the Plugin'''

    def setUp(self):
        '''Create temporary output and cache folders'''
        self.temp_path = mkdtemp(prefix='pelicantests.')
        self.temp_cache = mkdtemp(prefix='pelican_cache.')
        os.chdir(TEST_DATA_DIR)

    def tearDown(self):
        '''Remove output and cache folders'''
        rmtree(self.temp_path)
        rmtree(self.temp_cache)
        os.chdir(PLUGIN_DIR)

    @unittest.skipIf(IPYTHON_VERSION not in (2, 3),
                     reason="iPython v%d is not supported" % IPYTHON_VERSION)
    def test_generate(self):
        '''Test generation of site with the plugin.'''

        # set paths
        _pj = os.path.join
        base_path = _pj(os.path.dirname(os.path.abspath(__file__)), 'test_data')
        content_path = _pj(base_path, 'content')
        output_path = _pj(base_path, 'output')
        settings_path = _pj(base_path, 'pelicanconf.py')

        # read settings
        override = {
                'PATH': content_path,
                'OUTPUT_PATH': self.temp_path,
                'CACHE_PATH': self.temp_cache,
        }
        settings = read_settings(path=settings_path, override=override)

        # run and test created files
        pelican = Pelican(settings)
        pelican.run()

        # test existence
        assert os.path.exists(_pj(self.temp_path,
                                  'test-ipython-notebook-nb-format-3.html'))
        assert os.path.exists(_pj(self.temp_path,
                                  'test-ipython-notebook-nb-format-4.html'))

        # test differences
        if IPYTHON_VERSION == 3:
            f1 = _pj(output_path, 'test-ipython-notebook-v2.html')
            f2 = _pj(self.temp_path, 'test-ipython-notebook.html')
            #assert filecmp.cmp(f1, f2)
        elif IPYTHON_VERSION == 2:
            f1 = _pj(output_path, 'test-ipython-notebook-v3.html')
            f2 = _pj(self.temp_path, 'test-ipython-notebook.html')
            #assert filecmp.cmp(f1, f2)
        else:
            logging.error('Unexpected IPYTHON_VERSION: %s', IPYTHON_VERSION)
            assert False

