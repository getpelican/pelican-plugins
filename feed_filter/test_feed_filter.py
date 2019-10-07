# -*- coding: utf-8 -*-
"""Tests for the Feed Filter Plugin."""
import unittest
from datetime import datetime, timedelta

from pelican.contents import Article, Category, Author
from pelican.writers import Writer
from pelican.utils import get_date
from pelican.tests.support import get_context, get_settings

import feed_filter


class FeedFilterTestBase(object):
    @classmethod
    def setUpClass(cls):
        feed_filter.initialized(None)
        cls.writer = Writer('.', get_settings())

    def setUp(self):
        self.reset_settings()
        self.articles = []
        self.feed = None

    def reset_settings(self):
        self.context = get_context(get_settings())
        self.context['SITEURL'] = 'https://somedomain.net'
        self.context['SITENAME'] = 'Test Sitename'

    def create_articles(self, num):
        now = datetime.now()
        for i in range(num, 0, -1):
            date = now + timedelta(days=-i)
            self.articles.append(
                Article(
                    'Some content',
                    metadata={
                        'Title': 'Title ' + '{:02n}'.format(i),
                        'Date': date,
                        'Category': Category('Cat', self.context),
                        'Tags': [
                            'TagBecomesCategoryInFeed',
                            'OtherTag',
                            'Tag ' + '{:02n}'.format(i)
                        ],
                        'Author': Author('Author ' + str(i//10), self.context)
                    }
                )
            )

    def create_filtered_feed(self, feed_path):
        self.create_articles(100)
        # setup writer attributes required to create the feed
        self.writer.site_url = self.context['SITEURL']
        self.writer.feed_url = self.context['SITEURL'] + '/' + feed_path
        # create feed
        self.feed = self.writer._create_new_feed(
            self.feed_type,
            'Test feed',
            self.context
        )
        # add articles to feed
        for item in self.articles:
            self.writer._add_item_to_the_feed(self.feed, item)
        # simulate call to feed filter plugin
        feed_filter.filter_feeds(self.context, self.feed)

    def test_unmatched_feed_path_does_nothing(self):
        self.context['FEED_FILTER'] = {
            'feed/global': {
                'include.title': '*1'
            },
            'atom': {
                'include.title': '*1'
            },
        }
        self.create_filtered_feed('feed/' + self.feed_type)
        # No article was removed from the feed
        self.assertEqual(100, len(self.feed.items))

    def test_only_matched_feed_paths_are_applied(self):
        self.context['FEED_FILTER'] = {
            'feed/global': {  # does not match
                'include.title': '*02'
            },
            'feed/*': {  # match
                'include.title': '*01'
            }
        }
        self.create_filtered_feed('feed/' + self.feed_type)
        # Only one article verifies the inclusion filter
        self.assertEqual(1, len(self.feed.items))

    def test_include_only_by_title(self):
        self.context['FEED_FILTER'] = {
            'feed/*': {
                'include.title': '*05'
            }
        }
        self.create_filtered_feed('feed/' + self.feed_type)
        # Only one article verifies the inclusion filter
        self.assertEqual(1, len(self.feed.items))

    def test_exclude_only_by_category(self):
        self.context['FEED_FILTER'] = {
            'feed/*': {
                'exclude.categories': 'Tag 1?'
            }
        }
        self.create_filtered_feed('feed/' + self.feed_type)
        # Articles with Tag 10, 11, 12, ... 19, are excluded from the feed
        self.assertEqual(90, len(self.feed.items))

    def test_include_exclude_by_author(self):
        self.context['FEED_FILTER'] = {
            'feed/category.*': {
                'exclude.author_name': 'Author 4', # excludes 10 articles
                'include.title': 'Title 43', # except the one with this title
            }
        }
        self.create_filtered_feed('feed/category.' + self.feed_type)
        self.assertEqual(91, len(self.feed.items))

    def test_exclude_yesterday_article(self):
        self.context['FEED_FILTER'] = {
            'feed/category.*': {
                'exclude.pubdate':
                    (datetime.now() - timedelta(days=1)).strftime('*%d %b*'),
            }
        }
        self.create_filtered_feed('feed/category.' + self.feed_type)
        self.assertEqual(99, len(self.feed.items))


class RssFeedFilterTestCase(FeedFilterTestBase, unittest.TestCase):
    feed_type = 'rss'


class AtomFeedFilterTestCase(FeedFilterTestBase, unittest.TestCase):
    feed_type = 'atom'
