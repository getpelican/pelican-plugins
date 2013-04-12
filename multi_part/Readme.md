Multi parts posts
-----------------

The multi-part posts plugin allow you to write multi-part posts.

In order to mark posts as part of a multi-part post, use the `:parts:` metadata:

    :parts:  MY_AWESOME_MULTI_PART_POST

You can then use the `article.metadata.parts_articles` variable in your templates 
to display other parts of current post.

For example:

    {% if article.metadata.parts_articles %}
        <ol class="parts">
        <li>Post parts</li>
        {% for part_article in article.metadata.parts_articles %}
            {% if part_article == article %}
                <li class="active">
                    <a href='{{ SITEURL }}/{{ part_article.url }}'>{{ part_article.title }}
                    </a>
                </li>
            {% else %}
                <li>
                    <a href='{{ SITEURL }}/{{ part_article.url }}'>{{ part_article.title }}
                    </a>
                </li>
            {% endif %}
        {% endfor %}
        </ol>
    {% endif %}
