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

    PLUGIN_PATHS = ['path/to/pelican-plugins']
    PLUGINS = ['assets', 'sitemap', 'gravatar']

``PLUGIN_PATH`` can be a path relative to your settings file or an absolute path.

Alternatively, if plugins are in an importable path, you can omit ``PLUGIN_PATH``
and list them::

    PLUGINS = ['assets', 'sitemap', 'gravatar']

or you can ``import`` the plugin directly and give that::

    import my_plugin
    PLUGINS = [my_plugin, 'assets']

Plugin descriptions
===================

========================  ===========================================================
Plugin                    Description
========================  ===========================================================
AsciiDoc reader           Use AsciiDoc to write your posts.

Asset management          Use the Webassets module to manage assets such as CSS and JS files.
                    
Better code samples       Wraps all `table` blocks with a class attribute `.codehilitetable` in an additional `div` of class `.hilitewrapper`. It thus permits to style codeblocks better, especially to make them scrollable.
                    
Better figures/samples    Adds a `style="width: ???px; height: auto;"` attribute to any `<img>` tags in the content
           
CJK auto spacing          Inserts spaces between Chinese/Japanese/Korean characters and English words
                
Clean summary             Cleans your summary of excess images

Code include              Includes Pygments highlighted code in reStructuredText

Collate content           Makes categories of content available to the template as lists through a `collations` attribute 

Creole reader             Allows you to write your posts using the wikicreole syntax

Custom article URLs       Adds support for defining different default URLs for different categories

Disqus static comments    Adds a disqus_comments property to all articles. Comments are fetched at generation time using disqus API

Extract table of content  Extracts table of contents (ToC) from `article.content`

Feed Summary              Allows article summaries to be used in ATOM and RSS feeds instead of the entire article

Filetime from git         Uses git commit to determine page date

Gallery                   Allows an article to contain an album of pictures

GitHub activity           On the template side, you just have to iterate over the ``github_activity`` variable

Global license            Allows you to define a ``LICENSE`` setting and adds the contents of that license variable to the article's context

Goodreads activity        Lists books from your Goodreads shelves

GooglePlus comments       Adds GooglePlus comments to Pelican

Gravatar                  Assigns the ``author_gravatar`` variable to the Gravatar URL and makes the variable available within the article's context

Gzip cache                Enables certain web servers (e.g., Nginx) to use a static cache of gzip-compressed files to prevent the server from compressing files during an HTTP call

HTML entities             Allows you to enter HTML entities such as &copy;, &lt;, &#149; inline in a RST document

HTML tags for rST         Allows you to use HTML tags from within reST documents

I18N Sub-sites            Extends the translations functionality by creating internationalized sub-sites for the default site

ical                      Looks for and parses an ``.ics`` file if it is defined in a given page's ``calendar`` metadata.

Interlinks                Lets you add frequently used URLs to your markup using short keywords

Liquid-style tags         Allows liquid-style tags to be inserted into markdown within Pelican documents

Multi parts posts         Allows you to write multi-part posts

Neighbor articles         Adds ``next_article`` (newer) and ``prev_article`` (older) variables to the article's context

Optimize images           Applies lossless compression on JPEG and PNG images

PDF generator             Automatically exports RST articles and pages as PDF files

Pelican-flickr            Brings your Flickr photos & sets into your static website

Pelican Gist tag          Easily embed GitHub Gists in your Pelican articles

Pelican comment system    Allows you to add static comments to your articles

Pelican Vimeo             Enables you to embed Vimeo videos in your pages and articles

Pelican YouTube           Enables you to embed YouTube videos in your pages and articles

pelicanfly                Lets you type things like `i ♥ :fa-coffee:` in your Markdown documents and have it come out as little Font Awesome icons in the browser

Pin to top                Pin Pelican's article(s) to top "Sticky article"

PlantUML                  Allows you to define UML diagrams directly into rst documents using the great PlantUML tool

Post statistics           Calculates various statistics about a post and store them in an article.stats dictionary

Random article            Generates a html file which redirect to a random article

Read More link            Inserts an inline "read more" or "continue" link into the last html element of the object summary

Related posts             Adds the ``related_posts`` variable to the article's context

Math Render               Gives pelican the ability to render mathematics

Representative image      Extracts a representative image (i.e, featured image) from the article's summary or content

Share post                Creates share URLs of article

Simple footnotes          Adds footnotes to blog posts

Sitemap                   Generates plain-text or XML sitemaps

Static comments           Allows you to add static comments to an article

Subcategory               Adds support for subcategories

Summary                   Allows easy, variable length summaries directly embedded into the body of your articles

Thumbnailer               Creates thumbnails for all of the images found under a specific directory

Tipue Search              Serializes generated HTML to JSON that can be used by jQuery plugin - Tipue Search

Touch                     Does a touch on your generated files using the date metadata from the content

Twitter Bootstrap         Defines some rst directive that enable a clean usage of the twitter bootstrap CSS and Javascript components

W3C validate              Submits generated HTML content to the W3C Markup Validation Service
========================  ===========================================================


Please refer to the ``Readme`` file in a plugin's folder for detailed information about 
that plugin.

Contributing a plugin
=====================

Please refer to the `Contributing`_ file.

.. _Contributing: Contributing.rst
