# Comment Atom Feed
## Custom comment url
Be sure that the id of the html tag containing the comment matches `COMMENT_URL`.

##### pelicanconf.py
```python
COMMENT_URL = "#my_own_comment_id_{slug}"
```

##### Theme
```html
{% for comment in article.comments recursive %}
	...
	<article id="my_own_comment_id_{{comment.slug}}">{{ comment.content }}</article>
	...
{% endfor %}
```
## Theme
#### Link
To display a link to the article feed simply add the following to your theme:

```html
{% if article %}
	<a href="{{ FEED_DOMAIN }}/{{ PELICAN_COMMENT_SYSTEM_FEED|format(article.slug) }}">Comment Atom Feed</a>
{% endif %}
```

Link to the all comment feed:

```html
<a href="{{ FEED_DOMAIN }}/{{ PELICAN_COMMENT_SYSTEM_FEED_ALL }}">Comment All Atom Feed</a>
```

