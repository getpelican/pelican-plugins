"""
Include Code Tag
----------------
This implements a Liquid-style video tag for Pelican,
based on the octopress video tag [1]_

Syntax
------
{% include_code path/to/code [lang:python] [Title text] %}

The "path to code" is specified relative to the ``code`` subdirectory of
the content directory  Optionally, this subdirectory can be specified in the
config file:

    CODE_DIR = 'code'

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


SYNTAX = "{% include_code /path/to/code.py [lang:python] [title] %}"
FORMAT = re.compile(r"""^(?:\s+)?(?P<src>\S+)(?:\s+)?(?:(?:lang:)(?P<lang>\S+))?(?:\s+)?(?P<title>.+)?$""")


@LiquidTags.register('include_code')
def include_code(preprocessor, tag, markup):
    title = None
    lang = None
    src = None

    match = FORMAT.search(markup)
    if match:
        argdict = match.groupdict()
        title = argdict['title']
        lang = argdict['lang']
        src = argdict['src']

    if not src:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    settings = preprocessor.configs.config['settings']
    code_dir = settings.get('CODE_DIR', 'code')
    code_path = os.path.join('content', code_dir, src)

    if not os.path.exists(code_path):
        raise ValueError("File {0} could not be found".format(code_path))

    code = open(code_path).read()

    if title:
        title = "{0} {1}".format(title, os.path.basename(src))
    else:
        title = os.path.basename(src)

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
              + '\n    '.join(code.split('\n')) + '\n\n'
              + close_tag + '\n')

    return source


#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
