# Footer Insert

This plugin allows you to insert a `FOOTER_INSERT_HTML` to the end of the blog.

eg.  add authors / blog infomation to every blog.

## Usage

1. Insert `FOOTER_INSERT_HTML` to your `pelicanconf.py`. You can use
title / url / author / authors / slug / category / summary
/ date infomation in the config like this: `%(title)s`.
2. Insert this code to your artical template file, eg. `templates/article.html`:
```
{% if article.footer_insert_html %}
  {{ article.footer_insert_html }}
{% endif %}
```
