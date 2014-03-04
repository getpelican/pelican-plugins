Static comments
---------------

This plugin allows you to add static comments to an article. By default the
plugin looks for the comments of each article in a local file named
``comments/{slug}.md``, where ``{slug}`` is the value of the slug tag for the
article. The comments file should be formatted using markdown.

Set the ``STATIC_COMMENTS`` parameter to True to enable the plugin. Default is
False.

Set the ``STATIC_COMMENTS_DIR`` parameter to the directory where the comments
are located. Default is ``comments``.

On the template side, you just have to add a section for the comments to your
``article.html``, as in this example::

    {% if STATIC_COMMENTS %}
    <section id="comments" class="body">
    <h2>Comments!</h2>
    {{ article.metadata.static_comments }}
    </section>
    {% endif %}

Here is an example of usage:
<http://jesrui.sdf-eu.org/pelican-static-comments.html>
