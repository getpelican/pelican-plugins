# Feed Template

This plugin allows to customize article title, link and description in RSS feeds using a template.

## Usage

To use the plugin, add it to the `PLUGINS` list in `pelicanconf.py` and create a new template `feed.html` in your theme. The template should contain three macros corresponding to customized parts of RSS entry: `title`, `link`, and `description`. Each macro accepts article object as a parameter. If one of the macros is not defined, default value is used.

## Examples

Default Pelican feeds behavior corresponds to the following template:

    {% macro title(article) %}
      {{ article.title | striptags }}
    {% endmacro %}

    {% macro link(article) %}
      {{ SITEURL }}/{{ article.url }}
    {% endmacro %}

    {% macro description(article) %}
      {{ article.get_content(SITEURL) }}
    {% endmacro %}

The plugin can be very useful for blogs that publish links in a style of Daring Fireball. For example if link posts are placed in a separate category and link URL is specified in a `Link:` metadata field, feed can be customized in the following way:

    {% macro title(article) %}
      {% if article.category == "links" %}→{% endif %}
      {{ article.title | striptags }}
    {% endmacro %}

    {% macro link(article) %}
      {% if article.category == "links" %}
        {{ article.link }}
      {% else %}
        {{ SITEURL }}/{{ article.url }}
      {% endif %}
    {% endmacro %}

    {% macro description(article) %}
      {{ article.get_content(url) }}
      {% if article.category == "links" %}
        <p><a href="{{ SITEURL }}/{{ article.url }}">Permalink</a></p>
      {% endif %}
    {% endmacro %}
