# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from pelican.generators import ArticlesGenerator
from pelican.tests.support import unittest, get_settings
from tempfile import mkdtemp
from shutil import rmtree
import photos

CUR_DIR = os.path.dirname(__file__)


class TestPhotos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_path = mkdtemp(prefix='pelicantests.')
        cls.settings = get_settings(filenames={})
        cls.settings['PATH'] = os.path.join(CUR_DIR, 'test_data')
        cls.settings['PHOTO_LIBRARY'] = os.path.join(CUR_DIR, 'test_data')
        cls.settings['DEFAULT_DATE'] = (1970, 1, 1)
        cls.settings['FILENAME_METADATA'] = '(?P<slug>[^.]+)'
        cls.settings['PLUGINS'] = [photos]
        cls.settings['CACHE_CONTENT'] = False
        cls.settings['OUTPUT_PATH'] = cls.temp_path
        cls.settings['SITEURL'] = 'http://getpelican.com/sub'
        cls.settings['AUTHOR'] = 'Bob Anonymous'
        photos.initialized(cls)
        context = cls.settings.copy()
        context['generated_content'] = dict()
        context['static_links'] = set()
        cls.generator = ArticlesGenerator(
            context=context, settings=cls.settings,
            path=cls.settings['PATH'], theme=cls.settings['THEME'],
            output_path=cls.settings['OUTPUT_PATH'])
        photos.register()
        cls.generator.generate_context()
        for article in cls.generator.articles:
            photos.detect_image(cls.generator, article)
            photos.detect_gallery(cls.generator, article)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.temp_path)

    def test_image(self):
        for a in self.generator.articles:
            if 'image' in a.metadata:
                self.assertTrue(
                    hasattr(a, 'photo_image'),
                    msg="{} not recognized.".format(a.metadata['image']))

    def test_gallery(self):
        for a in self.generator.articles:
            if 'gallety' in a.metadata:
                self.assertTrue(
                    hasattr(a, 'photo_gallery'),
                    msg="{} not recognized.".format(a.metadata['gallery']))

    def get_article(self, slug):
        for a in self.generator.articles:
            if slug == a.slug:
                return a
        return None

    def test_photo_article_image(self):
        self.assertEqual(self.get_article('photo').photo_image,
                         ('best.jpg',
                          'photos/agallery/besta.jpg',
                          'photos/agallery/bestt.jpg'))

    def test_photo_article_gallery(self):
        photo_gallery = self.get_article('filename').photo_gallery[0][1]
        self.assertEqual(photo_gallery[0],
                         ('best.jpg',
                          'photos/agallery/best.jpg',
                          'photos/agallery/bestt.jpg',
                          'EXIF-best', 'Caption-best'))
        self.assertEqual(photo_gallery[1],
                         ('night.png',
                          'photos/agallery/night.jpg',
                          'photos/agallery/nightt.jpg',
                          'EXIF-night', ''))

    def test_photo_article_body(self):
        expected = ('<p>Here is my best photo, again.</p>\n'
                    '<p><img alt="" src="http://getpelican.com/sub/photos/agallery/besta.jpg">.</p>')
        self.assertEqual(expected, self.get_article('photo').content)

    def test_filename_article_image(self):
        self.assertEqual(
            ('best.jpg', 'photos/agallery/besta.jpg', 'photos/agallery/bestt.jpg'),
            self.get_article('filename').photo_image)

    def test_filename_article_gallery(self):
        photo_gallery = self.get_article('filename').photo_gallery[0][1]
        self.assertEqual(photo_gallery[0],
                         ('best.jpg',
                          'photos/agallery/best.jpg',
                          'photos/agallery/bestt.jpg',
                          'EXIF-best', 'Caption-best'))
        self.assertEqual(photo_gallery[1],
                         ('night.png',
                          'photos/agallery/night.jpg',
                          'photos/agallery/nightt.jpg',
                          'EXIF-night', ''))

    def test_filename_article_body(self):
        expected = ('<p>Here is my best photo, again.</p>\n'
                    '<p><img alt="" src="{filename}agallery/best.jpg">.</p>')
        self.assertEqual(expected, self.get_article('filename').content)

    def test_queue_resize(self):
        expected = [
            ('photos/agallery/best.jpg',
                (self.settings['PATH'] + '/agallery/best.jpg', (1024, 768, 80))),
            ('photos/agallery/besta.jpg',
                (self.settings['PATH'] + '/agallery/best.jpg', (760, 506, 80))),
            ('photos/agallery/bestt.jpg',
                (self.settings['PATH'] + '/agallery/best.jpg', (192, 144, 60))),
            ('photos/agallery/night.jpg',
                (self.settings['PATH'] + '/agallery/night.png', (1024, 768, 80))),
            ('photos/agallery/nightt.jpg',
                (self.settings['PATH'] + '/agallery/night.png', (192, 144, 60)))]
        self.assertEqual(sorted(expected), sorted(photos.DEFAULT_CONFIG['queue_resize'].items()))

if __name__ == '__main__':
    unittest.main()
