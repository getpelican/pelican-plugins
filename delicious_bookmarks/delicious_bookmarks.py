# -*- coding: utf-8 -*-

"""
Copyright (c) Gianluca Hotz (http://www.ghotz.com)

Delicious Activity
---------------
A plugin to list your Delicious activity
Inspired by
	https://github.com/getpelican/pelican-plugins/tree/master/github_activity
	https://github.com/getpelican/pelican-plugins/tree/master/goodreads_activity
"""

from __future__ import unicode_literals, print_function

import logging
logger = logging.getLogger(__name__)

from pelican import signals


class DeliciousBookmarks():
    """
        A class created to fetch Delicious with feedparser
    """
    def __init__(self, generator):
        import feedparser
        self.channel = feedparser.parse(
            generator.settings['DELICIOUS_BOOKMARKS_FEED'])

    def fetch(self):
        """
            returns nested channel/bookmarks/tags information
        """
        delicious_channel = {
            'title': self.channel.feed.title,
            'description': self.channel.feed.description,
            'bookmarks': []
        }
        for bookmark in self.channel['entries']:
            delicious_bookmark = {
                'title': bookmark.title,
                'description': bookmark.description,
                'link': bookmark.link,
                'tags': []
	    }
            for tag in bookmark.tags:
                delicious_tag = {
                    'term': tag.term,
                    'scheme': tag.scheme
                }
            	delicious_bookmark['tags'].append(delicious_tag)
            delicious_channel['bookmarks'].append(delicious_bookmark)
        return delicious_channel
                
    """
            for tag in bookmark.tags:
            	delicious_bookmark['tags'].append(tag)
            delicious_channel['bookmarks'].append(delicious_bookmark)
        return delicious_channel
    """


def fetch_delicious_bookmarks(gen, metadata):
    """
        registered handler for the Delicious Bookmarks plugin
        it puts in generator.context the html needed to be displayed on a
        template
    """

    if 'DELICIOUS_BOOKMARKS_FEED' in gen.settings.keys():
        gen.context['delicious_bookmarks'] = gen.plugin_instance.fetch()


def feed_parser_initialization(generator):
    """
        Initialization of feed parser
    """

    generator.plugin_instance = DeliciousBookmarks(generator)


def register():
    """
        Plugin registration
    """
    try:
        signals.article_generator_init.connect(feed_parser_initialization)
        signals.article_generator_context.connect(fetch_delicious_bookmarks)
    except ImportError:
        logger.warning('`delicious_bookmarks` failed to load dependency `feedparser`.'
                       '`delicious_bookmarks` plugin not loaded.')
