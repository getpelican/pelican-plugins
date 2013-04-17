# w3c_validate plugin

W3C validator (http://validator.w3.org) plugin for generated HTML content.

After all content is generated, output folder is traversed for HTML files, and
their content validated on W3C and the results displayed, for example:

    -> writing /tmp/_output/sitemap.xml
    -> Validating: /tmp/_output/archives.html
    ERROR: line: 2; col: 52; message: Bad value http://www.w3.org/1999/html for the attribute xmlns (only http://www.w3.org/1999/xhtml permitted here).
    -> Validating: /tmp/_output/categories.html
    ERROR: line: 2; col: 52; message: Bad value http://www.w3.org/1999/html for the attribute xmlns (only http://www.w3.org/1999/xhtml permitted here).

## Dependencies

* py_w3c, https://pypi.python.org/pypi/py_w3c/0.1.0 , which can be installed with pip:

    $ pip install py_w3c

## TODO

[ ] - add tests




