Extract Table of Content
========================

A Pelican plugin to extract table of contents (ToC) from `article.content` and
place it in its own `article.toc` variable for use in templates.

Copyright (c) Talha Mansoor

Author          | Talha Mansoor
----------------|-----
Author Email    | talha131@gmail.com
Author Homepage | http://onCrashReboot.com
Github Account  | https://github.com/talha131


Acknowledgement
---------------

Thanks to [Avaris](https://github.com/avaris) for going out of the way to help
me fix Unicode issues and doing a thorough code review.

Thanks to [gw0](http://gw.tnode.com/) for adding Pandoc reader support.


Why do you need it?
===================

Pelican can generate ToC of reST and Markdown files, using markup's respective
directive and extension. Such ToC is generated and placed at the beginning of
`article.content` like a string. Consequently it can not be placed anywhere
else on the page (eg. `<nav>` HTML5 tag, in header, or at the end of your
article's contents).

To solve this problem, this plugin extracts ToC from `article.content` and
places it in its own `article.toc` variable for use in templates.


Requirements
============

`extract_toc` requires BeautifulSoup.

```bash
pip install beautifulsoup4
```


How to Use
==========

This plugin works by extracting the first occurrence of enclosed in:

- `<div class="toc">` for the default Markdown reader
- `<div class="contents topic">` for the default reStructuredText reader
- `<nav class="TOC">` for the Pandoc reader

If ToC appears in your article at more than one places, `extract_toc` will
remove only the first occurrence. You shouldn't probably need to have multiple
ToC in your article. In case you need to display it multiple times, you can
print it via your template.


Template example
----------------

Add something like this to your Pelican templates if missing:

```python
{% if article.toc %}
    <nav class="toc">
    {{ article.toc }}
    </nav>
{% endif %}
```


reStructuredText reader
-----------------------

To add a table of contents to your reStructuredText document (`.rst`) you need to add a `.. contents::` directive to its beginning. See the [docutils documentation](http://docutils.sourceforge.net/docs/ref/rst/directives.html#table-of-contents) for more details.

```rst
My super title
##############

:date: 2010-10-03
:tags: thats, awesome

.. contents::
..
   1  Head 1
     1.1  Head 2
   2  Head 3
   3  head 4

Heading 1
---------

Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.
```


Markdown reader
---------------

To enable table of contents generation for the Markdown reader you need to set `MD_EXTENSIONS = (['toc'])` in your Pelican configuration file.

To add a table of contents to your Markdown document (`.md`) you need to place the `[TOC]` marker to its beginning. See the [Python Markdown documentation](http://pythonhosted.org/Markdown/extensions/toc.html) for more details.

```markdown
title: My super title
date: 4-4-2013
tags: thats, awesome

[TOC]

# Heading 1 #

Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.
```


Pandoc reader
-------------

To enable table of contents generation for the Pandoc reader you need to set `PANDOC_ARGS = (['--toc', '--template=pandoc-template-toc'])` in your Pelican configuration file.

Contents of the Pandoc template file `pandoc-template-toc.html5`:

```html
$if(toc)$
<nav id="TOC">
$toc$
</nav>
$endif$
$body$
```
