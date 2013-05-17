from __future__ import unicode_literals
import io
import os
import os.path
import unittest
import tempfile
import shutil
from functools import partial

from pelican import Pelican
from pelican.settings import read_settings
from pelican.utils import slugify
from pelican.tests.support import mute


PLUGIN_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_CONTENT_DIR_PATH = os.path.join(PLUGIN_DIR_PATH, 'test_content')

NOT_INCLUDED_LINES = [
    "These two comment lines will not",
    "be included in the output",
    "...but this one won't",
]
INCLUDED_LINES = [
    '<span class="kn">import</span> <span class="nn">random</span>',
    "This comment line will be included",
]

ARTICLE_OUTPUT_FILE_NAME = slugify('How to Insult the English') + '.html'


class TestCodeInclude(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix='pelican-plugins.')
        settings = read_settings(path=None, override={
            'PATH': TEST_CONTENT_DIR_PATH,
            'OUTPUT_PATH': self.tempdir,
            'PLUGINS': ['code_include'],
            'DEFAULT_DATE': 'fs',
            'SITEURL': 'http://www.example.com/blog',
            'TIMEZONE': 'UTC',
        })
        self.pelican = Pelican(settings=settings)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_code_include_import(self):
        from code_include import CodeInclude

    def test_code_include(self):
        mute(True)(self.pelican.run)()
        article_output_file_path = os.path.join(self.tempdir,
                                                ARTICLE_OUTPUT_FILE_NAME)
        with io.open(article_output_file_path, encoding='utf-8') as f:
            article_output_contents = f.read()
        for line in NOT_INCLUDED_LINES:
            self.assertNotIn(line, article_output_contents)
        for line in INCLUDED_LINES:
            self.assertIn(line, article_output_contents)
