Neighbor Articles Plugin for Pelican
====================================

This plugin adds ``next_article`` (newer) and ``prev_article`` (older)
variables to the article's context.

Also adds ``next_article_in_category`` and ``prev_article_in_category``.


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
   <ul>
    {% if article.prev_article_in_category %}
        <li>
            <a href="{{ SITEURL }}/{{ article.prev_article_in_category.url}}">
                {{ article.prev_article_in_category.title }}
            </a>
        </li>
    {% endif %}
    {% if article.next_article_in_category %}
        <li>
            <a href="{{ SITEURL }}/{{ article.next_article_in_category.url}}">
                {{ article.next_article_in_category.title }}
            </a>
        </li>
    {% endif %}
    </ul>

Usage with the Subcategory plugin
---------------------------------

If you want to get the neigbors within a subcategory it's a little different.
Since an article can belong to more than one subcategory, subcategories are
stored in a list. If you have an article with subcategories like

``Category/Foo/Bar``

it will belong to both subcategory Foo, and Foo/Bar. Subcategory neighbors are
added to an article as ``next_article_in_subcategory#`` and
``prev_article_in_subcategory#`` where ``#`` is the level of subcategory. So using
the example from above, subcategory1 will be Foo, and subcategory2 Foo/Bar.
Therefor the usage with subcategories is:

.. code-block:: html+jinja

    <ul>
    {% if article.prev_article_in_subcategory1 %}
        <li>
            <a href="{{ SITEURL }}/{{ article.prev_article_in_subcategory1.url}}">
                {{ article.prev_article_in_subcategory1.title }}
            </a>
        </li>
    {% endif %}
    {% if article.next_article_in_subcategory1 %}
        <li>
            <a href="{{ SITEURL }}/{{ article.next_article_in_subcategory1.url}}">
                {{ article.next_article_in_subcategory1.title }}
            </a>
        </li>
    {% endif %}
   </ul>
   <ul>
    {% if article.prev_article_in_subcategory2 %}
        <li>
            <a href="{{ SITEURL }}/{{ article.prev_article_in_subcategory2.url}}">
                {{ article.prev_article_in_subcategory2.title }}
            </a>
        </li>
    {% endif %}
    {% if article.next_article_in_subcategory2 %}
        <li>
            <a href="{{ SITEURL }}/{{ article.next_article_in_subcategory2.url}}">
                {{ article.next_article_in_subcategory2.title }}
            </a>
        </li>
    {% endif %}
    </ul>

