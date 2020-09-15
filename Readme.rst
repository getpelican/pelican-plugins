Pelican Plugins
###############

**Important note:** We are in the process of migrating plugins from this monolithic repository to their own individual repositories under the new `Pelican Plugins`_ organization, a place for plugin authors to collaborate more broadly with Pelican maintainers and other members of the community. The intention is for all the plugins under the new organization to be in the new “namespace plugin” format, which means these plugins can easily be Pip-installed and recognized immediately by Pelican 4.5+ — without having to explicitly enable them.

This transition process will take some time, so we appreciate your patience in the interim. If you would like to help speed up this transition, the following would be very helpful:

* **If you find a plugin here that has not yet been migrated to the new organization**, create a new issue under this repository and communicate which plugin you would like to help migrate, after which a Pelican maintainer will guide you through the process.

* **If you have come here to submit a pull request to add your plugin**, please consider instead moving your plugin under the `Pelican Plugins`_ organization. To get started, create a new issue under this repository with the details of your plugin, after which a Pelican maintainer will guide you through the process.

Whether you are creating a new plugin or migrating an existing plugin, please use the provided `Cookiecutter template <https://github.com/getpelican/cookiecutter-pelican-plugin>`_ to generate a scaffolded namespace plugin that conforms to community conventions. Have a look at the `Simple Footnotes <https://github.com/pelican-plugins/simple-footnotes>`_ repository to see an example of a migrated plugin.

The rest of the information below is relevant for legacy plugins but not for the new namespace plugins found at the `Pelican Plugins`_ organization.

.. _Pelican Plugins: https://github.com/pelican-plugins

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

Migration status:

* (blank): Local hosted plugin is still waiting for migration work.
* ⚠️ : Deprecated. Can be safely removed from this repository.
* ❓: Externally maintained plugins that do not need explicit migration from the mono-repo. Migration work need to happen in the original owners' repo.
* ✔ : Repository has been migrated to `Pelican Plugins`_ organization.

================================================================  ========================================================================  ===========================================================
Plugin                                                            ℹ️                                                                         Description
================================================================  ========================================================================  ===========================================================
Ace Editor                                                        `❓ <https://github.com/mothsART/ace_editor>`_                            Replace default **<code>** by an Ace__ code editor with settings configure on pelicanconf.py.

`Always modified <./always_modified>`_                                                                                                      Copy created date metadata into modified date for easy "latest updates" indexes

`AsciiDoc reader <./asciidoc_reader>`_                                                                                                      Use AsciiDoc to write your posts.

`Asset management <./assets>`_                                                                                                              Use the Webassets module to manage assets such as CSS and JS files.

`Author images <./author_images>`_                                                                                                          Adds support for author images and avatars.

`Auto Pages <./autopages>`_                                                                                                                 Generate custom content for generated Author, Category, and Tag pages (e.g. author biography)

Backref Translate                                                 `❓ <https://github.com/daltonmatos/pelican-plugin-backref-translate>`_   Add a new attribute (``is_translation_of``) to every article/page (which is a translation) pointing back to the original article/page which is being translated

Better code samples                                               `❓ <https://github.com/classner/better_code_samples>`_                   Wraps ``table`` blocks with ``div > .hilitewrapper > .codehilitetable`` class attribute, allowing for scrollable code blocks.

`Better code line numbers <./better_codeblock_line_numbering>`_                                                                             Allow code blocks with line numbers to wrap

`Better figures/samples <./better_figures_and_images>`_                                                                                     Adds a ``style="width: ???px; height: auto;"`` attribute to any ``<img>`` tags in the content

`Better tables <./better_tables>`_                                                                                                          Removes the excess attributes and elements in the HTML tables generated from reST.

`bootstrap-rst <./bootstrap-rst>`_                                                                                                          Provides most (though not all) of Bootstrap's features as rst directives

bootstrapify                                                      `❓ <https://github.com/ingwinlu/pelican-bootstrapify>`_                  Automatically add bootstraps default classes to your content

`Category meta <./category_meta>`_                                                                                                          Read metadata for each category from an index file in that category's directory.

Category Order                                                    `❓ <https://github.com/jhshi/pelican.plugins.category_order>`_           Order categories (and tags) by the number of articles in that category (or tag).

CJK auto spacing                                                  `❓ <https://github.com/yuex/cjk-auto-spacing>`_                          Inserts spaces between Chinese/Japanese/Korean characters and English words

`Clean summary <./clean_summary>`_                                                                                                          Cleans your summary of excess images

`Code include <./code_include>`_                                                                                                            Includes Pygments highlighted code in reStructuredText

`Collate content <./collate_content>`_                                                                                                      Makes categories of content available to the template as lists through a ``collations`` attribute

`Creole reader <./creole_reader>`_                                                                                                          Allows you to write your posts using the wikicreole syntax

`CSS HTML JS Minify <./css-html-js-minify>`_                                                                                                Minifies all CSS, HTML and JavaScript files in the output path after site generation.

`CTags generator <./ctags_generator>`_                                                                                                      Generates a "tags" file following the CTags in the "content/" directory, to provide autocompletion for code editors that support it.

`Custom article URLs <./custom_article_urls>`_                                                                                              Adds support for defining different default URLs for different categories

`Dateish <./dateish>`_                                                                                                                      Treat arbitrary metadata fields as datetime objects

Dead Links                                                        `❓ <https://github.com/silentlamb/pelican-deadlinks>`_                   Manage dead links (website not available, errors such as 403, 404)

`Disqus static comments <./disqus_static>`_                                                                                                 Adds a disqus_comments property to all articles. Comments are fetched at generation time using disqus API

Encrypt content                                                   `❓ <https://github.com/mindcruzer/pelican-encrypt-content>`_             Password protect pages and articles

`Events <./events>`_                                                                                                                        Add event start, duration, and location info to post metadata to generate an iCalendar file

`Extract table of content <./extract_toc>`_                                                                                                 Extracts table of contents (ToC) from ``article.content``

`Feed summary <./feed_summary>`_                                  ⚠️                                                                         Allows article summaries to be used in ATOM and RSS feeds instead of the entire article.

Figure References                                                 `❓ <https://github.com/cmacmackin/figure-ref>`_                          Provides a system to number and references figures

`Filetime from Git <./filetime_from_git>`_                                                                                                  Uses Git commit to determine page date

`Filetime from Hg <./filetime_from_hg>`_                                                                                                    Uses Mercurial commit to determine page date

`Footer Insert <./footer_insert>`_                                                                                                          Add standardized footer (e.g., author information) at end of every article

GA Page View                                                      `❓ <https://github.com/jhshi/pelican.plugins.ga_page_view>`_             Display Google Analytics page views on individual articles and pages

`Gallery <./gallery>`_                                                                                                                      Allows an article to contain an album of pictures

`Gist directive <./gist_directive>`_                                                                                                        This plugin adds a ``gist`` reStructuredText directive.

`GitHub wiki <./github-wiki>`_                                                                                                              Converts a flat github wiki into a structured read only wiki on your site

`GitHub activity <./github_activity>`_                                                                                                      On the template side, you just have to iterate over the ``github_activity`` variable

`Global license <./global_license>`_                                                                                                        Allows you to define a ``LICENSE`` setting and adds the contents of that license variable to the article's context

`Glossary <./glossary>`_                                                                                                                    Adds a variable containing definitions extracted from definition lists in articles and pages. This variable is visible to all page templates.

`Goodreads activity <./goodreads_activity>`_                                                                                                Lists books from your Goodreads shelves

`GooglePlus comments <./googleplus_comments>`_                                                                                              Adds GooglePlus comments to Pelican

`Gravatar <./gravatar>`_                                                                                                                    Assigns the ``author_gravatar`` variable to the Gravatar URL and makes the variable available within the article's context

`Gzip cache <./gzip_cache>`_                                                                                                                Enables certain web servers (e.g., Nginx) to use a static cache of gzip-compressed files to prevent the server from compressing files during an HTTP call

`Headerid <./headerid>`_                                                                                                                    This plugin adds an anchor to each heading so you can deeplink to headers in reStructuredText articles.

`HTML entities <./html_entity>`_                                                                                                            Allows you to enter HTML entities such as &copy;, &lt;, &#149; inline in a RST document

`HTML tags for rST <./html_rst_directive>`_                                                                                                 Allows you to use HTML tags from within reST documents

`I18N Sub-sites <./i18n_subsites>`_                                                                                                         Extends the translations functionality by creating internationalized sub-sites for the default site

`ical <./ical>`_                                                                                                                            Looks for and parses an ``.ics`` file if it is defined in a given page's ``calendar`` metadata.

Image Process                                                     `❓ <https://github.com/whiskyechobravo/image_process>`_                  Automates the processing of images based on their class attributes

`Interlinks <./interlinks>`_                                                                                                                Lets you add frequently used URLs to your markup using short keywords

Jinja2 Content                                                    `✔  <https://github.com/pelican-plugins/jinja2content>`_                  Allows the use of Jinja2 template code in articles, including ``include`` and ``import`` statements. Replacement for pelican-jinja2content.

`JPEG Reader <./jpeg_reader>`_                                                                                                              Create image gallery pages based on content of JPEG metadata

Just table                                                        `❓ <https://github.com/burakkose/just_table>`_                           Allows you to easily create and manage tables. You can embed the tables into posts with a simple way.

`Libravatar <./libravatar>`_                                                                                                                Allows inclusion of user profile pictures from libravatar.org

Lightbox                                                          `❓ <https://github.com/kura/lightbox>`_                                  A pure CSS lightbox for Pelican.

`Linker <./linker>`_                                                                                                                        Allows the definition of custom linker commands in analogy to the builtin ``{filename}``, ``{attach}``, ``{category}``, ``{tag}``, ``{author}``, and ``{index}`` syntax

`Liquid-style tags <./liquid_tags>`_                                                                                                        Allows liquid-style tags to be inserted into markdown within Pelican documents

Load CSV                                                          `❓ <https://github.com/e9t/pelican-loadcsv>`_                            Adds ``csv`` Jinja tag to display the contents of a CSV file as an HTML table

Markdown-metaYAML                                                 `❓ <https://github.com/joachimneu/pelican-md-metayaml>`_                 Pelican reader to enable YAML-style metadata in markdown articles

`Markdown Inline Extension <./md_inline_extension>`_                                                                                        Enables you to add customize inline patterns to your markdown

`Members <./members>`_                                                                                                                      Looks for a members metadata header containing key/value pairs and makes them available for use in templates.

More Categories                                                   `✔  <https://github.com/pelican-plugins/more-categories>`_                Multiple categories per article; nested categories (`foo/bar, foo/baz`)

Multi Neighbors                                                   `❓ <https://github.com/davidlesieur/multi_neighbors>`_                   Adds a list of newer articles and a list of older articles to every article's context.

`Multi parts posts <./multi_part>`_                               ⚠️                                                                         Allows you to write multi-part posts

MultiMarkdown reader                                              `❓ <https://github.com/dames57/multimarkdown_reader>`_                   A MultiMarkdown reader.

Neighbor articles                                                 `✔  <https://github.com/pelican-plugins/neighbors>`_                      Adds ``next_article`` (newer) and ``prev_article`` (older) variables to the article's context

`Optimize images <./optimize_images>`_                                                                                                      Applies lossless compression on JPEG and PNG images

Pandoc Org Reader                                                 `❓ <https://github.com/jo-tham/org_pandoc_reader>`_

`Python Org Reader <./org_python_reader>`_

`Org Reader <./org_reader>`_                                                                                                                Create posts via Emacs Orgmode files

Pandoc reader                                                     `❓ <https://github.com/liob/pandoc_reader>`_

Panorama                                                          `❓ <https://github.com/romainx/panorama>`_                               Creates charts from posts metadata

PDF Images                                                        `❓ <https://github.com/cmacmackin/pdf-img>`_                             If an img tag contains a PDF, EPS or PS file as a source, this plugin generates a PNG preview which will then act as a link to the original file.

`PDF generator <./pdf>`_                                                                                                                    Automatically exports articles and pages as PDF files

Pelican Cite                                                      `❓ <https://github.com/cmacmackin/pelican-cite>`_                        Produces inline citations and a bibliography in articles and pages, using a BibTeX file.

pelican-ert                                                       `❓ <https://github.com/nogaems/pelican-ert>`_                            Allows you to add estimated reading time of an article

Pelican-flickr                                                    `❓ <https://github.com/La0/pelican-flickr>`_                             Brings your Flickr photos & sets into your static website

Pelican Genealogy                                                 `❓ <https://github.com/zappala/pelican-genealogy>`_                      Add surnames and people so metadata and context can be accessed from within a theme to provide surname and person pages

Pelican Gist tag                                                  `❓ <https://github.com/streeter/pelican-gist>`_                          Easily embed GitHub Gists in your Pelican articles

Pelican Github Projects                                           `❓ <https://github.com/kura/pelican-githubprojects>`_                    Embed a list of your public GitHub projects in your pages

Jupyter Notebooks                                                 `❓ <https://github.com/danielfrg/pelican-jupyter>`_                      Provides two modes to use Jupyter notebooks in Pelican.

Pelican Jinja2Content                                             `⚠️  <https://github.com/joachimneu/pelican-jinja2content>`_               Allows the use of Jinja2 template code in articles, including ``include`` and ``import`` statements

Lang Category                                                     `❓ <https://github.com/CNBorn/pelican-langcategory>`_                    Make languages behave the same as categories (visitor can browse articles in certain language).

Pelican Link Class                                                `❓ <https://github.com/rlaboiss/pelican-linkclass>`_                     Set class attribute of ``<a>`` elements according to whether the link is external or internal

Pelican Mbox Reader                                               `❓ <https://github.com/TC01/pelican-mboxreader>`_                        Generate articles automatically via email, given a path to a Unix mbox

Pelican Open graph                                                `❓ <https://github.com/whiskyechobravo/pelican-open_graph>`_             Generates Open Graph tags for your articles

Pelican Page Hierarchy                                            `❓ <https://github.com/akhayyat/pelican-page-hierarchy>`_                Creates a URL hierarchy for pages that matches the filesystem hierarchy of their sources

Pelican Page Order                                                `❓ <https://github.com/akhayyat/pelican-page-order>`_                    Adds a ``page_order`` attribute to all pages if one is not defined.

`pelican-rdf <./pelican-rdf>`_                                                                                                              Allows the processing of .rdf vocabularies, and the generation of a lightweight documentation.

pelican-toc                                                       `❓ <https://github.com/ingwinlu/pelican-toc>`_                           Generates a Table of Contents and make it available to the theme via article.toc

Version Generator                                                 `❓ <https://github.com/Shaked/pelican-version>`_                         A simple version generator which generates an incremented version file.

`Pelican Comment System <./pelican_comment_system>`_                                                                                        Allows you to add static comments to your articles

pelican_javascript                                                `❓ <https://github.com/mortada/pelican_javascript>`_                     Allows you to embed Javascript and CSS files into individual articles

Pelican Meetup Info                                               `❓ <https://github.com/tylerdave/pelican-meetup-info>`_                  Include your Meetup.com group and event information on generated pages and articles

`Unity WebGL <./pelican_unity_webgl>`_                                                                                                      Easily embed Unity3d games into posts and pages

Pelican Vimeo                                                     `❓ <https://github.com/kura/pelican_vimeo>`_                             Enables you to embed Vimeo videos in your pages and articles

Pelican YouTube                                                   `❓ <https://github.com/kura/pelican_youtube>`_                           Enables you to embed YouTube videos in your pages and articles

pelicanfly                                                        `❓ <https://github.com/bmcorser/pelicanfly>`_                            Lets you type things like ``i ♥ :fa-coffee:`` in your Markdown documents and have it come out as little Font Awesome icons in the browser

Pelican Themes Generator                                          `❓ <https://github.com/badele/pelicanthemes-generator>`_                 Generates theme screenshots from the Pelican Themes repository

`permalink <./permalinks>`_                                                                                                                 Enables a kind of permalink using html redirects.

`Photos <./photos>`_                                                                                                                        Add a photo or a gallery of photos to an article, or include photos in the body text. Resize photos as needed.

Pin to top                                                        `❓ <https://github.com/Shaked/pin_to_top>`_                              Pin Pelican's article(s) to top "Sticky article"

`PlantUML <./plantuml>`_                                                                                                                    Allows you to define UML diagrams directly into rst documents using the great PlantUML tool

Post Revision                                                     `❓ <https://github.com/jhshi/pelican.plugins.post_revision>`_            Extract article and page revision information from Git commit history

`Post statistics <./post_stats>`_                                                                                                           Calculates various statistics about a post and store them in an article.stats dictionary

`Random article <./random_article>`_                                                                                                        Generates a html file which redirect to a random article

`Read More link <./read_more_link>`_                                                                                                        Inserts an inline "read more" or "continue" link into the last html element of the object summary

`Readtime <./readtime>`_                                                                                                                    Adds article estimated read time calculator to the site, in the form of '<n> minutes'.

`Reddit poster <./reddit_poster>`_                                                                                                          You can use the 'subreddit' attribute in you articles to specify which subbreddit the article should be post in aside of your default sub.

Related posts                                                     `✔  <https://github.com/pelican-plugins/related-posts>`_                  Adds the ``related_posts`` variable to the article's context

Render Math                                                       `✔  <https://github.com/pelican-plugins/render-math>`_                    Render mathematics in content via the MathJax Javascript engine

Replacer                                                          `❓ <https://github.com/narusemotoki/replacer>`_                          Replace a text of a generated HTML

`Representative image <./representative_image>`_                                                                                            Extracts a representative image (i.e, featured image) from the article's summary or content

`RMD Reader <./rmd_reader>`_                                                                                                                Create posts via knitr RMarkdown files

`Section number <./section_number>`_                                                                                                        Adds section numbers for article headers, in the form of ``2.3.3``

Series                                                            `✔  <https://github.com/pelican-plugins/series>`_                         Groups related articles into a series

`Shaarli poster <./shaarli_poster>`_                                                                                                        Upload newly redacted articles onto a specified `Shaarli <https://github.com/shaarli/Shaarli>`__ instance.

`Share post <./share_post>`_                                                                                                                Creates share URLs of article

`Shortcodes <./shortcodes>`_                                                                                                                Easy and explicit inline jinja2 macros

`Show Source <./show_source>`_                                                                                                              Place a link to the source text of your posts.

Similar Posts                                                     `❓ <https://github.com/davidlesieur/similar_posts>`_                     Adds a list of similar posts to every article's context.

Simple footnotes                                                  `✔  <https://github.com/pelican-plugins/simple-footnotes>`_               Adds footnotes to blog posts

Sitemap                                                           `✔  <https://github.com/pelican-plugins/sitemap>`_                        Generates plain-text or XML sitemaps

`Slim <./slim>`_                                                                                                                            Render theme template files via Plim, a Python port of Slim, instead of Jinja

`Static comments <./static_comments>`_                                                                                                      Allows you to add static comments to an article

`Sub parts <./sub_parts>`_                                                                                                                  Break a very long article in parts, without polluting the timeline with lots of small articles.

`Subcategory <./subcategory>`_                                                                                                              Adds support for subcategories

`Summary <./summary>`_                                                                                                                      Allows easy, variable length summaries directly embedded into the body of your articles

`tag_cloud <./tag_cloud>`_                                                                                                                  Provides a tag_cloud

`Textile Reader <./textile_reader>`_                                                                                                        Adds support for Textile markup

Thumbnailer                                                       `✔  <https://github.com/pelican-plugins/thumbnailer>`_                    Creates thumbnails for all of the images found under a specific directory

`Tipue Search <./tipue_search>`_                                                                                                            Serializes generated HTML to JSON that can be used by jQuery plugin - Tipue Search

`Touch <./touch>`_                                                                                                                          Does a touch on your generated files using the date metadata from the content

`Twitter Bootstrap <./twitter_bootstrap_rst_directives>`_                                                                                   Defines some rst directive that enable a clean usage of the twitter bootstrap CSS and Javascript components

`txt2tags_reader <./txt2tags_reader>`_                                                                                                      Reader that renders txt2tags markup in content

`Video Privacy Enhancer <./video_privacy_enhancer>`_                                                                                        Increases user privacy by stopping YouTube, Google, et al from placing cookies via embedded video

`W3C validate <./w3c_validate>`_                                                                                                            Submits generated HTML content to the W3C Markup Validation Service

Webring                                                           `✔  <https://github.com/pelican-plugins/webring>`_                        Add a webring to your site from a list of web feeds (e.g. RSS/Atom)

`Yuicompressor <./yuicompressor>`_                                                                                                          Minify CSS and JS files on building step
================================================================  ========================================================================  ===========================================================

__ https://ace.c9.io

Please refer to the ``Readme`` file in a plugin's folder for detailed information about
that plugin.

Contributing a plugin
=====================

Please refer to the `Contributing`_ file.

.. _Contributing: Contributing.rst
