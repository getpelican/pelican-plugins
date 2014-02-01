-----------------------------
Localizing themes with jinja2
-----------------------------

1. Localize templates
---------------------

To enable the |ext| extensions in your templates, you must add it to 
*JINJA_EXTENSIONS* in your pelican configuration::

  JINJA_EXTENSIONS = ['jinja2.ext.i18n', ...]

Then follow the `jinja2 templating documentation for the i18n plugin <http://jinja.pocoo.org/docs/templates/#i18n>`_ to make your templates localizable. To enable `newstyle gettext calls <http://jinja.pocoo.org/docs/extensions/#newstyle-gettext>`_ the *I18N_GETTEXT_NEWSTYLE* config variable must be True (default).

.. |ext| replace:: ``jinja2.ext.i18n``

2. Specify translations location
--------------------------------

The |ext| extension uses the `Python gettext library <http://docs.python.org/library/gettext.html>`_ for translating strings.

In your Pelican config you can give the path in which to look for translations in the *I18N_GETTEXT_LOCALEDIR* variable.
If not given, it is assumed to be the ``translations`` subfolder in the top folder of the theme specified by *THEME*.

The domain of the translations (the name of each translation file is ``domain.mo``) is controlled by the by the *I18N_GETTEXT_DOMAIN* config variable (defaults to ``messages``).

Example
.......

With the following in your pelican conf::

  I18N_GETTEXT_LOCALEDIR = 'some/path/'
  I18N_GETTEXT_DOMAIN = 'my_domain'

the translation for language 'cz' will be expected to be in ``some/path/cz/LC_MESSAGES/my_domain.mo``

3. Extract translatable strings and translate them
--------------------------------------------------

There are many ways to extract translatable strings and create ``gettext`` compatible translations. 
You can create the ``*.mo`` files yourself, or you can use some helper tool as described in `the Python gettext library howto <http://docs.python.org/library/gettext.html#internationalizing-your-programs-and-modules>`_.

Recommended tool: babel
.......................

`babel <http://babel.pocoo.org/>`_ makes it easy to extract translatable strings from the localized jinja2 templates
and assists with creating translations as documented in this `jinja2-babel howto <http://pythonhosted.org/Flask-Babel/#translating-applications>`_ [#flask]_.

.. [#flask] although the howto is oriented at Flask based webapps, the linked translation howto is not Flask specific


