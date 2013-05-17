"""
Extract Table of Content
========================

This plugin allows you to extract table of contents (ToC) from article.content
and place it in its own article.toc variable.
"""

from os import path
from bs4 import BeautifulSoup
from pelican import signals, readers


def extract_toc(content):
    soup = BeautifulSoup(content._content)
    filename = content.source_path
    extension = path.splitext(filename)[1][1:]
    toc = ''
    # if it is a Markdown file
    if extension in readers.MarkdownReader.file_extensions:
        toc = soup.find('div', class_='toc')
    # else if it is a reST file
    elif extension in readers.RstReader.file_extensions:
        toc = soup.find('div', class_='contents topic')
    if toc:
        toc.extract()
        content._content = soup.decode()
        content.toc = toc.decode()


def register():
    signals.content_object_init.connect(extract_toc)
