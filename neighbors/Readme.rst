Neighbor Articles Plugin for Pelican
====================================

This plugin adds ``next_article`` (newer) and ``prev_article`` (older) 
variables to the article's context

Usage
-----

.. code-block:: html+jinja

    <ul>
    {% if article.prev_article %}
        <li>
            <a href="{{ SITEURL }}/{{ article.prev_article.url}}">
                {{ article.prev_article.title }}
            </a>
        </li>
    {% endif %}
    {% if article.next_article %}
        <li>
            <a href="{{ SITEURL }}/{{ article.next_article.url}}">
                {{ article.next_article.title }}
            </a>
        </li>
    {% endif %}
    </ul>
