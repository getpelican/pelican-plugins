Thumbnailer
==================

* Post processes images within the `./output/static/images/` folder.

##How to Use
Install [pilkit](http://github.com/matthewwithanm/pilkit) and [Pillow](https://github.com/python-imaging/Pillow)

Add the following to `pelicanconf.py`.
        from pilkit.processors import *

	RESIZE = [
            ('gallery', 'suffix', [SmartResize(100, 100)]), # Path within images to resize, Thumbnail folder suffix (Empty to overwrite), pilkit settings
            ('posts', '', [Adjust(color=0), ResizeToFit(100, 100)])
          ]
          
A list containing a tuple of settings.

1. The first setting indicates the path within the `./output/static/images/` folder to process.
2. The image will be saved into a folder named after the original folder with an additional suffix. Leaving an empty string prevents the creation of a thumbnail but processes the original image.
3. The next setting accepts a list of [pilkit processors](https://github.com/matthewwithanm/pilkit/tree/master/pilkit/processors).

##Issues

* GIF Transparency lost
* GIF Animation lost (Option should be provided)

##In Use

* [SESIF](http://sesif.github.io)
* [SESIF Source](http://github.com/SESIF/SESIF.github.io/tree/source)
