# -*- coding: utf-8 -*-

"""
Optimized html and xml files
Assumes that minify is isntalled on path.
Copyright (c) 2019 Pouya Abbassi (https://pouyacode.net)
"""

import logging
import os
from subprocess import call

from pelican import signals

logger = logging.getLogger(__name__)

# A list of file types with their respective commands
COMMANDS = {
    # '.ext': ('command {flags} {filename', 'silent_flag', 'verbose_flag')
    '.html': ('minify "{filename}" -o "{filename}"', '--quiet', ''),
    '.xml': ('minify "{filename}" -o "{filename}"', '', ''),
}

# Display command output on DEBUG and TRACE
SHOW_OUTPUT = logger.getEffectiveLevel() <= logging.DEBUG

def create(pelican):
    for dirpath, _, filenames in os.walk(pelican.settings['OUTPUT_PATH']):
        for name in filenames:
            if os.path.splitext(name)[1] in COMMANDS.keys():
                optimize(dirpath, name)

def optimize(dirpath, filename):
    """
    Check if the name is a type of file that should be optimized.
    And optimizes it if required.

    :param dirpath: Path of the file to be optimzed
    :param name: A file name to be optimized
    """
    filepath = os.path.join(dirpath, filename)
    logger.info('optimizing %s', filepath)

    ext = os.path.splitext(filename)[1]
    command, silent, verbose = COMMANDS[ext]
    flags = verbose if SHOW_OUTPUT else silent
    command = command.format(filename=filepath, flags=flags)
    call(command, shell=True)

def register():
    signals.finalized.connect(create)
