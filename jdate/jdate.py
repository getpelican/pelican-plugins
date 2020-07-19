#! /usr/bin/env python3
# Danial Behzadi - 2018
# Released under AGPLv3

"""
Jdate Plugin for Pelican
========================

This plugins changes locale date to Jalali/Persian.
"""

from pelican import signals
from dateutil import parser
from jdatetime import datetime as convert

def jdate(generator):
    if generator.settings['DEFAULT_LANG'] != 'fa':
        print("You've been used jdate plugin, but the default language is not Persian!")
        return

    date_format = generator.settings['DEFAULT_DATE_FORMAT']
    for article in generator.articles:
        safe_date = getattr(article, 'date')
        date = parser.isoparse(safe_date.isoformat())
        jdate = convert.fromgregorian(date=date)
        formatted_jdate = str(jdate.strftime(date_format))
        trans_digits = str.maketrans({'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'})
        locale_date = formatted_jdate.translate(trans_digits)
        setattr(article, 'locale_date', locale_date)

def register():
    signals.article_generator_finalized.connect(jdate)
