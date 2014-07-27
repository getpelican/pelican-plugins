# Pelican comment system
The pelican comment system allows you to add static comments to your articles.
The comments are stored in files which can be processed by Pelican (e.g.: Markdown, reStructuredText, ...). Each comment in its own file.

#### Features
 - Static comments for each article
 - Replies to comments
 - Avatars and [Identicons](https://en.wikipedia.org/wiki/Identicon)
 - Comment Atom Feed for each article
 - Easy styleable via the themes


See it in action here: [blog.scheirle.de](http://blog.scheirle.de/posts/2014/March/29/static-comments-via-email/)

Author             | Website                   | Github
-------------------|---------------------------|------------------------------
Bernhard Scheirle  | <http://blog.scheirle.de> | <https://github.com/Scheirle>

## Instructions
 - [Installation and basic usage](doc/installation.md)
 - [Avatars and Identicons](doc/avatars.md)
 - [Comment Atom Feed](doc/feed.md)
 - [Comment Form (aka: never gather Metadata)](doc/form.md)
 
## Requirements
Pelican 3.4 or newer is required.

To create identicons the Python Image Library is needed. Therefore you either need PIL **or** Pillow (recommended).

##### Install Pillow
	easy_install Pillow
	
If you don't use avatars or identicons this plugin works fine without PIL/Pillow. You will however get a warning that identicons are deactivated (as expected).
