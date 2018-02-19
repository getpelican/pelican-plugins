# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
from pelican_evernote import EvernoteNotes


class TestPelicanEvernote(unittest.TestCase):
    def test_missing_mandatory_settings(self):
        settings = {'PATH': './'}
        try:
            EvernoteNotes(settings)
        except(UserWarning) as e:
            assert (str(e)) == 'Missing mandatory credential EVERNOTE_CONSUMER_KEY'

    def test_missing_article_path(self):
        class TestClass(EvernoteNotes):
            def __init__(self):
                pass

        test_class = TestClass()
        test_class.settings = {'PATH': '/tmp', 'EVERNOTE_ARTICLE_FOLDER': 'ev_notes'}
        try:
            test_class.get_evernote_article_path()
        except(UserWarning) as e:
            assert (str(e), '/tmp/ev_notes/ folder does not exist!')


if __name__ == '__main__':
    unittest.main()
