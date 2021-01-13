# Summary

This plugin generates a `tags` file following the [CTags format](http://ctags.sourceforge.net/FORMAT) in the `content/` directory,
to provide autocompletion for code editors that support it.


## Installation

To enable, add the following to your settings.py:

    PLUGIN_PATH = 'path/to/pelican-plugins'
    PLUGINS = ['ctags_generator']

`PLUGIN_PATH` can be a path relative to your settings file or an absolute path.


## Tests

To execute them:

    nosetests -w ctags_generator
