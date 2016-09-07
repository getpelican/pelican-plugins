"""
Blockdiag Tag
---------
This tag implements a liquid style tag for blockdiag [1].  You can use different
diagram types like blockdiag, seqdiag, packetdiag etc. [1]


[1] http://blockdiag.com/en/blockdiag/

Syntax
------
{% blockdiag {
        <diagramm type> {
            <CODE>
        }
    }
%}

Examples
--------
{% blockdiag {
        blockdiag {
          A -> B -> C;
          B -> D;
        }
    }
%}


{% blockdiag {
        actdiag {
          A -> B -> C -> D -> E;

          lane {
            A; C; E;
          }
          lane {
            B; D;
          }
        }
    }
%}


{% blockdiag {
        packetdiag {
           0-7: Source Port
           8-15: Destination Port
           16-31: Sequence Number
           32-47: Acknowledgment Number
        }
    }
%}

...


Output
------
<div class="blockdiag" style="align: center;"><img src="data:image/png;base64,_BASE64_IMAGE DATA_/></div>

"""

import io
import os
import sys

import base64
import re
from .mdx_liquid_tags import LiquidTags


SYNTAX = '{% blockdiag [diagram type] [code] %}'
DOT_BLOCK_RE = re.compile(r'^\s*(?P<diagram>\w+).*$', re.MULTILINE | re.DOTALL)

_draw_mode = 'PNG'
_publish_mode = 'PNG'


def get_diag(code, command):
    """ Generate diagramm and return data """
    import tempfile
    import shutil
    code = code + u'\n'

    try:
        tmpdir = tempfile.mkdtemp()
        fd, diag_name = tempfile.mkstemp(dir=tmpdir)

        f = os.fdopen(fd, "w")
        f.write(code.encode('utf-8'))
        f.close()

        format = _draw_mode.lower()
        draw_name = diag_name + '.' + format

        saved_argv = sys.argv
        argv = [diag_name, '-T', format, '-o', draw_name]

        if _draw_mode == 'SVG':
            argv += ['--ignore-pil']

        # Run command
        command.main(argv)

        # Read image data from file
        file_name = diag_name + '.' + _publish_mode.lower()

        with io.open(file_name, 'rb') as f:
            data = f.read()
            f.close()

    finally:
        for file in os.listdir(tmpdir):
            os.unlink(tmpdir + "/" + file)

        # os.rmdir will fail -> use shutil
        shutil.rmtree(tmpdir)

    return data


def diag(code, command):
    if command == "blockdiag":                      # blockdiag
        import blockdiag.command
        return get_diag(code, blockdiag.command)

    elif command == "diagram":                      # diagram
        import blockdiag.command
        return get_diag(code, blockdiag.command)

    elif command == "seqdiag":                      # seqdiag
        import seqdiag.command
        return get_diag(code, seqdiag.command)

    elif command == "actdiag":                      # actdiag
        import actdiag.command
        return get_diag(code, actdiag.command)

    elif command == "nwdiag":                       # nwdiag
        import nwdiag.command
        return get_diag(code, nwdiag.command)

    elif command == "packetdiag":                   # packetdiag
        import packetdiag.command
        return get_diag(code, packetdiag.command)

    elif command == "rackdiag":                     # racketdiag
        import rackdiag.command
        return get_diag(code, rackdiag.command)

    else:                                           # not found
        print("No such command %s" % command)
        return None


@LiquidTags.register("blockdiag")
def blockdiag_parser(preprocessor, tag, markup):
    """ Blockdiag parser """
    m = DOT_BLOCK_RE.search(markup)
    if m:
        # Get diagram type and code
        diagram = m.group('diagram').strip()
        code = markup

        # Run command
        output = diag(code, diagram)

        if output:
            # Return Base64 encoded image
            return '<div class="blockdiag" style="align: center;"><img src="data:image/png;base64,%s"></div>' % base64.b64encode(output)
    else:
        raise ValueError('Error processing input. '
                         'Expected syntax: {0}'.format(SYNTAX))

# This import allows image tag to be a Pelican plugin
from .liquid_tags import register
