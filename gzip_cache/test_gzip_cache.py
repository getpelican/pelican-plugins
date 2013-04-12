# -*- coding: utf-8 -*-
'''Core plugins unit tests'''

import os
import tempfile
import unittest

from contextlib import contextmanager
from tempfile import mkdtemp
from shutil import rmtree

import gzip_cache

@contextmanager
def temporary_folder():
    """creates a temporary folder, return it and delete it afterwards.

    This allows to do something like this in tests:

        >>> with temporary_folder() as d:
            # do whatever you want
    """
    tempdir = mkdtemp()
    try:
        yield tempdir
    finally:
        rmtree(tempdir)


class TestGzipCache(unittest.TestCase):

    def test_should_compress(self):
        # Some filetypes should compress and others shouldn't.
        self.assertTrue(gzip_cache.should_compress('foo.html'))
        self.assertTrue(gzip_cache.should_compress('bar.css'))
        self.assertTrue(gzip_cache.should_compress('baz.js'))
        self.assertTrue(gzip_cache.should_compress('foo.txt'))

        self.assertFalse(gzip_cache.should_compress('foo.gz'))
        self.assertFalse(gzip_cache.should_compress('bar.png'))
        self.assertFalse(gzip_cache.should_compress('baz.mp3'))
        self.assertFalse(gzip_cache.should_compress('foo.mov'))

    def test_creates_gzip_file(self):
        # A file matching the input filename with a .gz extension is created.

        # The plugin walks over the output content after the finalized signal
        # so it is safe to assume that the file exists (otherwise walk would
        # not report it). Therefore, create a dummy file to use.
        with temporary_folder() as tempdir:
            _, a_html_filename = tempfile.mkstemp(suffix='.html', dir=tempdir)
            gzip_cache.create_gzip_file(a_html_filename)
            self.assertTrue(os.path.exists(a_html_filename + '.gz'))

