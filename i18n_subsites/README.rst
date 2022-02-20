=======================
 I18N Sub-sites Plugin
=======================

This plugin extends the translations functionality by creating
internationalized sub-sites for the default site.

This plugin is designed for Pelican 3.4 and later.

How to install
==============

1. Clone the entire pelican-plugins repository, if you haven't done so already.
2. Add this plugin to the ``PLUGINS`` variable in ``pelicanconf.py``:

   .. code-block:: python

      PLUGIN_PATHS = [..., '/path/to/pelican-plugins']
      PLUGINS = [... , 'i18n_subsites']

How to configure
================

For each sub-site, you can override language specific parameters in the
``I18N_SUBSITES`` dictionary. For example, it allows you to localize
the ``SITENAME`` variable that you use in your template:

.. code-block:: python

    SITENAME = 'Amazing blog'
    I18N_SUBSITES = {
        'cz': {
             'SITENAME': 'Hezkej blog',
        }
    }

How to handle language specific templates
=========================================

You can choose one of these two approaches:

**Create language-specific templates**
  1. Copy the main template directory into its own language specific copy.
     For example copy ``themes/simple`` to ``themes/simple-cz``
  2. Edit ``pelicanconf.py`` as follows:

     .. code-block:: python

        DEFAULT_LANG = 'en'
        SITENAME = 'Beautiful blog'
        THEME = 'themes/simple'
        I18N_SUBSITES = {
            'cz': {
                 'SITENAME': 'Hezkej blog',
                 'THEME': 'themes/simple-cz',
            }
        }
  3. Include language buttons or links in the template so visitors can change
     from one language to the other. This short `howto <./implementing_language_buttons.rst>`_
     shows two example implementations of language buttons.

**Keep a single template and internationalize it**
  If you plan to keep a single template and internationalize it, you must also
  have the following in your pelican configuration. For a kickstart read this
  `guide <./localizing_using_jinja2.rst>`_.

  .. code-block:: python

      JINJA_ENVIRONMENT = {
         'extensions': ['jinja2.ext.i18n'],
     }

How to handle language specific content
=======================================

1. Add a ``lang`` metadata field to each article or page, if you haven't 
   done so already. This will make sure that the content will appear either
   in the main site, or in a particular sub-site. Articles or pages without
   a ``lang`` field will appear in every sub-site.
2. Add an identical ``slug`` metadata field to every translation of an article 
   or page. This will make sure it will contain 
   ``<link rel="alternate" hreflang="..." ... >`` pointing to other
   translations. The actual inclusion of this hreflang alternative link in
   the HTML head section depends on the template so refer to translations.html
   for more details.
3. Add both a language specific ``url`` and ``save_as`` metadata field to the
   translated article or page. See the example below how this works in practice.


Example
-------

Let's create `content/article1.md`, using the previous ``pelicanconf.py`` settings:

.. code-block:: markdown

    Title: Hello world
    Slug: hello-world
    Lang: en
    Date: 2021-05-23T15:04:59+02:00

    # Hello world

    This is the first paragraph of the content in English.

Additionally, let's translate this page into Czech by creating 
``content/article1-cz.md``:

.. code-block:: markdown

    Title: Ahoj svete
    Slug: hello-world
    Save_As: ahoj-svete.html
    Url: ahoj-svete.html
    Lang: cz
    Date: 2021-05-23T15:44:13+02:00

    # Ahoj svete

    Toto je prvni odstavec obsahu v cestine.

If you run Pelican, it will create these 2 files with hreflang tags
that correctly cross-reference each other:

.. code-block::

    output/hello-world.html
    output/cz/ahoj-svete.html

What this plugin does behind the scenes
=======================================

1. When the content of the main site is being generated, the settings
   are saved and the generation stops when content is ready to be
   written. While reading source files and generating content objects,
   the output queue is modified in certain ways:

   * translations that will appear as native in a different (sub-)site
     will be removed
   * untranslated articles will be transformed to drafts if
     ``I18N_UNTRANSLATED_ARTICLES`` is ``'hide'`` (default), removed if
     ``'remove'`` or kept as they are if ``'keep'``.
   * untranslated pages will be transformed into hidden pages if
     ``I18N_UNTRANSLATED_PAGES`` is ``'hide'`` (default), removed if
     ``'remove'`` or kept as they are if ``'keep'``.''
   * additional content manipulation similar to articles and pages can
     be specified for custom generators in the ``I18N_GENERATOR_INFO``
     setting.

2. For each language specified in the ``I18N_SUBSITES`` dictionary the
   settings overrides are applied to the settings from the main site
   and a new sub-site is generated in the same way as with the main
   site until content is ready to be written.
3. When all (sub-)sites are waiting for content writing, all removed
   contents, translations and static files are interlinked across the
   (sub-)sites.
4. Finally, all the output is written.


Default and special overrides
-----------------------------
The settings overrides may contain arbitrary settings, however, there
are some that are handled in a special way:

``SITEURL``
  Any overrides to this setting should ensure that there is some level
  of hierarchy between all (sub-)sites, because Pelican makes all URLs
  relative to ``SITEURL`` and the plugin can only cross-link between
  the sites using this hierarchy. For instance, with the main site
  ``http://example.com`` a sub-site ``http://example.com/de`` will
  work, but ``http://de.example.com`` will not. If not overridden, the
  language code (the language identifier used in the ``lang``
  metadata) is appended to the main ``SITEURL`` for each sub-site.
``OUTPUT_PATH``, ``CACHE_PATH``
  If not overridden, the language code is appended as with ``SITEURL``.
  Separate cache paths are required as parser results depend on the locale.
``STATIC_PATHS``, ``THEME_STATIC_PATHS``
  If not overridden, they are set to ``[]`` and all links to static
  files are cross-linked to the main site.
``THEME``, ``THEME_STATIC_DIR``
  If overridden, the logic with ``THEME_STATIC_PATHS`` does not apply.
``DEFAULT_LANG``
  This should not be overridden as the plugin changes it to the
  language code of each sub-site to change what is perceived as translations.

Localizing templates
--------------------

Most importantly, this plugin can use localized templates for each
sub-site. There are two approaches to having the templates localized:

- You can set a different ``THEME`` override for each language in
  ``I18N_SUBSITES``, e.g. by making a copy of a theme ``my_theme`` to
  ``my_theme_lang`` and then editing the templates in the new
  localized theme. This approach means you don't have to deal with
  gettext ``*.po`` files, but it is harder to maintain over time.
- You use only one theme and localize the templates using the
  `jinja2.ext.i18n Jinja2 extension
  <http://jinja.pocoo.org/docs/templates/#i18n>`_. 

Additional context variables
............................

It may be convenient to add language buttons to your theme in addition
to the translation links of articles and pages. These buttons could,
for example, point to the ``SITEURL`` of each (sub-)site. For this
reason the plugin adds these variables to the template context:

``main_lang``
  The language of the main site — the original ``DEFAULT_LANG``
``main_siteurl``
  The ``SITEURL`` of the main site — the original ``SITEURL``
``lang_siteurls``
  An ordered dictionary, mapping all used languages to their
  ``SITEURL``. The ``main_lang`` is the first key with ``main_siteurl``
  as the value. This dictionary is useful for implementing global
  language buttons that show the language of the currently viewed
  (sub-)site too.
``extra_siteurls``
  An ordered dictionary, subset of ``lang_siteurls``, the current
  ``DEFAULT_LANG`` of the rendered (sub-)site is not included, so for
  each (sub-)site ``set(extra_siteurls) == set(lang_siteurls) -
  set([DEFAULT_LANG])``. This dictionary is useful for implementing
  global language buttons that do not show the current language.
``relpath_to_site``
  A function that returns a relative path from the first (sub-)site to
  the second (sub-)site where the (sub-)sites are identified by the
  language codes given as two arguments.

If you don't like the default ordering of the ordered dictionaries,
use a Jinja2 filter to alter the ordering.

All the siteurls above are always absolute even in the case of
``RELATIVE_URLS == True`` (it would be to complicated to replicate the
Pelican internals for local siteurls), so you may rather use something
like ``{{ SITEURL }}/{{ relpath_to_site(DEFAULT_LANG, main_lang }}``
to link to the main site.

This short `howto <./implementing_language_buttons.rst>`_ shows two
example implementations of language buttons.

Development
===========

- A demo and a test site is in the ``gh-pages`` branch and can be seen
  at http://smartass101.github.io/pelican-plugins/
