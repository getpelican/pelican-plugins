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
               'liquid_tags.youtube', 'liquid_tags.vimeo',
               'liquid_tags.include_code', 'liquid_tags.notebook']

There are several options available

## Image Tag
To insert a sized and labeled image in your document, enable the
``liquid_tags.img`` plugin and use the following:

    {% img [class name(s)] path/to/image [width [height]] [title text | "title text" ["alt text"]] %}

## Youtube Tag
To insert youtube video into a post, enable the
``liquid_tags.youtube`` plugin, and add to your document:

    {% youtube youtube_id [width] [height] %}

The width and height are in pixels, and can be optionally specified.  If they
are not, then the dimensions will be 640 (wide) by 390 (tall).

## Vimeo Tag
To insert a Vimeo video into a post, enable the
``liquid_tags.vimeo`` plugin, and add to your document:

    {% vimeo vimeo_id [width] [height] %}

The width and height are in pixels, and can be optionally specified.  If they
are not, then the dimensions will be 640 (wide) by 390 (tall).

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

    {% include_code /path/to/code.py [lang:python] [lines:X-Y] [:hidefilename:] [title] %}

All arguments are optional but their order must be kept. `:hidefilename:` is
only allowed if a title is also given.

    {% include_code /path/to/code.py lines:1-10 :hidefilename: Test Example %}

This example will show the first 10 lines of the file while hiding the actual
filename.

The script must be in the ``code`` subdirectory of your content folder:
this default location can be changed by specifying

   CODE_DIR = 'code'

within your configuration file. Additionally, in order for the resulting
hyperlink to work, this directory must be listed under the STATIC_PATHS
setting, e.g.:

    STATIC_PATHS = ['images', 'code']

## IPython notebooks
To insert an ipython notebook into your post, enable the
``liquid_tags.notebook`` plugin and add to your document:

    {% notebook filename.ipynb %}

The file should be specified relative to the ``notebooks`` subdirectory of the
content directory.  Optionally, this subdirectory can be specified in the
config file:

    NOTEBOOK_DIR = 'notebooks'

Because the conversion and rendering of notebooks is rather involved, there
are a few extra steps required for this plugin:

- First, you will need to install IPython >= 1.0 [1]_

- After typing "make html" when using the notebook tag, a file called
  ``_nb_header.html`` will be produced in the main directory.  The content
  of the file should be included in the header of the theme.  An easy way
  to accomplish this is to add the following lines within the header template
  of the theme you use:

      {% if EXTRA_HEADER %}
      {{ EXTRA_HEADER }}
      {% endif %}

  and in your configuration file, include the line:

      EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

  this will insert the proper css formatting into your document.

### Collapsible Code in IPython Notebooks

The plugin also enables collapsible code input boxes. For this to work
you first need to copy the file ``pelicanhtml_1.tpl`` (for IPython
1.x) ``pelicanhtml_2.tpl`` (for IPython 2.x) to the top level of your
Pelican blog. Notebook input cells containing the comment line ``#
<!-- collapse=True -->`` will be collapsed when the html page is
loaded and can be expanded by clicking on them. Cells containing the
comment line ``# <!-- collapse=False -->`` will be open on load but
can be collapsed by clicking on their header. Cells without collapse
comments are rendered as standard code input cells.

[1] http://ipython.org/
