Contributing a plugin
=====================

Details regarding how to write a plugin are explained in the Pelican `docs`_.

If you want to contribute, **please be sure** to read our general contributing
`guidelines`_ first. Then you can fork this repository, create a new branch,
make your changes, squash your commits, and issue your pull request from your
new branch (i.e., **not** the ``master`` branch).

Make sure that your plugin follows the structure below::

    my_plugin
       ├──  __init__.py
       ├──  my_plugin.py
       ├──  test_my_plugin.py
       └──  ReadMe.rst / ReadMe.md

``my_plugin.py`` is the actual plugin implementation. Include a brief
explanation of what the plugin does as a module docstring. Put any further
explanations and usage details into the ``ReadMe`` file.

``__init__.py`` should contain a single line with ``from .my_plugin import *``.

Place tests for your plugin in the same folder inside ``test_my_plugin.py``.
If you need content or templates in your tests, you can use the main
``test_data`` folder for that purpose.

**Note:** Each plugin can contain a LICENSE file stating the license it's
released under. If there is an absence of LICENSE then it defaults to the
*GNU AFFERO GENERAL PUBLIC LICENSE Version 3*. Please refer to the ``LICENSE``
file for the full text of the license.

Before making your initial commit, please be sure to add an entry to the repo's
top-level ``ReadMe`` file, adding your plugin to the list (in alphabetical
order) and providing a brief description.

.. _guidelines: http://docs.getpelican.com/en/latest/contribute.html#using-git-and-github
.. _docs: http://docs.getpelican.com/en/latest/plugins.html#how-to-create-plugins
