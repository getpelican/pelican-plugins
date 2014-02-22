# -*- coding: utf-8 -*-
"""
Include Markdown
================

This plugin allows you to include a Markdown file (which will be converted to HTML).

TODO: Add tests for this plugin.

"""

from jinja2 import nodes
from jinja2.ext import Extension

from pelican import readers, signals
from pelican.settings import DEFAULT_CONFIG

import os.path

def _path(*args):
    return os.path.join(DEFAULT_CONFIG['PATH'], *args)

class IncludeMarkdownExtension(Extension):
    tags = set(['include_markdown'])
    
    def __init__(self, environment):
        super(IncludeMarkdownExtension, self).__init__(environment)
        
    def parse(self, parser):
        stream = parser.stream
        tag = next(stream)
        lineno = tag.lineno

        path_comps = []
        while stream.current.type != 'block_end':
            token = next(stream)
            path_comps.append(token.value)
        path = ''.join(path_comps)
        return nodes.Output([self.call_method('render_markdown', [nodes.Const(path),]),]).set_lineno(lineno)        

    def render_markdown(self, path):
        reader = readers.MarkdownReader(settings=DEFAULT_CONFIG)
        content, metadata = reader.read(_path(path))        
        return content

def registerExtension(gen):
    gen.settings['JINJA_EXTENSIONS'].append(IncludeMarkdownExtension)

def register():
    try:    
        signals.initialized.connect(registerExtension)
    except ImportError:
        logger.warning('`include_markdown` plugin not loaded.')
