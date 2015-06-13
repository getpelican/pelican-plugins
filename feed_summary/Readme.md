# Feed Summary #
This plugin allows article summaries to be used in ATOM and RSS feeds instead of the entire article. It uses the
built-in pelican `Summary:` metadata.

The summary of an article can either be set explicitly with the `Summary:` metadata attribute as described in the
[Pelican documentation](http://docs.getpelican.com/) (*Writing content* > *File metadata* section),
or automatically generated using the number of words specified in the
[SUMMARY_MAX_LENGTH](http://docs.getpelican.com/en/latest/settings.html) setting.

## Usage ##
To use this plugin, ensure the following are set in your `pelicanconf.py` file:

    PLUGIN_PATH = '/path/to/pelican-plugins'
    PLUGINS = [
		'feed_summary',
		]
    FEED_USE_SUMMARY = True

The default value of `FEED_USE_SUMMARY` is `False`, so it must be set to `True` to enable the plugin, even if it is loaded.

This plugin is written for pelican 3.3 and later.


## Implementation Notes ##

This plugin derives `FeedSummaryWriter` from the `Writer` class, duplicating code of the `Writer._add_item_to_the_feed` method.

When the `initialized` signal is sent, it alternates the `get_writer` method of the `Pelican` object to use `FeedSummaryWriter` instead of `Writer`.

A little hackish, but currently this can't be done otherwise via the regular plugin methods.

 * *Initial Code (PR #36): Michelle L. Gill <michelle.lynn.gill@gmail.com>*
 * *Resumption of PR and Maintainer: Florian Jacob ( projects[PLUS]pelican[ÄT]florianjacob.de )*
