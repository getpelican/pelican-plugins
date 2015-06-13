#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'The Tester'
SITENAME = 'Testing site'
SITEURL = 'http://example.com/test'

# to make the test suite portable
TIMEZONE = 'UTC'

DEFAULT_LANG = 'en'
LOCALE = 'en_US.UTF-8'

# Generate only one feed
FEED_ALL_ATOM = 'feeds_all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Disable unnecessary pages
CATEGORY_SAVE_AS = ''
TAG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAGS_SAVE_AS = ''

PLUGIN_PATHS = ['../../']
PLUGINS = ['i18n_subsites']

THEME = 'localized_theme'
JINJA_EXTENSIONS = ['jinja2.ext.i18n']

from blinker import signal
tmpsig = signal('tmpsig')
I18N_FILTER_SIGNALS = [tmpsig]

I18N_SUBSITES = {
    'de': {
        'SITENAME': 'Testseite',
        'AUTHOR': 'Der Tester',
        'LOCALE': 'de_DE.UTF-8',
        },
    'cz': {
        'SITENAME': 'Testovací stránka',
        'AUTHOR': 'Test Testovič',
        'I18N_UNTRANSLATED_PAGES': 'remove',
        'I18N_UNTRANSLATED_ARTICLES': 'keep',
        },
    }
