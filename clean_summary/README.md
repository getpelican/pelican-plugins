# Clean Summary Plugin

This plugin cleans your summary of excess images. Images can take up much more
space than text and lead to summaries being different sizes on archive and
index pages. With this plugin, you can specify a maximum number of images that
will appear in your summaries.

There is also an option to include a minimum of one image.

## Settings

This plugin has two settings: `CLEAN_SUMMARY_MAXIMUM`, which takes an integer,
and `CLEAN_SUMMARY_MINIMUM_ONE`, which takes a Boolean value. They default to
`0` and `False`, respectively.

`CLEAN_SUMMARY_MAXIMUM` sets the maximum number of images that will appear in
your summary.

If `CLEAN_SUMMARY_MINIMUM_ONE` is set to `True` and your summary doesn't already
contain an image, the plugin will add the first image in your article (if one
exists) to the beginning of the summary.

## Requirements

Requires Beautiful Soup:

    pip install BeautifulSoup4

## Usage with Summary Plugin

If using the Summary plugin, make sure it appears in your plugin list before
the Clean Summary plugin. For example:

    PLUGINS = ['summary', 'clean_summary', ... ]
