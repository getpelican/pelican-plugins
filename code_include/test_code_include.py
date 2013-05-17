from __future__ import unicode_literals
import io
import os
import os.path
import unittest
import tempfile
import textwrap
import shutil
import subprocess
from functools import partial

from pelican import Pelican
from pelican.settings import read_settings
from pelican.utils import slugify
from pelican.tests.support import mute


def dedent(text):
    return textwrap.dedent(text).lstrip()

def redent(text, levels=1):
    return '\n'.join(
        '    ' * levels + line if line.strip() else ''
        for line in text.split('\n')
    )

open_utf8 = partial(io.open, encoding='utf-8')


INC_FILE_NAME = 'incfile.py'

INC_FILE_CONTENT = dedent("""
    # These two comment lines will not
    # be included in the output
    import random

    insults = ['I fart in your general direction',
               'your mother was a hampster',
               'your father smelt of elderberries']

    def insult():
        print random.choice(insults)
    # This comment line will be included
    # ...but this one won't
    """)

NOT_INCLUDED_LINES = [
    "These two comment lines will not",
    "be included in the output",
    "...but this one won't",
]
INCLUDED_LINES = [
    '<span class="kn">import</span> <span class="nn">random</span>',
    "This comment line will be included",
]


ARTICLE_FILE_NAME = 'yourfile.rst'

ARTICLE_FILE_CONTENT = dedent("""
    How to Insult the English
    =========================

    :author: Pierre Devereaux

    A function to help insult those silly English knnnnnnniggets:

    .. code-include:: incfile.py
        :lexer: python
        :encoding: utf-8
        :tab-width: 4
        :start-line: 2
        :end-line: 11
    """)

ARTICLE_OUTPUT_FILE_NAME = slugify('How to Insult the English') + '.html'

README_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'README.rst'
)


class TestCodeInclude(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix='pelican-plugins.')
        self.content_path = os.path.join(self.tempdir, 'content')
        self.output_path = os.path.join(self.tempdir, 'output')
        self.inc_file_path = os.path.join(self.content_path, INC_FILE_NAME)
        self.article_file_path = os.path.join(self.content_path,
                                              ARTICLE_FILE_NAME)
        os.mkdir(self.content_path)
        os.mkdir(self.output_path)
        with open_utf8(self.inc_file_path, 'w') as f:
            f.write(INC_FILE_CONTENT)
        with open_utf8(self.article_file_path, 'w') as f:
            f.write(ARTICLE_FILE_CONTENT)
        settings = read_settings(path=None, override={
            'PATH': self.content_path,
            'OUTPUT_PATH': self.output_path,
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
        with open_utf8(README_FILE, 'r') as f:
            readme_text = f.read()
        self.assertIn(redent(INC_FILE_CONTENT), readme_text)
        self.assertIn(redent(ARTICLE_FILE_CONTENT), readme_text)

    def test_code_include(self):
        mute(True)(self.pelican.run)()
        article_output_file_path = os.path.join(self.output_path,
                                                ARTICLE_OUTPUT_FILE_NAME)
        with open_utf8(article_output_file_path, 'r') as f:
            article_output_contents = f.read()
        for line in NOT_INCLUDED_LINES:
            self.assertNotIn(line, article_output_contents)
        for line in INCLUDED_LINES:
            self.assertIn(line, article_output_contents)
