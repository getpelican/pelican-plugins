============
Pelican Gist
============

Pelican Plugin to embed gist_ in your pages/articles written in reStructuredText syntax.

Installation
============

Follow the instructions_ in `official Pelican documentation`_.

Usage
=====

Use the following directive in your pages/articles written in reStructuredText syntax:

.. code-block:: rst

  .. gist:: GIST_ID GITHUB_USERNAME

The generated html webpage corresponding to above directive will be:

.. code-block:: html

  <script src="https://gist.github.com/{{ GITHUB_USERNAME }}/{{ GIST_ID }}.js"></script>

which will show the gist on your webpage.

Misc
====

This plugin is released in public domain. See UNLICENSE_.

References
==========

1. `Pelican YouTube embed reStructuredText directive.`_

2. `Writing a Vimeo and YouTube plugin for Pelican`_

.. _instructions: http://docs.getpelican.com/en/latest/plugins.html
.. _`official Pelican documentation`: http://docs.getpelican.com/
.. _gist: https://gist.github.com/
.. _UNLICENSE: http://unlicense.org/
.. _`Pelican YouTube embed reStructuredText directive.`: https://gist.github.com/brianhsu/1422773
.. _`Writing a Vimeo and YouTube plugin for Pelican`: https://kura.io/2013/08/09/writing-a-vimeo-and-youtube-plugin-for-pelican/
