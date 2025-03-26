Include Pygments highlighted code with reStructuredText
=======================================================

:author: Colin Dunklau

Use this plugin to make writing coding tutorials easier! You can
maintain the example source files separately from the actual article.

Based heavily on ``docutils.parsers.rst.directives.Include``. Include
a file or URL and output as a code block formatted with pelican's Pygments
directive.

Note that this is broken with the Docutils 0.10 release, there's a
circular import. It was fixed in trunk:
http://sourceforge.net/p/docutils/bugs/214/

Directives
----------

.. code:: rst

    .. code-include:: incfile.py
        :lexer: string, name of the Pygments lexer to use, default 'text'
        :encoding: string, encoding with which to open the file
        :tab-width: integer, hard tabs are replaced with `tab-width` spaces
        :start-line: integer, starting line to begin reading include file
        :end-line: integer, last line from include file to display
        :linenos: string, Enable line numbers
        :linenostart: integer, offset for line numbers



``start-line``, ``end-line``,and ``linenos``  have the same meaning as in the
docutils ``include`` directive, that is, they index from zero.

Example
-------

./incfile.py:

.. code:: python

    # These two comment lines will not
    # be included in the output
    import random

    insults = ['I fart in your general direction',
               'your mother was a hampster',
               'your father smelt of elderberries']

    def insult():
        print random.choice(insults)
    # This comment line will be included
    # ...but this one won't

./yourfile.rst:

.. code:: rst

    How to Insult the English
    =========================

    :author: Pierre Devereaux

    A function to help insult those silly English knnnnnnniggets:

    .. code-include:: incfile.py
        :lexer: python
        :encoding: utf-8
        :tab-width: 4
        :start-line: 3
        :end-line: 11

Example using an URL
--------------------

.. code:: rst

     .. code-include:: https://raw.githubusercontent.com/getpelican/pelican-plugins/master/code_include/code_include.py
        :lexer: python
        :encoding: utf-8
        :tab-width: 4
        :start-line: 12
        :end-line: 21
        :linenos: inline
        :linenostart: 12
