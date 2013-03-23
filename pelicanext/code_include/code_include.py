# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os.path

from docutils import io, nodes, statemachine, utils
from docutils.utils.error_reporting import SafeString, ErrorString
from docutils.parsers.rst import directives, Directive

from pelican.rstdirectives import Pygments

"""
Include Pygments highlighted code with reStructuredText
=======================================================

:author: Colin Dunklau

Use this plugin to make writing coding tutorials easier! You can
maintain the example source files separately from the actual article.


Based heavily on ``docutils.parsers.rst.directives.Include``. Include
a file and output as a code block formatted with pelican's Pygments
directive.

Note that this is broken with the Docutils 0.10 release, there's a
circular import. It was fixed in trunk:
http://sourceforge.net/p/docutils/bugs/214/

Directives
----------

.. code:: rst

    .. code-include:: incfile.py
        :lexer: string, name of the Pygments lexer to use, default 'text'
        :encoding: string, encoding with which to open the file
        :tab-width: integer, hard tabs are replaced with `tab-width` spaces
        :start-line: integer, starting line to begin reading include file
        :end-line: integer, last line from include file to display

``start-line``, and ``end-line`` have the same meaning as in the
docutils ``include`` directive, that is, they index from zero.

Example
-------

./incfile.py:

.. code:: python

    # These two comment lines will not
    # be included in the output
    import random

    insults = ['I fart in your general direction',
               'your mother was a hampster',
               'your father smelt of elderberries']

    def insult():
        print random.choice(insults)
    # This comment line will be included
    # ...but this one won't

./yourfile.rst:

.. code:: rst

    How to Insult the English
    =========================

    :author: Pierre Devereaux

    A function to help insult those silly English knnnnnnniggets:

    .. code-include:: incfile.py
        :lexer: python
        :encoding: utf-8
        :tab-width: 4
        :start-line: 3
        :end-line: 11

"""

class CodeInclude(Directive):

    """
    Include content read from a separate source file, and highlight
    it with the given lexer (using pelican.rstdirectives.CodeBlock)

    The encoding of the included file can be specified. Only a part
    of the given file argument may be included by specifying start
    and end line. Hard tabs will be replaced with ``tab-width``
    spaces.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'lexer': directives.unchanged,
                   'encoding': directives.encoding,
                   'tab-width': int,
                   'start-line': int,
                   'end-line': int}

    def run(self):
        """Include a file as part of the content of this reST file."""
        if not self.state.document.settings.file_insertion_enabled:
            raise self.warning('"%s" directive disabled.' % self.name)
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1)
        source_dir = os.path.dirname(os.path.abspath(source))
        path = directives.path(self.arguments[0])
        path = os.path.normpath(os.path.join(source_dir, path))
        path = utils.relative_path(None, path)
        path = nodes.reprunicode(path)
        encoding = self.options.get(
            'encoding', self.state.document.settings.input_encoding)
        e_handler=self.state.document.settings.input_encoding_error_handler
        tab_width = self.options.get(
            'tab-width', self.state.document.settings.tab_width)
        try:
            self.state.document.settings.record_dependencies.add(path)
            include_file = io.FileInput(source_path=path,
                                        encoding=encoding,
                                        error_handler=e_handler)
        except UnicodeEncodeError, error:
            raise self.severe(u'Problems with "%s" directive path:\n'
                              'Cannot encode input file path "%s" '
                              '(wrong locale?).' %
                              (self.name, SafeString(path)))
        except IOError, error:
            raise self.severe(u'Problems with "%s" directive path:\n%s.' %
                      (self.name, ErrorString(error)))
        startline = self.options.get('start-line', None)
        endline = self.options.get('end-line', None)
        try:
            if startline or (endline is not None):
                lines = include_file.readlines()
                rawtext = ''.join(lines[startline:endline])
            else:
                rawtext = include_file.read()
        except UnicodeError, error:
            raise self.severe(u'Problem with "%s" directive:\n%s' %
                              (self.name, ErrorString(error)))

        include_lines = statemachine.string2lines(rawtext, tab_width,
                                                  convert_whitespace=True)

        # default lexer to 'text'
        lexer = self.options.get('lexer', 'text')

        self.options['source'] = path
        codeblock = Pygments(self.name,
                             [lexer], # arguments
                             {},  # no options for this directive
                             include_lines, # content
                             self.lineno,
                             self.content_offset,
                             self.block_text,
                             self.state,
                             self.state_machine)
        return codeblock.run()


def register():
    directives.register_directive('code-include', CodeInclude)

