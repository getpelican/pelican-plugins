# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from shutil import rmtree
from tempfile import mkdtemp

from pelican.generators import ArticlesGenerator
from pelican.tests.support import unittest, get_settings
import sub_parts

CUR_DIR = os.path.dirname(__file__)


class TestSubParts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_path = mkdtemp(prefix='pelicantests.')
        settings = get_settings(filenames={})
        settings['PATH'] = os.path.join(CUR_DIR, 'test_data')
        settings['AUTHOR'] = 'Me'
        settings['DEFAULT_DATE'] = (1970, 1, 1)
        settings['DEFAULT_CATEGORY'] = 'Default'
        settings['FILENAME_METADATA'] = '(?P<slug>[^.]+)'
        settings['PLUGINS'] = [sub_parts]
        settings['CACHE_CONTENT'] = False
        context = settings.copy()
        context['generated_content'] = dict()
        context['static_links'] = set()
        cls.generator = ArticlesGenerator(
            context=context, settings=settings,
            path=settings['PATH'], theme=settings['THEME'], output_path=cls.temp_path)
        cls.generator.generate_context()
        cls.all_articles = list(cls.generator.articles)
        sub_parts.patch_subparts(cls.generator)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.temp_path)

    def test_all_articles(self):
        self.assertEqual(
            sorted(['noparent', 'parent',
                    'parent--explicit', 'parent--implicit']),
            sorted([a.slug for a in self.all_articles]))

    def test_articles(self):
        self.assertEqual(
            sorted(['noparent', 'parent']),
            sorted([a.slug for a in self.generator.articles]))

    def test_dates(self):
        self.assertEqual(
            sorted(['noparent', 'parent']),
            sorted([a.slug for a in self.generator.dates]))

    def test_categories(self):
        self.assertEqual(
            sorted(['noparent', 'parent']),
            sorted([a.slug for a in self.generator.categories[0][1]]))

    def test_tags(self):
        self.assertEqual(
            sorted([a.slug for a in self.all_articles]),
            sorted([a.slug for a in self.generator.tags['atag']]))

    def test_authors(self):
        self.assertEqual(
            sorted([a.slug for a in self.all_articles]),
            sorted([a.slug for a in self.generator.authors[0][1]]))

    def test_subparts(self):
        for a in self.all_articles:
            if a.slug == 'parent':
                self.assertTrue(hasattr(a, 'subparts'))
                self.assertEqual(
                    sorted(['parent--explicit', 'parent--implicit']),
                    sorted([a.slug for a in a.subparts]))
            else:
                self.assertFalse(hasattr(a, 'subparts'))

    def test_subpart_of(self):
        for a in self.all_articles:
            if '--' in a.slug:
                self.assertTrue(hasattr(a, 'subpart_of'))
                self.assertEqual('parent', a.subpart_of.slug)
            else:
                self.assertFalse(hasattr(a, 'subpart_of'))

    def test_subtitle(self):
        for a in self.all_articles:
            if '--' in a.slug:
                self.assertTrue(hasattr(a, 'subtitle'))
                self.assertEqual(a.title,
                                 a.subtitle + ', ' + a.subpart_of.title)


class TestSubPartsPhotos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_path = mkdtemp(prefix='pelicantests.')
        settings = get_settings(filenames={})
        settings['PATH'] = os.path.join(CUR_DIR, 'test_data')
        settings['AUTHOR'] = 'Me'
        settings['DEFAULT_DATE'] = (1970, 1, 1)
        settings['DEFAULT_CATEGORY'] = 'Default'
        settings['FILENAME_METADATA'] = '(?P<slug>[^.]+)'
        settings['PLUGINS'] = [sub_parts]
        settings['CACHE_CONTENT'] = False
        context = settings.copy()
        context['generated_content'] = dict()
        context['static_links'] = set()
        cls.generator = ArticlesGenerator(
            context=context, settings=settings,
            path=settings['PATH'], theme=settings['THEME'], output_path=cls.temp_path)
        cls.generator.generate_context()
        cls.all_articles = list(cls.generator.articles)
        for a in cls.all_articles:
            a.photo_gallery = [('i.jpg', 'i.jpg', 'it.jpg', '', '')]
        sub_parts.patch_subparts(cls.generator)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.temp_path)

    def test_subphotos(self):
        for a in self.all_articles:
            if a.slug == 'parent':
                self.assertTrue(hasattr(a, 'subphotos'))
                self.assertEqual(3, a.subphotos)
            else:
                self.assertFalse(hasattr(a, 'subphotos'))


if __name__ == '__main__':
    unittest.main()
