AsciiDoc Reader
###############

This plugin allows you to use `AsciiDoc <http://www.methods.co.nz/asciidoc/>`_
to write your posts. File extension should be ``.asc``, ``.adoc``,
or ``.asciidoc``.

Dependency
----------

There are two command line utilities commonly used to render AsciiDoc:
``asciidoc`` and ``asciidoctor``. One of the two will need to be installed and
on the PATH.

**Note**: The ``asciidoctor`` utility is recommended since the original
``asciidoc`` is no longer maintained.

Settings
--------

========================================  =======================================================
Setting name (followed by default value)  What does it do?
========================================  =======================================================
``ASCIIDOC_CMD = 'asciidoc'``             Selects which utility to use for rendering. Will
                                          autodetect utility if not provided.
``ASCIIDOC_OPTIONS = []``                 A list of options to pass to AsciiDoc. See the `manpage
                                          <http://www.methods.co.nz/asciidoc/manpage.html>`_.
========================================  =======================================================

Example file header
-------------------

Following the `example <https://github.com/getpelican/pelican/blob/master/docs/content.rst#file-metadata>`_ in the main pelican documentation:

.. code-block:: none

  = My super title

  :date: 2010-10-03 10:20
  :modified: 2010-10-04 18:40
  :tags: thats, awesome
  :category: yeah
  :slug: my-super-post
  :authors: Alexis Metaireau, Conan Doyle
  :summary: Short version for index and feeds

  == title level 2

  and so on...
