# Quickstart Guide (with Comment form)

This guide shows you how to setup the plugin for basic usage.
The default theme has an comment form included.
This form allows your visitors to easily write comments and send them to you via email [1].

1. Merge the `./theme` folder with your own theme folder, or copy the files manually
	```
	mkdir -p [yourtheme]/templates/pcs
	mkdir -p [yourtheme]/static/js
	cp ./theme/templates/pcs/comments.html [yourtheme]/templates/pcs/comments.html
	cp ./theme/static/js/comments.js      [yourtheme]/static/js/comments.html
	```

2. Modify your `article.html` template:
	1. Add `{% import 'pcs/comments.html' as pcs with context %}` to the top
	2. Add `{{ pcs.comments_quickstart("emailuser", "example.com") }}` where you want your comments (e.g. below `{{ article.content }}`)  
	"emailuser@example.com" will be the e-mail address used for the `mailto:` link [1]

3. Enable the plugin: `pelicanconf.py` (See also [How to use plugins](https://github.com/getpelican/pelican-plugins/tree/master/#how-to-use-plugins))
	```
	PELICAN_COMMENT_SYSTEM = True
	PELICAN_COMMENT_SYSTEM_IDENTICON_DATA = ('author',)
	```

## Notes
 * Instead of using `pcs.comments_quickstart` you can also use the other macros available in `comments.html`.
   They are a bit more flexible and may generate "better" html output e.g.:
    * Don't force load jQuery
    * No inline css

[1] The comment form generates a `mailto:` link on submisson. The resulting email contains a valid Markdown block. Now you only have to copy this block to a new file, obviating the need to gather the metadata (such as date, author, replyto) yourself.