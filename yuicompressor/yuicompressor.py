# -*- coding: utf-8 -*-

from pelican import signals
from subprocess import call
import logging
import os

logger = logging.getLogger(__name__)

# Display command output on DEBUG and TRACE
SHOW_OUTPUT = logger.getEffectiveLevel() <= logging.DEBUG

"""
Minify CSS and JS files in output path
with Yuicompressor from Yahoo
Required : pip install yuicompressor
"""

def minify(pelican):
    """
      Minify CSS and JS with YUI Compressor
      :param pelican: The Pelican instance
    """
    for dirpath, _, filenames in os.walk(pelican.settings['OUTPUT_PATH']):
        for name in filenames:
            if os.path.splitext(name)[1] in ('.css','.js'):
                filepath = os.path.join(dirpath, name)
                logger.info('minifiy %s', filepath)
                verbose = '-v' if SHOW_OUTPUT else ''
                call("yuicompressor {} --charset utf-8 {} -o {}".format(
                    verbose, filepath, filepath), shell=True)

def register():
    signals.finalized.connect(minify)
