# -*- coding: utf-8 -*-
from os.path import dirname, join
from tempfile import TemporaryDirectory

from pelican import Pelican
from pelican.generators import ArticlesGenerator
from pelican.settings import configure_settings
from pelican.tests.support import get_settings, unittest
from pelican.writers import Writer

from .math import pelican_init, process_rst_and_summaries


CUR_DIR = dirname(__file__)


class RenderMathTest(unittest.TestCase):
    def test_ok_on_shared_test_data(self):
        settings = get_settings(filenames={})
        settings['PATH'] = join(CUR_DIR, '..', 'test_data')
        pelican_init(PelicanMock(settings))
        with TemporaryDirectory() as tmpdirname:
            generator = _build_article_generator(settings, tmpdirname)
            process_rst_and_summaries([generator])
    def test_ok_on_custom_data(self):
        settings = get_settings(filenames={})
        settings['PATH'] = join(CUR_DIR, 'test_data')
        settings['PLUGINS'] = ['pelican-ipynb.markup']  # to also parse .ipynb files
        configure_settings(settings)
        pelican_mock = PelicanMock(settings)
        pelican_init(pelican_mock)
        Pelican.init_plugins(pelican_mock)
        with TemporaryDirectory() as tmpdirname:
            generator = _build_article_generator(settings, tmpdirname)
            process_rst_and_summaries([generator])
            for article in generator.articles:
                if article.source_path.endswith('.rst'):
                    self.assertIn('mathjaxscript_pelican', article.content)
            generator.generate_output(Writer(tmpdirname, settings=settings))


def _build_article_generator(settings, output_path):
    context = settings.copy()
    context['generated_content'] = dict()
    context['static_links'] = set()
    article_generator = ArticlesGenerator(
        context=context, settings=settings,
        path=settings['PATH'], theme=settings['THEME'], output_path=output_path)
    article_generator.generate_context()
    return article_generator

class PelicanMock:
    'A dummy class exposing the only attributes needed'
    def __init__(self, settings):
        self.plugins = []
        self.settings = settings
