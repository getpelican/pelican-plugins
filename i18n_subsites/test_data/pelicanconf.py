#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITEURL = 'http://example.com/test'
# to make the test suite portable
TIMEZONE = 'UTC'

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
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

from blinker import signal
tmpsig = signal('tmpsig')
I18N_FILTER_SIGNALS = [tmpsig]

DEFAULT_LANG = 'en'

# Base setting used to render the theme.
AUTHOR = 'The Tester'

LOCALE = 'en_US.UTF-8'
# Having all the translatable values in a root dict help organize
# the translation and coordinate with the development and
# the translation teams.
L10N = {
    'SITE_NAME': 'Testing site',
    'COMPANY': {
        # This is not translated to test deep merge.
        'NAME': 'Acme',
        # This is translated.
        'INCORPORATION': 'Ltd'
        },
}

# Translation for pelicanconf.py settings.
I18N_SUBSITES = {
    'de': {
        'AUTHOR': 'Der Tester',
        'L10N': {
            'SITE_NAME': 'Testseite',
            'COMPANY': {'INCORPORATION': 'AG'}
        },
        'LOCALE': 'de_DE.UTF-8',
        },
    'cz': {
        'AUTHOR': 'Test Testovič',
        'L10N': {
            'SITE_NAME': 'Testovací stránka',
        },
        'I18N_UNTRANSLATED_PAGES': 'remove',
        'I18N_UNTRANSLATED_ARTICLES': 'keep',
        },
    }
