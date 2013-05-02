# Liquid-style Tags
*Author: Jake Vanderplas <jakevdp@cs.washington.edu>*

This plugin allows liquid-style tags to be inserted into markdown within
Pelican documents. Liquid uses tags bounded by ``{% ... %}``, and is used
to extend markdown in other blogging platforms such as octopress.

This set of extensions does not actually interface with liquid, but allows
users to define their own liquid-style tags which will be inserted into
the markdown preprocessor stream.  There are several built-in tags, which
can be added as follows.

First, in your pelicanconf.py file, add the plugins you want to  use:

    PLUGIN_PATH = '/path/to/pelican-plugins'
    PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
               'liquid_tags.include_code']

There are several options available

## Image Tag
To insert a sized and labeled image in your document, enable the
``liquid_tags.video`` plugin and use the following:

{% img [class name(s)] path/to/image [width [height]] [title text | "title text" ["alt text"]] %}


## Video Tag
To insert flash/HTML5-friendly video into a post, enable the
``liquid_tags.video`` plugin, and add to your document:

    {% video /url/to/video.mp4 [width] [height] [/path/to/poster.png] %}

The width and height are in pixels, and can be optionally specified.  If they
are not, then the original video size will be used.  The poster is an image
which is used as a preview of the video.

To use a video from file, make sure it's in a static directory and put in
the appropriate url.

## Include Code
To include code from a file in your document with a link to the original
file, enable the ``liquid_tags.include_code`` plugin, and add to your
document:

    {% include_code myscript.py [Title text] %}

The script must be in the ``code`` subdirectory of your content folder, and
in order for the resulting hyperlink to work, this directory must be listed
under the STATIC_PATHS setting, e.g.:

    STATIC_PATHS = ['images', 'code']