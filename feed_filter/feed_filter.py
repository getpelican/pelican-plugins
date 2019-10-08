# -*- coding: utf-8 -*-
"""
Feed Filter plugin for Pelican
==============================

A plugin to filter feed elements using custom filters.
"""
from datetime import datetime
from fnmatch import fnmatch
from urllib.parse import urlparse
from logging import warning
from pelican import signals
from pelican.settings import DEFAULT_CONFIG

FEED_FILTER_VERSION = '0.1'


def register():
    """Signal registration."""
    signals.initialized.connect(initialized)
    signals.feed_generated.connect(filter_feeds)


def initialized(pelican):
    DEFAULT_CONFIG.setdefault('FEED_FILTER', {})
    if pelican:
        pelican.settings.setdefault('FEED_FILTER', {})


def filter_feeds(context, feed):
    feed_filters = context['FEED_FILTER']
    for feed_path_pattern, filters in feed_filters.items():
        feed_path = get_path_from_feed_url(feed)
        if fnmatch(feed_path, feed_path_pattern):
            apply_filters_to_feed(feed, filters)


def get_path_from_feed_url(feed):
    try:
        feed_path = urlparse(feed.feed['feed_url']).path
        feed_path = feed_path.strip('/')
    except ValueError as e:
        warning('feed_filter plugin: error parsing feed url (%s)',
                str(e))
        return ''
    return feed_path


def apply_filters_to_feed(feed, filters):
    if len(feed.items) == 0:
        return

    inclusion, exclusion = dict(), dict()
    for f, value_pattern in filters.items():
        f_type, f_attr = f.split('.')
        if f_attr not in feed.items[0]:
            warning('feed_filter plugin: invalid filter attribute (%s)', f)
            continue
        if f_type == 'include':
            inclusion[f_attr] = value_pattern
        elif f_type == 'exclude':
            exclusion[f_attr] = value_pattern
        else:
            warning('feed_filter plugin: invalid filter type (%s)', f)

    if len(inclusion) == 0 and len(exclusion) == 0:
        return

    new_items = []
    for item in feed.items:
        add_it = True if len(exclusion) > 0 else False
        for attr, value_pattern in exclusion.items():
            if attribute_match(item[attr], value_pattern):
                add_it = False
        for attr, value_pattern in inclusion.items():
            if attribute_match(item[attr], value_pattern):
                add_it = True
        if add_it:
            new_items.append(item)
    feed.items = new_items


def attribute_match(attr, value):
    attr = attr if not isinstance(attr, str) else [attr]
    attr = (
        [attr.strftime('%a, %d %b %Y %H:%M:%S')]
        if isinstance(attr, datetime)
        else attr
    )
    value = value if not isinstance(value, str) else [value]
    for a in attr:
        for v in value:
            if fnmatch(a, v):
                return True
    return False
