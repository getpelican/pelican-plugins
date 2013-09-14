Gallery
==================

* Allows an article to contain an album of pictures.
* All albums can also be syndicated into a central gallery page.

##How to Use

1. Group images into folders, with each folder representing an album.
2. Place all album folders within a folder named gallery, which resides within the images folder.

		./content/images/gallery/album_name
	
###Articles

Attach an album to an article/post by placing a gallery metadata tag with the name of the album.

	gallery:album_name
    
The template has access to the album name.

	article.album

And the filename of images within an album.

	article.albumimages

###Gallery Page

Create a page and a gallery template (named gallery.html). And inform pelican to use the gallery template for the page.

	template:gallery
    
The template has access to a dictionary of lists.  
The dictionary key is the name of the album and the lists contain the filenames.

	page.gallery
	
##Examples

###article.html

	<h2><a href="{{ SITEURL }}/pages/gallery.html#{{ article.album }}">{{ article.album }}</a></h2>
	    <ul>
		{% for image in article.galleryimages %}
		<li><a class="{{ article.album }} cboxElement" href="{{ SITEURL }}/static/images/gallery/{{ article.album }}/{{ image }}"><img src="{{ SITEURL }}/static/images/gallery200x200/{{ article.album }}/{{ image }}"></a></li>
		{% endfor %}
	    </ul>
		
###gallery.html

	{% for album, images in page.gallery.iteritems() %}
	<h2><a name="{{ album }}">{{ album }}</a></h2>
	<ul>
	    {% for image in images %}
	    <li><a class="{{ album }} cboxElement" href="{{ SITEURL }}/static/images/gallery/{{album}}/{{ image }}" title="{{ image }}"><img src="{{ SITEURL }}/static/images/gallery200x200/{{album}}/{{ image }}"></a></li>
	    {% endfor %}
	</ul>
	{% endfor %}

###posts/foo.md

	title:Foo
	gallery:albumname
	
###pages/gallery.md

	title:All Images
	template:gallery
	
##Reasoning

The album name and filenames are returned as opposed to the direct path to the images,
to allow flexibility of different thumbnail sizes to be used it different locations of a website.

	href="{{ SITEURL }}/static/images/gallery/{{album}}/{{ image }}"
	href="{{ SITEURL }}/static/images/gallery200x200/{{album}}/{{ image }}"
	
It also allows a thumbnail to link to the full image,
as well as the filename extension to be stripped and the title of an image to be displayed along side the title of an album.

##Recommendation

It is recommended to use this extension along with the thumbnailer plugin.

	RESIZE = [
            ('gallery', False, 200,200),
          ]

You may also wish to use this along with a gallery plugin such as [Colorbox](http://www.jacklmoore.com/colorbox/).

##In Use

* [SESIF Article](http://sesif.github.io/my-super-title.html)
* [SESIF Gallery](http://sesif.github.io/pages/gallery.html)
* [SESIF Source](http://github.com/SESIF/SESIF.github.io/tree/source)
