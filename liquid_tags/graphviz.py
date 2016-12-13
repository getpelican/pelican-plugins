"""
GraphViz Tag
---------
This implements a Liquid-style graphviz tag for Pelican. You can use different
Graphviz programs like dot, neato, twopi etc. [1]


[1] http://www.graphviz.org/

Syntax
------
{% graphviz
    <program> {
        <DOT code>
    }
%}

Examples
--------
{% graphviz
    dot {
        digraph graphname {
            a -> b -> c;
            b -> d;
        }
    }
%}


{% graphviz
    twopi {
        <code goes here>
    }
%}


{% graphviz
    neato {
        <code goes here>
    }
%}

...


Output
------
<span class="graphviz" style="text-align: center;"><img src="data:image/png;base64,_BASE64_IMAGE DATA_/></span>

"""

import base64
import re
from .mdx_liquid_tags import LiquidTags

SYNTAX = '{% dot graphviz [program] [dot code] %}'
DOT_BLOCK_RE = re.compile(r'^\s*(?P<program>\w+)\s*\{\s*(?P<code>.*\})\s*\}$', re.MULTILINE | re.DOTALL)


def run_graphviz(program, code, options=[], format='png'):
    """ Runs graphviz programs and returns image data

        Copied from https://github.com/tkf/ipython-hierarchymagic/blob/master/hierarchymagic.py
    """
    import os
    from subprocess import Popen, PIPE

    dot_args = [program] + options + ['-T', format]

    if os.name == 'nt':
        # Avoid opening shell window.
        # * https://github.com/tkf/ipython-hierarchymagic/issues/1
        # * http://stackoverflow.com/a/2935727/727827
        p = Popen(dot_args, stdout=PIPE, stdin=PIPE, stderr=PIPE, creationflags=0x08000000)
    else:
        p = Popen(dot_args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        wentwrong = False

    try:
        # Graphviz may close standard input when an error occurs,
        # resulting in a broken pipe on communicate()
        stdout, stderr = p.communicate(code.encode('utf-8'))
    except (OSError, IOError) as err:
        if err.errno != EPIPE:
            raise
        wentwrong = True
    except IOError as err:
        if err.errno != EINVAL:
            raise
        wentwrong = True

    if wentwrong:
    # in this case, read the standard output and standard error streams
    # directly, to get the error message(s)
        stdout, stderr = p.stdout.read(), p.stderr.read()
        p.wait()

    if p.returncode != 0:
        raise RuntimeError('dot exited with error:\n[stderr]\n{0}'.format(stderr.decode('utf-8')))

    return stdout


@LiquidTags.register('graphviz')
def graphviz_parser(preprocessor, tag, markup):
    """ Simple Graphviz parser """

    # Parse the markup string
    m = DOT_BLOCK_RE.search(markup)
    if m:
        # Get program and DOT code
        code = m.group('code')
        program = m.group('program').strip()

        # Run specified program with our markup
        output = run_graphviz(program, code)

        # Return Base64 encoded image
        return '<span class="graphviz" style="text-align: center;"><img src="data:image/png;base64,%s"></span>' % base64.b64encode(output).decode('utf-8')
    else:
        raise ValueError('Error processing input. '
                         'Expected syntax: {0}'.format(SYNTAX))

#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from .liquid_tags import register

