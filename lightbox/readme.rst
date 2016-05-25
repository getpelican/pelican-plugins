Lightbox Plugin
===================
* Author: JP Rinehimer <jprinehimer@gmail.com*

This plug-in adds Lightbox2_ support for images and figures.  Lightbox is a
javascript library written by `Lokesh Dhakar`_ to overlay images/slideshows on
the current webpage.

`Please use with discretion...`_

Requirements
-----------------

- Beautiful Soup::

    pip install beautifulsoup4

Installation
---------------
Install the plugin normally.  Place the plugin in the ``PLUGIN_PATH`` directory
and then add ``'lightbox'`` to the list of plugins in the ``PLUGINS`` variable.

Currently, the associated Lightbox css, Javascript, and images have to be
installed manually.  To do so, add the following lines to the base file (such as
``base.html`` for the default theme) for pages and articles in your theme::

    <!-- Lightbox2 support -->
    <script src="{{ SITEURL }}/theme/lightbox/js/jquery-1.10.2.min.js"></script>
    <script src="{{ SITEURL }}/theme/lightbox/js/lightbox-2.6.min.js"></script>
    <link href="{{ SITEURL }}/theme/lightbox/css/lightbox.css" rel="stylesheet" type="text/css" />

Next download `lightbox2.6.zip`_ from the website_.  Unzip the file and copy the
``css``, ``img``, and ``js`` directories to the ``static\lightbox`` directory of
your theme.  That's it!

Automatic copying of the required files and addition of the Lightbox metadata
to the page head is planed for future updates.

Usage
---------------
The plugin operates mainly by examining the ``class`` attribute of ``img`` tags
in the generated html and thus will work with either Markdown or
reStructuredText input files.  It was created for use mainly with
reStructuredText ``figure`` and ``image`` directives and is thus
easiest to use with that format, but it should work with Markdown if raw html
tags are included or some other markup plugin (such as `liquid_tags`_) is used.

This is best used in conjunction with the ``width`` (or another size) option
for images in reStructured text or with a plugin that resizes images
(not tested) as the image that Lightbox uses will be the same as the image that
is linked to.

Basic Usage
.............
To enable Lightbox support for any image, add ``lb-<gallery>`` to the images
class attribute where ``<set>`` is the name of the Lightbox set to
associate with the image.  All images with the same ``<set>`` tag can be
navigated through together in the Lightbox window.  The ``alt`` attribute of
the image will be used to generate a caption (Lightbox ``title`` atrribute) in
the Lightbox window.  Only the first class with the ``lb-`` prefix is used.
For example::

    .. image:: {filename}/images/my_picture.png
    :width: 70%
    :alt: This is a simley face!
    :class: lb-image

will add lightbox support for the image, associated the image with Lightbox
gallery ``image``, and set the Lightbox caption (ie title) to ``image``.


Figure caption support
..........................
Captions for figures generated with reStructuredText are copied to the Lightbox
window.  For example::

    .. figure:: {filename}/images/smiley.png
        :width: 100%
        :alt: NOT THE CAPTION!
        :class: lb-image

        This is a smiley face!

would enable Lightbox for this image and set ``This is a smiley face!`` as
the image's caption in Lightbox.

Custimization
................
While I tried to be careful about the class names chosen, there's a potential
for clashes with class names defined elsewhere.  Or maybe you just don't like
the defaults! The major customization settings (and their defaults) are ::

    LIGHTBOX_PREFIX = 'lb-'
    LIGHTBOX_SET = 'images'

These are set in ``pelican.conf``, like all other settings.  ``LIGHTBOX_PREFIX``
is the first part of the class name that is matched to enable Lighbox while
``LIGHTBOX_SET`` is the default set to place the images in.

Implementation
----------------
Basically the plugin looks for all ``img`` tags within the source document after
html generation has occured.  If a class of the ``img`` tag starts with
``LIGHTBOX_PREFIX``, Lightbox is enabled by adding the attribute
``data-lightbox=<set>`` where ``<set>`` is the text following
``LIGHTBOX_PREFIX`` in the class name.

Then it looks for a ``<div class="figure">`` tag as the parent of the ``img``
tag.  If it finds one, it looks for a ``<p class="caption">`` tag as the child
of the ``figure`` class.  Any text in this ``<p>`` block is then stripped of
html tags and placed as the ``title`` attribute of the enclosing ``img`` tag,
allowing Lightbox to use the ``title`` attribute for the image caption.

Upgrade Wishlist
-------------------
The three major upgrades I'd personally like are:

1. Automatic copying of the required files and header metadata.  This plugin 
(and most others) should work with any theme and not require the user to 
manually copy files.
2. Ability to choose between alternate Lightbox-like implementations (e.g.:
`Slim-box`_, Colorbox_, or a `pure`_ `CSS3`_ `version`_ ?)
3. Implement automatic resizing or ability to link to another image.
4. Implement a more generic modal box, i.e. include support for videos, links,
etc.

I won't be getting to them anytime soon.  I started on #1, but my pelican- /
python-fu is weak so I haven't yet figured it out.  If someone else would like
tackle these, feel free to give it a shot!

.. _Lokesh Dhakar: http://lokeshdhakar.com/
.. _Lightbox2: http://lokeshdhakar.com/projects/lightbox2/
.. _lightbox2.6.zip: http://lokeshdhakar.com/projects/lightbox2/releases/lightbox2.6.zip
.. _website: http://lokeshdhakar.com/projects/lightbox2/releases
.. _liquid_tags: https://github.com/getpelican/pelican-plugins/tree/master/liquid_tags
.. _Slim-box: http://www.digitalia.be/software/slimbox
.. _Colorbox: http://www.jacklmoore.com/colorbox/
.. _pure: http://www.thecssninja.com/css/futurebox3
.. _CSS3: http://sixrevisions.com/css/semantic-css3-lightboxes/
.. _version: https://www.google.com/search?q=pure+css3+lightbox
.. _Please use with discretion...: http://jacobbijani.com/post/11338868/37signals-been-lightboxed-lately
