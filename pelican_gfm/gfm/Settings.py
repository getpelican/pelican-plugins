#!/usr/bin/python -B

# Location of the libcmark files
LIBCMARKLOCATION = "/usr/lib/x86_64-linux-gnu"

# GitHub Cmark version we're using
VERSION = "0.28.3.gfm.12"

# The CMARK extensions that we want to use
EXTENSIONS = (
    'autolink',
    'table',
    'strikethrough',
    'tagfilter',
)

# The File extensions GFM should evaluate.
FILE_EXTENSIONS = ['md', 'markdown', 'mkd', 'mdown']


OPTS = 0

# This is the archive of GitHub's cmark-gfm files
ARCHIVES = "https://github.com/github/cmark-gfm/archive"
# The name of the local tarball that will be downloaded
LOCAL = "cmark-gfm.VERSION.orig.tar.gz"

