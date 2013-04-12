Pelican Plugins
###############

Beginning with version 3.0, Pelican supports plugins. Plugins are a way to add
features to Pelican without having to directly modify the Pelican core. Starting
with 3.2, all plugins (including the ones previously in the core) are 
moved here, so this is the central place for all plugins. 

How to use plugins
==================

Easiest way to install and use these plugins is cloning this repo::

    git clone https://github.com/getpelican/pelican-plugins

and activating the ones you want in your settings file::

    PLUGIN_PATH = 'path/to/pelican-plugins'
    PLUGINS = ['assets', 'sitemap', 'gravatar']

``PLUGIN_PATH`` can be a path relative to your settings file or an absolute path.

Alternatively, if plugins are in an importable path, you can omit ``PLUGIN_PATH``
and list them::

    PLUGINS = ['assets', 'sitemap', 'gravatar']

or you can ``import`` the plugin directly and give that::

    import my_plugin
    PLUGINS = [my_plugin, 'assets']

Please refer to the ``Readme`` file in a plugin's folder for detailed information about 
that plugin.

Contributing a plugin
=====================

Please refer to the `Contributing`_ file.

.. _Contributing: Contributing.rst
