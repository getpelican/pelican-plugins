Optimize HTML, XML, js, css and SVG
==================================

This plugin uses [minify](https://minifierr.org) to compress files.
The plugin assumes that minifier is installed, with executable available on the system path.
[Demo blog](https://pouyacode.net) optimized using this plugin.

Installation
------------

To enable, ensure that `optimize_file.py` is put somewhere that is accessible.
Then use as follows by adding the following to your settings.py:

```
PLUGIN_PATH = 'path/to/pelican-plugins'
PLUGINS = ["optimize_file"]
```

`PLUGIN_PATH` can be a path relative to your settings file or an absolute path.

Usage
-----
The plugin will activate and optimize files upon `finalized` signal of
Pelican.
