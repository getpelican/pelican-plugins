# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from pelican.generators import ArticlesGenerator
from pelican.tests.support import unittest, get_settings
from tempfile import mkdtemp
from shutil import rmtree
import music

CUR_DIR = os.path.dirname(__file__)


class TestMusic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_path = mkdtemp(prefix='pelicantests.')
        cls.settings = get_settings(filenames={})
        cls.settings['PATH'] = os.path.join(CUR_DIR, 'test_data')
        cls.settings['MUSIC_LIBRARY'] = os.path.join(CUR_DIR, 'test_data')
        cls.settings['DEFAULT_DATE'] = (1970, 1, 1)
        cls.settings['FILENAME_METADATA'] = '(?P<slug>[^.]+)'
        cls.settings['PLUGINS'] = [music]
        cls.settings['CACHE_CONTENT'] = False
        cls.settings['OUTPUT_PATH'] = cls.temp_path
        cls.settings['SITEURL'] = 'http://getpelican.com/sub'
        cls.settings['AUTHOR'] = 'Bob Anonymous'
        music.initialized(cls)
        context = cls.settings.copy()
        context['generated_content'] = dict()
        context['static_links'] = set()
        cls.generator = ArticlesGenerator(
            context=context, settings=cls.settings,
            path=cls.settings['PATH'], theme=cls.settings['THEME'],
            output_path=cls.settings['OUTPUT_PATH'])
        music.register()
        cls.generator.generate_context()
        for article in cls.generator.articles:
            music.detect_track(cls.generator, article)
            music.detect_album(cls.generator, article)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.temp_path)

    def test_track(self):
        for a in self.generator.articles:
            if 'track' in a.metadata:
                self.assertTrue(
                    hasattr(a, 'music_track'),
                    msg="{} not recognized.".format(a.metadata['track']))

    def test_album(self):
        for a in self.generator.articles:
            if 'album' in a.metadata:
                self.assertTrue(
                    hasattr(a, 'music_album'),
                    msg="{} not recognized.".format(a.metadata['album']))

    def get_article(self, slug):
        for a in self.generator.articles:
            if slug == a.slug:
                return a
        return None

    def test_music_article_track(self):
        self.assertEqual(self.get_article('music').music_track,
                         ('best.ogg'))

    def test_music_article_album(self):
        music_album = self.get_article('filename').music_album[0][1]
        self.assertEqual(music_album[0],
                         ('best.ogg'))
        self.assertEqual(music_album[1],
                         ('mem.ogg'))

if __name__ == '__main__':
    unittest.main()
