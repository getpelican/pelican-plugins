# -*- coding: utf-8 -*-
# This file is part of Shinxsearch for Pelican
#
# Copyright (C) 2017 Ysard
#
# Shinxsearch for Pelican is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Shinxsearch for Pelican is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinxsearch for Pelican.
# If not, see <http://www.gnu.org/licenses/>.

'''
Sphinx Search
-------------

This pelican plugin generates an xmlpipe2 formatted file that can be used by the
sphinxsearch indexer to index the entire site.
'''

from __future__ import unicode_literals

import os.path
from bs4 import BeautifulSoup
from codecs import open
import html
import zlib

from pelican import signals


class sphinxsearch_xml_generator(object):

    def __init__(self, context, settings, path, theme, output_path, *null):

        self.output_path = output_path
        self.context = context
        self.siteurl = settings.get('SITEURL')
        self.dict_nodes = []


    def get_raw_text(self, html_content):

        html_content = BeautifulSoup(html_content, "html.parser")

        # Todo: Suppress this ?
        # lots of entities are rencoded by html.escape func,
        # and Sphinsearch index can strip html entities
        cleaner_db = \
            {'“': '"',
             '”': '"',
             '’': "'",
             '^': '&#94;',
             '¶': ' ',
            }

        # Get raw text from html & replace some entitites
        raw_text = list()
        for string in html_content.stripped_strings:
            for old, new in cleaner_db.items():
                string = string.replace(old, new)

            raw_text.append(string)

        # Escape all html entities to respect xml rules
        return html.escape(' '.join(raw_text))


    def build_data(self, page):

        # Only published pages are concerned (not drafts)
        if getattr(page, 'status', 'published') != 'published':
            return

        # Reconstruct url (without the extension)
        page_url = self.siteurl + '/' + page.url
        # Get timestamp
        page_time = str(page.date.timestamp())

        # There may be possible collisions, but it's the best I can think of.
        page_index = zlib.crc32(str(page_time + page_url).encode('utf-8'))

        return {'title':  self.get_raw_text(page.title),
                'author': page.author,
                'tags': page.category,
                'url': page_url,
                'content': self.get_raw_text(page.content),
                'slug': page.slug,
                'time': page_time,
                'index': page_index,
                'summary': self.get_raw_text(page.summary)}


    def generate_output(self, writer):

        # Export sphinxsearch.xml in output folder
        path = os.path.join(self.output_path, 'sphinxsearch.xml')

        pages = self.context['pages'] + self.context['articles']

        for article in self.context['articles']:
            pages += article.translations

        with open(path, 'w', encoding='utf-8') as fd:
            fd.write('<?xml version="1.0" encoding="utf-8"?><sphinx:docset>')
            for page in pages:
                data = self.build_data(page)
                fd.write(
                    '<sphinx:document id="{0}">'
                    '<title>{1}</title>'
                    '<author>{2}</author>'
                    '<category>{3}</category>'
                    '<url>{4}</url>'
                    '<content><![CDATA[{5}]]></content>'
                    '<summary><![CDATA[{6}]]></summary>'
                    '<slug>{7}</slug>'
                    '<published>{8}</published>'
                    '</sphinx:document>'.format(
                        data['index'],
                        data['title'],
                        data['author'],
                        data['tags'],
                        data['url'],
                        data['content'],
                        data['summary'],
                        data['slug'],
                        data['time']
                    )
                )
            fd.write('</sphinx:docset>')


def get_generators(generators):
    return sphinxsearch_xml_generator


def register():
    signals.get_generators.connect(get_generators)
