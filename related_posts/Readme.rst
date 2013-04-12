Related posts
-------------

This plugin adds the ``related_posts`` variable to the article's context.
By default, up to 5 articles are listed. You can customize this value by 
defining ``RELATED_POSTS_MAX`` in your settings file::

    RELATED_POSTS_MAX = 10

You can then use the ``article.related_posts`` variable in your templates.
For example::

    {% if article.related_posts %}
        <ul>
        {% for related_post in article.related_posts %}
            <li><a href="{{ SITEURL }}/{{ related_post.url }}">{{ related_post.title }}</a></li>
        {% endfor %}
        </ul>
    {% endif %}
