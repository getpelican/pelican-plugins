# -*- coding: utf-8 -*-
import os, shutil

from pelican.generators import ArticlesGenerator
from pelican.tests.support import get_settings, unittest
from pelican.writers import Writer

from ctags_generator import generate_ctags


CUR_DIR = os.path.dirname(__file__)
TEST_CONTENT_DIR = os.path.join(CUR_DIR, 'test_content')


class CtagsGeneratorTest(unittest.TestCase):

    def test_generate_ctags(self):
        settings = get_settings(filenames={})
        settings['GENERATE_CTAGS'] = True

        generator = ArticlesGenerator(
            context=settings.copy(), settings=settings,
            path=TEST_CONTENT_DIR, theme=settings['THEME'], output_path=None)
        generator.generate_context()

        writer = Writer(None, settings=settings)
        generate_ctags(generator, writer)

        output_path = os.path.join(TEST_CONTENT_DIR, 'tags')
        self.assertTrue(os.path.exists(output_path))

        try:
            # output content is correct
            with open(output_path, 'r') as output_file:
                ctags = [l.split('\t')[0] for l in output_file.readlines()]
                self.assertEqual(['bar', 'bar', 'foo', 'foo', 'foobar', 'foobar', 'マック', 'パイソン'], ctags)
        finally:
            os.remove(output_path)
