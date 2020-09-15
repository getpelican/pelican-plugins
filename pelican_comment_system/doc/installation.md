# Installation

Activate the plugin by adding it to your `pelicanconf.py`: (See also [How to use plugins](https://github.com/getpelican/pelican-plugins/tree/master/#how-to-use-plugins))

	PELICAN_COMMENT_SYSTEM = True

Then, modify your `article.html` theme as follows below.

## Settings

Name                                           | Type      | Default                      | Description
-----------------------------------------------|-----------|------------------------------|-------
`PELICAN_COMMENT_SYSTEM`                       | `boolean` | `False`                      | Activates or deactivates the comment system
`PELICAN_COMMENT_SYSTEM_DIR`                   | `string`  | `comments`                   | Folder where the comments are stored, relative to `PATH`
`PELICAN_COMMENT_SYSTEM_IDENTICON_OUTPUT_PATH` | `string`  | `images/identicon`           | Relative URL to the output folder where the identicons are stored
`PELICAN_COMMENT_SYSTEM_IDENTICON_DATA`        | `tuple`   | `()`                         | Contains all Metadata tags, which in combination identifies a comment author (like `('author', 'email')`)
`PELICAN_COMMENT_SYSTEM_IDENTICON_SIZE`        | `int`     | `72`                         | Width and height of the identicons. Has to be a multiple of 3.
`PELICAN_COMMENT_SYSTEM_AUTHORS`               | `dict`    | `{}`                         | Comment authors, which should have a specific avatar. More info [here](avatars.md)
`PELICAN_COMMENT_SYSTEM_FEED`                  | `string`  |`feeds/comment.%s.atom.xml`   | Relative URL to output the Atom feed for each article.`%s` gets replaced with the slug of the article. More info [here](http://docs.getpelican.com/en/latest/settings.html#feed-settings)
`PELICAN_COMMENT_SYSTEM_FEED_ALL`              | `string`  |`feeds/comments.all.atom.xml` | Relative URL to output the Atom feed which contains all comments of all articles. More info [here](http://docs.getpelican.com/en/latest/settings.html#feed-settings)
`COMMENT_URL`                                  | `string`  | `#comment-{slug}`            | `{slug}` gets replaced with the slug of the comment. More info [here](feed.md)

## Folder structure

Every comment file has to be stored in a sub-folder of `PELICAN_COMMENT_SYSTEM_DIR`.

Sub-folders are named after the `slug` of the articles.

So the comments to your `foo-bar` article are stored in `comments/foo-bar/`

The filenames of the comment files are up to you. But the filename is the identifier of the comment (**with** extension).

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
`slug`        | no        | Slug of the comment. If not present it will be computed from the file name (including the extension)
`replyto`     | no        | Slug of the parent comment

Every other (custom) tag gets parsed as well and will be available through the theme.

##### Example of a comment file

	date: 2014-3-21 15:02
	author: Author of the comment
	website: http://authors.website.com
	replyto: 1md
	anothermetatag: some random tag

	Content of the comment.

## Theme

In the `article.html` template file, there are now two additional variables available.

Variables                | Description
-------------------------|--------------------------
`article.comments_count` | Number of total comments for this article (including replies to comments)
`article.comments`       | Array containing the top-level comments for this article (no replies to comments)

### Comment object

The comment object is a [content](https://github.com/getpelican/pelican/blob/master/pelican/contents.py#L34) object, so all common attributes are available (author, content, date, local_date, slug, metadata, etc.).

The additional following attributes are also available:

Attribute  | Description
-----------|--------------------------
`replies`  | Array containing the top level replies for this comment
`avatar`   | Path to the avatar or identicon of the comment author

##### Example article.html template

(only the comment section is shown here)

```html
{% if article.comments %}
	{% for comment in article.comments recursive %}
		{% if loop.depth0 == 0 %}
			{% set marginLeft = 0 %}
		{% else %}
			{% set marginLeft = 50 %}
		{% endif %}
			<article id="comment-{{comment.slug}}" style="border: 1px solid #DDDDDD; padding: 5px 0px 0px 5px; margin: 0px -1px 5px {{marginLeft}}px;">
				<a href="{{ SITEURL }}/{{ article.url }}#comment-{{comment.slug}}" rel="bookmark" title="Permalink to this comment">Permalink</a>
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

For a more complex / extensive example have a look at [theme/templates/pcs/comments.html](../theme/templates/pcs/comments.html)