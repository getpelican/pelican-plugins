# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path
import re

from docutils import io, nodes, statemachine, utils
from docutils.utils.error_reporting import SafeString, ErrorString
from docutils.parsers.rst import directives, Directive

from pelican.rstdirectives import Pygments


class CodeInclude(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'lexer': directives.unchanged,
                   'encoding': directives.encoding,
                   'linenos': directives.unchanged,
                   'linenostart': directives.unchanged,
                   'tab-width': int,
                   'start-line': int,
                   'end-line': int}

    def fetch_url(self, url):
        import requests

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('Got a bad status looking up url.')
        body = response.text
        if not body:
            raise Exception('Unable to get the url contents.')

        return body

    def start_end_lines(self, text, startline, endline):
        try:
            lines = text.splitlines(True)
            rawtext = ''.join(lines[startline:endline])
        except UnicodeError as error:
            raise self.severe('Problem with "%s" directive:\n%s' %
                              (self.name, ErrorString(error)))
        return rawtext

    def run(self):
        """Include a file as part of the content of this reST file."""
        if not self.state.document.settings.file_insertion_enabled:
            raise self.warning('"%s" directive disabled.' % self.name)
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1)
        source_dir = os.path.dirname(os.path.abspath(source))

        startline = self.options.get('start-line', None)
        endline = self.options.get('end-line', None)

        encoding = self.options.get(
            'encoding', self.state.document.settings.input_encoding)
        e_handler = self.state.document.settings.input_encoding_error_handler
        tab_width = self.options.get(
            'tab-width', self.state.document.settings.tab_width)

        if re.match('^https*://', self.arguments[0]):
            rawtext = self.fetch_url(self.arguments[0])
            if startline or (endline is not None):
                rawtext = self.start_end_lines(rawtext, startline, endline)

        else:
            path = directives.path(self.arguments[0])
            path = os.path.normpath(os.path.join(source_dir, path))
            path = utils.relative_path(None, path)
            path = nodes.reprunicode(path)

            try:
                self.state.document.settings.record_dependencies.add(path)
                include_file = io.FileInput(source_path=path,
                                            encoding=encoding,
                                            error_handler=e_handler)
            except UnicodeEncodeError as error:
                raise self.severe('Problems with "%s" directive path:\n'
                                  'Cannot encode input file path "%s" '
                                  '(wrong locale?).' %
                                  (self.name, SafeString(path)))
            except IOError as error:
                    raise self.severe('Problems with "%s" directive '
                                      'path:\n%s.' %
                                      (self.name, ErrorString(error)))
            self.options['source'] = path

            if startline or (endline is not None):
                rawtext = include_file.read()
                rawtext = self.start_end_lines(rawtext, startline, endline)

        include_lines = statemachine.string2lines(rawtext, tab_width,
                                                  convert_whitespace=True)

        # default lexer to 'text'
        lexer = self.options.get('lexer', 'text')
        linenos = self.options.get('linenos', 'none')
        linenostart = self.options.get('linenostart', 1)

        codeblock = Pygments(self.name,
                             [lexer],  # arguments
                             { 'linenos': linenos, 'linenostart': linenostart },  # no options for this directive
                             include_lines,  # content
                             self.lineno,
                             self.content_offset,
                             self.block_text,
                             self.state,
                             self.state_machine)
        return codeblock.run()


def register():
    directives.register_directive('code-include', CodeInclude)
