# -*- coding: utf-8 -*-
"""
Wrap python git interface for compatibility with older/newer version
"""
try:
    from itertools import zip_longest
except ImportError:
    from six.moves import zip_longest
import logging
import os
from time import mktime
from datetime import datetime
from pelican.utils import set_date_tzinfo
from git import Git, Repo

DEV_LOGGER = logging.getLogger(__name__)


def grouper(iterable, n, fillvalue=None):
    '''
    Collect data into fixed-length chunks or blocks
    '''
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


class _GitWrapperCommon(object):
    '''
    Wrap git module to provide a more stable interface across versions
    '''
    def __init__(self, repo_path):
        self.git = Git()
        self.git.update_environment(
            GIT_CONFIG_NOSYSTEM='true',
            HOME=os.getcwd(),
            XDG_CONFIG_HOME=os.getcwd()
        )
        self.repo = Repo(os.path.abspath("."), search_parent_directories=True)

    def is_file_managed_by_git(self, path):
        '''
        :param path: Path to check
        :returns: True if path is managed by git
        '''
        status, _stdout, _stderr = self.git.execute(
            ['git', 'ls-files', path, '--error-unmatch'],
            with_extended_output=True,
            with_exceptions=False)
        return status == 0

    def is_file_modified(self, path):
        '''
        Does a file have local changes not yet committed

        :returns: True if file has local changes
        '''
        status, _stdout, _stderr = self.git.execute(
            ['git', 'diff', '--quiet', 'HEAD', path],
            with_extended_output=True,
            with_exceptions=False)
        return status != 0

    def get_commits_following(self, path):
        '''
        Get all commits including path following the file through
        renames

        :param path: Path which we will find commits for
        :returns: Sequence of commit objects. Newest to oldest
        '''
        return [
            commit for commit, _ in self.get_commits_and_names_iter(
                path)]

    def get_commits_and_names_iter(self, path):
        '''
        Get all commits including a given path following renames
        '''
        log_result = self.git.log(
            '--pretty=%H',
            '--follow',
            '--name-only',
            '--',
            path).splitlines()

        for commit_sha, _, filename in grouper(log_result, 3):
            yield self.repo.commit(commit_sha), filename

    def get_commits(self, path, follow=False):
        '''
        Get all commits including path

        :param path: Path which we will find commits for
        :param bool follow: If True we will follow path through renames

        :returns: Sequence of commit objects. Newest to oldest
        '''
        if follow:
            return self.get_commits_following(path)
        else:
            return self._get_commits(path)


class _GitWrapperLegacy(_GitWrapperCommon):
    def _get_commits(self, path):
        '''
        Get all commits including path without following renames

        :param path: Path which we will find commits for

        :returns: Sequence of commit objects. Newest to oldest
        '''
        return self.repo.commits(path=path)

    @staticmethod
    def get_commit_date(commit, tz_name):
        '''
        Get datetime of commit comitted_date
        '''
        return set_date_tzinfo(
            datetime.fromtimestamp(mktime(commit.committed_date)),
            tz_name=tz_name)


class _GitWrapper(_GitWrapperCommon):
    def _get_commits(self, path):
        '''
        Get all commits including path without following renames

        :param path: Path which we will find commits for

        :returns: Sequence of commit objects. Newest to oldest

        .. NOTE ::
            If this fails it could be that your gitpython version is out of
            sync with the git binary on your distro.
            Make sure you use the correct gitpython version.

            Alternatively enabling GIT_FILETIME_FOLLOW may also make your
            problem go away.
        '''
        return list(self.repo.iter_commits(paths=path))

    @staticmethod
    def get_commit_date(commit, tz_name):
        '''
        Get datetime of commit comitted_date
        '''
        return set_date_tzinfo(
            datetime.fromtimestamp(commit.committed_date),
            tz_name=tz_name)


_wrapper_cache = {}


def git_wrapper(path):
    '''
    Get appropriate wrapper factory and cache instance for path
    '''
    path = os.path.abspath(path)
    if path not in _wrapper_cache:
        if hasattr(Repo, 'commits'):
            _wrapper_cache[path] = _GitWrapperLegacy(path)
        else:
            _wrapper_cache[path] = _GitWrapper(path)

    return _wrapper_cache[path]
