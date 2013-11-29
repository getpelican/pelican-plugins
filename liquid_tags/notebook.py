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

Requirements
------------
- The plugin requires IPython version 1.0 or above.  It no longer supports the
  standalone nbconvert package, which has been deprecated.

Details
-------
Because the notebook relies on some rather extensive custom CSS, the use of
this plugin requires additional CSS to be inserted into the blog theme.
After typing "make html" when using the notebook tag, a file called
``_nb_header.html`` will be produced in the main directory.  The content
of the file should be included in the header of the theme.  An easy way
to accomplish this is to add the following lines within the header template
of the theme you use:

    {% if EXTRA_HEADER %}
      {{ EXTRA_HEADER }}
    {% endif %}

and in your ``pelicanconf.py`` file, include the line:

    EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

this will insert the appropriate CSS.  All efforts have been made to ensure
that this CSS will not override formats within the blog theme, but there may
still be some conflicts.
"""
import re
import os
from .mdx_liquid_tags import LiquidTags

from distutils.version import LooseVersion
import IPython
if not LooseVersion(IPython.__version__) >= '1.0':
    raise ValueError("IPython version 1.0+ required for notebook tag")

from IPython import nbconvert

from IPython.nbconvert.filters.highlight import _pygment_highlight
from pygments.formatters import HtmlFormatter

from IPython.nbconvert.exporters import HTMLExporter
from IPython.config import Config

from IPython.nbformat import current as nbformat

try:
    from IPython.nbconvert.transformers import Transformer
except ImportError:
    raise ValueError("IPython version 2.0 is not yet supported")

from IPython.utils.traitlets import Integer
from copy import deepcopy

from jinja2 import DictLoader


#----------------------------------------------------------------------
# Some code that will be added to the header:
#  Some of the following javascript/css include is adapted from
#  IPython/nbconvert/templates/fullhtml.tpl, while some are custom tags
#  specifically designed to make the results look good within the
#  pelican-octopress theme.
JS_INCLUDE = r"""
<style type="text/css">
/* Overrides of notebook CSS for static HTML export */
div.entry-content {
  overflow: visible;
  padding: 8px;
}
.input_area {
  padding: 0.2em;
}

a.heading-anchor {
 white-space: normal;
}

.rendered_html
code {
 font-size: .8em;
}

pre.ipynb {
  color: black;
  background: #f7f7f7;
  border: none;
  box-shadow: none;
  margin-bottom: 0;
  padding: 0;
  margin: 0px;
  font-size: 13px;
}

img.anim_icon{padding:0; border:0; vertical-align:middle; -webkit-box-shadow:none; -box-shadow:none}
</style>

<script src="https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS_HTML" type="text/javascript"></script>
<script type="text/javascript">
init_mathjax = function() {
    if (window.MathJax) {
        // MathJax loaded
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
            },
            displayAlign: 'left', // Change this to 'center' to center equations.
            "HTML-CSS": {
                styles: {'.MathJax_Display': {"margin": 0}}
            }
        });
        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    }
}
init_mathjax();
</script>
"""

CSS_WRAPPER = """
<style type="text/css">
{0}
</style>
"""


#----------------------------------------------------------------------
# Create a custom transformer
class SliceIndex(Integer):
    """An integer trait that accepts None"""
    default_value = None

    def validate(self, obj, value):
        if value is None:
            return value
        else:
            return super(SliceIndex, self).validate(obj, value)


class SubCell(Transformer):
    """A transformer to select a slice of the cells of a notebook"""
    start = SliceIndex(0, config=True,
                       help="first cell of notebook to be converted")
    end = SliceIndex(None, config=True,
                     help="last cell of notebook to be converted")

    def call(self, nb, resources):
        nbc = deepcopy(nb)
        for worksheet in nbc.worksheets :
            cells = worksheet.cells[:]
            worksheet.cells = cells[self.start:self.end]
        return nbc, resources


#----------------------------------------------------------------------
# Customize the html template:
#  This changes the <pre> tags in basic_html.tpl to <pre class="ipynb"
pelican_loader = DictLoader({'pelicanhtml.tpl':
"""
{%- extends 'basichtml.tpl' -%}

{% block stream_stdout -%}
<div class="box-flex1 output_subarea output_stream output_stdout">
<pre class="ipynb">{{output.text |ansi2html}}</pre>
</div>
{%- endblock stream_stdout %}

{% block stream_stderr -%}
<div class="box-flex1 output_subarea output_stream output_stderr">
<pre class="ipynb">{{output.text |ansi2html}}</pre>
</div>
{%- endblock stream_stderr %}

{% block pyerr -%}
<div class="box-flex1 output_subarea output_pyerr">
<pre class="ipynb">{{super()}}</pre>
</div>
{%- endblock pyerr %}

{%- block data_text %}
<pre class="ipynb">{{output.text | ansi2html}}</pre>
{%- endblock -%}
"""})


#----------------------------------------------------------------------
# Custom highlighter:
#  instead of using class='highlight', use class='highlight-ipynb'
def custom_highlighter(source, language='ipython'):
    formatter = HtmlFormatter(cssclass='highlight-ipynb')
    output = _pygment_highlight(source, formatter, language)
    return output.replace('<pre>', '<pre class="ipynb">')


#----------------------------------------------------------------------
# Below is the pelican plugin code.
#
SYNTAX = "{% notebook /path/to/notebook.ipynb [ cells[start:end] ] %}"
FORMAT = re.compile(r"""^(\s+)?(?P<src>\S+)(\s+)?((cells\[)(?P<start>-?[0-9]*):(?P<end>-?[0-9]*)(\]))?(\s+)?$""")


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
        start = 0

    if end:
        end = int(end)
    else:
        end = None

    settings = preprocessor.configs.config['settings']
    nb_dir =  settings.get('NOTEBOOK_DIR', 'notebooks')
    nb_path = os.path.join('content', nb_dir, src)

    if not os.path.exists(nb_path):
        raise ValueError("File {0} could not be found".format(nb_path))

    # Create the custom notebook converter
    c = Config({'CSSHTMLHeaderTransformer':
                    {'enabled':True, 'highlight_class':'.highlight-ipynb'},
                'SubCell':
                    {'enabled':True, 'start':start, 'end':end}})

    exporter = HTMLExporter(config=c,
                            template_file='basic',
                            filters={'highlight2html': custom_highlighter},
                            transformers=[SubCell],
                            extra_loaders=[pelican_loader])

    # read and parse the notebook
    with open(nb_path) as f:
        nb_text = f.read()
    nb_json = nbformat.reads_json(nb_text)
    (body, resources) = exporter.from_notebook_node(nb_json)

    # if we haven't already saved the header, save it here.
    if not notebook.header_saved:
        print ("\n ** Writing styles to _nb_header.html: "
               "this should be included in the theme. **\n")

        header = '\n'.join(CSS_WRAPPER.format(css_line)
                           for css_line in resources['inlining']['css'])
        header += JS_INCLUDE

        with open('_nb_header.html', 'w') as f:
            f.write(header)
        notebook.header_saved = True

    # this will stash special characters so that they won't be transformed
    # by subsequent processes.
    body = preprocessor.configs.htmlStash.store(body, safe=True)
    return body

notebook.header_saved = False


#----------------------------------------------------------------------
# This import allows notebook to be a Pelican plugin
from liquid_tags import register
