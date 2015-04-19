# Textbundle Reader

This plugin helps you creating posts from Textbundles
(<http://textbundle.org/spec/>).

In a nutshell a textbundle is a folder with a `.textbundle` name suffix and
a predefined folder hierarchy. The Markdown text is always in a file `text.md`,
all referenced assets (images, videos, etc.) are located in a subfolder named
`assets/` and a file `info.json` (obviously in JSON format) provides some meta
data.

## Dependency

This plugin needs [Markdown](https://pypi.python.org/pypi/Markdown) to work.
Install it with:

```
pip install Markdown
```

## Installation and configuration

Install the textbundle plugin and add it to the `PLUGINS` setting in
`pelicanconf.py`:

```
PLUGINS = [
    'textbundle',
     ...
    ]
```

Furthermore the content of the `ARTICLE_PATHS` setting has to be appended to the
`STATIC_PATHS` list.

```
ARTICLE_PATHS = ['posts']
...
STATIC_PATHS = [
    'posts',
     ...
    ]
```

The output content pages has to be generated into files `index.html` inside the
folder named after the page slug or article slug. This way the assets can be
placed next to the content file and do not interfere with asset files of other
textbundles.

A working example of article/page slugs and output URLs are:

```
ARTICLE_URL = 'post/{slug}/'
ARTICLE_SAVE_AS = 'post/{slug}/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
```

## Usage

Inside a Markdown file (the file `text.md` in a textbundle) the files from the
`assets/` folder are referenced using relative pathnames and the `{attach}`
suffix, as described in the [pelican documentation][pelican-docs], section
"Linking to static files".

An article with the slug "my-blog-post" and an image named `screenshot.png` in
the `assets/` folder contains a link like this:

```
![alt text]({attach}assets/screenshot.png "title text")
```

Assuming the above mentioned settings in `pelicanconf.py` the following files
are generated in the output folder:

* posts/my-blog-post/index.html
* posts/my-blog-post/assets/screenshot.png

Further examples can be found in my personal blog ([GitHub][niebegegnet-gh],
[Link][niebegegnet-blog]).

### Generating the boilerplate

To create a new post I have a shell function `new_post` defined in `~/.bashrc` or
`~/.zshrc`. Running

```
new_post "My next blogpost"
```

at the shell prompt creates the file structure of a textbundle in the posts dir
of my blog project. The code can be found in my [new_post
gist](https://gist.github.com/DirkR/aabb1b6fa97ff92ed86a).  The path names
are hardcoded as it's quite easy to adopt the script to one's personal needs.

[pelican-docs]: http://docs.getpelican.com/en/latest/content.html#linking-to-static-files
[niebegegnet-gh]: https://github.com/DirkR/niebegeg.net
[niebegegnet-blog]: https://niebegeg.net
