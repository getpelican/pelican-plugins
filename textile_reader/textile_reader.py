# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import datetime
import logging
import os
import re

from pelican import signals
from pelican.readers import BaseReader
from pelican.contents import Page, Category, Tag, Author
from pelican.utils import get_date, pelican_open


try:
    from textile import textile
except ImportError:
    textile = False


class TextileReader(BaseReader):
    enabled = bool(textile)
    file_extensions = ['textile']

    def __init__(self, *args, **kwargs):
        super(TextileReader, self).__init__(*args, **kwargs)

    def _parse_metadata(self, meta):
        """Return the dict containing document metadata"""
        output = {}
        for name, value in meta.items():
            name = name.lower()
            if name == "summary":
                summary = textile(value)
                output[name] = self.process_metadata(name, summary)
            else:
                output[name] = self.process_metadata(name, value)
        return output

    def read(self, source_path):
        """Parse content and metadata of textile files"""

        with pelican_open(source_path) as text:
            parts = text.split('----',1)
            if len(parts)==2:
                headerlines = parts[0].splitlines()
                headerpairs = map(lambda l:l.split(':',1), headerlines)
                headerdict = { pair[0]:pair[1].strip()
                               for pair in headerpairs
                               if len(pair)==2 }
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
