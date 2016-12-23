from __future__ import unicode_literals
import io
import os
import os.path
import unittest
import tempfile
import textwrap
import shutil
from functools import partial

from pelican import Pelican
from pelican.settings import read_settings
from pelican.utils import slugify
from pelican.tests.support import mute


def redent(text, levels=1):
    return '\n'.join(
        '    ' * levels + line if line.strip() else ''
        for line in text.split('\n')
    )


PLUGIN_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
README_FILE_PATH = os.path.join(PLUGIN_DIR_PATH, 'README.rst')

TEST_CONTENT_DIR_PATH = os.path.join(PLUGIN_DIR_PATH, 'test_content')
INC_FILE_PATH = os.path.join(TEST_CONTENT_DIR_PATH, 'incfile.py')
ARTICLE_FILE_PATH = os.path.join(TEST_CONTENT_DIR_PATH, 'yourfile.rst')

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

    def test_code_include_readme_content_matches_test_content(self):
        with io.open(INC_FILE_PATH, 'r', encoding='utf-8') as f:
            inc_file_content = f.read()
        with io.open(ARTICLE_FILE_PATH, 'r', encoding='utf-8') as f:
            article_file_content = f.read()
        with io.open(README_FILE_PATH, 'r', encoding='utf-8') as f:
            readme_file_content = f.read()
        self.assertIn(redent(inc_file_content), readme_file_content)
        self.assertIn(redent(article_file_content), readme_file_content)

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
