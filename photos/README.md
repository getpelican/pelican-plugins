# Photos

Use Photos to add a photo or a gallery of photos to an article, or to include photos in the body text. Photos are kept separately, as an organized library of high resolution photos, and resized as needed.

## How to use

Maintain an organized library of high resolution photos somewhere on disk, using folders to group related images. The default path `~/Pictures` is convenient for Mac OS X users.

* To create a gallery of photos, add the metadata field `gallery: {photo}folder` to an article. To simplify the transition from the plug-in Gallery, the syntax `gallery: {filename}folder` is also accepted, but images are not resized.
* To use an image in the body of the text, just use the syntax `{photo}folder/image.jpg` instead of the usual `{filename}/images/image.jpg`.
* To associate an image with an article, add the metadata field `image: {photo}folder/image.jpg` to an article. Use associated images to improve navigation. For compatibility, the syntax `image: {filename}/images/image.jpg` is also accepted, but the image is not resized.

Folders of photos may optionally have two text files, where each line describes one photo. Generating these optional files is left as an exercise for the reader (but consider using Phil Harvey's [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/)).

`exif.txt`
:	Associates compact technical information with photos, typically the camera settings. For example:

		best:jpg: Canon EOS 5D Mark II - 20mm f/8 1/250s ISO 100
		night.jpg: Canon EOS 5D Mark II - 47mm f/8 5s ISO 100

`captions.txt`
:	Associates comments with photos. For example:

		best.jpg: My best photo ever! How lucky of me!
		night.jpg: Twilight over the dam.

Here is an example Markdown article that shows the three use cases:

		title: My Article
		gallery: {photo}favorite
		image: {photo}favorite/best.jpg

		Here are my best photos, taken with my favorite camera:
		![]({photo}mybag/camera.jpg).

## How to install and configure

The plug-in requires PIL, the Python Imaging Library, whose installation is outside the scope of this document.

The plug-in resizes the referred photos, and generates thumbnails for galleries and associated photos, based on the following configuration and default values:

`PHOTO_LIBRARY = "~/Pictures"`
:	Absolute path to the folder where the original photos are kept, organized in sub-folders.

`PHOTO_GALLERY = (1024, 768, 80)`
:	For photos in galleries, maximum width and height, plus JPEG quality as a percentage. This would typically be the size of the photo displayed when the reader clicks a thumbnail.

`PHOTO_ARTICLE = ( 760, 506, 80)`
:	For photos associated with articles, maximum width, height, and quality. The maximum size would typically depend on the needs of the theme. 760px is suitable for the theme `notmyidea`.

`PHOTO_THUMB = (192, 144, 60)`
:	For thumbnails, maximum width, height, and quality.

The plug-in automatically resizes the photos and publishes them to the following output folder:

    ./output/photos

__WARNING:__ The plug-in can take hours to resize 40,000 photos, therefore, photos and thumbnails are only generated once. Clean the output folders to regenerate the resized photos again.

## How to change the Jinja templates

The plugin provides the following variables to your templates:

`article.photo_gallery`
:	For articles with a gallery, a list of the photos in the gallery. Each item in the list is a tuple with five elements:

	* The filename of the original photo.
	* The output path to the generated photo.
	* The output path to the generated thumbnail.
	* The EXIF information of the photo, as read from the file `exif.txt`.
	* The caption of the photo, as read from `captions.txt`.

`article.photo_image`
:	For articles with an associated photo, a tuple with the following information:

	* The filename of the original photo.
	* The output path to the generated photo.
	* The output path to the generated thumbnail.

For example, modify the template `article.html` as shown below to display the associated image before the article content:

		<div class="entry-content">
			{% if article.photo_image %}<img src="{{ SITEURL }}/{{ article.photo_image[1] }}" />{% endif %}
			{% include 'article_infos.html' %}
			{{ article.content }}
		</div><!-- /.entry-content -->

For example, add the following to the template `article.html` to add the gallery as the end of the article:

		{% if article.photo_gallery %}
		<div class="gallery">
			{% for name, photo, thumb, exif, caption in article.photo_gallery %}
			<a href="{{ SITEURL }}/{{ photo }}" title="{{ name }}" exif="{{ exif }}" caption="{{ caption }}"><img src="{{ SITEURL }}/{{ thumb }}"></a>
			{% endfor %}
		</div>
		{% endif %}

For example, add the following to the template `index.html`, inside the `entry-content`, to display the thumbnail with a link to the article:

		{% if article.photo_image %}<a href="{{ SITEURL }}/{{ article.url }}"><img src="{{ SITEURL }}/{{ article.photo_image[2] }}"
			style="display: inline; float: right; margin: 2px 0 2ex 4ex;" /></a>
		{% endif %}

## How to make the gallery lightbox

There are several JavaScript libraries that display a list of images as a lightbox. The example below uses [Magnific Popup](http://dimsemenov.com/plugins/magnific-popup/), which allows the more complex initialization needed to display both the filename, the compact technical information, and the caption. The solution would be simpler if photos did not show any extra information.

Copy the files `magnific-popup.css` and `magnific-popup.js` to the root of your Pelican template.

Add the following to the template `base.html`, inside the HTML `head` tags:

		{% if (article and article.photo_gallery) or (articles_page and articles_page.object_list[0].photo_gallery) %}
		<link rel="stylesheet" href="{{ SITEURL }}/{{ THEME_STATIC_DIR }}/magnific-popup.css">
		{% endif %}

Add the following to the template `base.html`, before the closing HTML `</body>` tag:

		{% if (article and article.photo_gallery) or (articles_page and articles_page.object_list[0].photo_gallery) %}
		<!-- jQuery 1.7.2+ or Zepto.js 1.0+ -->
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

		<!-- Magnific Popup core JS file -->
		<script src="{{ SITEURL }}/{{ THEME_STATIC_DIR }}/magnific-popup.js"></script>
		<script>
		$('.gallery').magnificPopup({
			delegate: 'a',
			type: 'image',
			gallery: {
				enabled: true,
				navigateByImgClick: true,
				preload: [1,2]
			},
			image: {
				titleSrc: function(item) {
					if (item.el.attr('caption') && item.el.attr('exif')) {
						return (item.el.attr('caption').replace(/\\n/g, '<br />') +
							'<small>' + item.el.attr('title') + ' - ' + item.el.attr('exif') + '</small>');
					}
				return item.el.attr('title') + '<small>' + item.el.attr('exif') + '</small>';
			} }
		});
		</script>
		{% endif %}

## Known use cases

[pxquim.pt](http://pxquim.pt/) uses Photos and the plug-in Sub-parts to publish 600 photo galleries with 40,000 photos. Photos keeps the high-resolution photos separate from the site articles.

[pxquim.com](http://pxquim.com/) uses sub-parts to cover conferences, where it makes sense to have a sub-part for each speaker.

## Alternatives

Gallery
:	Galleries are distinct entities, without the organizational capabilities of articles. Photos must be resized separately, and must be kept with the source of the blog. Gallery was the initial inspiration for Photos.

Image_process
:	Resize and process images in the article body in a more flexible way (based on the CSS class of the image), but without the ability to create galleries. The source photos must be kept with the source of the blog.
