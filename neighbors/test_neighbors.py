# -*- coding: utf-8 -*-
from os.path import dirname, join

from pelican.generators import ArticlesGenerator
from pelican.tests.support import get_settings, unittest

from .neighbors import neighbors


CUR_DIR = dirname(__file__)


class NeighborsTest(unittest.TestCase):
    def test_neighbors_basic(self):
        generator = _build_article_generator(join(CUR_DIR, '..', 'test_data'))
        neighbors(generator)
    def test_neighbors_with_single_article(self):
        generator = _build_article_generator(join(CUR_DIR, 'test_data'))
        neighbors(generator)


def _build_article_generator(content_path):
    settings = get_settings(filenames={})
    settings['PATH'] = content_path
    context = settings.copy()
    context['generated_content'] = dict()
    context['static_links'] = set()
    article_generator = ArticlesGenerator(
        context=context, settings=settings,
        path=settings['PATH'], theme=settings['THEME'], output_path=None)
    article_generator.generate_context()
    return article_generator
