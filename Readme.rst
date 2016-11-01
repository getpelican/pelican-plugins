Pelican Plugins
###############

Beginning with version 3.0, Pelican supports plugins. Plugins are a way to add
features to Pelican without having to directly modify the Pelican core. Starting
with 3.2, all plugins (including the ones previously in the core) have been
moved to this repository, so this is the central place for all plugins.

How to use plugins
==================

The easiest way to install and use these plugins is to clone this repo::

    git clone --recursive https://github.com/getpelican/pelican-plugins

and activate the ones you want in your settings file::

    PLUGIN_PATHS = ['path/to/pelican-plugins']
    PLUGINS = ['assets', 'sitemap', 'gravatar']

``PLUGIN_PATHS`` can be a path relative to your settings file or an absolute path.

Alternatively, if plugins are in an importable path, you can omit ``PLUGIN_PATHS``
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
Ace Editor                Replace default **<code>** by an Ace__ code editor with settings configure on pelicanconf.py.

Always modified           Copy created date metadata into modified date for easy "latest updates" indexes

AsciiDoc reader           Use AsciiDoc to write your posts.

Asset management          Use the Webassets module to manage assets such as CSS and JS files.

Auto Pages                Generate custom content for generated Author, Category, and Tag pages (e.g. author biography)

Backref Translate         Add a new attribute (``is_translation_of``) to every article/page (which is a translation) pointing back to the original article/page which is being translated

Better code line numbers  Allow code blocks with line numbers to wrap

Better code samples       Wraps ``table`` blocks with ``div > .hilitewrapper > .codehilitetable`` class attribute, allowing for scrollable code blocks.

Better figures/samples    Adds a ``style="width: ???px; height: auto;"`` attribute to any ``<img>`` tags in the content

bootstrap-rst             Provides most (though not all) of Bootstrap's features as rst directives

bootstrapify              Automatically add bootstraps default classes to your content

Category Order            Order categories (and tags) by the number of articles in that category (or tag).

CJK auto spacing          Inserts spaces between Chinese/Japanese/Korean characters and English words

Clean summary             Cleans your summary of excess images

Code include              Includes Pygments highlighted code in reStructuredText

Collate content           Makes categories of content available to the template as lists through a ``collations`` attribute

Creole reader             Allows you to write your posts using the wikicreole syntax

Custom article URLs       Adds support for defining different default URLs for different categories

Dateish                   Treat arbitrary metadata fields as datetime objects

Dead Links                Manage dead links (website not available, errors such as 403, 404)

Disqus static comments    Adds a disqus_comments property to all articles. Comments are fetched at generation time using disqus API

Encrypt content           Password protect pages and articles

Events                    Add event start, duration, and location info to post metadata to generate an iCalendar file

Extract table of content  Extracts table of contents (ToC) from ``article.content``

Feed Summary              Allows article summaries to be used in ATOM and RSS feeds instead of the entire article

Figure References         Provides a system to number and references figures

Filetime from Git         Uses Git commit to determine page date

Filetime from Hg          Uses Mercurial commit to determine page date

Footer Insert             Add standardized footer (e.g., author information) at end of every article

GA Page View              Display Google Analytics page views on individual articles and pages

Gallery                   Allows an article to contain an album of pictures

Gist directive            This plugin adds a ``gist`` reStructuredText directive.

GitHub activity           On the template side, you just have to iterate over the ``github_activity`` variable

Global license            Allows you to define a ``LICENSE`` setting and adds the contents of that license variable to the article's context

Glossary                  Adds a variable containing definitions extracted from definition lists in articles and pages. This variable is visible to all page templates.

Goodreads activity        Lists books from your Goodreads shelves

GooglePlus comments       Adds GooglePlus comments to Pelican

Gravatar                  Assigns the ``author_gravatar`` variable to the Gravatar URL and makes the variable available within the article's context

Gzip cache                Enables certain web servers (e.g., Nginx) to use a static cache of gzip-compressed files to prevent the server from compressing files during an HTTP call

Headerid                  This plugin adds an anchor to each heading so you can deeplink to headers in reStructuredText articles.

HTML entities             Allows you to enter HTML entities such as &copy;, &lt;, &#149; inline in a RST document

HTML tags for rST         Allows you to use HTML tags from within reST documents

I18N Sub-sites            Extends the translations functionality by creating internationalized sub-sites for the default site

ical                      Looks for and parses an ``.ics`` file if it is defined in a given page's ``calendar`` metadata.

Image Process             Automates the processing of images based on their class attributes

Interlinks                Lets you add frequently used URLs to your markup using short keywords

Jinja2 Content            Allows the use of Jinja2 template code in articles, including ``include`` and ``import`` statements. Replacement for pelican-jinja2content.

Just table                Easily create tables in articles

Libravatar                Allows inclusion of user profile pictures from libravatar.org

Link Class                Allows the insertion of class attributes into generated <a> elements (Markdown only)

Linker                    Allows the definition of custom linker commands in analogy to the builtin ``{filename}``, ``{attach}``, ``{category}``, ``{tag}``, ``{author}``, and ``{index}`` syntax

Liquid-style tags         Allows liquid-style tags to be inserted into markdown within Pelican documents

Load CSV                  Adds ``csv`` Jinja tag to display the contents of a CSV file as an HTML table

Markdown Inline Extend    Enables you to add customize inline patterns to your markdown

Markdown-metaYAML         Pelican reader to enable YAML-style metadata in markdown articles

Math Render               Gives pelican the ability to render mathematics

Mbox Reader               Generate articles automatically via email, given a path to a Unix mbox

Multi parts posts         Allows you to write multi-part posts

Neighbor articles         Adds ``next_article`` (newer) and ``prev_article`` (older) variables to the article's context

Open graph                Generates Open Graph tags for your articles

Optimize images           Applies lossless compression on JPEG and PNG images

Org Reader                Create posts via Emacs Orgmode files

Page View                 Pull page view count from Google Analytics.

Panorama                  Creates charts from posts metadata

PDF generator             Automatically exports articles and pages as PDF files

PDF Images                If an img tag contains a PDF, EPS or PS file as a source, this plugin generates a PNG preview which will then act as a link to the original file.

Pelican Cite              Produces inline citations and a bibliography in articles and pages, using a BibTeX file.

Pelican Comment System    Allows you to add static comments to your articles

Pelican-flickr            Brings your Flickr photos & sets into your static website

Pelican Genealogy         Add surnames and people so metadata and context can be accessed from within a theme to provide surname and person pages

Pelican Gist tag          Easily embed GitHub Gists in your Pelican articles

Pelican Github Projects   Embed a list of your public GitHub projects in your pages

pelican_javascript        Allows you to embed Javascript and CSS files into individual articles

Pelican Jinja2Content     Allows the use of Jinja2 template code in articles, including ``include`` and ``import`` statements

Pelican Link Class        Set class attribute of ``<a>`` elements according to whether the link is external or internal

Pelican Page Hierarchy    Creates a URL hierarchy for pages that matches the filesystem hierarchy of their sources

Pelican Page Order        Adds a ``page_order`` attribute to all pages if one is not defined.

Pelican Themes Generator  Generates theme screenshots from the Pelican Themes repository

pelican-toc               Generates a Table of Contents and make it available to the theme via article.toc

Pelican Vimeo             Enables you to embed Vimeo videos in your pages and articles

Pelican YouTube           Enables you to embed YouTube videos in your pages and articles

pelicanfly                Lets you type things like ``i ♥ :fa-coffee:`` in your Markdown documents and have it come out as little Font Awesome icons in the browser

Photos                    Add a photo or a gallery of photos to an article, or include photos in the body text. Resize photos as needed.

permalink                 Enables a kind of permalink using html redirects.

Pin to top                Pin Pelican's article(s) to top "Sticky article"

PlantUML                  Allows you to define UML diagrams directly into rst documents using the great PlantUML tool

Post Revision             Extract article and page revision information from Git commit history

Post statistics           Calculates various statistics about a post and store them in an article.stats dictionary

Random article            Generates a html file which redirect to a random article

Read More link            Inserts an inline "read more" or "continue" link into the last html element of the object summary

Related posts             Adds the ``related_posts`` variable to the article's context

Render Math               Render mathematics in content via the MathJax Javascript engine

Replacer                  Replace a text of a generated HTML

Representative image      Extracts a representative image (i.e, featured image) from the article's summary or content

RMD Reader                Create posts via knitr RMarkdown files

Section number            Adds section numbers for article headers, in the form of ``2.3.3``

Series                    Groups related articles into a series

Share post                Creates share URLs of article

Show Source               Place a link to the source text of your posts.

Simple footnotes          Adds footnotes to blog posts

Sitemap                   Generates plain-text or XML sitemaps

Slim                      Render theme template files via Plim, a Python port of Slim, instead of Jinja

Static comments           Allows you to add static comments to an article

Subcategory               Adds support for subcategories

Sub parts                 Break a very long article in parts, without polluting the timeline with lots of small articles.

Summary                   Allows easy, variable length summaries directly embedded into the body of your articles

tag_cloud                 Provides a tag_cloud

Textile Reader            Adds support for Textile markup

Thumbnailer               Creates thumbnails for all of the images found under a specific directory

Tipue Search              Serializes generated HTML to JSON that can be used by jQuery plugin - Tipue Search

Touch                     Does a touch on your generated files using the date metadata from the content

Twitter Bootstrap         Defines some rst directive that enable a clean usage of the twitter bootstrap CSS and Javascript components

txt2tags_reader           Reader that renders txt2tags markup in content

Video Privacy Enhancer    Increases user privacy by stopping YouTube, Google, et al from placing cookies via embedded video

W3C validate              Submits generated HTML content to the W3C Markup Validation Service

Yuicompressor             Minify CSS and JS files on building step
========================  ===========================================================

__ https://ace.c9.io

Please refer to the ``Readme`` file in a plugin's folder for detailed information about
that plugin.

Contributing a plugin
=====================

Please refer to the `Contributing`_ file.

.. _Contributing: Contributing.rst
