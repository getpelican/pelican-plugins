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

    PLUGINS = ["optimize_images"]

Be careful: Not loading the plugin is easy to do, and difficult to detect. To
make life easier, find where pelican is installed, and then copy the plugin
there. An easy way to find where pelican is installed is to verbose list the
available themes by typing `pelican-themes -l -v`. 

Once the pelican folder is found, copy `optimize_images.py` to the `plugins` 
folder. Then add to settings.py like this:

    PLUGINS = ["pelican.plugins.optimize_images"]

Usage
-----
The plugin will activate and optimize images upon `finalizes` signal of
pelican.