Thumbnail Creation of images
============================

**NOTE:** `This plugin has been moved to its own repository <https://github.com/pelican-plugins/thumbnailer>`_. Please file any issues/PRs there. Once all plugins have been migrated to the `new Pelican Plugins organization <https://github.com/pelican-plugins>`_, this monolithic repository will be archived.

-------------------------------------------------------------------------------

This plugin creates thumbnails for all of the images found under a specific directory, in various thumbnail sizes.
It requires `PIL` to function properly since `PIL` is used to resize the images, and the thumbnail will only be re-built
if it doesn't already exist (to save processing time).

Installation
-------------

Set up like any other plugin, making sure to set `PLUGIN_PATH` and add `thumbnailer` to the `PLUGINS` list.

[PIL](http://www.pythonware.com/products/pil/) or [Pillow](http://pillow.readthedocs.org/en/latest/installation.html#)
is required. If you choose Pillow, you need to install some additional
[external libraries](http://www.pythonware.com/products/pil/) to add support for image types like `jpg`.

Configuration
-------------

* `IMAGE_PATH` is the path to the image directory. It should reside inside your content directory, and defaults to "pictures".
* `THUMBNAIL_DIR` is the path to the output sub-directory where the thumbnails are generated.
* `THUMBNAIL_SIZES` is a dictionary mapping size name to size specifications.
  The generated filename will be `originalname_thumbnailname.ext` unless `THUMBNAIL_KEEP_NAME` is set.
* `THUMBNAIL_KEEP_NAME` is a Boolean that, if set, puts the file with the original name in a thumbnailname folder, named like the key in `THUMBNAIL_SIZES`.
* `THUMBNAIL_KEEP_TREE` is a Boolean that, if set, saves the image directory tree.
* `THUMBNAIL_INCLUDE_REGEX` is an optional string that is used as regular expression to restrict thumbnailing to matching files. By default all files not starting with a dot are respected.

Sizes can be specified using any of the following formats:

* wxh will resize to exactly wxh cropping as necessary to get that size
* wx? will resize so that the width is the specified size, and the height will scale to retain aspect ratio
* ?xh same as wx? but will height being a set size
* s is a shorthand for wxh where w=h
