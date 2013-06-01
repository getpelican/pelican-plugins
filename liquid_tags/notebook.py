"""
Notebook Tag
------------
This is a liquid-style tag to include a static html rendering of an IPython
notebook in a blog post.

Syntax
------
{% notebook filename.ipynb [ cells[start:end] ]%}

The file should be specified relative to the ``notebooks`` subdirectory of the
content directory.  Optionally, this subdirectory can be specified in the
config file:

    NOTEBOOK_DIR = 'notebooks'

The cells[start:end] statement is optional, and can be used to specify which
block of cells from the notebook to include.

Details
-------
Because the conversion and formatting of notebooks is rather involved, there
are a few extra steps required for this plugin:

- First, the plugin requires that the nbconvert package [1]_ to be in the
  python path. For example, in bash, this can be set via

      >$ export PYTHONPATH=/path/to/nbconvert/

- After typing "make html" when using the notebook tag, a file called
  ``_nb_header.html`` will be produced in the main directory.  The content
  of the file should be included in the header of the theme.  An easy way
  to accomplish this is to add the following lines within the header template
  of the theme you use:

      {% if EXTRA_HEADER %}
        {{ EXTRA_HEADER }}
      {% endif %}

  and in your ``pelicanconf.py`` file, include the line:

      EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

[1] https://github.com/ipython/nbconvert
"""
import re
import os
from .mdx_liquid_tags import LiquidTags

# nbconverters: part of the nbconvert package
from converters import ConverterBloggerHTML  # requires nbconvert package
separate_available = False

SYNTAX = "{% notebook /path/to/notebook.ipynb [ cells[start:end] ] %}"
FORMAT = re.compile(r"""^(\s+)?(?P<src>\S+)(\s+)?((cells\[)(?P<start>-?[0-9]*):(?P<end>-?[0-9]*)(\]))?(\s+)?$""")


def process_body(body):
    body = '\n'.join(body)

    # replace the highlight tags
    body = body.replace('highlight', 'highlight-ipynb')

    # specify <pre> tags
    body = body.replace('<pre', '<pre class="ipynb"')

    # create a special div for notebook
    body = '<div class="ipynb">\n\n' + body + "\n\n</div>"

    # specialize headers
    for h in '123456':
        body = body.replace('<h%s' % h, '<h%s class="ipynb"' % h)
    
    return body.split('\n')


def process_header(header):
    header = '\n'.join(header)

    # replace the highlight tags
    header = header.replace('highlight', 'highlight-ipynb')

    # specify pre tags
    header = header.replace('html, body', '\n'.join(('pre.ipynb {',
                                                     '  color: black;',
                                                     '  background: #f7f7f7;',
                                                     '  border: 0;',
                                                     '  box-shadow: none;',
                                                     '  margin-bottom: 0;',
                                                     '  padding: 0;'
                                                     '}\n',
                                                     'html, body')))


    # create a special div for notebook
    R = re.compile(r'^body ?{', re.MULTILINE)
    header = R.sub('div.ipynb {', header)

    # specify all headers
    R = re.compile(r'^(h[1-6])', re.MULTILINE)
    repl = lambda match: '.ipynb ' + match.groups()[0]
    header = R.sub(repl, header)

    # substitude ipynb class for html and body modifiers
    header = header.replace('html, body', '.ipynb div,')

    return header.split('\n')


def strip_divs(body, start=None, end=None):
    """Strip divs from the body for partial notebook insertion

    If L represents the list of parsed main divs, then this returns
    the document corresponding to the divs L[start:end].

    body should be a list of lines in the body of the html file.
    """
    # TODO: this is a bit hackish.  It would be better to add a PR to
    #       nbconvert which does this at the source.
    DIV = re.compile('<div')
    UNDIV = re.compile('</div')

    # remove ipynb div
    body_lines = body[1:-1]
    
    # split divs
    L = []
    count = 0
    div_start = 0
    for i, line in enumerate(body_lines):
        if not line:
            continue
        count += len(DIV.findall(line))
        count -= len(UNDIV.findall(line))
        
        if count == 0:
            L.append(body_lines[div_start:i + 1])
            div_start = i + 1
        elif count < 0:
            raise ValueError("Fatal: parsing error -- lost a tag")

    # check that we've parsed to the end
    # the last line may be blank, so we check two conditions
    if div_start not in [len(body_lines), len(body_lines) - 1]:
        raise ValueError("parsing error: didn't find the end of the div")

    body_lines = sum(L[start:end], [])

    return body[:1] + body_lines + body[-1:]


@LiquidTags.register('notebook')
def notebook(preprocessor, tag, markup):
    match = FORMAT.search(markup)
    if match:
        argdict = match.groupdict()
        src = argdict['src']
        start = argdict['start']
        end = argdict['end']
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    if start:
        start = int(start)
    else:
        start = None

    if end:
        end = int(end)
    else:
        end = None

    settings = preprocessor.configs.config['settings']
    nb_dir =  settings.get('NOTEBOOK_DIR', 'notebooks')
    nb_path = os.path.join('content', nb_dir, src)

    if not os.path.exists(nb_path):
        raise ValueError("File {0} could not be found".format(nb_path))

    # Call the notebook converter
    converter = ConverterBloggerHTML(infile=nb_path)
    converter.read()

    header_lines = process_header(converter.header_body())
    body_lines = process_body(converter.main_body('\n'))
    
    if not notebook.header_saved:
        notebook.header_saved = True
        print ("\n *** Writing styles to _nb_header.html: "
               "this should be included in the theme.\n")
        lines = '\n'.join(header_lines).encode('utf-8')
        open('_nb_header.html', 'w').write(lines)

    body_lines = strip_divs(body_lines, start, end)

    body = preprocessor.configs.htmlStash.store('\n'.join(body_lines),
                                                safe=True)
    return body

notebook.header_saved = False


#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
