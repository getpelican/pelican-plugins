# YUI Compressor Plugin

A pelican plugin that minifies CSS/JS files using YUI Compressor during the
building step.

# Installation

YUI Compressor needs to be present on your system. One way to obtain it is by
installing it using pip:

Important: This method assumes that JRE is already installed.

```bash
pip install yuicompressor
```

More information about YUI Compressor: https://github.com/yui/yuicompressor

# Instructions

Add `yuicompressor` to `pelicanconf.py` after installing YUI Compressor:

```python
PLUGINS = ['yuicompressor']
```

By default, this plugin expects the YUI Compressor executable to be named
`yuicompressor`. This can be changed by defining `YUICOMPRESSOR_EXECUTABLE` in
`pelicanconf.py`:

```python
YUICOMPRESSOR_EXECUTABLE = 'yui-compressor'
```

# Licence

GNU AFFERO GENERAL PUBLIC LICENSE Version 3
