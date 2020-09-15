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
import sys
from .mdx_liquid_tags import LiquidTags


SYNTAX = "{% include_code /path/to/code.py [lang:python] [lines:X-Y] "\
         "[:hidefilename:] [:hidelink:] [:hideall:] [title] %}"
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
(?P<hidelink>:hidelink:)?          # Hide download link
(?:\s+)?                           # Whitespace
(?P<hideall>:hideall:)?            # Hide title and download link
(?:\s+)?                           # Whitespace
(?:(?:codec:)(?P<codec>\S+))?      # Optional language
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
        hide_link = bool(argdict['hidelink'])
        hide_all = bool(argdict['hideall'])
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

    if not codec:
        codec = 'utf-8'

    with open(code_path, encoding=codec) as fh:
        if lines:
            code = fh.readlines()[first_line - 1: last_line]
            code[-1] = code[-1].rstrip()
            code = "".join(code)
        else:
            code = fh.read()

    if (not title and hide_filename) and not hide_all:
        raise ValueError("Either title must be specified or filename must "
                         "be available")

    open_tag = "<figure class='code'>\n"
    close_tag = "</figure>"

    if not hide_all:
        open_tag+= "<figcaption>"

        if title:
            open_tag += "<span class=\"liquid-tags-code-title\">{title}</span>".format(title=title.strip())

        if not hide_filename:
            filename = "%s" % os.path.basename(src)
            open_tag += "<span class=\"liquid-tags-code-filename\">{filename}</span>".format(filename=filename.strip())

        if lines:
            lines = " [Lines %s]" % lines
            open_tag += "<span class=\"liquid-tags-code-lines\">{lines}</span>".format(lines=lines.strip())

        if not hide_link:
            url = '/{0}/{1}'.format(code_dir, src)
            url = re.sub('/+', '/', url)
            open_tag += "<a href='{url}'>download</a>".format(url=url)

        open_tag += "</figcaption>"

    # store HTML tags in the stash.  This prevents them from being
    # modified by markdown.
    open_tag = preprocessor.configs.htmlStash.store(open_tag)
    close_tag = preprocessor.configs.htmlStash.store(close_tag)

    if lang:
        lang_include = ':::' + lang + '\n    '
    else:
        lang_include = ''

    if sys.version_info[0] < 3:
        source = (open_tag
                  + '\n\n    '
                  + lang_include
                  + '\n    '.join(code.decode(codec).split('\n')) + '\n\n'
                  + close_tag + '\n')
    else:
        source = (open_tag
                  + '\n\n    '
                  + lang_include
                  + '\n    '.join(code.split('\n')) + '\n\n'
                  + close_tag + '\n')

    return source


#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
