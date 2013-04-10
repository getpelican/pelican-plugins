# -*- coding: utf-8 -*-
"""
Goodreads Activity
==================

A Pelican plugin to lists books from your Goodreads shelves.

Copyright (c) Talha Mansoor
"""

from __future__ import unicode_literals
from pelican import signals
import feedparser


class GoodreadsActivity():
    def __init__(self, generator):
        self.activities = feedparser.parse(
            generator.settings['GOODREADS_ACTIVITY_FEED'])

    def fetch(self):
        goodreads_activity = {
            'shelf_title': self.activities.feed.title,
            'books': []
        }
        for entry in self.activities['entries']:
            book = {
                'title': entry.title,
                'author': entry.author_name,
                'link': entry.link,
                'l_cover': entry.book_large_image_url,
                'm_cover': entry.book_medium_image_url,
                's_cover': entry.book_small_image_url,
                'description': entry.book_description,
                'rating': entry.user_rating,
                'review': entry.user_review,
                'tags': entry.user_shelves
            }
            goodreads_activity['books'].append(book)

        return goodreads_activity


def fetch_goodreads_activity(gen, metadata):
    if 'GOODREADS_ACTIVITY_FEED' in gen.settings:
        gen.context['goodreads_activity'] = gen.goodreads.fetch()


def initialize_feedparser(generator):
    generator.goodreads = GoodreadsActivity(generator)


def register():
    signals.article_generator_init.connect(initialize_feedparser)
    signals.article_generate_context.connect(fetch_goodreads_activity)
