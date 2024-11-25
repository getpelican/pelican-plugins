#!/usr/bin/env python

from pelican import signals
from pelican.utils import strftime

from datetime import datetime
import os
import subprocess


def git_mtime(filename, use_last_modification=True, git_binary="git"):
    """Determines the git modification time of a file and returns it as a
    datetime.datetime object.

    If use_last_modification is True, then the date and time of the last
    modification will be returned. Otherwise the date and time of the first
    commit containing the file will be returned.

    The optional argument 'git_binary' can be used to specify the git binary to
    use.
    """

    call = [git_binary, "log", r"--pretty=format:%at ", filename]
    repository= os.path.dirname(filename)
    try:
        output = subprocess.check_output(call, cwd=repository).decode('utf-8').splitlines()
    except Exception as e:
        print("ERROR: Could not get git time information for {0}: {1}".format(filename, str(e)))
        return None

    dates = [ datetime.fromtimestamp(int(x)) for x in output ]
    sorted_dates = sorted(dates)

    if len(sorted_dates) > 0:
        return sorted_dates[-1] if use_last_modification else sorted_dates[0]
    return None


def generate_date(content):
    mode = content.settings.get('GIT_TIME_LAST_MODIFIED', False)
    date = git_mtime(content.source_path, mode)

    if not date:
        # This happens usually when the file is not checked into git yet. It
        # is probably a new file and 'now' should be the correct time
        date = datetime.now()

    content.metadata['date'] = date
    content.date = date
    content.locale_date = strftime(content.date, content.date_format)

def register():
    signals.content_object_init.connect(generate_date)
