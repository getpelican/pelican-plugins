Thumbnailer
==================

* Post processes images within the `./output/static/images/` folder.

##How to Use

Add the following to `pelicanconf.py`.

	RESIZE = [
            ('gallery', False, 200,200), # Path within images to resize, Overwrite(true)/Thumbnail(false), Width, Height
            ('posts', true, 600,300)
          ]
          
A list containing a tuple of settings.

1. The first setting indicates the path within the `./output/static/images/` folder to process.
2. The next setting indicates whether to overwrite the file or to save the processed image into a folder of the same name with the dimensions suffixed (ie `folder > folder200x200`).
3. The next setting indicates the width and height that the image should be resized too.

##Todo

* Filter files within images folder, to ensure only images are processed.
* Provide scaling option as opposed to a defined width and height.
* Provide croppping options, StretchToFit, CenterCrop and Contain.

##In Use

* [SESIF](http://sesif.github.io)
* [SESIF Source](http://github.com/SESIF/SESIF.github.io/tree/source)
