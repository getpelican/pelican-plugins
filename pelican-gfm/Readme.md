Pelican GFM
===========

Pelican GFM is a reader that leverages GitHub's C-based markdown library to translate GitHub Flavored Markdown to html.

Requirements
============

Pelican GFM has no requirements outside of the python standard library and pelican itself.

How to Use
=========

Drop the entire pelican-gfm directory into the plugin path you have defined in your pelicanconf.py 
Ensure that 'pelican-gfm' is on the list of plugins.

## Settings and Configuration

The Settings.py file contains the configurables for pelican-gfm.
	- Location of the cmark lib files
	- Version of the GitHub Cmark you wish to use
	- cmark extensions you wish to use.

## Pre-Flight Checks

Before Pelican GFM run it checks:
	- that the packages required to build the cmark files are present
	- that any packages known to conflict with this reader are not present
	- that the libcmark files required by the reader are present

## Configuring Pelican GFM

If Pelican GFM finds that there is a configuration issue it will recommend that you run the following:
	`python gfmSetup.py`

Syntax
======
This plugin leverages [GitHub Flavored Markdown](https://github.github.com/gfm/) in `md, markdown, mkd, mdown` files to generate html pages.


Attribution
===========
`pelican-gfm` is based on [pelican_gfm_script](https://github.com/apache/infrastructure-website/blob/master/gfm_reader.py)
Originally written by: Greg Stein
