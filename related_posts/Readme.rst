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


Your related posts should share a common tag. You can also use ``related_posts:`` in your post's meta data.
The 'related_posts:' meta data works together with your existing slugs:

    related_posts: slug1,slug2,slug3...slugN 

N represents the RELATED_POSTS_MAX
