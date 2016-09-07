# Pelican Comment System

Pelican Comment System allows you to add static comments to your articles.

Comments are stored in files in formats that can be processed by Pelican (e.g., Markdown, reStructuredText). Each comment resides in its own file.

### Features

 - Static comments for each article
 - Replies to comments
 - Avatars and [Identicons](https://en.wikipedia.org/wiki/Identicon)
 - Comment Atom feed for each article
 - Easy styleable via themes


See it in action here: [bernhard.scheirle.de](http://bernhard.scheirle.de/posts/2014/March/29/static-comments-via-email/)

Author             | Website                       | Github
-------------------|-------------------------------|------------------------------
Bernhard Scheirle  | <http://bernhard.scheirle.de> | <https://github.com/Scheirle>

## Instructions

 - [Quickstart Guide](doc/quickstart.md)
 - [Installation and basic usage](doc/installation.md)
 - [Avatars and identicons](doc/avatars.md)
 - [Comment Atom feed](doc/feed.md)
 
## Requirements

Pelican 3.4 or newer is required.

To create identicons, the Python Image Library is needed. Therefore you either need PIL **or** Pillow (recommended).

**Install Pillow via:**

    pip install Pillow

If you don't want avatars or identicons, this plugin works fine without PIL/Pillow. You will, however, see a warning that identicons are deactivated (as expected).
