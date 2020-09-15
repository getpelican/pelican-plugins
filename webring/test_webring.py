# -*- coding: utf-8 -*-
"""Tests for webring plugin

Test Atom and RSS feeds have been generated using Pelican itself using the
contents of its `samples/content` folder.
"""
import unittest
import os
from collections import Counter
from operator import itemgetter, attrgetter

from pelican.settings import DEFAULT_CONFIG
from pelican.generators import Generator
from pelican.tests.support import (
    module_exists,
    get_settings,
    get_context,
)

import webring


class NullGenerator(Generator):
    pass


@unittest.skipUnless(module_exists('feedparser'), 'install feedparser module')
class WebringTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        webring.initialized(None)
        cls.generators = [NullGenerator(
            get_context(), get_settings(), '', '', '')]
        cls.settings = cls.generators[0].settings

    def setUp(self):
        self.reset_settings()
        self.set_feeds()

    def reset_settings(self):
        for name, value in self.settings.items():
            if name.startswith('WEBRING'):
                self.settings[name] = DEFAULT_CONFIG[name]

    def set_feeds(self):
        test_data_path = os.path.join(os.path.dirname(__file__), 'test_data')
        # Contents will be duplicated but still different, as they come from
        # two different feed URLs.
        self.settings[webring.WEBRING_FEED_URLS_STR] = [
            'file://' + os.path.join(test_data_path, 'pelican-rss.xml'),
            'file://' + os.path.join(test_data_path, 'pelican-atom.xml'),
        ]

    def get_fetched_articles(self):
        return self.generators[0].context['webring_articles']

    def test_max_articles(self):
        webring.fetch_feeds(self.generators)
        articles = self.get_fetched_articles()
        self.assertLessEqual(len(articles),
                             self.settings[webring.WEBRING_MAX_ARTICLES_STR])

    def test_articles_per_feed(self):
        self.settings[webring.WEBRING_MAX_ARTICLES_STR] = 6
        self.settings[webring.WEBRING_ARTICLES_PER_FEED_STR] = 3
        webring.fetch_feeds(self.generators)
        articles = self.get_fetched_articles()
        feed_counts = Counter(a.source_id for a in articles)
        self.assertEqual(list(map(itemgetter(1), feed_counts.items())), [3, 3])

    def test_clean_summary(self):
        webring.fetch_feeds(self.generators)
        articles = self.get_fetched_articles()
        summaries = list(map(attrgetter('summary'), articles))
        self.assertTrue(all(s.find('<') < 0 for s in summaries))

    def test_dont_clean_summary(self):
        self.settings[webring.WEBRING_CLEAN_SUMMARY_HTML_STR] = False
        webring.fetch_feeds(self.generators)
        articles = self.get_fetched_articles()
        summaries = list(map(attrgetter('summary'), articles))
        self.assertTrue(all(s.find('<') >= 0 for s in summaries))

    def test_summary_length(self):
        self.settings[webring.WEBRING_SUMMARY_LENGTH_STR] = 10
        webring.fetch_feeds(self.generators)
        articles = self.get_fetched_articles()
        self.assertTrue(all(
            len(a.summary) - len('...') <= 10 for a in articles))

    def test_long_summary_length(self):
        self.settings[webring.WEBRING_SUMMARY_LENGTH_STR] = 1000
        webring.fetch_feeds(self.generators)
        articles = self.get_fetched_articles()
        self.assertTrue(not any(a.summary.endswith('...') for a in articles))

    def test_malformed_url(self):
        self.settings[webring.WEBRING_FEED_URLS_STR] = [
            '://pelican-atom.xml',
        ]
        webring.fetch_feeds(self.generators)
        self.assertEqual(len(self.get_fetched_articles()), 0)


if __name__ == '__main__':
    unittest.main()
