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


def extract_toc(content):
    if isinstance(content, contents.Static):
        return

    soup = BeautifulSoup(content._content,'html.parser')
    toc = None
    if not toc:  # default Markdown reader
        toc = soup.find('div', class_='toc')
    if not toc:  # default reStructuredText reader
        toc = soup.find('div', class_='contents topic')
    if not toc:  # Pandoc reader
        toc = soup.find('nav', id='TOC')
    if toc:
        toc.extract()
        content._content = soup.decode()
        content.toc = toc.decode()


def register():
    signals.content_object_init.connect(extract_toc)
