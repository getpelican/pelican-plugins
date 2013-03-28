Disqus static comment plugin for Pelican
====================================

This plugin adds a disqus_comments property to all articles.
Comments are fetched at generation time using disqus API.

Installation
------------
Because we use disqus API to retrieve the comments you need to create an application at
http://disqus.com/api/applications/ which will provide you with a secret and public keys for the API.

We use disqus-python package for communication with disqus API:
``pip install disqus-python``

Put ``disqus_static.py`` plugin in ``plugins`` folder in pelican installation 
and use the following in your settings::

    PLUGINS = [u"pelican.plugins.disqus_static"]

    DISQUS_SITENAME = u'YOUR_SITENAME'
    DISQUS_SECRET_KEY = u'YOUR_SECRET_KEY'
    DISQUS_PUBLIC_KEY = u'YOUR_PUBLIC_KEY'

Usage
-----

.. code-block:: html+jinja

    {% if article.disqus_comments %}
    <div id="disqus_static_comments">
        <h4>{{ article.disqus_comment_count }} comments</h4>
        <ul class="post-list">
            {% for comment in article.disqus_comments recursive %}
            <li class="post">
                <div class="post-content">
                    <div class="avatar hovercard">
                        <img alt="Avatar" src="{{ comment.author.avatar.small.cache }}">
                    </div>
                    <div class="post-body">
                        <header>
                            <span class="publisher-anchor-color">{{ comment.author.name }}</span>
                            <span class="time-ago" title="{{ comment.createdAt }}">{{ comment.createdAt }}</span>
                        </header>
                        <div class="post-message-container">
                            <div class="post-message publisher-anchor-color ">
                                {{ comment.message }}
                            </div>
                        </div>
                    </div>
                </div>
                {% if comment.children %}
                <ul class="children">
                    {{ loop(comment.children) }}
                </ul>
                {% endif %}
            </li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
