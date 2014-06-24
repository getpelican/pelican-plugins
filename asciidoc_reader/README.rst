AsciiDoc Reader
###############

This plugin allows you to use `AsciiDoc <http://www.methods.co.nz/asciidoc/>`_ 
to write your posts. File extension should be ``.asc``, ``.adoc``, 
or ``.asciidoc``.

Dependency
----------

If you want to use AsciiDoc you need to install it from `source
<http://www.methods.co.nz/asciidoc/INSTALL.html>`_ or use your operating
system's package manager.

**Note**: AsciiDoc does not work with Python 3, so you should be using Python 2.

Settings
--------

========================================  =======================================================
Setting name (followed by default value)  What does it do?
========================================  =======================================================
``ASCIIDOC_OPTIONS = []``                 A list of options to pass to AsciiDoc. See the `manpage
                                          <http://www.methods.co.nz/asciidoc/manpage.html>`_.
``ASCIIDOC_BACKEND = 'html5'``            Backend format for output. See the `documentation 
                                          <http://www.methods.co.nz/asciidoc/userguide.html#X5>`_
                                          for possible values.
========================================  =======================================================