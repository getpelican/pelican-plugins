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

def aggregate_multi_part(generator):
        multi_part = defaultdict(list)

        for article in generator.articles:
            if 'series' in article.metadata:
                multi_part[article.metadata['series']].append(article)
            elif 'parts' in article.metadata:
                warning("multi_part plugin: the 'parts' metadata has been deprecated: use 'series' instead")
                multi_part[article.metadata['parts']].append(article)

        for part_id in multi_part:
            parts = multi_part[part_id]

            # Sort by date
            parts.sort(key=lambda x: x.metadata['date'])

            enumerated_parts = list(enumerate(parts))

            for idx, article in enumerated_parts:
                article.multi_part = dict()
                article.multi_part['series'] = part_id
                article.multi_part['index'] = idx
                article.multi_part['all'] = parts
                article.multi_part['previous'] = parts[0:idx]
                article.multi_part['next'] = parts[idx+1:]

def register():
    signals.article_generator_finalized.connect(aggregate_multi_part)
