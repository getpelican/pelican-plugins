# -*- coding: utf-8 -*-
"""
Handle registration and setup for plugin
"""
import logging
from blinker import signal
from .content_adapter import GitContentAdapter
from pelican import signals

DEV_LOGGER = logging.getLogger(__name__)

content_git_object_init = signal('content_git_object_init')

def send_content_git_object_init(content):
    content_git_object_init.send(content, git_content=GitContentAdapter(content))


def setup_option_defaults(pelican_inst):
    pelican_inst.settings.setdefault('GIT_FILETIME_FROM_GIT', True)
    pelican_inst.settings.setdefault('GIT_HISTORY_FOLLOWS_RENAME', True)
    pelican_inst.settings.setdefault('GIT_SHA_METADATA', True)
    pelican_inst.settings.setdefault('GIT_GENERATE_PERMALINK', False)


def register():
    signals.content_object_init.connect(send_content_git_object_init)
    signals.initialized.connect(setup_option_defaults)

    # Import actions
    from . import actions
