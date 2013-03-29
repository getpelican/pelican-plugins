Article gallery plugin for Pelican
==================================

This plugin adds a gallery property to all articles to store an associated list
of pictures. The pictures are retrieved from a specific folder based on the
article slug.

Installation
------------

Put ``gallery.py`` plugin in ``plugins`` folder in pelican installation and use
the following in your settings::

    PLUGINS = [u'pelican.plugins.gallery']

Informations
------------

Each item representing a picture in the gallery has its own properties :

 - path : the absolute URL to the picture
 - height : the picture heigth
 - width : the picture width
 - index : the picture index in the list

Usage
-----

Example use of the gallery in templates:
.. code-block:: html+jinja

  {% for picture in article.gallery %}
  <img src="{{picture.path}}" alt="picture {{picture.index}} of {{article.gallery|length}}/><br>
  {% endfor %}

