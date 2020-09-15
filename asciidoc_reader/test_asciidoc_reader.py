# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os

from pelican.readers import Readers
from pelican.tests.support import unittest, get_settings

from .asciidoc_reader import ENABLED

CUR_DIR = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(CUR_DIR, 'test_data')

@unittest.skipUnless(ENABLED, "asciidoc isn't installed")
class AsciiDocReaderTest(unittest.TestCase):
    def read_file(self, path, **kwargs):
        # Isolate from future API changes to readers.read_file
        r = Readers(settings=get_settings(**kwargs))
        return r.read_file(base_path=CONTENT_PATH, path=path)

    def test_article_with_asc_extension(self):
        # Ensure the asc extension is being processed by the correct reader
        page = self.read_file(
            path='article_with_asc_extension.asc')
        expected = ('<div class="sect1">'
                    '<h2 id="_used_for_pelican_test">'
                    'Used for pelican test</h2>'
                    '<div class="sectionbody">'
                    '<div class="paragraph">'
                    '<p>The quick brown fox jumped over '
                    'the lazy dog&#8217;s back.</p>'
                    '</div></div></div>')
        actual = "".join(page.content.splitlines())
        expected = "".join(expected.splitlines())
        self.assertEqual(actual, expected)
        expected = {
            'category': 'Blog',
            'author': 'Author O. Article',
            'title': 'Test AsciiDoc File Header',
            'date': datetime.datetime(2011, 9, 15, 9, 5),
            'tags': ['Linux', 'Python', 'Pelican'],
        }
        for key, value in expected.items():
            self.assertEqual(value, page.metadata[key], (
                'Metadata attribute \'%s\' does not match expected value.\n'
                'Expected: %s\n'
                'Actual: %s') % (key, value, page.metadata[key]))

    def test_article_with_asc_options(self):
        # test to ensure the ASCIIDOC_OPTIONS is being used
        page = self.read_file(path='article_with_asc_options.asc',
            ASCIIDOC_OPTIONS=["-a revision=1.0.42"])
        expected = ('<div class="sect1">'
                    '<h2 id="_used_for_pelican_test">'
                    'Used for pelican test</h2>'
                    '<div class="sectionbody">'
                    '<div class="paragraph">'
                    '<p>version 1.0.42</p></div>'
                    '<div class="paragraph">'
                    '<p>The quick brown fox jumped over '
                    'the lazy dog&#8217;s back.</p>'
                    '</div></div></div>')
        actual = "".join(page.content.splitlines())
        expected = "".join(expected.splitlines())
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
