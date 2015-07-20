# -*- coding: utf-8 -*-
"""
Copyright (c) FELD Boris <lothiraldan@gmail.com>

Multiple part support
=====================

Create a navigation menu for multi-part related_posts
"""

from collections import defaultdict

from pelican import signals

from logging import warning

warning_message = """multi_part plugin: this plugin has been deprecated.
The 'series' plugin provides better support for multi part articles.
"""

def aggregate_multi_part(generator):
    warning(warning_message)
    multi_part = defaultdict(list)

    for article in generator.articles:
        if 'parts' in article.metadata:
            multi_part[article.metadata['parts']].append(article)

    for part_id in multi_part:
        parts = multi_part[part_id]

        # Sort by date
        parts.sort(key=lambda x: x.metadata['date'])

        for article in parts:
            article.metadata['parts_articles'] = parts


def register():
    signals.article_generator_finalized.connect(aggregate_multi_part)
