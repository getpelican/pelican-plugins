import os
import os.path
import unittest
import tempfile
import shutil
import subprocess


INC_FILE_NAME = 'incfile.py'

INC_FILE_CONTENT = b"""# These two comment lines will not
# be included in the output
import random

insults = ['I fart in your general direction',
           'your mother was a hampster',
           'your father smelt of elderberries']

def insult():
    print random.choice(insults)
# This comment line will be included
# ...but this one won't
"""

ARTICLE_FILE_NAME = 'yourfile.rst'

ARTICLE_FILE_CONTENT = b"""How to Insult the English
=========================

:author: Pierre Devereaux

A function to help insult those silly English knnnnnnniggets:

.. code-include:: incfile.py
    :lexer: python
    :encoding: utf-8
    :tab-width: 4
    :start-line: 3
    :end-line: 11
"""

CONFIG_FILE_NAME = 'pelicanconf.py'
CONFIG_FILE_CONTENT = b"""PLUGINS = ['code_include']
DEFAULT_DATE = 'fs'
"""

class TestCodeInclude(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix='pelican-plugins.')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_import(self):
        from code_include import CodeInclude

    def test_plugin(self):
        config_file_path = os.path.join(self.tempdir, CONFIG_FILE_NAME)
        content_path = os.path.join(self.tempdir, 'content')
        os.mkdir(content_path)
        output_path = os.path.join(self.tempdir, 'output')
        os.mkdir(output_path)
        inc_file_path = os.path.join(content_path, INC_FILE_NAME)
        article_file_path = os.path.join(content_path, ARTICLE_FILE_NAME)
        with open(inc_file_path, 'wb') as f:
            f.write(INC_FILE_CONTENT)
        with open(article_file_path, 'wb') as f:
            f.write(ARTICLE_FILE_CONTENT)
        with open(config_file_path, 'wb') as f:
            f.write(CONFIG_FILE_CONTENT)
        subprocess.check_output([
            'pelican',
            '-s', config_file_path,
            '-o', output_path,
            content_path,
        ])




