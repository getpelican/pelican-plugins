import unittest
import os
import locale
import logging
import pdf

from tempfile import mkdtemp
from pelican import Pelican
from pelican.readers import MarkdownReader
from pelican.settings import read_settings
from shutil import rmtree

CUR_DIR = os.path.dirname(__file__)


class TestPdfGeneration(unittest.TestCase):
    def setUp(self, override=None):
        self.temp_path = mkdtemp(prefix='pelicantests.')
        settings = {
            'PATH': os.path.join(CUR_DIR, '..', 'test_data', 'content'),
            'OUTPUT_PATH': self.temp_path,
            'PLUGINS': [pdf],
            'LOCALE': locale.normalize('en_US'),
        }
        if override:
            settings.update(override)

        self.settings = read_settings(override=settings)
        pelican = Pelican(settings=self.settings)

        try:
            pelican.run()
        except ValueError:
            logging.warn('Relative links in the form of ' +
                         '|filename|images/test.png are not yet handled by ' +
                         ' the pdf generator')
            pass

    def tearDown(self):
        rmtree(self.temp_path)

    def test_existence(self):
        assert os.path.exists(os.path.join(self.temp_path, 'pdf',
                                           'this-is-a-super-article.pdf'))
        if MarkdownReader.enabled:
            assert os.path.exists(os.path.join(self.temp_path, 'pdf',
                                  'a-markdown-powered-article.pdf'))
