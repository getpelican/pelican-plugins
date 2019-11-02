# -*- coding: utf-8 -*-
"""
Pelican Inline Markdown Extension
==================================
An extension for the Python Markdown module that enables
the Pelican Python static site generator to add inline patterns.
"""

import markdown
import re

from markdown.util import etree
from markdown.util import AtomicString

class PelicanInlineMarkdownExtensionPattern(markdown.inlinepatterns.Pattern):
    """Inline Markdown processing"""

    def __init__(self, pelican_markdown_extension, tag, pattern):
        super(PelicanInlineMarkdownExtensionPattern,self).__init__(pattern)
        self.tag = tag
        self.config = pelican_markdown_extension.getConfig('config')

    def handleMatch(self, m):
        node = markdown.util.etree.Element(self.tag)
        tag_attributes = self.config.get(m.group('prefix'), ('', 'pelican-inline'))
        tag_class = 'pelican-inline'  # default class
        tag_style = ''  # default is for no styling

        if isinstance(tag_attributes, tuple):
            tag_style = tag_attributes[0]
            tag_class = tag_attributes[1] if len(tag_attributes) > 1 else ''
        elif isinstance(tag_attributes, str):
            tag_class = tag_attributes

        if tag_class != '':
            node.set('class', tag_class)
        if tag_style!= '':
            node.set('style', tag_style)

        node.text = markdown.util.AtomicString(m.group('text'))

        return node

class PelicanInlineMarkdownExtension(markdown.Extension):
    """A Markdown extension enabling processing in Markdown for Pelican"""
    def __init__(self, config):

        try:
            # Needed for Markdown versions >= 2.5
            self.config['config'] = ['{}', 'config for markdown extension']
            super(PelicanInlineMarkdownExtension,self).__init__(**config)
        except AttributeError:
            # Markdown versions < 2.5
            config['config'] = [config['config'], 'config for markdown extension']
            super(PelicanInlineMarkdownExtension, self).__init__(config)

    def extendMarkdown(self, md, md_globals):
        # Regex to detect mathjax
        config = self.getConfig('config')
        patterns = []

        # The following mathjax settings can be set via the settings dictionary
        for key in config:
            patterns.append(re.escape(key))

        inline_regex = r'(?P<prefix>%s)(?P<text>.+?)\2' % ('|'.join(patterns))

        # Process after escapes
        md.inlinePatterns.add('texthighlight_inlined', PelicanInlineMarkdownExtensionPattern(self, 'span', inline_regex), '>emphasis2')
