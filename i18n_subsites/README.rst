======================
 i18n subsites plugin
======================

This plugin extends the translations functionality by creating i8n-ized sub-sites for the default site.
It is therefore redundant with the *\*_LANG_{SAVE_AS,URL}* variables, so it disables them to prevent conflicts.

What it does
============
1. The *\*_LANG_URL* and *\*_LANG_SAVE_AS* variables are set to their normal counterparts (e.g. *ARTICLE_URL*) so they don't conflict with this scheme.
2. While building the site for *DEFAULT_LANG* the translations of pages and articles are not generated, but their relations to the original content is kept via links to them.
3. For each non-default language a "sub-site" with a modified config [#conf]_ is created [#run]_, linking the translations to the originals (if available). The configured language code is appended to the *OUTPUT_PATH* and *SITEURL* of each sub-site.

If *HIDE_UNTRANSLATED_CONTENT* is True (default), content without a translation for a language is generated as hidden (for pages) or draft (for articles) for the corresponding language sub-site.

.. [#conf] for each language a config override is given in the *I18N_SUBSITES* dictionary
.. [#run] using a new *PELICAN_CLASS* instance and its ``run`` method, so each subsite could even have a different *PELICAN_CLASS* if specified in *I18N_SUBSITES* conf overrides.

Setting it up
=============

For each extra used language code a language specific variables overrides dictionary must be given (but can be empty) in the *I18N_SUBSITES* dictionary::

    PLUGINS = ['i18n_subsites', ...]

    # mapping: language_code -> conf_overrides_dict
    I18N_SUBSITES = {
        'cz': {
	    'SITENAME': 'Hezkej blog',
	    }
	}

- The language code is the language identifier used in the *lang* metadata. It is appended to *OUTPUT_PATH* and *SITEURL* of each i18n sub-site.
- The i18n-ized config overrides dictionary may specify configuration variable overrides, e.g. a different *LOCALE*, *SITENAME*, *TIMEZONE*, etc. 
  However, it **must not** override *OUTPUT_PATH* and *SITEURL* as they are modified automatically by appending the language code.

Localizing templates
--------------------

Most importantly, this plugin can use localized templates for each sub-site. There are two approaches to having the templates localized:

- You can set a different *THEME* override for each language in *I18N_SUBSITES*, e.g. by making a copy of a theme ``my_theme`` to ``my_theme_lang`` and then editing the templates in the new localized theme. This approach means you don't have to deal with gettext ``*.po`` files, but it is harder to maintain over time.
- You use only one theme and localize the templates using the `jinja2.ext.i18n Jinja2 extension <http://jinja.pocoo.org/docs/templates/#i18n>`_. For a kickstart read this `howto <./localizing_using_jinja2.rst>`_.

It is convenient to add language buttons to your theme in addition to the translations links. These buttons could point to e.g. the *SITEURL* of each (sub-)site. For this reason the plugin adds these variables to the template context:

extra_siteurls
  A dictionary mapping languages to their *SITEURL*. The *DEFAULT_LANG* language of the current sub-site is not included, so this dictionary serves as a complement to current *DEFAULT_LANG* and *SITEURL*. This dictionary is useful for implementing global language buttons.
main_lang
  The language of the top-level site - the original *DEFAULT_LANG*
main_siteurl
  The *SITEURL* of the top-level site - the original *SITEURL*

Usage notes
===========
- It is **mandatory** to specify *lang* metadata for each article and page as *DEFAULT_LANG* is later changed for each sub-site.
- As with the original translations functionality, *slug* metadata is used to group translations. It is therefore often
  convenient to compensate for this by overriding the content url (which defaults to slug) using the *url* and *save_as* metadata.

Future plans
============

- add a testsuite

Development
===========
- Please file issues, pull requests at https://github.com/smartass101/pelican-plugins
- Main-line development happens in the ``i18n_subsites_plugin`` branch, squashed commits are then merged into the ``master`` branch for PRs to the pelican plugin repository.
- A demo and test site is in the ``gh-pages`` branch and can be seen at http://smartass101.github.io/pelican-plugins/

..  LocalWords:  lang metadata
