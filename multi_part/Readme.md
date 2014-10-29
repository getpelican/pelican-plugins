Multi parts posts
-----------------

The multi-part posts plugin allow you to write posts that belong to a series.

In order to mark posts as part of a multi-part post, use the `:series:` metadata:

    :series:  NAME_OF_THIS_SERIES

[The old :parts: metadata is still supported but deprecated]

You can then use the following variables in your templates

    * `article.multi_part.series` is the name of the series as specified in the article metadata
    * `article.multi_part.index` is the index of the current article inside the series
    * `article.multi_part.all` is a date-ordered list of all articles in the series (including the current one)
    * `article.multi_part.previous` is a date-ordered list of the articles published before the current one
    * `article.multi_part.next` is a date-ordered list of the articles published after the current one

For example:

    {% if article.multi_part %}
        <p>This post is part {{ article.multi_part.index }} of the "{{ article.multi_part.series }}" series:</p>
        <ol class="parts">
            {% for part_article in article.multi_part.all %}
                <li {% if part_article == article %}class="active"{% endif %}>
                    <a href='{{ SITEURL }}/{{ part_article.url }}'>{{ part_article.title }}</a>
                </li>
            {% endfor %}
        </ol>
    {% endif %}
