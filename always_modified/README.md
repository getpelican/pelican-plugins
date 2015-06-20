# Always Modified

Puts a "modified" date on articles, defaulting to the normal "created" date.

## Usage

1. Insert `ALWAYS_MODIFIED=True` in your `pelicanconf.py`.
2. Now you can sort by modified date in your templates:
```
{% for article in articles|sort(reverse=True,attribute='modified') %}
```
