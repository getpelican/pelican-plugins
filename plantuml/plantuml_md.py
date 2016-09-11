#!/usr/bin/env python
"""
   PlantUML_ Extension for Python-Markdown_
   ========================================

   Syntax:

       ::uml:: [format="png|svg"] [classes="class1 class2 ..."] [alt="text for alt"]
          PlantUML script diagram
       ::end-uml::

   Example:

       ::uml:: format="png" classes="uml myDiagram" alt="My super diagram"
          Goofy ->  MickeyMouse: calls
          Goofy <-- MickeyMouse: responds
       ::end-uml::

   Options are optional, but if present must be specified in the order format, classes, alt.
   The option value may be enclosed in single or double quotes.

.. _Python-Markdown: http://pythonhosted.org/Markdown/
.. _PlantUML: http://plantuml.sourceforge.net/
"""
import os
import re
import markdown
from markdown.util import etree
from .generateUmlDiagram import generate_uml_image

# For details see https://pythonhosted.org/Markdown/extensions/api.html#blockparser
class PlantUMLBlockProcessor(markdown.blockprocessors.BlockProcessor):
    # Regular expression inspired by the codehilite Markdown plugin
    RE = re.compile(r'''::uml::
                        \s*(format=(?P<quot>"|')(?P<format>\w+)(?P=quot))?
                        \s*(classes=(?P<quot1>"|')(?P<classes>[\w\s]+)(?P=quot1))?
                        \s*(alt=(?P<quot2>"|')(?P<alt>[\w\s"']+)(?P=quot2))?
                    ''', re.VERBOSE)
    # Regular expression for identify end of UML script
    RE_END = re.compile(r'::end-uml::\s*$')

    def test(self, parent, block):
        return self.RE.search(block)

    def run(self, parent, blocks):
        block = blocks.pop(0)
        text = block

        # Parse configuration params
        m = self.RE.search(block)
        format  = m.group('format')  if m.group('format')  else self.config['format']
        classes = m.group('classes') if m.group('classes') else self.config['classes']
        alt     = m.group('alt')     if m.group('alt')     else self.config['alt']

        # Read blocks until end marker found
        while blocks and not self.RE_END.search(block):
            block = blocks.pop(0)
            text = text + '\n' + block
        else:
            if not blocks:
                raise RuntimeError("[plantuml] UML block not closed, text is:\n"+text)

        # Remove block header and footer
        text = re.sub(self.RE, "", re.sub(self.RE_END, "", text))

        path = os.path.abspath(os.path.join('output', 'images'))
        if not os.path.exists(path):
            os.makedirs(path)

        # Generate image from PlantUML script
        imageurl = self.config['siteurl']+'/'+generate_uml_image(path, text, format)
        # Create image tag and append to the document
        etree.SubElement(parent, "img", src=imageurl, alt=alt, classes=classes)


# For details see https://pythonhosted.org/Markdown/extensions/api.html#extendmarkdown
class PlantUMLMarkdownExtension(markdown.Extension):
    # For details see https://pythonhosted.org/Markdown/extensions/api.html#configsettings
    def __init__(self, *args, **kwargs):
        self.config = {
            'classes': ["uml","Space separated list of classes for the generated image. Default uml."],
            'alt'    : ["uml diagram", "Text to show when image is not available."],
            'format' : ["png", "Format of image to generate (png or svg). Default png."],
            'siteurl': ["", "URL of document, used as a prefix for the image diagram."]
        }

        super(PlantUMLMarkdownExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        blockprocessor = PlantUMLBlockProcessor(md.parser)
        blockprocessor.config = self.getConfigs()
        md.parser.blockprocessors.add('plantuml', blockprocessor, '>code')

def makeExtension(**kwargs):
    return PlantUMLMarkdownExtension(**kwargs)
