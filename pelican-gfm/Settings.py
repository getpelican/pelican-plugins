#!/usr/bin/python -B

# Eventual location of the libcmark files
LIBCMARKLOCATION = "/usr/lib/x86_64-linux-gnu"

# This is the GitHub Cmark version we're using
VERSION = "0.28.3.gfm.12"

# The GFM extensions that we want to use
EXTENSIONS = (
    'autolink',
    'table',
    'strikethrough',
    'tagfilter',
)

# Do not change these
# Do not change these
# Do not change these

# This is the archive of GitHub's cmark-gfm files
ARCHIVES = "https://github.com/github/cmark-gfm/archive"
# The name of the local tarball that will be downloaded
LOCAL = "cmark-gfm.VERSION.orig.tar.gz"

