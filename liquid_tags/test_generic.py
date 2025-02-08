# -*- coding: utf-8 -*-
from __future__ import print_function

import filecmp
import os
import unittest
from shutil import rmtree
from tempfile import mkdtemp

import pytest
from pelican import Pelican
from pelican.settings import read_settings

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


    def test_generic_tag_with_config(self):
        '''Test generation of site with a generic tag that reads in a config file.'''

        _pj = os.path.join
        base_path = _pj(os.path.dirname(os.path.abspath(__file__)), 'test_data')
        content_path = _pj(base_path, 'content')
        output_path = _pj(base_path, 'output')
        settings_path = _pj(base_path, 'pelicanconf.py')
        override = {
                'PATH': content_path,
                'OUTPUT_PATH': self.temp_path,
                'CACHE_PATH': self.temp_cache,
        }
        settings = read_settings(path=settings_path, override=override)

        pelican = Pelican(settings)
        pelican.run()

        # test normal tags
        f = _pj(self.temp_path, 'test-generic-config-tag.html')
        assert os.path.exists(f)
        assert "Tester" in open(f).read()

        # test differences
        f1 = _pj(output_path, 'test-ipython-notebook-v3.html')
        f2 = _pj(self.temp_path, 'test-ipython-notebook.html')
        #assert filecmp.cmp(f1, f2)

    def test_generic_alt_delimiters(self):
        '''Test generation of site with alternatively delimited tags.'''

        _pj = os.path.join
        base_path = _pj(os.path.dirname(os.path.abspath(__file__)), 'test_data')
        content_path = _pj(base_path, 'content')
        output_path = _pj(base_path, 'output')
        settings_path = _pj(base_path, 'pelicanconf.py')
        override = {
                'PATH': content_path,
                'OUTPUT_PATH': self.temp_path,
                'CACHE_PATH': self.temp_cache,
                'LT_DELIMITERS': ('<+', '+>'),
        }
        settings = read_settings(path=settings_path, override=override)

        pelican = Pelican(settings)
        pelican.run()

        # test alternate delimiters
        f = _pj(self.temp_path, 'test-alternate-tag-delimiters.html')
        fc = open(f).read()
        assert '{% generic config author %} is stupid' in fc
        assert 'The Tester is smart' in fc
        assert 'The Tester is stupid' not in fc

