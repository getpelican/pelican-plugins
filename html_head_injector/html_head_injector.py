# -*- coding: utf-8 -*-
"""
HTML additional head statements injector
========================================

This plugin allows you to place custom HTML per article at the end of <head>.
"""

from __future__ import unicode_literals
from pelican import signals
from docutils import nodes
from docutils.parsers.rst import directives, Directive
import threading
from threading import current_thread

threadLocal = threading.local()

class InjectedHtmlHead(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        src = '\n'.join(self.content)
        threadLocal.injected_head_data.append( src )
        # No visible output at current position
        return []

def initHeadData(gen):
    threadLocal.injected_head_data = []

def addHeadData(gen, metadata):
    head_data = '\n'.join(threadLocal.injected_head_data)
    metadata['inject_head'] = head_data

def register():
    
    # Clear additional head data before every source file
    signals.article_generate_preread.connect(initHeadData)
    
    # Add head data after page generation to Jinja environment
    signals.article_generate_context.connect(addHeadData)
    signals.pages_generate_context.connect(addHeadData)
    
    # Handle '.. injecthead::' in RST source
    directives.register_directive('injecthead', InjectedHtmlHead)