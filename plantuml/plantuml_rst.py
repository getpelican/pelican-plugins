#!/usr/bin/env python
"""Custom reST_ directive for plantuml_ integration.
   Adapted from ditaa_rst plugin.

.. _reST: http://docutils.sourceforge.net/rst.html
.. _plantuml: http://plantuml.sourceforge.net/
"""

import sys
import os

from docutils.nodes import image, literal_block
from docutils.parsers.rst import Directive, directives
from pelican import signals, logger

from .generateUmlDiagram import generate_uml_image


global_siteurl = "" # URL of the site, filled on plugin initialization


class PlantUML_rst(Directive):
    """ reST directive for PlantUML """
    required_arguments = 0
    optional_arguments = 0
    has_content = True

    global global_siteurl

    option_spec = {
        'class' : directives.class_option,
        'alt'   : directives.unchanged,
        'format': directives.unchanged,
    }

    def run(self):
        path = os.path.abspath(os.path.join('output', 'images'))
        if not os.path.exists(path):
            os.makedirs(path)

        nodes = []
        body = '\n'.join(self.content)

        try:
            url = global_siteurl+'/'+generate_uml_image(path, body, "png")
        except Exception as exc:
            error = self.state_machine.reporter.error(
                'Failed to run plantuml: %s' % exc,
                literal_block(self.block_text, self.block_text),
                line=self.lineno)
            nodes.append(error)
        else:
            alt = self.options.get('alt', 'uml diagram')
            classes = self.options.pop('class', ['uml'])
            imgnode = image(uri=url, classes=classes, alt=alt)
            nodes.append(imgnode)

        return nodes


def custom_url(generator, metadata):
    """ Saves globally the value of SITEURL configuration parameter """
    global global_siteurl
    global_siteurl = generator.settings['SITEURL']


def pelican_init(pelicanobj):
    """ Prepare configurations for the MD plugin """
    try:
        import markdown
        from plantuml_md import PlantUMLMarkdownExtension
    except:
        # Markdown not available
        logger.debug("[plantuml] Markdown support not available")
        return

    # Register the Markdown plugin
    config = { 'siteurl': pelicanobj.settings['SITEURL'] }

    try:
        pelicanobj.settings['MD_EXTENSIONS'].append(PlantUMLMarkdownExtension(config))
    except:
        logger.error("[plantuml] Unable to configure plantuml markdown extension")


def register():
    """Plugin registration."""
    signals.initialized.connect(pelican_init)
    signals.article_generator_context.connect(custom_url)
    directives.register_directive('uml', PlantUML_rst)
