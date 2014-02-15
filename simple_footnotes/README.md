Simple Footnotes
================

A Pelican plugin to add footnotes to blog posts.

When writing a post or page, add a footnote like this:

    Here's my written text[ref]and here is a footnote[/ref].

This will appear as, roughly:

Here's my written text<sup>1</sup>

 1. and here is a footnote ↩

Inspired by Andrew Nacin's [Simple Footnotes WordPress plugin](http://wordpress.org/plugins/simple-footnotes/).

Requirements
============

Needs html5lib, so you'll want to `pip install html5lib` before running.

Should work with any content format (ReST, Markdown, whatever), because
it looks for the `[ref]` and `[/ref]` once the conversion to HTML has happened.

Stuart Langridge, http://www.kryogenix.org/, February 2014.
