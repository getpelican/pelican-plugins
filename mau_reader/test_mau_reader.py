# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os

from pelican.readers import Readers
from pelican.tests.support import unittest, get_settings

from .mau_reader import mau_enabled

CUR_DIR = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(CUR_DIR, 'test_data')

@unittest.skipUnless(readers.Mau, "Mau isn't installed")
class MauReaderTest(ReaderTest):
    def test_article_with_metadata(self):
        reader = readers.MauReader(settings=get_settings())
        content, metadata = reader.read(_path("article_with_metadata.mau"))
        expected = {
            "category": "test",
            "title": "Test Mau file",
            "summary": "<p>I have a lot to test</p>",
            "date": SafeDatetime(2021, 2, 17, 13, 00),
            "modified": SafeDatetime(2021, 2, 17, 14, 00),
            "tags": ["foo", "bar", "foobar"],
        }
        self.assertDictHasSubset(metadata, expected)

        content, metadata = reader.read(
            _path('article_with_nonascii_metadata.mau'))
        expected = {
            'title': 'マックOS X 10.8でパイソンとVirtualenvをインストールと設定',
            'summary': '<p>パイソンとVirtualenvをまっくでインストールする方法について明確に説明します。</p>',
            'category': '指導書',
            'date': SafeDatetime(2012, 12, 20),
            'modified': SafeDatetime(2012, 12, 22),
            'tags': ['パイソン', 'マック'],
            'slug': 'python-virtualenv-on-mac-osx-mountain-lion-10.8',
        }
        self.assertDictHasSubset(metadata, expected)

    def test_article_with_mau_content(self):
        reader = readers.MauReader(settings=get_settings())
        content, _ = reader.read(_path("article_with_content.mau"))
        expected = (
            '<h1 id="h1-a%20test%20document-14001568">A test document</h1>'
            '<p>This is just a test. '
            'Some typography with <em>underscores</em> '
            'and <strong>stars</strong>.</p>'
            '<p>This is a replaced variable: 42</p>'
        )

        # Mau header ids are not deterministic
        content = content[0:31] + "14001568" + content[39:]

        self.assertEqual(content, expected)
