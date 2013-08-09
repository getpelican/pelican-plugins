Pelican Plugins
###############

Beginning with version 3.0, Pelican supports plugins. Plugins are a way to add
features to Pelican without having to directly modify the Pelican core. Starting
with 3.2, all plugins (including the ones previously in the core) are 
moved here, so this is the central place for all plugins. 

How to use plugins
==================

Easiest way to install and use these plugins is cloning this repo::

    git clone https://github.com/getpelican/pelican-plugins

and activating the ones you want in your settings file::

    PLUGIN_PATH = 'path/to/pelican-plugins'
    PLUGINS = ['assets', 'sitemap', 'gravatar']

``PLUGIN_PATH`` can be a path relative to your settings file or an absolute path.

Alternatively, if plugins are in an importable path, you can omit ``PLUGIN_PATH``
and list them::

    PLUGINS = ['assets', 'sitemap', 'gravatar']

or you can ``import`` the plugin directly and give that::

    import my_plugin
    PLUGINS = [my_plugin, 'assets']

Please refer to the ``Readme`` file in a plugin's folder for detailed information about 
that plugin.

Contributing a plugin
=====================

Please refer to the `Contributing`_ file.

.. _Contributing: Contributing.rst

Plugin Index
============

Assets
------
This plugin allows you to use the Webassets module to manage assets such as CSS and JS files.

better_figures_and_images
-------------------------
Adds a style="width: ???px; height: auto;" attribute to any <img> tags in the content

code_include
------------
Include Pygments highlighted code with reStructuredText

disqus_static
-------------
This plugin adds a disqus_comments property to all articles.

extract_toc
-----------
A Pelican plugin to extract table of contents (ToC) from `article.content` and place it in its own `article.toc` variable.

github_activity
---------------
Set the `GITHUB_ACTIVITY_FEED` parameter to your GitHub activity feed.

global_licence
--------------
This plugin allows you to define a LICENSE setting and adds the contents of that license variable to the article's context, making that variable available to use from within your theme's templates.

goodreads_activity
------------------
A Pelican plugin to lists books from your Goodreads shelves.

gravatar
--------
This plugin assigns the `author_gravatar` variable to the Gravatar URL and makes the variable available within the article's context.

gzip_cache
----------
Certain web servers (e.g., Nginx) can use a static cache of gzip-compressed files to prevent the server from compressing files during an HTTP call

html_entity
-----------
This plugin allows you to enter HTML entities such as &copy;, &lt;, &#149; inline in a RST document

html_rst_directive
------------------
This plugin allows you to use HTML tags from within reST documents.

ical
----
This plugin looks for and parses an `.ics` file if it is defined in a given page's `calendar` metadata.

latex
-----
This plugin allows you to write mathematical equations in your articles using Latex.

multi_part
----------
The multi-part posts plugin allow you to write multi-part posts.

neighbors
---------
This plugin adds `next_article` (newer) and `prev_article` (older) variables to the article's context

optimize_images
---------------
This plugin applies lossless compression on JPEG and PNG images, with no effect on image quality.

pdf
---
The PDF Generator plugin automatically exports RST articles and pages as PDF files as part of the site-generation process

post_stats
----------
A Pelican plugin to calculate various statistics about a post and store them in an article.stats dictionary

random_article
--------------
This plugin generates a html file which redirect to a random article using javascript's `window.location`. 

related_posts
-------------
This plugin adds the `related_posts` variable to the article's context.

sitemap
-------
The sitemap plugin generates plain-text or XML sitemaps.

summary
-------
This plugin allows easy, variable length summaries directly embedded into the body of your articles.

test_data
---------
Place tests for your plugin here. `test_data` folder contains following common data for your tests, if you need them.

thumbnailer
-----------
This plugin creates thumbnails for all of the images found under a specific directory, in various thumbnail sizes.

w3c_validate
------------
This is a plugin for Pelican that submits generated HTML content to the W3C Markup Validation Service.


