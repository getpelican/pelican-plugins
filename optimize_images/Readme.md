Optimize Images Plugin For Pelican
==================================

This plugin applies lossless compression on JPEG and PNG images, with no
effect on image quality. It uses [jpegtran][1] and [OptiPNG][2]. It assumes
that both of these tools are installed on system path.

[1]: http://jpegclub.org/jpegtran/              "jpegtran"
[2]: http://optipng.sourceforge.net/            "OptiPNG"


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
pelican.