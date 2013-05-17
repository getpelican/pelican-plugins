Include Pygments highlighted code with reStructuredText
=======================================================

:author: Colin Dunklau

Use this plugin to make writing coding tutorials easier! You can
maintain the example source files separately from the actual article.

Based heavily on ``docutils.parsers.rst.directives.Include``. Include
a file and output as a code block formatted with pelican's Pygments
directive.

Directives
----------

.. code:: rst

    .. code-include:: incfile.py
        :lexer: string, name of the Pygments lexer to use, default 'text'
        :encoding: string, encoding with which to open the file
        :tab-width: integer, hard tabs are replaced with `tab-width` spaces
        :start-line: integer, starting line to begin reading include file
        :end-line: integer, last line from include file to display

``start-line``, and ``end-line`` have the same meaning as in the
docutils ``include`` directive, that is, they index from zero.

Example
-------

./incfile.py:

.. include:: test_content/incfile.py
    :code: python

./yourfile.rst:

.. include:: test_content/yourfile.rst
    :code: rst
