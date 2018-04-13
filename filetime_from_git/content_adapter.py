# -*- coding: utf-8 -*-
"""
Wraps a content object to provide some git information
"""
import logging
from pelican.utils import memoized
from .git_wrapper import git_wrapper

DEV_LOGGER = logging.getLogger(__name__)


class GitContentAdapter(object):
    """
    Wraps a content object to provide some git information
    """
    def __init__(self, content):
        self.content = content
        self.git = git_wrapper('.')
        self.tz_name = content.settings.get('TIMEZONE', None)
        self.follow = content.settings['GIT_HISTORY_FOLLOWS_RENAME']

    @memoized
    def is_committed(self):
        '''
        Is committed
        '''
        return len(self.get_commits()) > 0

    @memoized
    def is_modified(self):
        '''
        Has content been modified since last commit
        '''
        return self.git.is_file_modified(self.content.source_path)

    @memoized
    def is_managed_by_git(self):
        '''
        Is content stored in a file managed by git
        '''
        return self.git.is_file_managed_by_git(self.content.source_path)

    @memoized
    def get_commits(self):
        '''
        Get all commits involving this filename
        :returns: List of commits newest to oldest
        '''
        if not self.is_managed_by_git():
            return []
        return self.git.get_commits(self.content.source_path, self.follow)

    @memoized
    def get_oldest_commit(self):
        '''
        Get oldest commit involving this file

        :returns: Oldest commit
        '''
        return self.git.get_commits(self.content.source_path, self.follow)[-1]

    @memoized
    def get_newest_commit(self):
        '''
        Get oldest commit involving this file

        :returns: Newest commit
        '''
        return self.git.get_commits(self.content.source_path, follow=False)[0]

    @memoized
    def get_oldest_filename(self):
        '''
        Get the original filename of this content. Implies follow
        '''
        commit_and_name_iter = self.git.get_commits_and_names_iter(
            self.content.source_path)
        _commit, name = next(commit_and_name_iter)
        return name

    @memoized
    def get_oldest_commit_date(self):
        '''
        Get datetime of oldest commit involving this file

        :returns: Datetime of oldest commit
        '''
        oldest_commit = self.get_oldest_commit()
        return self.git.get_commit_date(oldest_commit, self.tz_name)

    @memoized
    def get_newest_commit_date(self):
        '''
        Get datetime of newest commit involving this file

        :returns: Datetime of newest commit
        '''
        newest_commit = self.get_newest_commit()
        return self.git.get_commit_date(newest_commit, self.tz_name)
