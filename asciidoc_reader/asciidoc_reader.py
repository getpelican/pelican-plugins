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
import six

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

    def read(self, source_path):
        """Parse content and metadata of asciidoc files"""
        from cStringIO import StringIO
        with pelican_open(source_path) as source:
            text = StringIO(source.encode('utf8'))
        content = StringIO()
        ad = AsciiDocAPI()

        options = self.settings.get('ASCIIDOC_OPTIONS', [])
        options = self.default_options + options
        for o in options:
            ad.options(*o.split())

        backend = self.settings.get('ASCIIDOC_BACKEND', self.default_backend)
        ad.execute(text, content, backend=backend)
        content = content.getvalue().decode('utf8')

        metadata = {}
        for name, value in ad.asciidoc.document.attributes.items():
            name = name.lower()
            metadata[name] = self.process_metadata(name, six.text_type(value))
        if 'doctitle' in metadata:
            metadata['title'] = metadata['doctitle']
        return content, metadata

def add_reader(readers):
    for ext in AsciiDocReader.file_extensions:
        readers.reader_classes[ext] = AsciiDocReader

def register():
    signals.readers_init.connect(add_reader)
