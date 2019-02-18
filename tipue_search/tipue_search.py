# -*- coding: utf-8 -*-
"""
Tipue Search
============

A Pelican plugin to serialize generated HTML to JSON
that can be used by jQuery plugin - Tipue Search.

Copyright (c) Talha Mansoor
"""

from __future__ import unicode_literals

import os.path
import json
from bs4 import BeautifulSoup
from codecs import open
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from pelican import signals


class Tipue_Search_JSON_Generator(object):

    def __init__(self, context, settings, path, theme, output_path, *null):

        self.output_path = output_path
        self.context = context
        self.siteurl = settings.get('SITEURL')
        self.relative_urls = settings.get('RELATIVE_URLS')
        self.tpages = settings.get('TEMPLATE_PAGES')
        self.output_path = output_path
        self.json_nodes = []


    def create_json_node(self, page):

        if getattr(page, 'status', 'published') != 'published':
            return

        soup_title = BeautifulSoup(page.title.replace('&nbsp;', ' '), 'html.parser')
        page_title = soup_title.get_text(' ', strip=True).replace('“', '"').replace('”', '"').replace('’', "'").replace('^', '&#94;')

        soup_text = BeautifulSoup(page.content, 'html.parser')
        page_text = soup_text.get_text(' ', strip=True).replace('“', '"').replace('”', '"').replace('’', "'").replace('¶', ' ').replace('^', '&#94;')
        page_text = ' '.join(page_text.split())

        page_category = page.category.name if getattr(page, 'category', 'None') != 'None' else ''

        page_url = '.'
        if page.url:
            page_url = page.url if self.relative_urls else (self.siteurl + '/' + page.url)

        node = {'title': page_title,
                'text': page_text,
                'tags': page_category,
                'url': page_url,
                'loc': page_url} # changed from 'url' following http://blog.siphos.be/2015/08/updates-on-my-pelican-adventure/ (an update to Pelican made it not work, because the update (e.g., in the theme folder, static/tipuesearch/tipuesearch.js is looking for the 'loc' attribute.

        self.json_nodes.append(node)


    def create_tpage_node(self, srclink):

        srcfile = open(os.path.join(self.output_path, self.tpages[srclink]), encoding='utf-8')
        soup = BeautifulSoup(srcfile, 'html.parser')
        page_title = soup.title.string if soup.title is not None else ''
        page_text = soup.get_text()

        # Should set default category?
        page_category = ''
        page_url = urljoin(self.siteurl, self.tpages[srclink])

        node = {'title': page_title,
                'text': page_text,
                'tags': page_category,
                'url': page_url}

        self.json_nodes.append(node)


    def generate_output(self, writer):
        path = os.path.join(self.output_path, 'tipuesearch_content.js')

        pages = self.context['pages'] + self.context['articles']

        for article in self.context['articles']:
            pages += article.translations

        for srclink in self.tpages:
            self.create_tpage_node(srclink)

        for page in pages:
            self.create_json_node(page)
        root_node = {'pages': self.json_nodes}
        
        root_node_js = 'var tipuesearch = ' + json.dumps(root_node, separators=(',', ':'), ensure_ascii=False) + ';'

        with open(path, 'w', encoding='utf-8') as fd:
            fd.write(root_node_js)


def get_generators(generators):
    return Tipue_Search_JSON_Generator


def register():
    signals.get_generators.connect(get_generators)
