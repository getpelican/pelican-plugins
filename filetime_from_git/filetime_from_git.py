# -*- coding: utf-8 -*-

import os
from pelican import signals, contents
from pelican.utils import strftime, set_date_tzinfo
from datetime import datetime
from .git_wrapper import git_wrapper


def datetime_from_timestamp(timestamp, content):
    """
    Helper function to add timezone information to datetime,
    so that datetime is comparable to other datetime objects in recent versions
    that now also have timezone information.
    """
    return set_date_tzinfo(
        datetime.fromtimestamp(timestamp),
        tz_name=content.settings.get('TIMEZONE', None))


def filetime_from_git(content):
    if isinstance(content, contents.Static):
        return

    git = git_wrapper('.')
    tz_name = content.settings.get('TIMEZONE', None)

    gittime = content.metadata.get('gittime', 'yes').lower()
    gittime = gittime.replace("false", "no").replace("off", "no")
    if gittime == "no":
        return

    # 1. file is not managed by git
    #    date: fs time
    # 2. file is staged, but has no commits
    #    date: fs time
    # 3. file is managed, and clean
    #    date: first commit time, update: last commit time or None
    # 4. file is managed, but dirty
    #    date: first commit time, update: fs time
    path = content.source_path
    if git.is_file_managed_by_git(path):
        commits = git.get_commits(
            path, follow=content.settings.get('GIT_FILETIME_FOLLOW', False))

        if len(commits) == 0:
            # never commited, but staged
            content.date = datetime_from_timestamp(
                os.stat(path).st_ctime, content)
        else:
            # has commited
            content.date = git.get_commit_date(
                commits[-1], tz_name)

            if git.is_file_modified(path):
                # file has changed
                content.modified = datetime_from_timestamp(
                    os.stat(path).st_ctime, content)
            else:
                # file is not changed
                if len(commits) > 1:
                    content.modified = git.get_commit_date(
                        commits[0], tz_name)
    else:
        # file is not managed by git
        content.date = datetime_from_timestamp(os.stat(path).st_ctime, content)

    if not hasattr(content, 'modified'):
        content.modified = content.date

    if hasattr(content, 'date'):
        content.locale_date = strftime(content.date, content.date_format)

    if hasattr(content, 'modified'):
        content.locale_modified = strftime(
            content.modified, content.date_format)


def register():
    signals.content_object_init.connect(filetime_from_git)
