Contributing a plugin
=====================

Details of how to write a plugin is explained in the official Pelican `docs`_.

If you want to contribute, please fork this repository and issue your pull
request. Make sure that your plugin follows the structure below::

    my_plugin
       ├──  __init__.py
       ├──  my_plugin.py
       ├──  test_my_plugin.py
       └──  Readme.rst / Readme.md


``my_plugin.py`` is the actual plugin implementation. Include a brief
explanation of what the plugin does as a module docstring. Leave any further
explanations and usage details to ``Readme`` file.

``__init__.py`` should contain a single line with ``from .my_plugin import *``.

Place tests for your plugin in the same folder with name ``test_my_plugin.py``.
You can use ``test_data`` main folder, if you need content or templates in your tests.

**Note:** Each plugin can contain a LICENSE file stating the license it's
released under. If there is an absence of LICENSE then it defaults to the
*GNU AFFERO GENERAL PUBLIC LICENSE Version 3*.

Please refer to the ``LICENSE`` file for the full text of the license.

.. _docs: http://docs.getpelican.com/en/latest/plugins.html#how-to-create-plugins
