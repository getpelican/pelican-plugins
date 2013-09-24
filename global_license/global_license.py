"""
License plugin for Pelican
==========================

This plugin allows you to define a LICENSE setting and adds the contents of that
license variable to the article's context, making that variable available to use
from within your theme's templates.
"""

from pelican import signals

def add_license(generator, metadata):
    if 'license' not in metadata.keys()\
        and 'LICENSE' in generator.settings.keys():
            metadata['license'] = generator.settings['LICENSE']

def register():
    signals.article_generator_context.connect(add_license)
