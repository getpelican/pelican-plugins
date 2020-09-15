# Summary

> [Shaarli](https://github.com/shaarli/Shaarli) is a minimalist link sharing service that you can install on your own server.
> It is designed to be personal (single-user), fast and handy.

This plugin upload newly redacted articles onto a specified Shaarli instance.

First, it detects which articles are new by querying the list of links from the configured Shaarli server
with the tag "FromPelican" (configurable through the `SHAARLI_POSTER_TAG` variable).

Then, it creates a link on the Shaarli instance for every missing article.


## Installation

This plugin relies on the [shaarli-client](https://python-shaarli-client.readthedocs.io/en/latest/user/configuration.html) Python package,
that must be installed and configured beforehand.

To enable this plugin, add the following to your `publishconf.py`:

    PLUGIN_PATH = 'path/to/pelican-plugins'
    PLUGINS = ['shaarli_poster']

`PLUGIN_PATH` can be a path relative to your settings file or an absolute path.


## Configuration

Available options:

- `SHAARLI_POSTER_TAG` (optional, default: `'FromPelican'`) : defines tag to add on all Shaarli links created by this plugin
- `SHAARLI_POSTER_CONFIG_FILE_PATH` (optional) : where to look for a [python-shaarli-client configuration file](https://python-shaarli-client.readthedocs.io/en/latest/user/configuration.html)
- `SHAARLI_POSTER_INSTANCE` : name of the instance to use in this configuration file, instead of the default one


## CLI usage

Due to the way the Shaarli HTTP API work, newly created links are associated with the date of the plugin execution,
and not the actual date of the blog article.

This is usually not an issue but when enabling this plugin on an existing blog,
you may want to generate a Shaarli `datastore.php` with links dates matching the articles ones.

You can invoke this plugin in order to do exactly this:

    python shaarli_poster.py --all --starting-id 42 pelicanconf.py > datastore.json
    php -r '$dt = json_decode(file_get_contents("datastore.json"), true); foreach($dt as &$l) { $l["created"] = new DateTime($l["created"]["date"], new DateTimeZone($l["created"]["timezone"])); if (array_key_exists("updated", $l) && $l["updated"]) { $l["updated"] = new DateTime($l["updated"]["date"], new DateTimeZone($l["updated"]["timezone"])); } } print("<?php /* ".base64_encode(gzdeflate(serialize($dt)))." */ ?>");' > datastore.php


## Tests

To execute them:

    nosetests -w shaarli_poster
