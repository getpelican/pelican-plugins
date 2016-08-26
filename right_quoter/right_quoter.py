# -*- coding: utf-8 -*-

""" Right Quoter: Fix direction of assorted curly apostrophes

When used with typogrify/smartypants, this plugin attempts to fix the
direction of the curly single quote for contractions with leading
apostrophes, e.g. two-digit decade or year references like '90s or '78.
"""

from __future__ import unicode_literals

import re

from pelican import contents
from pelican import signals


__author__ = 'Scott Carpenter'
__email__ = 'scottc@movingtofreedom.org'


regex_pattern = re.compile(
    r'''(?xi)                # verbose mode, ignore case
        &\#8216;             # left apos from typogrify/smartypants
        (?=                  # positive lookahead
          (</span>)?         # possible quote wrapper
          (<span[^>]*>)?     # possible CAPS wrapper
          (                  # exceptions
            \d\d |           # two-digit years
            \d0s |           # decades
            em |             #
            tis |            #
            twas             #
          )                  #
          \b                 # word boundary
        )                    # end of lookahead
    '''
)


def rightify(text):
    return re.sub(regex_pattern, '&#8217;', text)


def right_quoter(content):
    if isinstance(content, contents.Static):
        return

    content._content = rightify(content._content)
    content.title = rightify(content.title)
    if hasattr(content, '_summary'):  # summary metadata is set
        content._summary = rightify(content._summary)


def register():
    signals.content_object_init.connect(right_quoter)
