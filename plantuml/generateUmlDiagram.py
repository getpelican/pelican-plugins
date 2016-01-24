#!/usr/bin/env python
import logging
import os
import tempfile
from zlib import adler32
from subprocess import Popen, PIPE
from pelican import logger


def generate_uml_image(path, plantuml_code, imgformat):
    tf = tempfile.NamedTemporaryFile(delete=False)
    tf.write('@startuml\n'.encode('utf8'))
    tf.write(plantuml_code.encode('utf8'))
    tf.write('\n@enduml'.encode('utf8'))
    tf.flush()

    logger.debug("[plantuml] Temporary PlantUML source at "+(tf.name))

    if imgformat == 'png':
        imgext = ".png"
        outopt = "-tpng"
    elif imgformat == 'svg':
        imgext = ".svg"
        outopt = "-tsvg"
    else:
        logger.error("Bad uml image format '"+imgformat+"', using png")
        imgext = ".png"
        outopt = "-tpng"

    # make a name
    name = tf.name+imgext
    # build cmd line
    cmdline = ['plantuml', '-o', path, outopt, tf.name]

    try:
        logger.debug("[plantuml] About to execute "+" ".join(cmdline))
        p = Popen(cmdline, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
    except Exception as exc:
        raise Exception('Failed to run plantuml: %s' % exc)
    else:
        if p.returncode == 0:
            # diagram was correctly generated, we can remove the temporary file (if not debugging)
            if not logger.isEnabledFor(logging.DEBUG):
                os.remove(tf.name)
            # renaming output image using an hash code, just to not pollute
            # output directory with a growing number of images
            name = os.path.join(path, os.path.basename(name))
            newname = os.path.join(path, "%08x" % (adler32(plantuml_code.encode()) & 0xffffffff))+imgext

            if os.path.exists(newname):
                os.remove(newname)

            os.rename(name, newname)
            return 'images/' + os.path.basename(newname)
        else:
            # the temporary file is still available as aid understanding errors
            raise RuntimeError('Error calling plantuml: %s' % err)
