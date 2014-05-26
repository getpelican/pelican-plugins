#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from git import Git, Repo, InvalidGitRepositoryError
from pelican import signals, contents
from datetime import datetime
from time import mktime, altzone

try:
    repo = Repo(os.path.abspath('.'))
    git = Git(os.path.abspath('.'))
except InvalidGitRepositoryError as e:
    repo = None

def filetime_from_git(content):
    if isinstance(content, contents.Static) or repo is None:
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
    metadata = content.metadata
    status, stdout, stderr = git.execute(['git', 'ls-files', path, '--error-unmatch'],
            with_extended_output=True, with_exceptions=False)
    if status != 0:
        # file is not managed by git
        metadata['date'] = datetime.fromtimestamp(os.stat(path).st_ctime)
    else:
        # file is managed by git
        commits = repo.commits(path=path)
        if len(commits) == 0:
            # never commited, but staged
            metadata['date'] = datetime.fromtimestamp(os.stat(path).st_ctime)
        else:
            # has commited
            metadata['date'] = datetime.fromtimestamp(mktime(commits[-1].committed_date) - altzone)

            status, stdout, stderr = git.execute(['git', 'diff', '--quiet', 'HEAD', path],
                    with_extended_output=True, with_exceptions=False)
            if status != 0:
                # file has changed
                metadata['updated'] = datetime.fromtimestamp(os.stat(path).st_ctime)
            else:
                # file is not changed
                if len(commits) > 1:
                    metadata['updated'] = datetime.fromtimestamp(mktime(commits[0].committed_date) - altzone)
    if not metadata.has_key('updated'):
        metadata['updated'] = metadata['date']

def register():
    signals.content_object_init.connect(filetime_from_git)
