#!/usr/bin/env python
"""Custom reST_ directive for plantuml_ integration.
   Adapted from ditaa_rst plugin.

.. _reST: http://docutils.sourceforge.net/rst.html
.. _plantuml: http://plantuml.sourceforge.net/
"""

import os
import tempfile
from zlib import adler32
from subprocess import Popen, PIPE

from docutils.nodes import image, literal_block
from docutils.parsers.rst import Directive, directives
from docutils import utils, nodes

from pelican import logger, signals

global_siteurl = ""

class PlantUML(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = True
    
    global global_siteurl

    option_spec = {
        'class' : directives.class_option,
        'alt'   : directives.unchanged,
        'format': directives.unchanged,
    }

    def run(self):
	source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
	source_dir = os.path.dirname(os.path.abspath(source))
	source_dir = utils.relative_path(None, source_dir)

        path = os.path.abspath(os.path.join('output', 'images'))
        if not os.path.exists(path):
            os.makedirs(path)

        nodes = []

        body = '\n'.join(self.content)
        tf = tempfile.NamedTemporaryFile(delete=True)
        tf.write('@startuml\n')
        tf.write(body.encode('utf8'))
        tf.write('\n@enduml')
        tf.flush()
        
        imgformat = self.options.get('format', 'png')
        
        if imgformat == 'png':
            imgext = ".png"
            outopt = "-tpng"
        elif imgformat == 'svg':
            imgext = ".svg"
            outopt = "-tsvg"
        else:
	    logger.error("Bad uml image format: "+imgformat)

        # make a name
        name =  tf.name+imgext

        alt = self.options.get('alt', 'uml diagram')
        classes = self.options.pop('class', ['uml'])
        cmdline = ['plantuml', '-o', path, outopt, tf.name ]

        try:
            p = Popen(cmdline, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
        except Exception, exc:
            error = self.state_machine.reporter.error(
                'Failed to run plantuml: %s' % (exc, ),
                literal_block(self.block_text, self.block_text),
                line=self.lineno)
            nodes.append(error)
        else:
            if p.returncode == 0:
	        # renaming output image using an hash code, just to not pullate 
	        # output directory with a growing number of images
                name = os.path.join(path, os.path.basename(name))
	        newname = os.path.join(path, "%08x" % (adler32(body) & 0xffffffff))+imgext
	        
	        try: # for Windows
		    os.remove(newname)  
		except Exception, exc:
		    logger.debug('File '+newname+' does not exist, not deleted')
		
	        os.rename(name, newname)
                url = global_siteurl + '/images/' + os.path.basename(newname)
                imgnode = image(uri=url, classes=classes, alt=alt)
                nodes.append(imgnode)
            else:
                error = self.state_machine.reporter.error(
                    'Error in "%s" directive: %s' % (self.name, err),
                    literal_block(self.block_text, self.block_text),
                    line=self.lineno)
                nodes.append(error)

        return nodes

def custom_url(generator, metadata):
    global global_siteurl
    global_siteurl = generator.settings['SITEURL']
    
def register():
    """Plugin registration."""
    signals.article_generator_context.connect(custom_url)
    directives.register_directive('uml', PlantUML)
