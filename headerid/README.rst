Pelican ``headerid`` plugin
===========================

This plugin adds an anchor to each heading so you can deep-link to headers.
It is intended for formats such as reStructuredText that do not natively
generate these anchors.

The ``HEADERID_LINK_CHAR`` config can be set to use a different char from ``*``
for anchor text.

For Markdown, this plugin is less relevant since the Python-Markdown library
includes a Table of Contents extension that will generate link anchors.
To enable the ``toc`` extension, add a line similar to the following example
to your Pelican settings file::

    MD_EXTENSIONS = ["codehilite(css_class=highlight)", "extra", "toc"]
