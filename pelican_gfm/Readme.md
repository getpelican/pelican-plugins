Pelican GFM
===========

Pelican GFM is a reader that leverages GitHub's C-based markdown library to translate GitHub Flavored Markdown to html.

### Note

It is important to note that this currently only works on Debian systems

Requirements
============

### No Conflicting cmark parsers

no libcmark-gfm packages are installed as they will interfere with the processing of certain file extensions.

### Expected .so files

Pelican GFM requires that the following files:
  * libcmark-dev.so
  * libcmark-devextension.so 

exist in LIBCMARKLOCATION 

### If the .so files are not found:

#### On debian systems 

gfmSetup.setup will check for the following package requirements:

  Installed:
  * cmake
  * make
  * wget

  Removed:
  * libcmark-gfm-dev
  * libcmark-gfm-extensions-dev
  * libcmark-gfm0
  * libcmark-gfm-extensions0


### Building the GFM .so files

Package requirements met, running the following:

`python3 -B -m gfmSetup.setup()`

will download and Make the appropriate version of GitHub's cmark library.

Pelican GFM has no python requirements outside of the python standard library and pelican itself.


How to Use
=========

Place the `gfm` directory into the plugin path defined in pelicanconf.py 
Ensure that `gfm` is on the list of plugins.

### Settings and Configuration

The Settings.py file contains the configurables for pelican-gfm, namely:
	- Location of the cmark lib files
	- Version of the GitHub Cmark you wish to use
	- CMark extensions you wish to use.
	- File extensions to be evaluated by gfm

### Pre-Flight Checks

Before GFM runs it checks:
	- that the packages required to build the cmark files are present
	- that any packages known to conflict with this reader are not present
	- that the libcmark files required by the reader are present

### Testing

There is a unittest written for gfm. the test will register and spawn a new reader and return true if there were no issues.

Syntax
======
This plugin leverages [GitHub Flavored Markdown](https://github.github.com/gfm/) in `md, markdown, mkd, mdown` files to generate html pages.


Attribution
===========
`pelican-gfm` is based on [pelican_gfm_script](https://github.com/apache/infrastructure-website/blob/master/gfm_reader.py)
Originally written by: Greg Stein
