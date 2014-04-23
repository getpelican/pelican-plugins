#-*- conding: utf-8 -*-

'''
Creole Reader
-------------

This plugins allows you to write your posts using the wikicreole syntax. Give to
these files the creole extension.
For the syntax, look at: http://www.wikicreole.org/
'''

from pelican import readers
from pelican import signals
from pelican import settings

from pelican.utils import pelican_open

try:
    from creole import creole2html
    creole = True
except ImportError:
    creole = False

class CreoleReader(readers.BaseReader):
    enabled = creole

    file_extensions = ['creole']

    def __init__(self, settings):
        super(CreoleReader, self).__init__(settings)

    def _parse_header_macro(self, text):
        for line in text.split('\n'):
            name, value = line.split(':')
            name, value = name.strip(), value.strip()
            if name == 'title':
                self._metadata[name] = value
            else:
                self._metadata[name] = self.process_metadata(name, value)
        return u''

    # You need to have a read method, which takes a filename and returns
    # some content and the associated metadata.
    def read(self, source_path):
        """Parse content and metadata of creole files"""

        self._metadata = {}
        with pelican_open(source_path) as text:
            content = creole2html(text, macros={'header': self._parse_header_macro})
        return content, self._metadata

def add_reader(readers):
    readers.reader_classes['creole'] = CreoleReader

def register():
    signals.readers_init.connect(add_reader)
