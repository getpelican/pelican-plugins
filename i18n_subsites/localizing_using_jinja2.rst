-----------------------------
Localizing themes with Jinja2
-----------------------------

1. Localize templates
---------------------

To enable the |ext| extension in your templates, you must add it to 
*JINJA_EXTENSIONS* in your Pelican configuration

.. code-block:: python

  JINJA_EXTENSIONS = ['jinja2.ext.i18n', ...]

Then follow the `Jinja2 templating documentation for the I18N plugin <http://jinja.pocoo.org/docs/templates/#i18n>`_ to make your templates localizable. This usually means surrounding strings with the ``{% trans %}`` directive or using ``gettext()`` in expressions

.. code-block:: jinja

    {% trans %}translatable content{% endtrans %}
    {{ gettext('a translatable string') }}

For pluralization support, etc. consult the documentation

To enable `newstyle gettext calls <http://jinja.pocoo.org/docs/extensions/#newstyle-gettext>`_ the *I18N_GETTEXT_NEWSTYLE* config variable must be set to ``True`` (default).

.. |ext| replace:: ``jinja2.ext.i18n``

2. Specify translations location
--------------------------------

The |ext| extension uses the `Python gettext library <http://docs.python.org/library/gettext.html>`_ for translating strings.

In your Pelican config you can give the path in which to look for translations in the *I18N_GETTEXT_LOCALEDIR* variable. If not given, it is assumed to be the ``translations`` subfolder in the top folder of the theme specified by *THEME*.

The domain of the translations (the name of each translation file is ``domain.mo``) is controlled by the *I18N_GETTEXT_DOMAIN* config variable (defaults to ``messages``).

Example
.......

With the following in your Pelican settings file

.. code-block:: python

  I18N_GETTEXT_LOCALEDIR = 'some/path/'
  I18N_GETTEXT_DOMAIN = 'my_domain'

… the translation for language 'cz' will be expected to be in ``some/path/cz/LC_MESSAGES/my_domain.mo``


3. Extract translatable strings and translate them
--------------------------------------------------

There are many ways to extract translatable strings and create ``gettext`` compatible translations. You can create the ``*.po`` and ``*.mo`` message catalog files yourself, or you can use some helper tool as described in `the Python gettext library tutorial <http://docs.python.org/library/gettext.html#internationalizing-your-programs-and-modules>`_.

You of course don't need to provide a translation for the language in which the templates are written which is assumed to be the original *DEFAULT_LANG*. This can be overridden in the *I18N_TEMPLATES_LANG* variable.

Recommended tool: babel
.......................

`Babel <http://babel.pocoo.org/>`_ makes it easy to extract translatable strings from the localized Jinja2 templates and assists with creating translations as documented in this `Jinja2-Babel tutorial <http://pythonhosted.org/Flask-Babel/#translating-applications>`_ [#flask]_ on which the following is based.

1. Add babel mapping
~~~~~~~~~~~~~~~~~~~~

Let's assume that you are localizing a theme in ``themes/my_theme/`` and that you use the default settings, i.e. the default domain ``messages`` and will put the translations in the ``translations`` subdirectory of the theme directory as ``themes/my_theme/translations/``.

It is up to you where to store babel mappings and translation files templates (``*.pot``), but a convenient place is to put them in ``themes/my_theme/`` and work in that directory. From now on let's assume that it will be our current working directory (CWD).

To tell babel to extract translatable strings from the templates create a mapping file ``babel.cfg`` with the following line

.. code-block:: cfg

    [jinja2: ./templates/**.html]


2. Extract translatable strings from templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following command to create a ``messages.pot`` message catalog template file from extracted translatable strings

.. code-block:: bash

    pybabel extract --mapping babel.cfg --output messages.pot ./


3. Initialize message catalogs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to translate the template to language ``lang``, run the following command to create a message catalog
``translations/lang/LC_MESSAGES/messages.po`` using the template ``messages.pot``

.. code-block:: bash

    pybabel init --input-file messages.pot --output-dir translations/ --locale lang --domain messages

babel expects ``lang`` to be a valid locale identifier, so if e.g. you are translating for language ``cz`` but the corresponding locale is ``cs``, you have to use the locale identifier. Nevertheless, the gettext infrastructure should later correctly find the locale for a given language.

4. Fill the message catalogs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The message catalog files format is quite intuitive, it is fully documented in the `GNU gettext manual <http://www.gnu.org/software/gettext/manual/gettext.html#PO-Files>`_. Essentially, you fill in the ``msgstr`` strings


.. code-block:: po

    msgid "just a simple string"
    msgstr "jenom jednoduchý řetězec"

    msgid ""
    "some multiline string"
    "looks like this"
    msgstr ""
    "nějaký více řádkový řetězec"
    "vypadá takto"

You might also want to remove ``#,fuzzy`` flags once the translation is complete and reviewed to show that it can be compiled.

5. Compile the message catalogs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The message catalogs must be compiled into binary format using this command

.. code-block:: bash

    pybabel compile --directory translations/ --domain messages

This command might complain about "fuzzy" translations, which means you should review the translations and once done, remove the fuzzy flag line.

(6.) Update the catalogs when templates change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you add any translatable patterns into your templates, you have to update your message catalogs too.
First you extract a new message catalog template as described in the 2. step. Then you run the following command [#pybabel_error]_

.. code-block:: bash

   pybabel update --input-file messages.pot --output-dir translations/ --domain messages

This will merge the new patterns with the old ones. Once you review and fill them, you have to recompile them as described in the 5. step.

.. [#flask] Although the tutorial is focused on Flask-based web applications, the linked translation tutorial is not Flask-specific.
.. [#pybabel_error] If you get an error ``TypeError: must be str, not bytes`` with Python 3.3, it is likely you are suffering from this `bug <https://github.com/mitsuhiko/flask-babel/issues/43>`_. Until the fix is released, you can use babel with Python 2.7.
