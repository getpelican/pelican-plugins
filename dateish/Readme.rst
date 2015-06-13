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
    Idea_Date: 1993-03-04
    Important_Dates: 2013-10-12
                     2013-11-08
                     2013-12-02

Normally, the Idea_Date and Important_Dates variables will be strings, so
you will not be able to use the strftime() Jinja filter on them.

With this plugin, you define in your settings file a list of the names of
the additional metadata fields you want to treat as dates:

.. code-block:: python

    # pelicanconf.py
    DATEISH_PROPERTIES = ['idea_date', 'important_dates']

Then you can use them in templates just like date:

.. code-block:: html+jinja

    # mytemplate.html
    <p>Idea date: {{ article.idea_date | strftime('%d %B %Y') }}</p>
    {% for d in article.important_dates %}
        <p>Important date: {{ d | strftime('%d %B %Y') }}</p>
    {% endfor %}

