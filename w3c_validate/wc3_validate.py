# -*- coding: utf-8 -*-
"""
W3C HTML Validator plugin for genrated content.
"""


from pelican import signals
import logging
import os

LOG = logging.getLogger(__name__)

INCLUDE_TYPES = ['html']


def validate_files(pelican):
    """
    Validate a generated HTML file
    :param pelican: pelican object
    """
    for dirpath, _, filenames in os.walk(pelican.settings['OUTPUT_PATH']):
        for name in filenames:
            if should_validate(name):
                filepath = os.path.join(dirpath, name)
                validate(filepath)


def validate(filename):
    """
    Use W3C validator service: https://bitbucket.org/nmb10/py_w3c/ .
    :param filename: the filename to validate
    """
    try:
        from html.parser import HTMLParser
    except ImportError:  # fallback for Python 2:
        from HTMLParser import HTMLParser
    from py_w3c.validators.html.validator import HTMLValidator

    h = HTMLParser()  # for unescaping WC3 messages

    vld = HTMLValidator()
    LOG.info("Validating: {0}".format(filename))

    # call w3c webservice
    vld.validate_file(filename)

    # display errors and warning
    for err in vld.errors:
        line = err.get('line') or err['lastLine']
        col = err.get('col') or '{}-{}'.format(err['firstColumn'], err['lastColumn'])
        LOG.error(u'line: {0}; col: {1}; message: {2}'.
                  format(line, col, h.unescape(err['message']))
                  )
    for err in vld.warnings:
        line = err.get('line') or err['lastLine']
        col = err.get('col') or '{}-{}'.format(err['firstColumn'], err['lastColumn'])
        LOG.warning(u'line: {0}; col: {1}; message: {2}'.
                    format(line, col, h.unescape(err['message']))
                    )


def should_validate(filename):
    """Check if the filename is a type of file that should be validated.
    :param filename: A file name to check against
    """
    for extension in INCLUDE_TYPES:
        if filename.endswith(extension):
            return True
    return False


def register():
    """
    Register Pelican signal for validating content after it is generated.
    """
    signals.finalized.connect(validate_files)
