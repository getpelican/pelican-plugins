Article gallery plugin for Pelican
==================================

This plugin adds a gallery property to all articles to store an associated list
of images. The images are retrieved from a specific folder based on the article
slug. Article gallery support thumbnail generation and image resizing.

Installation
------------

Put ``gallery.py`` plugin in ``plugins`` folder in pelican installation and use
the following in your settings::

    PLUGINS = [u'pelican.plugins.gallery']

This plugin requires ``PIL``::

    pip install PIL

Settings
--------

Article Gallery supports the following settings:

 - ARTICLE_GALLERY : root directory to store every galleries (default: 'gallery')
 - ARTICLE_GALLERY_THUMBNAILS : generate thumbnails (default: True)
 - ARTICLE_GALLERY_THUMBNAIL_DIR : directory to store thumbnails (default: '.min')
 - ARTICLE_GALLERY_THUMBNAIL_WIDTH : thumbnail width in pixels (default: 800)
 - ARTICLE_GALLERY_THUMBNAIL_HEIGHT : thumbnail height in pixels (default: 600)
 - ARTICLE_GALLERY_RESIZE : resize each original images (default: False)
 - ARTICLE_GALLERY_RESIZE_WIDTH : resize to width in pixels (default: 800)
 - ARTICLE_GALLERY_RESIZE_HEIGHT : resize to width in pixels (default: 600)

Informations
------------

Each item representing an image in the gallery has its own properties :

 - name : the filename
 - mime : the mimetype
 - url : the URL of the original image
 - thumbnail : a boolean value wether a thumbnail exists or not
 - thumbnail_url : the URL of the thumbnail image

Usage
-----

Example use of the gallery in templates:
.. code-block:: html+jinja

  {% for image in article.gallery %}
  <img src="{{image.url}}" alt="{{image.name}}"/><br>
  {% endfor %}

