# -*- coding: utf-8 -*-

from pelican import signals
from subprocess import check_call
import logging
import os

logger = logging.getLogger(__name__)

"""
Minify CSS and JS files in output path with YUI Compressor from Yahoo.
Required: an existing installation of YUI Compressor.
"""

def minify(pelican):
    """
      Minify CSS and JS with YUI Compressor
      :param pelican: The Pelican instance
    """
    executable = pelican.settings.get('YUICOMPRESSOR_EXECUTABLE', 'yuicompressor')
    for dirpath, _, filenames in os.walk(pelican.settings['OUTPUT_PATH']):
        for name in filenames:
            if os.path.splitext(name)[1] in ('.css','.js'):
                filepath = os.path.join(dirpath, name)
                logger.info('minify %s', filepath)
                check_call([executable, '--charset', 'utf-8', filepath, '-o', filepath])

def register():
    signals.finalized.connect(minify)
