# -*- coding: utf-8 -*-
"""
Dateish Plugin for Pelican
==========================

This plugin adds the ability to treat arbitrary metadata fields as datetime
objects.
"""

from pelican import signals
from pelican.utils import get_date


def dateish(generator):
    if 'DATEISH_PROPERTIES' not in generator.settings:
        return

    for article in generator.articles:
        for field in generator.settings['DATEISH_PROPERTIES']:
            if hasattr(article, field):
                text = getattr(article, field)
                as_datetime = get_date(text)
                setattr(article, field, as_datetime)

def register():
    signals.article_generator_finalized.connect(dateish)
