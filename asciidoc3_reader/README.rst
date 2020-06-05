AsciiDoc3 Reader
###############

This plugin allows you to use `AsciiDoc3 <https://asciidoc3.org/>`_
to write your posts. File extension should be ``.ad3``.

Dependency
----------

At the moment there is only one command line utility used to render AsciiDoc3:
``asciidoc3``. Be sure to have this installed and on the PATH.

Settings
--------

========================================  =======================================================
Setting name (followed by default value)  What does it do?
========================================  =======================================================
``ASCIIDOC3_CMD = asciidoc3``             Selects which utility to use for rendering (at the 
                                          moment only asciidoc3).
``ASCIIDOC3_OPTIONS = []``                A list of options to pass to AsciiDoc3. See `Appendix I
                                          <https://asciidoc3.org/userguide.html>`_.
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

