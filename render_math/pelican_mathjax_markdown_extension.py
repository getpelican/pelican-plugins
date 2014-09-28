# -*- coding: utf-8 -*-
"""
Pelican Mathjax Markdown Extension
==================================
An extension for the Python Markdown module that enables
the Pelican python blog to process mathjax. This extension
gives Pelican the ability to use Mathjax as a "first class
citizen" of the blog
"""

import markdown

from markdown.util import etree
from markdown.util import AtomicString

class PelicanMathJaxPattern(markdown.inlinepatterns.Pattern):
    """Pattern for matching mathjax"""

    def __init__(self, pelican_mathjax_extension, tag, pattern):
        super(PelicanMathJaxPattern,self).__init__(pattern)
        self.math_tag_class = pelican_mathjax_extension.getConfig('math_tag_class')
        self.pelican_mathjax_extension = pelican_mathjax_extension
        self.tag = tag

    def handleMatch(self, m):
        node = markdown.util.etree.Element(self.tag)
        node.set('class', self.math_tag_class)

        prefix = '\\(' if m.group('prefix') == '$' else m.group('prefix')
        suffix = '\\)' if m.group('suffix') == '$' else m.group('suffix')
        node.text = markdown.util.AtomicString(prefix + m.group('math') + suffix)

        # If mathjax was successfully matched, then JavaScript needs to be added
        # for rendering. The boolean below indicates this
        self.pelican_mathjax_extension.mathjax_needed = True
        return node

class PelicanMathJaxTreeProcessor(markdown.treeprocessors.Treeprocessor):
    """Tree Processor for adding Mathjax JavaScript to the blog"""

    def __init__(self, pelican_mathjax_extension):
        self.pelican_mathjax_extension = pelican_mathjax_extension

    def run(self, root):
        # If no mathjax was present, then exit
        if (not self.pelican_mathjax_extension.mathjax_needed):
            return root

        # Add the mathjax script to the html document
        mathjax_script = etree.Element('script')
        mathjax_script.set('type','text/javascript')
        mathjax_script.text = AtomicString(self.pelican_mathjax_extension.getConfig('mathjax_script'))
        root.append(mathjax_script)

        # Reset the boolean switch to false so that script is only added
        # to other pages if needed
        self.pelican_mathjax_extension.mathjax_needed = False
        return root

class PelicanMathJaxExtension(markdown.Extension):
    """A markdown extension enabling mathjax processing in Markdown for Pelican"""
    def __init__(self, config):

        try:
            # Needed for markdown versions >= 2.5
            self.config['mathjax_script'] = ['', 'Mathjax JavaScript script']
            self.config['math_tag_class'] = ['math', 'The class of the tag in which mathematics is wrapped']
            super(PelicanMathJaxExtension,self).__init__(**config)
        except AttributeError:
            # Markdown versions < 2.5
            config['mathjax_script'] = [config['mathjax_script'], 'Mathjax JavaScript script']
            config['math_tag_class'] = [config['math_tag_class'], 'The class of the tag in which mathematic is wrapped']
            super(PelicanMathJaxExtension,self).__init__(config)

        # Used as a flag to determine if javascript
        # needs to be injected into a document
        self.mathjax_needed = False

    def extendMarkdown(self, md, md_globals):
        # Regex to detect mathjax
        mathjax_inline_regex = r'(?P<prefix>\$)(?P<math>.+?)(?P<suffix>(?<!\s)\2)'
        mathjax_display_regex = r'(?P<prefix>\$\$|\\begin\{(.+?)\})(?P<math>.+?)(?P<suffix>\2|\\end\{\3\})'

        # Process mathjax before escapes are processed since escape processing will
        # intefer with mathjax. The order in which the displayed and inlined math
        # is registered below matters
        md.inlinePatterns.add('mathjax_displayed', PelicanMathJaxPattern(self, 'div', mathjax_display_regex), '<escape')
        md.inlinePatterns.add('mathjax_inlined', PelicanMathJaxPattern(self, 'span', mathjax_inline_regex), '<escape')

        # If necessary, add the JavaScript Mathjax library to the document. This must
        # be last in the ordered dict (hence it is given the position '_end')
        md.treeprocessors.add('mathjax', PelicanMathJaxTreeProcessor(self), '_end')
