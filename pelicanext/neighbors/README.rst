Neighbor Articles Plugin for Pelican
====================================

This plugin adds ``next_article`` (newer) and ``prev_article`` (older) 
variables to the article's context

Installation
------------
To enable, ensure that ``neighbors.py`` is in somewhere you can ``import``.
Then use the following in your `settings`::

    PLUGINS = ["neighbors"]

Or you can put the plugin in ``plugins`` folder in pelican installation. You 
can find the location by typing::

    python -c 'import pelican.plugins as p, os; print os.path.dirname(p.__file__)'

Once you get the folder, copy the ``neighbors.py`` there and use the following
in your settings::

    PLUGINS = ["pelican.plugins.neighbors"]

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