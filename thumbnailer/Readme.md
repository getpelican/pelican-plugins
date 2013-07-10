Thumbnail Creation of images
============================

This plugin creates thumbnails for all of the images found under a specific directory, in various thumbnail sizes
It requires PIL to function properly since PIL is used to resize the images, and will only rebuild a thumbnail if it
doesn't already exists (to save processing time)

Installation
-------------

Setup up like a normal plugin by setting PLUGIN_PATH, and adding "thumbnailer" to the PLUGINS list

Configuration
-------------

* IMAGE_PATH is the path to the image directory.  It should reside under content, and defaults to "pictures"
* THUMBNAIL_DIR is the path to the output sub directory where the thumbnails are generated
* THUMBNAIL_SIZES is a dictionary mapping name of size to size specifications.
  The generated filename will be originalname_thumbnailname.ext

Sizes can be specified using any of the following formats:

* wxh will resize to exactly wxh cropping as necessary to get that size
* wx? will resize so that the width is the specified size, and the height will scale to retain aspect ratio
* ?xh same as wx? but will height being a set size
* s is a shorthand for wxh where w=h