======================
 I18N Sub-sites Plugin
======================

This plugin extends the translations functionality by creating internationalized sub-sites for the default site. It is therefore redundant with the *\*_LANG_{SAVE_AS,URL}* variables, so it disables them to prevent conflicts.

What it does
============
1. The *\*_LANG_URL* and *\*_LANG_SAVE_AS* variables are set to their normal counterparts (e.g. *ARTICLE_URL*) so they don't conflict with this scheme.
2. While building the site for *DEFAULT_LANG* the translations of pages and articles are not generated, but their relations to the original content is kept via links to them.
3. For each non-default language a "sub-site" with a modified config [#conf]_ is created [#run]_, linking the translations to the originals (if available). The configured language code is appended to the *OUTPUT_PATH* and *SITEURL* of each sub-site. For each sub-site, *DEFAULT_LANG* is changed to the language of the sub-site so that articles in a different language are treated as translations.

If *HIDE_UNTRANSLATED_CONTENT* is True (default), content without a translation for a language is generated as hidden (for pages) or draft (for articles) for the corresponding language sub-site.

.. [#conf] For each language a config override is given in the *I18N_SUBSITES* dictionary.
.. [#run] Using a new *PELICAN_CLASS* instance and its ``run`` method, so each sub-site could even have a different *PELICAN_CLASS* if specified in *I18N_SUBSITES* conf overrides.

Setting it up
=============

For each extra used language code, a language-specific variables overrides dictionary must be given (but can be empty) in the *I18N_SUBSITES* dictionary

.. code-block:: python

    PLUGINS = ['i18n_subsites', ...]

    # mapping: language_code -> conf_overrides_dict
    I18N_SUBSITES = {
        'cz': {
	    'SITENAME': 'Hezkej blog',
	    }
	}

- The language code is the language identifier used in the *lang* metadata. It is appended to *OUTPUT_PATH* and *SITEURL* of each I18N sub-site.
- The internationalized config overrides dictionary may specify configuration variable overrides — e.g. a different *LOCALE*, *SITENAME*, *TIMEZONE*, etc. However, it **must not** override *OUTPUT_PATH* and *SITEURL* as they are modified automatically by appending the language code.

Localizing templates
--------------------

Most importantly, this plugin can use localized templates for each sub-site. There are two approaches to having the templates localized:

- You can set a different *THEME* override for each language in *I18N_SUBSITES*, e.g. by making a copy of a theme ``my_theme`` to ``my_theme_lang`` and then editing the templates in the new localized theme. This approach means you don't have to deal with gettext ``*.po`` files, but it is harder to maintain over time.
- You use only one theme and localize the templates using the `jinja2.ext.i18n Jinja2 extension <http://jinja.pocoo.org/docs/templates/#i18n>`_. For a kickstart read this `guide <./localizing_using_jinja2.rst>`_.

It may be convenient to add language buttons to your theme in addition to the translation links of articles and pages. These buttons could, for example, point to the *SITEURL* of each (sub-)site. For this reason the plugin adds these variables to the template context:

main_lang
  The language of the top-level site — the original *DEFAULT_LANG*
main_siteurl
  The *SITEURL* of the top-level site — the original *SITEURL*
lang_siteurls
  An ordered dictionary, mapping all used languages to their *SITEURL*. The ``main_lang`` is the first key with ``main_siteurl`` as the value. This dictionary is useful for implementing global language buttons that show the language of the currently viewed (sub-)site too.
extra_siteurls
  An ordered dictionary, subset of ``lang_siteurls``, the current *DEFAULT_LANG* of the rendered (sub-)site is not included, so for each (sub-)site ``set(extra_siteurls) == set(lang_siteurls) - set([DEFAULT_LANG])``. This dictionary is useful for implementing global language buttons that do not show the current language.

If you don't like the default ordering of the ordered dictionaries, use a Jinja2 filter to alter the ordering.

This short `howto <./implementing_language_buttons.rst>`_ shows two example implementations of language buttons.

Usage notes
===========
- It is **mandatory** to specify *lang* metadata for each article and page as *DEFAULT_LANG* is later changed for each sub-site, so content without *lang* metadata woudl be rendered in every (sub-)site.
- As with the original translations functionality, *slug* metadata is used to group translations. It is therefore often convenient to compensate for this by overriding the content URL (which defaults to slug) using the *URL* and *Save_as* metadata.

Future plans
============

- add a test suite

Development
===========

- A demo and test site is in the ``gh-pages`` branch and can be seen at http://smartass101.github.io/pelican-plugins/
