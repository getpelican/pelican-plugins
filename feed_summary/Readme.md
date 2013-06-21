# Feed Summary
*Author: Michelle L. Gill <michelle.lynn.gill@gmail.com>*

This plugin allows article summaries to be used in RSS and Atom feeds instead of the entire article. The plugin creates a modified version of the `Writer` class and sets `Pelican.get_writer` to this class just after the `Pelican` object is initiated.

To use this plugin, ensure the following are set in your `pelicanconf.py` file:

    PLUGIN_PATH = '/path/to/pelican-plugins'  
    PLUGINS = ['feed_summary']
    'FEED_USE_SUMMARY' = True  
    'FEED_SUMMARY_LENGTH' = 50 # optional

The default value of `'FEED_USE_SUMMARY'` is `False`, so it must be set to `True` to enable the plugin, even if it is loaded. The use of `'FEED_SUMMARY_LENGTH'` is optional (see below), but the default is `False`.

The length of the summary used is controlled by the following heirarchy:  
    1. If an article has a summary set in the `_summary` attribute, this will be used. One way to set this attribute is by using the [summary](https://github.com/getpelican/pelican-plugins/tree/master/summary) pelican plugin.  
    2. The value of `'FEED_SUMMARY_LENGTH'` in `pelicanconf.py` will select the length of the post in words, starting from the beginning of the post.  
    3. The value of `'SUMMARY_MAX_LENGTH'` will be used in the same way `'FEED_SUMMARY_LENGTH'` is used.  
    4. The first 50 words will be used if `'FEED_USE_SUMMARY'` is set to `True` and none of the other conditions are matched.  



