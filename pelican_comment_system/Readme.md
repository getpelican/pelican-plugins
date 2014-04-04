# Pelican comment system
The pelican comment system allows you to add static comments to your articles. It also supports replies to comments.

The comments are stored in Markdown files. Each comment in it own file.

See it in action here: [blog.scheirle.de](http://blog.scheirle.de/posts/2014/March/29/static-comments-via-email/)

Thanks to jesrui the author of [Static comments](https://github.com/getpelican/pelican-plugins/tree/master/static_comments). I reused some code from it.

Author             | Website                   | Github
-------------------|---------------------------|------------------------------
Bernhard Scheirle  | <http://blog.scheirle.de> | <https://github.com/Scheirle>

## Installation
Activate the plugin by adding it to your `pelicanconf.py`

	PLUGIN_PATH = '/path/to/pelican-plugins'
	PLUGINS = ['pelican_comment_system']
	PELICAN_COMMENT_SYSTEM = True

And modify your `article.html` theme (see below).

## Settings
Name                         | Type      | Default    | Description
-----------------------------|-----------|------------|-------
`PELICAN_COMMENT_SYSTEM`     | `boolean` | `False`    | Activates or deactivates the comment system
`PELICAN_COMMENT_SYSTEM_DIR` | `string`  | `comments` | Folder where the comments are stored


### Folder structure
Every comment file has to be stored in a sub folder of `PELICAN_COMMENT_SYSTEM_DIR`.
Sub folders are named after the `slug` of the articles.

So the comments to your `foo-bar` article are stored in `comments/foo-bar/`

The filenames of the comment files are up to you. But the filename is the Identifier of the comment (without extension).

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


### Comment file
##### Meta information
Tag           | Required  | Description
--------------|-----------|----------------
`date`        | yes       | Date when the comment was posted
`replyto`     | no        | Identifier of the parent comment. Identifier = Filename (without extension)
`locale_date` | forbidden | Will be overwritten with a locale representation of the date

Every other (custom) tag gets parsed as well and will be available through the theme.


##### Example of a comment file

	date: 2014-3-21 15:02
	author: Author of the comment
	website: http://authors.website.com
	replyto: 7
	anothermetatag: some random tag

	Content of the comment.

### Theme
In the `article.html` theme file are now two more variables available.

Variables                         | Description
----------------------------------|--------------------------
`article.metadata.comments_count` | Amount of total comments for this article (including replies to comments)
`article.metadata.comments`       | Array containing the top level comments for this article (no replies to comments)

#### Comment object
Variables  | Description
-----------|--------------------------
`id`       | Identifier of this comment
`content`  | Content of this comment
`metadata` | All metadata as in the comment file (or described above)
`replies`  | Array containing the top level replies for this comment

##### Example article.html theme
(only the comment section)

```html
{% if article.metadata.comments %}
	{% for comment in article.metadata.comments recursive %}
		{% set metadata = comment.metadata %}
		{% if loop.depth0 == 0 %}
			{% set marginLeft = 0 %}
		{% else %}
			{% set marginLeft = 50 %}
		{% endif %}
			<article id="comment-{{comment.id}}" style="border: 1px solid #DDDDDD; padding: 5px 0px 0px 5px; margin: 0px -1px 5px {{marginLeft}}px;">
				<a href="{{ SITEURL }}/{{ article.url }}#comment-{{comment.id}}" rel="bookmark" title="Permalink to this comment">Permalink</a>
				<h4>{{ metadata['author'] }}</h4>
				<p>Posted on <abbr class="published" title="{{ metadata['date'].isoformat() }}">{{ metadata['locale_date'] }}</abbr></p>

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
## Recommendation
Add a form, which allows your visitors to easily write comments.

But more importantly, on submit the form generates a mailto-link.
The resulting email contains a valid markdown block. Now you only have to copy this block in a new file. And therefore there is no need to gather the metadata (like date, author, replyto) yourself.

##### Reply button
Add this in the above `for` loop, so your visitors can reply to a comment.

```html
<button onclick="reply('{{comment.id | urlencode}}');">Reply</button>
```

##### form + javascript

```html
<form role="form" id="commentForm" action="#">
	<input name="Name" type="text" id="commentForm_inputName" placeholder="Enter your name or synonym">
	<textarea name="Text" id="commentForm_inputText" rows="10" style="resize:vertical;" placeholder="Your comment"></textarea>
	<button type="submit" id="commentForm_button">Post via email</button>
	<input name="replyto" type="hidden" id="commentForm_replyto">
</form>
```

```javascript
<script type="text/javascript">
	function reply(id)
	{
		id = decodeURIComponent(id);
		$('#commentForm_replyto').val(id);
	}

	$(document).ready(function() {
		function generateMailToLink()
		{
			var user = 'your_user_name'; //user@domain = your email address
			var domain = 'your_email_provider';
			var subject = 'Comment for \'{{ article.slug }}\'' ;

			var d = new Date();
			var body = ''
				+ 'Hey,\nI posted a new comment on ' + document.URL + '\n\nGreetings ' + $("#commentForm_inputName").val() + '\n\n\n'
				+ 'Raw comment data:\n'
				+ '----------------------------------------\n'
				+ 'date: ' + d.getFullYear() + '-' + (d.getMonth()+1) + '-' + d.getDate() + ' ' + d.getHours() + ':' + d.getMinutes() + '\n'
				+ 'author: ' + $("#commentForm_inputName").val() + '\n';

			var replyto = $('#commentForm_replyto').val();
			if (replyto.length != 0)
			{
				body += 'replyto: ' + replyto + '\n'
			}

			body += '\n'
				+ $("#commentForm_inputText").val() + '\n'
				+ '----------------------------------------\n';

			var link = 'mailto:' + user + '@' + domain + '?subject='
				+ encodeURIComponent(subject)
				+ "&body="
				+ encodeURIComponent(body);
			return link;
		}


		$('#commentForm').on("submit",
			function( event )
			{
				event.preventDefault();
				$(location).attr('href', generateMailToLink());
			}
		);
	});
</script>
```
(jQuery is required for this script)

Don't forget to set the Variables `user` and `domain`.
