# -*- coding: utf-8 -*-
"""
This plugin is mostly a copy of the filetime_from_git plugin
by Zhang Cheng <StephenPCG@gmail.com> and others.

Copyright (c) David Douard <david.douard@sdfa3.org>

Compute Date and Modified metadata from Mercurial revisions.
"""

import os
from pelican import signals, contents
from pelican.utils import strftime, set_date_tzinfo
from datetime import datetime

import hglib

def datetime_from_timestamp(timestamp, content):
    """
    Helper function to add timezone information to datetime,
    so that datetime is comparable to other datetime objects in recent versions
    that now also have timezone information.
    """
    return set_date_tzinfo(
        datetime.fromtimestamp(timestamp),
        tz_name=content.settings.get('TIMEZONE', None))


def filetime_from_hg(content):
    if isinstance(content, contents.Static):
        return
    if 'date' in content.metadata:
        # if user did explicitely set a date, do not overwrite it
        return
    repo = hglib.open('.')
    tz_name = content.settings.get('TIMEZONE', None)

    hgtime = content.metadata.get('hgtime', 'yes').lower()
    if hgtime in ('no', 'off', 'false', '0'):
        return

    # 1. file is not managed by hg
    #    date: fs time
    # 2. file is staged, but has no commits
    #    date: fs time
    # 3. file is managed, and clean
    #    date: first commit time, update: last commit time or None
    # 4. file is managed, but dirty
    #    date: first commit time, update: fs time
    path = content.source_path
    root = repo.root()
    filelog = repo.log(revrange='.:0', files=[path,],
                       follow=content.settings.get('HG_FILETIME_FOLLOW', False))
    if filelog:
        # has commited
        content.date = set_date_tzinfo(filelog[-1][6], tz_name)
        if path in [os.path.join(root, mfile) for flag, mfile in repo.status(modified=True)]:
            # file is modified in the wd
            content.modified = datetime_from_timestamp(
                os.stat(path).st_ctime, content)
        else:
            # file is not changed
            if len(filelog) > 1:
                content.modified = set_date_tzinfo(filelog[0][6], tz_name)
    else:
        # file is not managed by hg
        content.date = datetime_from_timestamp(os.stat(path).st_ctime, content)

    if not hasattr(content, 'modified'):
        content.modified = content.date

    content.locale_date = strftime(content.date, content.date_format)
    content.locale_modified = strftime(content.modified, content.date_format)
    # ensure the metadata directory is synchronized. Might be used by
    # some other plugin (eg. series)
    content.metadata['modified'] = content.modified
    content.metadata['date'] = content.date


def register():
    signals.content_object_init.connect(filetime_from_hg)
