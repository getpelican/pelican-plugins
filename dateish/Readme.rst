Dateish Plugin for Pelican
==========================

This plugin adds the ability to treat arbitrary metadata fields as datetime
objects.

Usage
-----

For example, if you have the following pieces of metadata in an article:

.. code-block:: markdown

    # my_article.markdown
    Date: 2000-01-01
    Created_Date: 1999-08-04
    Idea_Date: 1993-03-04

Normally, the Created_Date and Idea_Date variables will be strings, so you will
not be able to use the strftime() Jinja filter on them.

With this plugin, you define in your settings file a list of the names of
the additional metadata fields you want to treat as dates:

.. code-block:: python

    # pelicanconf.py
    DATEISH_PROPERTIES = ['created_date', 'idea_date']

Then you can use them in templates just like date:

.. code-block:: html+jinja

    # mytemplate.html
    <p>Created date: {{ article.created_date | strftime('%d %B %Y') }}</p>

