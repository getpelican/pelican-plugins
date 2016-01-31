#-*- conding: utf-8 -*-

import os
import warnings
import logging

logger = logging.getLogger(__name__)

from pelican import readers
from pelican import signals
from pelican import settings
from pelican.utils import pelican_open
from markdown import Markdown

knitr = None
rmd = False

def initsignal(pelicanobj):
    global knitr,rmd
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from rpy2.robjects.packages import importr
        knitr = importr('knitr')
        idx = knitr.opts_knit.names.index('set')
        PATH = pelicanobj.settings.get('PATH','%s/content' % settings.DEFAULT_CONFIG.get('PATH'))
        logger.debug("RMD_READER PATH = %s", PATH)
        knitr.opts_knit[idx](**{'base.dir': PATH})
        idx = knitr.opts_chunk.names.index('set')
        knitroptschunk = pelicanobj.settings.get('RMD_READER_KNITR_OPTS_CHUNK', None)
        if knitroptschunk is not None:     
            knitr.opts_chunk[idx](**{str(k): v for k,v in knitroptschunk.iteritems()})
        rmd = True
    except ImportError as ex:
        rmd = False
    
class RmdReader(readers.BaseReader):
    file_extensions = ['Rmd', 'rmd']
    
    @property
    def enabled():
        global rmd
        return rmd

    # You need to have a read method, which takes a filename and returns
    # some content and the associated metadata.
    def read(self, filename):
        """Parse content and metadata of markdown files"""
        global knitr
        QUIET = self.settings.get('RMD_READER_KNITR_QUIET', True)
        ENCODING = self.settings.get('RMD_READER_KNITR_ENCODING', 'UTF-8')
        CLEANUP = self.settings.get('RMD_READER_CLEANUP', True)
        logger.debug("RMD_READER_KNITR_QUIET = %s", QUIET)
        logger.debug("RMD_READER_KNITR_QUIET = %s", ENCODING)
        logger.debug("RMD_READER_CLEANUP = %s", CLEANUP)
        # replace single backslashes with double backslashes
        filename = filename.replace('\\', '\\\\')
        # parse Rmd file - generate md file
        md_filename = filename.replace('.Rmd', '.aux').replace('.rmd', '.aux')
        knitr.knit(filename, md_filename, quiet=QUIET, encoding=ENCODING)
        # read md file - create a MarkdownReader
        md_reader = readers.MarkdownReader(self.settings)
        content, metadata = md_reader.read(md_filename)
        # remove md file
        if CLEANUP:
            os.remove(md_filename)
        return content, metadata

def add_reader(readers):
    readers.reader_classes['rmd'] = RmdReader

def register():
    signals.readers_init.connect(add_reader)
    signals.initialized.connect(initsignal)
