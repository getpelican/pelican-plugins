# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Goodreads Activity
==================

A Pelican plugin to lists books from your Goodreads shelves.

Copyright (c) Talha Mansoor

Author          | Talha Mansoor
----------------|-----
Author Email    | talha131@gmail.com 
Author Homepage | http://onCrashReboot.com 
Github Account  | https://github.com/talha131 

## Credits

This plugin is inspired by Marco Milanesi <kpanic@gnufunk.org> Github activity
plugin.

How to Use
==========

**Important** Unlike Marco's Github activity plugin, this plugin returns
a dictionary composed of the books in your Goodreads shelf and their
details.

To enable it, set `GOODREADS_ACTIVITY_FEED` in your pelican config file.
It should point to the activity feed of your bookshelf.

To find your self's activity feed,

1.  Open Goodreads homepage and login
2.  Click on My Books in the top navigational bar
3.  Select the bookshelf you are interested in from the left hand column
4.  Look for RSS link in the footer. Copy it's link.

Here is an example feed of currently-reading shelf,

```python
GOODREADS_ACTIVITY_FEED='http://www.goodreads.com/review/list_rss/8028663?key=b025l3000336epw1pix047e853agggannc9932ed&shelf=currently-reading'
```

You can access the `goodreads_activity` in your Jinja2 template.
`goodreads_activity` is a dictionary. Its valid keys are

1.  `shelf_title` it has the title of your shelf
2.  `books` it is an array of book dictionary

Valid keys for `book` dictionary are

1.  `title`
2.  `author`
3.  `link` link to your book review
4.  `l_cover` large cover
5.  `m_cover` medium cover
6.  `s_cover` small cover
7.  `description`
8.  `rating`
9.  `review`
10. `tags`

Template Example
================

```python
{% if GOODREADS_ACTIVITY_FEED %}
    <h2>{{ goodreads_activity.shelf_title }}</h2>
    {% for book in goodreads_activity.books %}
        <img src="{{book.s_cover}}"/>
        <header>{{book.title}}<small> by {{book.author}}</small></header>
        <article>{{book.description|truncate(end='')}}
        <a href={{book.link}} target="_blank">...more</a></article>
    {% endfor %}
{% endif %}
```
"""

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
    if 'GOODREADS_ACTIVITY_FEED' in gen.settings.keys():
        gen.context['goodreads_activity'] = gen.goodreads_instance.fetch()


def initialize_feedparser(generator):
    generator.goodreads_instance = GoodreadsActivity(generator)


def register():
    signals.article_generator_init.connect(initialize_feedparser)
    signals.article_generate_context.connect(fetch_goodreads_activity)
