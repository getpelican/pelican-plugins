# -*- coding: utf-8 -*-
"""
HTML tags for reStructuredText
==============================

This plugin allows you to use HTML tags from within reST documents. 

"""

from __future__ import unicode_literals
from docutils import nodes
from docutils.parsers.rst import directives, Directive


class RawHtml(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        html = ' '.join(self.content)
        node = nodes.raw('', html, format='html')
        return [node]



def register():
    directives.register_directive('html', RawHtml)

