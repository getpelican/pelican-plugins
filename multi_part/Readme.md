Multi parts posts
-----------------

The multi-part posts plugin allow you to write multi-part posts.

In order to mark posts as part of a multi-part post, use the `:parts:` metadata:

    :parts:  MY_AWESOME_MULTI_PART_POST

You can then use the `article.metadata.parts_articles` variable in your templates 
to display other parts of current post.

For example:

    {% if article.metadata.parts_articles %}
        <p>This post is part of a series:</p>
        <ol class="parts">
            {% for part_article in article.metadata.parts_articles %}
                <li {% if part_article == article %}class="active"{% endif %}>
                    <a href='{{ SITEURL }}/{{ part_article.url }}'>{{ part_article.title }}</a>
                </li>
            {% endfor %}
        </ol>
    {% endif %}
