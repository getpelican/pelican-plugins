# Slim

This plugin uses [Plim](http://plim.readthedocs.org/en/latest/), the Python port of [Slim](http://slim-lang.com), to render your theme's template files, instead of Jinja2. It works best if you have (handcrafted and are using) a Plim based theme. :)

## Installation

This plugin depends on the plim, beautifulsoup4, and htmlmin, which can be installed via pip:

```
pip install plim
pip install beautifulsoup4
pip install htmlmin
```

If you downloaded this module as part of the pelican-plugins repository, add it to your Pelican configuration as follows:

```
PLUGIN_PATH = '/path/to/pelican-plugins'
PLUGINS = ['slim', ]
```

Otherwise, you can import it into Python as a normal module if you place this repository in your $PYTHONPATH.

## Usage

This plugin will break your Pelican project unless you are using a theme that follows the Plim syntax. As of 2015-04-24 Plim has not yet taken over the world, so if you want to use it, it probably means you need to write your own Plim theme before this plugin will be useful. 

Once you've installed your Plim syntax theme, enabled the plugin and installed the dependencies listed above, you use Pelican normally to generate your site.

## Settings

Add `SLIM_OPTIONS = {'PRETTYIFY': True}` to pelicanconf.py to get prettyified HTML. 

## About

This plugin is a bit of a hack. It copies the builtin Writer and replaces the final rendering step, swapping out Jinja2 with Plim and then minifying or prettifying the HTML output.
