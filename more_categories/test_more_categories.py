"""Unit tests for the more_categories plugin"""

import os
import unittest

from . import more_categories
from pelican.generators import ArticlesGenerator
from pelican.tests.support import get_context, get_settings


class TestArticlesGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        more_categories.register()
        settings = get_settings()
        settings['DEFAULT_CATEGORY'] = 'default'
        settings['CACHE_CONTENT'] = False
        settings['PLUGINS'] = more_categories
        context = get_context(settings)

        base_path = os.path.dirname(os.path.abspath(__file__))
        test_data_path = os.path.join(base_path, 'test_data')
        cls.generator = ArticlesGenerator(
            context=context, settings=settings,
            path=test_data_path, theme=settings['THEME'], output_path=None)
        cls.generator.generate_context()

    def test_generate_categories(self):
        """Test whether multiple categories are generated correctly,
        including ancestor categories"""

        cats_generated = [cat.name for cat, _ in self.generator.categories]
        cats_expected = ['default', 'foo', 'foo/bar', 'foo/baz',]
        self.assertEqual(sorted(cats_generated), sorted(cats_expected))

    def test_assign_articles_to_categories(self):
        """Test whether articles are correctly assigned to categories,
        including whether articles are not assigned multiple times to the same
        ancestor category"""

        for cat, articles in self.generator.categories:
            self.assertEqual(len(articles), 1)