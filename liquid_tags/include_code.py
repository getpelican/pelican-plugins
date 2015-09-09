"""
Include Code Tag
----------------
This implements a Liquid-style video tag for Pelican,
based on the octopress video tag [1]_

Syntax
------
{% include_code path/to/code [lang:python] [Title text] [codec:utf8] %}

The "path to code" is specified relative to the ``code`` subdirectory of
the content directory  Optionally, this subdirectory can be specified in the
config file:

    CODE_DIR = 'code'

If your input file is not ASCII/UTF-8 encoded, you need to specify the
appropriate input codec by using the ``codec`` option.
Example ``codec:iso-8859-1``
Using this option does not affect the output encoding.

For a list of valid codec identifiers, see
https://docs.python.org/2/library/codecs.html#standard-encodings

Example
-------
{% include_code myscript.py %}

This will import myscript.py from content/code/myscript.py
and output the contents in a syntax highlighted code block inside a figure,
with a figcaption listing the file name and download link.

The file link will be valid only if the 'code' directory is listed
in the STATIC_PATHS setting, e.g.:

    STATIC_PATHS = ['images', 'code']

[1] https://github.com/imathis/octopress/blob/master/plugins/include_code.rb
"""
import re
import os
from .mdx_liquid_tags import LiquidTags


SYNTAX = "{% include_code /path/to/code.py [lang:python] [lines:X-Y] [:hidefilename:] [title] %}"
FORMAT = re.compile(r"""
^(?:\s+)?                          # Allow whitespace at beginning
(?P<src>\S+)                       # Find the path
(?:\s+)?                           # Whitespace
(?:(?:lang:)(?P<lang>\S+))?        # Optional language
(?:\s+)?                           # Whitespace
(?:(?:lines:)(?P<lines>\d+-\d+))?  # Optional lines
(?:\s+)?                           # Whitespace
(?P<hidefilename>:hidefilename:)?  # Hidefilename flag
(?:\s+)?                           # Whitespace
(?:(?:codec:)(?P<codec>\S+))?        # Optional language
(?:\s+)?                           # Whitespace
(?P<title>.+)?$                    # Optional title
""", re.VERBOSE)


@LiquidTags.register('include_code')
def include_code(preprocessor, tag, markup):

    title = None
    lang = None
    src = None

    match = FORMAT.search(markup)
    if match:
        argdict = match.groupdict()
        title = argdict['title'] or ""
        lang = argdict['lang']
        codec = argdict['codec'] or "utf8"
        lines = argdict['lines']
        hide_filename = bool(argdict['hidefilename'])
        if lines:
            first_line, last_line = map(int, lines.split("-"))
        src = argdict['src']

    if not src:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    code_dir = preprocessor.configs.getConfig('CODE_DIR')
    code_path = os.path.join('content', code_dir, src)

    if not os.path.exists(code_path):
        raise ValueError("File {0} could not be found".format(code_path))

    with open(code_path) as fh:
        if lines:
            code = fh.readlines()[first_line - 1: last_line]
            code[-1] = code[-1].rstrip()
            code = "".join(code)
        else:
            code = fh.read()

    if not title and hide_filename:
        raise ValueError("Either title must be specified or filename must "
                         "be available")

    if not hide_filename:
        title += " %s" % os.path.basename(src)
    if lines:
        title += " [Lines %s]" % lines
    title = title.strip()

    url = '/{0}/{1}'.format(code_dir, src)
    url = re.sub('/+', '/', url)

    open_tag = ("<figure class='code'>\n<figcaption><span>{title}</span> "
                "<a href='{url}'>download</a></figcaption>".format(title=title,
                                                                   url=url))
    close_tag = "</figure>"

    # store HTML tags in the stash.  This prevents them from being
    # modified by markdown.
    open_tag = preprocessor.configs.htmlStash.store(open_tag, safe=True)
    close_tag = preprocessor.configs.htmlStash.store(close_tag, safe=True)

    if lang:
        lang_include = ':::' + lang + '\n    '
    else:
        lang_include = ''

    source = (open_tag
              + '\n\n    '
              + lang_include
              + '\n    '.join(code.decode(codec).split('\n')) + '\n\n'
              + close_tag + '\n')

    return source


#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
