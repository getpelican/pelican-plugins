# Installation
Activate the plugin by adding it to your `pelicanconf.py`

	PLUGIN_PATH = '/path/to/pelican-plugins'
	PLUGINS = ['pelican_comment_system']
	PELICAN_COMMENT_SYSTEM = True

And modify your `article.html` theme (see below).

## Settings
Name                                           | Type      | Default                    | Description
-----------------------------------------------|-----------|----------------------------|-------
`PELICAN_COMMENT_SYSTEM`                       | `boolean` | `False`                    | Activates or deactivates the comment system
`PELICAN_COMMENT_SYSTEM_DIR`                   | `string`  | `comments`                 | Folder where the comments are stored
`PELICAN_COMMENT_SYSTEM_IDENTICON_OUTPUT_PATH` | `string`  | `images/identicon`         | Relative URL to the output folder where the identicons are stored
`PELICAN_COMMENT_SYSTEM_IDENTICON_DATA`        | `tuple`   | `()`                       | Contains all Metadata tags, which in combination identifies a comment author (like `('author', 'email')`)
`PELICAN_COMMENT_SYSTEM_IDENTICON_SIZE`        | `int`     | `72`                       | Width and height of the identicons. Has to be a multiple of 3.
`PELICAN_COMMENT_SYSTEM_AUTHORS`               | `dict`    | `{}`                       | Comment authors, which should have a specific avatar. More info [here](avatars.md)
`PELICAN_COMMENT_SYSTEM_FEED`                  | `string`  |`feeds/comment.%s.atom.xml` | Relative URL to output the Atom feed for each article.`%s` gets replaced with the slug of the article. More info [here](http://docs.getpelican.com/en/latest/settings.html#feed-settings)
`COMMENT_URL`                                  | `string`  | `#comment-{path}`          | `{path}` gets replaced with the id of the comment. More info [here](feed.md)

## Folder structure
Every comment file has to be stored in a sub folder of `PELICAN_COMMENT_SYSTEM_DIR`.
Sub folders are named after the `slug` of the articles.

So the comments to your `foo-bar` article are stored in `comments/foo-bar/`

The filenames of the comment files are up to you. But the filename is the Identifier of the comment (**with** extension).

##### Example folder structure

	.
	└── comments
		└── foo-bar
		│   ├── 1.md
		│   └── 0.md
		└── some-other-slug
			├── random-Name.md
			├── 1.md
			└── 0.md


## Comment file
### Meta information
Tag           | Required  | Description
--------------|-----------|----------------
`date`        | yes       | Date when the comment was posted
`author`      | yes       | Name of the comment author
`replyto`     | no        | Identifier of the parent comment. Identifier = Filename (**with** extension)

Every other (custom) tag gets parsed as well and will be available through the theme.

##### Example of a comment file

	date: 2014-3-21 15:02
	author: Author of the comment
	website: http://authors.website.com
	replyto: 7
	anothermetatag: some random tag

	Content of the comment.

## Theme
In the `article.html` theme file are now two more variables available.

Variables                | Description
-------------------------|--------------------------
`article.comments_count` | Amount of total comments for this article (including replies to comments)
`article.comments`       | Array containing the top level comments for this article (no replies to comments)

### Comment object
The comment object is a [content](https://github.com/getpelican/pelican/blob/master/pelican/contents.py#L34) object, so all common attributes are available (like author, content, date, local_date, metadata, ...).

Additional following attributes are added:

Attribute  | Description
-----------|--------------------------
`id`       | Identifier of this comment
`replies`  | Array containing the top level replies for this comment
`avatar`   | Path to the avatar or identicon of the comment author

##### Example article.html theme
(only the comment section)
```html
{% if article.comments %}
	{% for comment in article.comments recursive %}
		{% if loop.depth0 == 0 %}
			{% set marginLeft = 0 %}
		{% else %}
			{% set marginLeft = 50 %}
		{% endif %}
			<article id="comment-{{comment.id}}" style="border: 1px solid #DDDDDD; padding: 5px 0px 0px 5px; margin: 0px -1px 5px {{marginLeft}}px;">
				<a href="{{ SITEURL }}/{{ article.url }}#comment-{{comment.id}}" rel="bookmark" title="Permalink to this comment">Permalink</a>
				<h4>{{ comment.author }}</h4>
				<p>Posted on <abbr class="published" title="{{ comment.date.isoformat() }}">{{ comment.locale_date }}</abbr></p>
				{{ comment.metadata['my_custom_metadata'] }}
				{{ comment.content }}
				{% if comment.replies %}
					{{ loop(comment.replies) }}
				{% endif %}
			</article>
	{% endfor %}
{% else %}
	<p>There are no comments yet.<p>
{% endif %}
```
