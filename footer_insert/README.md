# Footer Insert

This plugin allows you to insert a `FOOTER_INSERT_HTML` to the end of the blog.

And you shoud add this to your template:

```
{% if article.footer_insert_html %}
  {{ article.footer_insert_html }}
{% endif %}
```
