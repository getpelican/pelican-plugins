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
global_dest_static = ""  # Absolute path to the first writable PATH in "STATIC_PATHS" ON THE DISK
global_static_path = ""  # Path of the first writable PATH in "STATIC_PATHS" ON THE WEBSITE


class PlantUML_rst(Directive):
    """ reST directive for PlantUML """
    required_arguments = 0
    optional_arguments = 0
    has_content = True

    global global_siteurl
    global global_static_path
    global global_dest_static

    option_spec = {
        'class' : directives.class_option,
        'alt'   : directives.unchanged,
        'format': directives.unchanged,
    }

    def run(self):
        path = global_dest_static
        if not os.path.exists(path):
            os.makedirs(path)

        nodes = []
        body = '\n'.join(self.content)

        try:
            uml_format = self.options.get('format', 'png')
            url = global_siteurl+global_static_path+generate_uml_image(path, body, uml_format)
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

def pelican_init(pelicanobj):

    global global_siteurl, global_static_path, global_dest_static
    global_siteurl = pelicanobj.settings['SITEURL']
    for static_path in pelicanobj.settings['STATIC_PATHS']:
        output_static_path = os.path.abspath(
            os.path.join(
                pelicanobj.settings['OUTPUT_PATH'],
                static_path
            )
        )
        if not os.path.exists(output_static_path):
            os.makedirs(output_static_path)
        if os.path.isdir(output_static_path) and os.access(output_static_path, os.W_OK):
            global_static_path = static_path
            global_dest_static = output_static_path
    if global_static_path == "":
        raise Exception("No writable static path found. Use the key `STATIC_PATHS` on your configuration.")
    logger.debug("[plantuml] Will write generated diagrams into %s", global_dest_static)

    """ Prepare configurations for the MD plugin """
    try:
        import markdown
        from .plantuml_md import PlantUMLMarkdownExtension
    except:
        # Markdown not available
        logger.debug("[plantuml] Markdown support not available")
        return

    # Register the Markdown plugin
    config = {
        'siteurl': pelicanobj.settings['SITEURL'],
        'dest_directory': global_dest_static,
        'static_path': global_static_path,
    }

    try:
        if 'MD_EXTENSIONS' in pelicanobj.settings.keys(): # pre pelican 3.7.0
            pelicanobj.settings['MD_EXTENSIONS'].append(PlantUMLMarkdownExtension(config))
        elif 'MARKDOWN' in pelicanobj.settings.keys() and \
             not ('extension_configs' in pelicanobj.settings['MARKDOWN']['extension_configs']):  # from pelican 3.7.0
            pelicanobj.settings['MARKDOWN']['extension_configs']['plantuml.plantuml_md'] = config
    except:
        logger.error("[plantuml] Unable to configure plantuml markdown extension")


def register():
    """Plugin registration."""
    signals.initialized.connect(pelican_init)
    directives.register_directive('uml', PlantUML_rst)
