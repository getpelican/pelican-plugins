# CommonMark for Pelican

This reader plugin replaces the markdown reader with one that uses the
[Python parser for CommonMark][1].

It is useful if you want to use the [CommonMark][2] way of parsing markdown
inside non-trivial nested HTML tags. It is not useful if you want to
use the extensions available to the python markdown parser.

## Requirements

The plugin uses the CommonMark python package. It can be installed
with the following command:

    pip install -r REQUIREMENTS

[1]: https://pypi.python.org/pypi/CommonMark
[2]: http://commonmark.org
