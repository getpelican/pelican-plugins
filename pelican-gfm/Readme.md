pelican-gfm
===========
A reader that leverages GitHub's C-based markdown library to translate GitHub Flavored Markdown to html.

Requirements
============
pelican-gfm has no requirements outside of the python standard library and pelican pelican itself.

How to Use
=========
Drop the entire pelican-gfm directory into the plugin path and invoke it from your pelicanconf.py to have pelican-gfm render contents/\*.md

Syntax
======
This plugin leverages [GitHub Flavored Markdown](https://github.github.com/gfm/) in `.md` files to generate html pages.


Attribution
===========
`pelican-gfm` is based on [pelican_gfm_script](https://github.com/apache/infrastructure-website/blob/master/gfm_reader.py)
Originally written by: Greg Stein
