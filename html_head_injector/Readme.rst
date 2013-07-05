Additional <head> content per article
=====================================

This plugin allows you to place custom HTML at the end of the <head> directive
of an article.

Usage
-----

Place your head content somewhere in the article, surrounded by::

    .. injecthead

Example::

    .. injecthead::
    
        your content, e.g.:
        <style> td { text-align: center; } </style>

Also, you need to add the generated HTML in your template file::

    {% if article and article.inject_head %}
        {{ article.inject_head }}
    {% endif %}
    {% if page and page.inject_head %}
        {{ page.inject_head }}
    {% endif %}