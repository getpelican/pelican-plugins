# -*- coding: utf-8 -*-

"""
Optimized images (jpg and png)
Assumes that jpegtran and optipng are isntalled on path.
http://jpegclub.org/jpegtran/
http://optipng.sourceforge.net/
Copyright (c) 2012 Irfan Ahmad (http://i.com.pk)
"""

import logging
from os import path
import os
from shutil import copyfile
import hashlib
import mmap
from subprocess import call

from pelican import signals

logger = logging.getLogger(__name__)

CACHE = 'optimize_images_cache'

# Display command output on DEBUG and TRACE
SHOW_OUTPUT = logger.getEffectiveLevel() <= logging.DEBUG

# A list of file types with their respective commands
COMMANDS = {
    # '.ext': ('command {flags} {filename', 'silent_flag', 'verbose_flag')
    '.svg': ('svgo {flags} --input="{filename}" --output="{filename}"', '--quiet', ''),
    '.jpg': ('jpegtran {flags} -copy none -optimize -progressive -outfile "{filename}" "{filename}"', '', '-v'),
    '.png': ('optipng {flags} "{filename}"', '--quiet', ''),
}


def optimize_images(pelican):
    """
    Optimized jpg and png images

    :param pelican: The Pelican instance
    """
    for dirpath, _, filenames in os.walk(pelican.settings['OUTPUT_PATH']):
        for name in filenames:
            if os.path.splitext(name)[1] in COMMANDS.keys():
                optimize(dirpath, name)

                
def is_cached(checksum):
    if not os.path.exists(CACHE):
        os.makedirs(CACHE)
        return False
    if os.path.isfile(os.path.join(CACHE, checksum)):
            return True
    return False
    

def optimize(dirpath, filename):
    """
    Check if the name is a type of file that should be optimized.
    And optimizes it if required.

    :param dirpath: Path of the file to be optimzed
    :param name: A file name to be optimized
    """
        
    filepath = os.path.join(dirpath, filename)
    checksum = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()

    if is_cached(checksum):
        # copy optimized image from cache
        copyfile(os.path.join(CACHE, checksum), filepath)
        logger.info('read %s from cache', filepath)
    else:
        logger.info('optimizing %s', filepath)
    ext = os.path.splitext(filename)[1]
    command, silent, verbose = COMMANDS[ext]
    flags = verbose if SHOW_OUTPUT else silent
    command = command.format(filename=filepath, flags=flags)
    call(command, shell=True)
    # copy optimized image to cache
    copyfile(filepath, os.path.join(CACHE, checksum))


def register():
    signals.finalized.connect(optimize_images)
