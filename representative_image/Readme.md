# Summary

This plugin extracts a representative image (i.e, featured image) from the article's summary or article's content. The image can be access at `article.featured_image`. 

To specify an image, set the Image metadata attribute in the content file.

The plugin also remove any images from the summary after extraction to avoid duplication. 

It allows the flexibility on where and how to display the featured image of an article together with its summary in a template page. For example, the article metadata can be displayed in thumbnail format, in which there is a short summary and an image. The layout of the summary and the image can be varied for aesthetical purpose. It doesn't have to depend on article's content format. 

Installation
------------

This plugin requires BeautifulSoup. 

	pip install beautifulsoup4

To enable, add the following to your settings.py:

    PLUGIN_PATH = 'path/to/pelican-plugins'
    PLUGINS = ["representative_image"]

`PLUGIN_PATH` can be a path relative to your settings file or an absolute path.

Usage
-----

To include a representative image add the following to the template
	
    {% if  article.featured_image %}
        <img src="{{ article.featured_image }}">
    {% endif %}
