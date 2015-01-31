# -*- coding: utf-8 -*-
"""
AsciiDoc Reader
===============

This plugin allows you to use AsciiDoc to write your posts. 
File extension should be ``.asc``, ``.adoc``, or ``asciidoc``.
"""

from pelican.readers import BaseReader
from pelican.utils import pelican_open
from pelican import signals
import logging, inspect

logger = logging.getLogger(__name__)
whoami = lambda: inspect.stack()[1][3]

try:
    # asciidocapi won't import on Py3
    from .asciidocapi import AsciiDocAPI, AsciiDocError
    # AsciiDocAPI class checks for asciidoc.py
    AsciiDocAPI()
except:
    asciidoc_enabled = False
else:
    asciidoc_enabled = True



class AsciiDocReader(BaseReader):
    """Reader for AsciiDoc files"""

    enabled = asciidoc_enabled
    file_extensions = ['asc', 'adoc', 'asciidoc']
    default_options = ["--no-header-footer", "-a newline=\\n"]
    default_backend = 'html5'

    def oread(self, source_path):
        """Parse content and metadata of asciidoc files"""

        from cStringIO import StringIO
        with pelican_open(source_path) as source:
            text = StringIO(source)
        content = StringIO()
        ad = AsciiDocAPI()

        options = self.settings.get('ASCIIDOC_OPTIONS', [])
        options = self.default_options + options
        for o in options:
            ad.options(*o.split())

        backend = self.settings.get('ASCIIDOC_BACKEND', self.default_backend)
        ad.execute(text, content, backend=backend)
        content = content.getvalue()

        metadata = {}
        for name, value in ad.asciidoc.document.attributes.items():
            name = name.lower()
            metadata[name] = self.process_metadata(name, value)
        if 'doctitle' in metadata:
            metadata['title'] = metadata['doctitle']
        return content, metadata


def add_writer(self, content):
    if hasattr(content, 'save_as'):
        content.override_save_as = content.save_as.replace('-None', '')
    if hasattr(content, 'url'):
        content.override_url = content.url.replace('-None', '')

def add_reader(readers):
    for ext in AsciiDocReader.file_extensions:
        readers.reader_classes[ext] = AsciiDocReader

def register():
    signals.readers_init.connect(add_reader)
    signals.article_generator_write_article.connect(add_writer)
