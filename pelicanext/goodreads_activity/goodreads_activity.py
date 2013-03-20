# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""A Pelican plugin to lists books from your Goodreads shelves.

Copyright (c) Talha Mansoor <http://onCrashReboot.com>

Author
    Talha Mansoor
Author Email
    talha131@gmail.com
Author Homepage
    http://onCrashReboot.com
Github Account
    https://github.com/talha131

Credits
-------

This plugin is inspired by Marco Milanesi <kpanic@gnufunk.org> Github activity
plugin.

How to
======

**Important** Unlike Marco's Github activity plugin, this plugin returns a
dictionary composed of the books in your Goodreads shelf and their details.

To enable it, set GOODREADS_ACTIVITY_FEED in your pelican config file. It
should point to the activity feed of your bookshelf.

To find your self's activity feed,

#. Open Goodreads homepage and login
#. Click on My Books in the top navigational bar
#. Select the bookshelf you are interested in from the left hand column
#. Look for RSS link in the footer. Copy it's link.

Here is an example,

GOODREADS_ACTIVITY_FEED='http://www.goodreads.com/review/list_rss/8028663?key=b025l3000336epw1pix047e853agggannc9932ed&shelf=currently-reading'

You can access the ``goodreads_activity`` in your Jinja2 template.

``goodreads_activity`` is a dictionary. Its valid keys are

#. 'shelf_title' it has the title of your shelf
#. 'books' it is an array of book dictionary

Valid keys for ``book`` dictionary are

#. 'title'
#. 'author'
#. 'link' link to your book review
#. 'l_cover' large cover
#. 'm_cover' medium cover
#. 's_cover' small cover
#. 'description'
#. 'rating'
#. 'review'
#. 'tags'
 
Template Example
----------------

{% if GOODREADS_ACTIVITY_FEED %}
    <h2>{{ goodreads_activity.shelf_title }}</h2>
    {% for book in goodreads_activity.books %}
        <img src="{{book.sicon}}"/>
        <header>{{book.title}}<small> by {{book.author}}</small></header>
        <article>
            {{book.description|truncate(end='')}}
            <a href={{book.link}} target="_blank">...more</a>
        </article>
    {% endfor %}
{% endif %}

"""

from pelican import signals


class GoodreadsActivity():
    def __init__(self, generator):
        try:
            import feedparser
            self.activities = feedparser.parse(
                generator.settings['GOODREADS_ACTIVITY_FEED'])
        except ImportError:
            raise Exception("Unable to find feedparser")

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
    if 'GOODREADS_ACTIVITY_FEED' in gen.settings.keys():
        gen.context['goodreads_activity'] = gen.goodreads_instance.fetch()


def initialize_feedparser(generator):
    generator.goodreads_instance = GoodreadsActivity(generator)


def register():
    signals.article_generator_init.connect(initialize_feedparser)
    signals.article_generate_context.connect(fetch_goodreads_activity)
