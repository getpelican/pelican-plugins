# -*- coding: utf-8 -*-
"""
Archives per category plugin for Pelican
========================================

This plugin allows you to create separate archives for selected categories.
"""
from __future__ import unicode_literals

import calendar
import six

from itertools import groupby
from operator import attrgetter
from functools import partial

from pelican import signals


def generate_archives_per_category(generator, writer):
    """Generate per-year, per-month, and per-day archives for defined
    categories.
    """
    try:
        template = generator.get_template('archives_per_category')
    except Exception:
        try:
            template = generator.get_template('period_archives')
        except Exception:
            template = generator.get_template('archives')

    categories_to_archive = generator.settings.get('CATEGORIES_TO_ARCHIVE')

    period_save_as = {
        'year': generator.settings.get('YEAR_ARCHIVES_PER_CATEGORY_SAVE_AS'),
        'month': generator.settings.get('MONTH_ARCHIVES_PER_CATEGORY_SAVE_AS'),
        'day': generator.settings.get('DAY_ARCHIVES_PER_CATEGORY_SAVE_AS')
    }

    period_date_key = {
        'year': attrgetter('date.year'),
        'month': attrgetter('date.year', 'date.month'),
        'day': attrgetter('date.year', 'date.month', 'date.day')
    }

    def _generate_archives_per_category(dates, key, save_as_fmt):
        """Generate period category archives from `dates`, grouped by `key` and
        written to `save_as`.
        """
        write = partial(writer.write_file,
                        relative_urls=generator.settings['RELATIVE_URLS'])

        for _period, group in groupby(dates, key=key):
            archive = list(group)

            def get_category(item):
                return item.category
            for category, articles in groupby(archive, lambda x: x.category):
                if (categories_to_archive is not None and
                        (category not in categories_to_archive and
                         category.slug not in categories_to_archive)):
                    # Skip unwanted categories defined by name or slug
                    continue

                category_archive = list(articles)

                date = category_archive[0].date
                save_as = save_as_fmt.format(date=date, category=category.slug)
                context = generator.context.copy()

                context["category"] = category
                context["category-slug"] = category.slug
                context["articles"] = category_archive

                if key == period_date_key['year']:
                    context["period"] = (_period,)
                else:
                    month_name = calendar.month_name[_period[1]]
                    if not six.PY3:
                        month_name = month_name.decode('utf-8')
                    if key == period_date_key['month']:
                        context["period"] = (_period[0], month_name)
                    else:
                        context["period"] = (_period[0], month_name,
                                             _period[2])

                write(save_as, template, context, dates=category_archive,
                      blog=True)

    for period in 'year', 'month', 'day':
        save_as = period_save_as[period]
        if save_as:
            key = period_date_key[period]
            _generate_archives_per_category(generator.dates, key, save_as)


def register():
    signals.article_writer_finalized.connect(generate_archives_per_category)
