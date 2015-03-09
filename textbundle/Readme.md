# Textbundle Reader

This plugin helps you creating posts from Textbundles
(http://textbundle.org/spec/).

In anutshell a textbundle is a folder with a ".textbundle" name suffix and
a predefined folder hierarchy. The Markdown text is always in a file "text.md",
all referenced assets (images, videos, etc.) are located in a subfolder named
"assets/" and a file "info.json" (obviously in JSON format) provides some meta
data.

## Dependency

This plugin needs [Markdown](https://pypi.python.org/pypi/Markdown) to work.
Install it with:

```
pip install Markdown
```

## Usage

Install the textbundle plugin and add it to the PLUGINS setting:

```
PLUGINS = [
    'textbundle',
    ...
    ]
```
