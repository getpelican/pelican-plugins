# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open

try:
    from textile import textile
except ImportError:
    textile = False


class TextileReader(BaseReader):
    """Reader for Textile files.  Written using the core MarkdownReader as
a template.  Textile input files must be of the form:

Title: An example
Date: 2013-08-10
----
p. Lorem ipsum dolar sit amet...

Specifically, the header values as with Markdown files, then four
dashes, then the body.

    """

    enabled = bool(textile)
    file_extensions = ['textile']

    def __init__(self, *args, **kwargs):
        super(TextileReader, self).__init__(*args, **kwargs)

    def _parse_metadata(self, meta):
        """Process the metadata dict, lowercasing the keys and textilizing the
value of the 'summary' key (if present).  Keys that share the same
lowercased form will be overridden in some arbitrary order.

        """
        output = {}
        for name, value in meta.items():
            name = name.lower()
            if name == "summary":
                value = textile(value)
            output[name] = self.process_metadata(name, value)
        return output

    def read(self, source_path):
        """Parse content and metadata of textile files."""

        with pelican_open(source_path) as text:
            parts = text.split('----', 1)
            if len(parts) == 2:
                headerlines = parts[0].splitlines()
                headerpairs = map(lambda l: l.split(':', 1), headerlines)
                headerdict = {pair[0]: pair[1].strip()
                              for pair in headerpairs
                              if len(pair) == 2}
                metadata = self._parse_metadata(headerdict)
                content = textile(parts[1])
            else:
                metadata = {}
                content = textile(text)

        return content, metadata


def add_reader(readers):
    readers.reader_classes['textile'] = TextileReader


def register():
    signals.readers_init.connect(add_reader)
