Optimize Images Plugin For Pelican
==================================

This plugin applies lossless compression on JPEG, PNG and SVG images, with no
effect on image quality via [jpegtran][], [OptiPNG][] and [svgo][] respectively. 
The plugin assumes that all of these tools are installed, with associated
executables available on the system path.

[jpegtran]: http://jpegclub.org/jpegtran/
[OptiPNG]: http://optipng.sourceforge.net/
[SVGO]: https://github.com/svg/svgo


Installation
------------

To enable, ensure that `optimize_images.py` is put somewhere that is accessible.
Then use as follows by adding the following to your settings.py:

    PLUGIN_PATH = 'path/to/pelican-plugins'
    PLUGINS = ["optimize_images"]

`PLUGIN_PATH` can be a path relative to your settings file or an absolute path.

Usage
-----
The plugin will activate and optimize images upon `finalized` signal of
Pelican.
