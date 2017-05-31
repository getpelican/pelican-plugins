import unittest
import os
import six
import tag_cloud

from pelican.generators import ArticlesGenerator
from pelican.tests.support import get_settings
from pelican.urlwrappers import Tag

CUR_DIR = os.path.dirname(__file__)
CONTENT_DIR = os.path.join(CUR_DIR, 'test_data')


class TestTagCloudGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._settings = get_settings(filenames={})
        cls._settings['DEFAULT_CATEGORY'] = 'Default'
        cls._settings['DEFAULT_DATE'] = (1970, 1, 1)
        cls._settings['READERS'] = {'asc': None}
        cls._settings['CACHE_CONTENT'] = False
        tag_cloud.set_default_settings(cls._settings)

        cls.generator = ArticlesGenerator(
            context=cls._settings.copy(), settings=cls._settings,
            path=CONTENT_DIR, theme=cls._settings['THEME'], output_path=None)
        cls.generator.generate_context()

    def test_tag_cloud_random(self):
        self.generator.settings['TAG_CLOUD_STEPS'] = 10
        self.generator.settings['TAG_CLOUD_BADGE'] = False
        tag_cloud.generate_tag_cloud(self.generator)
        expected = [
            (Tag('pelican', self._settings), 1),
            (Tag('plugins', self._settings), 2),
            (Tag('fun', self._settings), 3),
            (Tag('python', self._settings), 10)
        ]
        six.assertCountEqual(self, self.generator.tag_cloud, expected)

    def test_tag_cloud_badge(self):
        self.generator.settings['TAG_CLOUD_STEPS'] = 10
        self.generator.settings['TAG_CLOUD_BADGE'] = True
        tag_cloud.generate_tag_cloud(self.generator)
        expected = [
            (Tag('pelican', self._settings), 1, 5),
            (Tag('plugins', self._settings), 2, 4),
            (Tag('fun', self._settings), 3, 3),
            (Tag('python', self._settings), 10, 1)
        ]
        six.assertCountEqual(self, self.generator.tag_cloud, expected)

    def test_tag_cloud_alphabetical(self):
        self.generator.settings['TAG_CLOUD_STEPS'] = 10
        self.generator.settings['TAG_CLOUD_SORTING'] = 'alphabetically'
        tag_cloud.generate_tag_cloud(self.generator)
        expected = [
            (Tag('fun', self._settings), 3),
            (Tag('pelican', self._settings), 1),
            (Tag('plugins', self._settings), 2),
            (Tag('python', self._settings), 10)
        ]
        self.assertEqual(self.generator.tag_cloud, expected)

    def test_tag_cloud_alphabetical_rev(self):
        self.generator.settings['TAG_CLOUD_STEPS'] = 10
        self.generator.settings['TAG_CLOUD_SORTING'] = 'alphabetically-rev'
        tag_cloud.generate_tag_cloud(self.generator)
        expected = [
            (Tag('python', self._settings), 10),
            (Tag('plugins', self._settings), 2),
            (Tag('pelican', self._settings), 1),
            (Tag('fun', self._settings), 3)
        ]
        self.assertEqual(self.generator.tag_cloud, expected)

    def test_tag_cloud_size(self):
        self.generator.settings['TAG_CLOUD_STEPS'] = 10
        self.generator.settings['TAG_CLOUD_SORTING'] = 'size'
        tag_cloud.generate_tag_cloud(self.generator)
        expected = [
            (Tag('pelican', self._settings), 1),
            (Tag('plugins', self._settings), 2),
            (Tag('fun', self._settings), 3),
            (Tag('python', self._settings), 10)
        ]
        self.assertEqual(self.generator.tag_cloud, expected)

    def test_tag_cloud_size_rev(self):
        self.generator.settings['TAG_CLOUD_STEPS'] = 10
        self.generator.settings['TAG_CLOUD_SORTING'] = 'size-rev'
        tag_cloud.generate_tag_cloud(self.generator)
        expected = [
            (Tag('python', self._settings), 10),
            (Tag('fun', self._settings), 3),
            (Tag('plugins', self._settings), 2),
            (Tag('pelican', self._settings), 1)
        ]
        self.assertEqual(self.generator.tag_cloud, expected)

if __name__ == "__main__":
    unittest.main()
