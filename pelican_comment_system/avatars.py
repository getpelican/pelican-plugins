# -*- coding: utf-8 -*-
"""
Author: Bernhard Scheirle
"""

from __future__ import unicode_literals

import logging
import os

import hashlib


logger = logging.getLogger(__name__)
_log = "pelican_comment_system: avatars: "
try:
    from . identicon import identicon
    _identiconImported = True
except ImportError as e:
    logger.warning(_log + "identicon deactivated: " + str(e))
    _identiconImported = False

# Global Variables
_identicon_save_path = None
_identicon_output_path = None
_identicon_data = None
_identicon_size = None
_initialized = False
_authors = None
_missingAvatars = []


def _ready():
    if not _initialized:
        logger.warning(_log + "Module not initialized. use init")
    if not _identicon_data:
        logger.debug(_log + "No identicon data set")
    return _identiconImported and _initialized and _identicon_data


def init(pelican_output_path, identicon_output_path, identicon_data,
         identicon_size, authors):
    global _identicon_save_path
    global _identicon_output_path
    global _identicon_data
    global _identicon_size
    global _initialized
    global _authors
    if _initialized:
        return
    _identicon_save_path = os.path.join(pelican_output_path,
                                        identicon_output_path)
    _identicon_output_path = identicon_output_path
    _identicon_data = identicon_data
    _identicon_size = identicon_size
    _authors = authors
    _initialized = True


def _createIdenticonOutputFolder():
    if not _ready():
        return

    if not os.path.exists(_identicon_save_path):
        os.makedirs(_identicon_save_path)


def getAvatarPath(comment_id, metadata):
    if not _ready():
        return ''

    md5 = hashlib.md5()
    author = tuple()
    for data in _identicon_data:
        if data in metadata:
            string = "{}".format(metadata[data])
            md5.update(string.encode('utf-8'))
            author += tuple([string])
        else:
            logger.warning(_log + data +
                           " is missing in comment: " + comment_id)

    if author in _authors:
        return _authors[author]

    global _missingAvatars

    code = md5.hexdigest()

    if not code in _missingAvatars:
        _missingAvatars.append(code)

    return os.path.join(_identicon_output_path, '%s.png' % code)


def generateAndSaveMissingAvatars():
    _createIdenticonOutputFolder()
    for code in _missingAvatars:
        avatar_path = '%s.png' % code
        avatar = identicon.render_identicon(int(code, 16), _identicon_size)
        avatar_save_path = os.path.join(_identicon_save_path, avatar_path)
        avatar.save(avatar_save_path, 'PNG')
