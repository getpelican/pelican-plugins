# w3c_validate plugin

This is a plugin for Pelican that submits generated HTML content to the
[W3C Markup Validation Service](http://validator.w3.org/).

After all content is generated, the output folder is traversed for HTML files,
and the content is submitted to the W3C validator, after which the results
are displayed. For example:

    -> writing /tmp/_output/sitemap.xml
    -> Validating: /tmp/_output/archives.html
    ERROR: line: 2; col: 52; message: Bad value http://www.w3.org/1999/html for the attribute xmlns (only http://www.w3.
    -> Validating: /tmp/_output/categories.html
    ERROR: line: 2; col: 52; message: Bad value http://www.w3.org/1999/html for the attribute xmlns (only http://www.w3.

**Note**: The above output assumes you have called Pelican with the ``--debug``
flag. Otherwise, you will see errors (if any) but not the file currently being
validated.

## Dependencies

* [py_w3c](https://pypi.python.org/pypi/py_w3c/0.1.0), which can be installed with pip:

    $ pip install py_w3c
    
## Instructions

Add `w3c_validate` to your config file's plugins after installing dependencies - `PLUGINS = ['w3c_validate']`

## TODO

[ ] - add tests

