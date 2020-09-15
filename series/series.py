# -*- coding: utf-8 -*-
"""
This plugin extends the original series plugin
by FELD Boris <lothiraldan@gmail.com>

Copyright (c) Leonardo Giordani <giordani.leonardo@gmail.com>

Joins articles in a series and provides variables to
manage the series in the template.
"""

from collections import defaultdict
from operator import itemgetter

from pelican import signals


def aggregate_series(generator):
    series = defaultdict(list)

    # This cycles through all articles in the given generator
    # and collects the 'series' metadata, if present.
    # The 'series_index' metadata is also stored, if specified
    for article in generator.articles:
        if 'series' in article.metadata:
            article_entry = (
                article.metadata.get('series_index', None),
                article.metadata['date'],
                article
            )

            series[article.metadata['series']].append(article_entry)

    # This uses items() which on Python2 is not a generator
    # but we are dealing with a small amount of data so
    # there shouldn't be performance issues =)
    for series_name, series_articles in series.items():
        # This is not DRY but very simple to understand
        forced_order_articles = [
            art_tup for art_tup in series_articles if art_tup[0] is not None]

        date_order_articles = [
            art_tup for art_tup in series_articles if art_tup[0] is None]

        forced_order_articles.sort(key=itemgetter(0))
        date_order_articles.sort(key=itemgetter(1))

        all_articles = forced_order_articles + date_order_articles
        ordered_articles = [art_tup[2] for art_tup in all_articles]
        enumerated_articles = enumerate(ordered_articles)

        for index, article in enumerated_articles:
            article.series = dict()
            article.series['name'] = series_name
            article.series['index'] = index + 1
            article.series['all'] = ordered_articles
            article.series['all_previous'] = ordered_articles[0: index]
            article.series['all_next'] = ordered_articles[index + 1:]

            if index > 0:
                article.series['previous'] = ordered_articles[index - 1]
            else:
                article.series['previous'] = None

            try:
                article.series['next'] = ordered_articles[index + 1]
            except IndexError:
                article.series['next'] = None


def register():
    signals.article_generator_finalized.connect(aggregate_series)
