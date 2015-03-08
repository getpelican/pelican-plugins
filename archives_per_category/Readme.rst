Archives per category
=====================

This plugin allows you to create period archives for selected (or all) categories.
It works pretty like normal period archives.

Settings
--------

.. code:: python

    PLUGIN_PATHS = ('plugins',)
    PLUGINS = ('archives_per_category',)

    # Categories to archive, if not set, archive them all. Categories could be
    # defined by name or slug.
    CATEGORIES_TO_ARCHIVE = ('misc', 'Python')

    YEAR_ARCHIVES_PER_CATEGORY_SAVE_AS = 'category_archives/{category}/{date:%Y}/index.html'
    MONTH_ARCHIVES_PER_CATEGORY_SAVE_AS = 'category_archives/{category}/{date:%Y-%m}/index.html'
    DAY_ARCHIVES_PER_CATEGORY_SAVE_AS = 'category_archives/{category}/{date:%Y-%m-%d}/index.html'


Template
--------

Template is quite similiar to period archive's template. You could use the same
variables, plus :code:`{{ category }}` and :code:`{{ category-slug }}`.

Plugin looks for templates in this order 1. 'archives_per_category',
2. 'period_archives', 3. 'archives'.

.. code:: html

    {% extends "base.html" %}
    {% block content %}
      <h1>Archives for {{ category }} {{ period | reverse | join(' ') }}</h1>
      <dl>
        {% for article in dates %}
        <dt>{{ article.locale_date }}</dt>
        <dd><a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></dd>
        {% endfor %}
      </dl>
    {% endblock %}
