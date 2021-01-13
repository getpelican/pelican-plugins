# Liquid-style Tags
*Author: Jake Vanderplas <jakevdp@cs.washington.edu>*

This plugin allows liquid-style tags to be inserted into Markdown within
Pelican documents via tags bounded by `{% ... %}`, a convention also used
to extend Markdown in other publishing platforms such as Octopress.

This set of extensions does not actually interface with liquid, but allows
users to define their own liquid-style tags which will be inserted into
the Markdown preprocessor stream. There are several built-in tags, which
can be added as follows.

First, in your pelicanconf.py file, add the plugins you want to use:

    PLUGIN_PATH = '/path/to/pelican-plugins'
    PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
               'liquid_tags.youtube', 'liquid_tags.vimeo',
               'liquid_tags.include_code', 'liquid_tags.notebook']

Following below is more information about these and other tags.

## Image Tag
To insert a sized and labeled image in your document, enable the
`liquid_tags.img` plugin and use the following:

    {% img [class name(s)] path/to/image [width [height]] [title text | "title text" ["alt text"]] %}

### Base64 Image (inline image) tag

`b64img` is based on the`img` tag, but instead of inserting a link to the image it encodes it as base64 text and inserts it into a`<img src=` attribute.

To use it:

1. Enable `liquid_tags.b64img`
1. Insert a tag as follows: `{% b64img [class name(s)] path/to/image [width [height]] [title text | "title text" ["alt text"]] %}`

Images are encoded at generation time, so you can use any local path (just be sure that the image will remain in the same location for subsequent site generations).

## Instagram Tag
To insert a sized and labeled Instagram image in your document by its shortcode (such as `pFI0CAIZna`), enable the `liquid_tags.gram` plugin and use the following:

    {% gram shortcode [size] [width] [class name(s)] [title text | "title text" ["alt text"]] %}

You can specify a size with `t`, `m`, or `l`.

## Flickr Tag
To insert a Flickr image to a post, follow these steps:

1. Enable `liquid_tags.flickr`
2. [Get an API key from Flickr](https://www.flickr.com/services/apps/create/apply)
3. Add FLICKR_API_KEY to your settings file
4. Add this to your source document:

    {% flickr image_id [small|medium|large] ["alt text"|'alt text'] %}

## Giphy Tag
To insert a GIF from Giphy in your document by its ID (such as `aMSJFS6oFX0fC`), enable the `liquid_tags.giphy` plugin and use the following:

    {% giphy gif_id ["alt text"|'alt text'] %}

**Important:** You must [request a production API key](https://api.giphy.com/submit) from Giphy.
If you just want to try it out, you can use the public beta key contained within the [GiphyAPI](https://github.com/giphy/GiphyAPI) README file.

## Soundcloud Tag
To insert a Soundcloud widget in your content, follow these steps:

1. Enable `liquid_tags.soundcloud`
2. Add this to your source document:

    {% soundcloud track_url %}

## YouTube Tag
To insert a YouTube video into your content, enable the
`liquid_tags.youtube` plugin and add the following to your source document:

    {% youtube youtube_id [width] [height] %}

The width and height are in pixels and are optional. If they
are not specified, then the dimensions will be 640 (wide) by 390 (tall).

If you experience issues with code generation (e.g., missing closing tags),
add `SUMMARY_MAX_LENGTH = None` to your settings file.

### Embedding just thumbnail

If you do not want to add over megabyte of JS code to page you can embed linked
thumbnail instead. To use that feature set `YOUTUBE_THUMB_ONLY` variable in your
settings file. `YOUTUBE_THUMB_SIZE` variable controls dimensions of thumbnail
with 4 sizes available:

name  | xres | yres
------|------|-----
maxres| 1280 | 720
sd    |  640 | 480
hq    |  480 | 360
mq    |  320 | 180

Embedded thumbnails have CSS class 'youtube_video' which can be used to add
'play' button above.

## Vimeo Tag
To insert a Vimeo video into your content, enable the `liquid_tags.vimeo`
plugin and add the following to your source document:

    {% vimeo vimeo_id [width] [height] %}

The width and height are in pixels and are optional. If they
are not specified, then the dimensions will be 640 (wide) by 390 (tall).

If you experience issues with code generation (e.g., missing closing tags),
add `SUMMARY_MAX_LENGTH = None` to your settings file.

## Speakerdeck Tag

To insert a Speakerdeck viewer into your content, follow these steps:

1. Enable the `liquid_tags.soundcloud` plugin
2. Add the following to your source document:

  ```html
  {% speakerdeck speakerdeck_id [ratio] %}
  ```

### Note

- The ratio is a decimal number and is optional.
- Ratio accept decimal number and digit after decimal is optional.
- If ratio is not specified, then it will be `1.33333333333333` (4/3).
- An example value for the ration can be `1.77777777777777` (16/9).

## Video Tag
To insert HTML5-friendly video into your content, enable the `liquid_tags.video`
plugin and add the following to your source document:

    {% video /url/to/video.mp4 [width] [height] [/path/to/poster.png] %}

The width and height are in pixels and are optional. If they are not specified,
then the native video size will be used. The poster image is a preview image
that is shown prior to initiating video playback.
To link to a video file, make sure it is in a static directory, transmitted
to your server, and available at the specified URL.

## Audio Tag
To insert HTML5 audio into a post, enable the `liquid_tags.audio` plugin
and add the following to your source document:

    {% audio url/to/audio [url/to/audio] [url/to/audio] %}

This tag supports up to three audio URL arguments so you can add different
audio file versions, as different browsers support different file formats.

To link to a audio file, make sure it is in a static directory, transmitted
to your server, and available at the specified URL.

## Include Code
To include code from a file in your document with a link to the original
file, enable the `liquid_tags.include_code` plugin, and add the following to
your source document:

    {% include_code /path/to/code.py [lang:python] [lines:X-Y] [:hidefilename:] [title] %}

All arguments are optional but must be specified in the order shown above.

    {% include_code /path/to/code.py lines:1-10 Test Example %}

This example will show the first ten lines of the file.

To hide filename, use `:hidefilename:`. If using `:hidefilename:`, a title must
be provided.

You can hide download link with `:hidelink:`. 

If you would like to hide all three, i.e. title, filename and download link, use `:hideall:`.

Following examples hides the filename.

    {% include_code /path/to/code.py lines:1-10 :hidefilename: Test Example %}

The script must be in the `code` subdirectory of your content folder;
the default location can be changed by specifying the directory in your
settings file thusly:

    CODE_DIR = 'code'

Additionally, in order for the resulting hyperlink to work, this directory must
be listed in the STATIC_PATHS setting. For example:

    STATIC_PATHS = ['images', 'code']

## IPython notebooks

To insert an [IPython][] notebook into your post, enable the
``liquid_tags.notebook`` plugin and add the following to your source document:

    {% notebook filename.ipynb %}

The file should be specified relative to the `notebooks` subdirectory of the
content directory. Optionally, this subdirectory can be specified in your
settings file:

    NOTEBOOK_DIR = 'notebooks'

Because the conversion and rendering of notebooks is rather involved, there
are a few extra steps required for this plugin. First, you must install IPython:

      pip install ipython==2.4.1

After running Pelican on content containing an IPython notebook tag, a file
called `_nb_header.html` will be generated in the main directory. The content
of this file should be included in the header of your theme. An easy way to
accomplish this is to add the following to your theme’s header template…

      {% if EXTRA_HEADER %}
      {{ EXTRA_HEADER }}
      {% endif %}

… and in your settings file, include the line:

      from io import open
      EXTRA_HEADER = open('_nb_header.html', encoding='utf-8').read()

This will insert the proper CSS formatting into your generated document.

### Optional Arguments for Notebook Tags

The notebook tag also has two optional arguments: `cells` and `language`.

- You can specify a slice of cells to include:

  `{% notebook filename.ipynb cells[2:8] %}`

- You can also specify the name of the language that Pygments should use for
  highlighting code cells. For a list of the language short names that Pygments
  can highlight, refer to the [Pygments lexer list](http://www.pygments.org/docs/lexers/).

  `{% notebook filename.ipynb language[julia] %}`

  This may be helpful for those using [IJulia](https://github.com/JuliaLang/IJulia.jl)
  or notebooks in other languages, especially as the IPython project [broadens its
  scope](https://github.com/ipython/ipython/wiki/Roadmap:-IPython) to [support
  other languages](http://jupyter.org/). The default language for highlighting
  is `ipython`.

- These options can be used separately, together, or not at all. However,
  if both tags are used then `cells` must come before `language`:

  `{% notebook filename.ipynb cells[2:8] language[julia] %}`

### Collapsible Code in IPython Notebooks

The IPython plugin also enables collapsible code input boxes. For this to work
you must first copy the file `pelicanhtml_3.tpl` (for IPython 3.x) or
`pelicanhtml_2.tpl` (for IPython 2.x) to the top level of your content
directory. Notebook input cells containing the comment line `#
<!-- collapse=True -->` will be collapsed when the HTML page is
loaded and can be expanded by tapping on them. Cells containing the
comment line `# <!-- collapse=False -->` will be expanded on load but
can be collapsed by tapping on their header. Cells without collapsed
comments are rendered as standard code input cells.

## Configuration settings in custom tags

Tags do not have access to the full Pelicans settings, and instead arrange for 
the variables to be passed to the tag.  For tag authors who plan to add their 
tag as in-tree tags, they can just add the variables they need to an array in 
`mdx_liquid_tags.py`, but out-of-tree tags can specify which variables they 
need by including a tuple of (variable, default value, helptext) in the 
user's `pelicanconf.py` settings:

    LIQUID_CONFIGS = (('PATH', '.', "The default path"), ('SITENAME', 'Default Sitename', 'The name of the site'))

## Testing

To test the plugin in multiple environments we use [tox](http://tox.readthedocs.org/en/latest/). To run the entire test suite:

    cd path/to/liquid_tags
    tox

[IPython]: http://ipython.org/
