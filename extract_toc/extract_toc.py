# -*- coding: utf-8 -*-
"""
Extract Table of Content
========================

A Pelican plugin to extract table of contents (ToC) from `article.content` and
place it in its own `article.toc` variable for use in templates.
"""

from os import path
from bs4 import BeautifulSoup
from pelican import signals, readers, contents
import logging

logger = logging.getLogger(__name__)


def extract_toc(content):
    if isinstance(content, contents.Static):
        return

    soup = BeautifulSoup(content._content, 'html.parser')
    filename = content.source_path
    extension = path.splitext(filename)[1][1:]
    toc = None

    # default Markdown reader
    if not toc and readers.MarkdownReader.enabled and extension in readers.MarkdownReader.file_extensions:
        toc = soup.find('div', class_='toc')
        if toc:
            toc.extract()
            if len(toc.find_next('ul').find_all('li')) == 0:
                toc = None

    # default reStructuredText reader
    if not toc and readers.RstReader.enabled and extension in readers.RstReader.file_extensions:
        toc = soup.find('div', class_='contents topic')
        if toc:
            toc.extract()
            tag = BeautifulSoup(str(toc), 'html.parser')
            tag.div['class'] = 'toc'
            tag.div['id'] = ''
            p = tag.find('p', class_='topic-title first')
            if p:
                p.extract()
            toc = tag

    # Pandoc reader (markdown and other formats)
    if 'pandoc_reader' in content.settings['PLUGINS']:
        try:
            from pandoc_reader import PandocReader
        except ImportError:
            PandocReader = False
        if not toc and PandocReader and PandocReader.enabled and extension in PandocReader.file_extensions:
            toc = soup.find('nav', id='TOC')

    if toc:
        toc.extract()
        content._content = soup.decode()
        content.toc = toc.decode()
        if content.toc.startswith('<html>'):
            content.toc = content.toc[12:-14]


def register():
    signals.content_object_init.connect(extract_toc)
