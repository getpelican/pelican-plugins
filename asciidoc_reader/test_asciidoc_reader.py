# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os

from pelican.readers import Readers
from pelican.tests.support import unittest, get_settings

from .asciidoc_reader import asciidoc_enabled

CUR_DIR = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(CUR_DIR, 'test_data')

@unittest.skipUnless(asciidoc_enabled, "asciidoc isn't installed")
class AsciiDocReaderTest(unittest.TestCase):
    def read_file(self, path, **kwargs):
        # Isolate from future API changes to readers.read_file
        r = Readers(settings=get_settings(**kwargs))
        return r.read_file(base_path=CONTENT_PATH, path=path)

    def test_article_with_asc_extension(self):
        # Ensure the asc extension is being processed by the correct reader
        page = self.read_file(
            path='article_with_asc_extension.asc')
        expected = ('<div class="sect1">\n'
                    '<h2 id="_used_for_pelican_test">'
                    'Used for pelican test</h2>\n'
                    '<div class="sectionbody">\n'
                    '<div class="paragraph">'
                    '<p>The quick brown fox jumped over '
                    'the lazy dog&#8217;s back.</p>'
                    '</div>\n</div>\n</div>\n')
        self.assertEqual(page.content, expected)
        expected = {
            'category': 'Blog',
            'author': 'Author O. Article',
            'title': 'Test AsciiDoc File Header',
            'date': datetime.datetime(2011, 9, 15, 9, 5),
            'tags': ['Linux', 'Python', 'Pelican'],
        }

        for key, value in expected.items():
            self.assertEqual(value, page.metadata[key], key)

    def test_article_with_asc_options(self):
        # test to ensure the ASCIIDOC_OPTIONS is being used
        page = self.read_file(
            path='article_with_asc_options.asc',
            ASCIIDOC_OPTIONS=["-a revision=1.0.42"]
        )
        expected = ('<div class="sect1">\n'
                    '<h2 id="_used_for_pelican_test">'
                    'Used for pelican test</h2>\n'
                    '<div class="sectionbody">\n'
                    '<div class="paragraph">'
                    '<p>version 1.0.42</p></div>\n'
                    '<div class="paragraph">'
                    '<p>The quick brown fox jumped over '
                    'the lazy dog&#8217;s back.</p>'
                    '</div>\n</div>\n</div>\n')
        self.assertEqual(page.content, expected)


    def test_unicode(self):
        page = self.read_file(
            path='article_with_utf8.asc',
        )
        expected = (u'<div id="preamble">\n'
                    '<div class="sectionbody">\n'
                    '<div class="paragraph">'
                    '<p>A utf-8 euro sign: \u20ac</p>'
                    '</div>\n</div>\n</div>\n')
        self.assertEqual(page.content, expected)


    def test_pygments_source_highlighter(self):
        page = self.read_file(
            path='article_for_pygments_highlighting.asc',
            ASCIIDOC_OPTIONS=['-a source-highlighter=pygments']
        )
        expected = (u'<div id="preamble">\n'
                    '<div class="sectionbody">\n'
                    '<div class="listingblock">\n'
                    '<div class="content"><div class="highlight"><pre><span class="k">Given </span><span class="nf">we are using pygments</span>\n'
                    '<span class="k">And </span><span class="nf">source-highlight doesnt recognise gherkin</span>\n'
                    '<span class="k">Then </span><span class="nf">this should work</span>\n'
                    '</pre></div></div></div>\n'
                    '</div>\n'
                    '</div>\n')

        self.assertMultiLineEqual(page.content, expected)


    def test_images(self):
        page = self.read_file(
            path='article_with_image.asc',
        )
        expected = (u'<div id="preamble">\n'
                    '<div class="sectionbody">\n'
                    '<div class="imageblock">\n'
                    '<div class="content">\n'
                    '<img src="images/image.png" alt="alt text">\n'
                    '</div>\n'
                    '<div class="title">Figure 1. An image</div>\n'
                    '</div>\n'
                    '</div>\n'
                    '</div>\n')

        self.assertMultiLineEqual(page.content, expected)



