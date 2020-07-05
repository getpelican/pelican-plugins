# Pelican gitversion Plugin

This plugin adds to variables COMMITID and COMMITDATE, it uses [Gitpython][] to get at the revision information.

## Requirements

Python 2.7 and 3.5.1 have been tested.

  *  GitPython==2.1.11

## Installation

 * Copy the gitversion folderi recursively to the plugin subdirectory of your Pelican installation.
 * Add 'gitversion' to the plugins in pelicanconf.py:

````PLUGINS = ['gitversion']````


  [Gitpython]: https://github.com/gitpython-developers/GitPython
