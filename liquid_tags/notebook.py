"""
Notebook Tag
------------
This is a liquid-style tag to include a static html rendering of an IPython
notebook in a blog post.

Syntax
------
{% notebook filename.ipynb %}

The file should be specified relative to the ``notebook`` subdirectory of the
content directory.  [TODO: make this configurable].
This will include the IPython notebook in the file.

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

      {% if IPYNB_FORMATTING %}
        {{ IPYNB_FORMATTING }}
      {% endif %}

  and in your ``pelicanconf.py`` file, include the line:

      IPYNB_FORMATTING = open('_nb_header.html').read().decode('utf-8')

[1] https://github.com/ipython/nbconvert
"""
import re
import os
from .mdx_liquid_tags import LiquidTags
from converters import ConverterBloggerHTML  # part of the nbconvert package

SYNTAX = "{% notebook /path/to/notebook.ipynb %}"
FORMAT = re.compile(r"""^(?:\s+)?(?P<src>\S+)(?:\s+)?$""")


def process_body(body):
    body = '\n'.join(body)

    # replace the highlight tags
    body = body.replace('class="highlight"', 'class="highlight-ipynb"')

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

    # specify <pre> tags
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
    header = header.replace('body {', 'div.ipynb {')

    # specialize headers
    header = header.replace('html, body,',
                            '\n'.join((('h1.ipynb h2.ipynb h3.ipynb '
                                        'h4.ipynb h5.ipynb h6.ipynb {'),
                                       'h1.ipynb h2.ipynb ... {',
                                       '  margin: 0;',
                                       '  padding: 0;',
                                       '  border: 0;',
                                       '  font-size: 100%;',
                                       '  font: inherit;',
                                       '  vertical-align: baseline;',
                                       '}\n',
                                       'html, body,')))

    header = header.replace('html, body,',
                            '/*html, body,*/')
    header = header.replace('h1, h2, h3, h4, h5, h6,',
                            '/*h1, h2, h3, h4, h5, h6,*/')

    return header.split('\n')


@LiquidTags.register('notebook')
def notebook(preprocessor, tag, markup):
    match = FORMAT.search(markup)
    if match:
        argdict = match.groupdict()
        src = argdict['src']
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    # TODO: make the notebook directory a configurable setting
    nb_dir = 'notebooks'
    nb_path = os.path.join('content', nb_dir, src)
    url = '/{0}/{1}/{2}'.format('static', nb_dir, src)

    if not os.path.exists(nb_path):
        raise ValueError("File {0} could not be found".format(nb_path))

    # Call the notebook converter
    converter = ConverterBloggerHTML(nb_path)
    converter.read()

    header_lines = process_header(converter.header_body())
    
    print ("\n *** Writing styles to _nb_header.html: "
           "this should be included in the theme.\n")
    open('_nb_header.html', 'w').write('\n'.join(header_lines).encode('utf-8'))

    body_lines = process_body(converter.main_body('\n'))

    body = preprocessor.configs.htmlStash.store('\n'.join(body_lines),
                                                safe=True)
    return body


#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
