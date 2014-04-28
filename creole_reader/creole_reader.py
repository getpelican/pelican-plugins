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

try:
    from pygments import lexers
    from pygments.formatters import HtmlFormatter
    from pygments import highlight
    PYGMENTS = True
except:
    PYGMENTS = False

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

    def _no_highlight(self, text):
        html = u'\n<pre><code>{}</code></pre>\n'.format(text)
        return html

    def _get_lexer(self, source_type, code):
        try:
            return lexers.get_lexer_by_name(source_type)
        except:
            return lexers.guess_lexer(code)

    def _get_formatter(self):
        formatter = HtmlFormatter(lineos = True, encoding='utf-8',
                                  style='colorful', outencoding='utf-8',
                                  cssclass='pygments')
        return formatter

    def _parse_code_macro(self, ext, text):
        if not PYGMENTS:
            return self._no_highlight(text)

        try:
            source_type = ''
            if '.' in ext:
                source_type = ext.strip().split('.')[1]
            else:
                source_type = ext.strip()
        except IndexError:
            source_type = ''
        lexer = self._get_lexer(source_type, text)
        formatter = self._get_formatter()

        try:
            return highlight(text, lexer, formatter).decode('utf-8')
        except:
            return self._no_highlight(text)

    # You need to have a read method, which takes a filename and returns
    # some content and the associated metadata.
    def read(self, source_path):
        """Parse content and metadata of creole files"""

        self._metadata = {}
        with pelican_open(source_path) as text:
            content = creole2html(text, macros={'header': self._parse_header_macro,
                                            'code': self._parse_code_macro})
        return content, self._metadata

def add_reader(readers):
    readers.reader_classes['creole'] = CreoleReader

def register():
    signals.readers_init.connect(add_reader)
