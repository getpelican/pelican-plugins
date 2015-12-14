# -*- coding: utf-8 -*- #
"""
premailer for newsletters
=========================

This Pelican plugin process html generated files thought premailer
which turns CSS blocks into style attributes.

Intended is is to generate email newsletters with Pelican.

See:
 * Pelican : http://blog.getpelican.com/
 * premailer : https://github.com/peterbe/premailer

Author : Alexandre Norman - norman at xael.org
Licence : GNU AFFERO GENERAL PUBLIC LICENSE Version 3

"""

__author__ = 'Alexandre Norman (norman at xael.org)'
__version__ = '1.0.0'
__last_modification__ = '2015.12.13'


import os
from pelican import signals
import logging


__LOG__ = logging.getLogger(__name__)
INCLUDE_TYPES = ['html']


def register():
    """
    Register premailer
    """
    signals.finalized.connect(premailer_files)


def premailer_files(pelican):
    """
    Run premailer on generated HTML file
    :param pelican: pelican object
    """
    for dirpath, _, filenames in os.walk(pelican.settings['OUTPUT_PATH']):
        for name in filenames:
            if should_premailer(name):
                filepath = os.path.join(dirpath, name)
                go_premailer(filepath, pelican.settings['SITEURL'])


def go_premailer(filename, siteurl):
    """
    Run premailer on given file
    :param filename: the filename to validate
    """
    import premailer

    # Read and process file
    __LOG__.info(
        "Processing premailer_for_newsletters for: {0}".format(filename)
    )
    try:
        with open(filename, 'r') as rf:
            p = premailer.Premailer(
                rf.read(),
                cssutils_logging_handler=__LOG__,
                cssutils_logging_level=logging.INFO,
                base_url=siteurl,
            )
            output = p.transform()
    except:
        __LOG__.error(
            "Error in premailer_for_newsletters for: {0}".format(filename)
        )
    else:
        # Write back file
        with open(filename, 'w') as wf:
            wf.write(output)


def should_premailer(filename):
    """
    Check if the filename is a type of file that should be premailed.
    :param filename: A file name to check against
    """
    for extension in INCLUDE_TYPES:
        if filename.endswith(extension):
            return True
    return False
