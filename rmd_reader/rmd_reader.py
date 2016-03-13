#-*- conding: utf-8 -*-

import os
import warnings
import logging

logger = logging.getLogger('RMD_READER')

from pelican import readers
from pelican import signals
from pelican import settings

knitr = None
rmd = False

def initsignal(pelicanobj):
    global knitr, rmd, robjects
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from rpy2.robjects.packages import importr
            import rpy2.robjects as robjects
        knitr = importr('knitr')
        idx = knitr.opts_knit.names.index('set')
        PATH = pelicanobj.settings.get('PATH','%s/content' % settings.DEFAULT_CONFIG.get('PATH'))
        logger.debug("RMD_READER PATH = %s", PATH)
        knitr.opts_knit[idx](**{'base.dir': PATH})
        knitroptsknit = pelicanobj.settings.get('RMD_READER_KNITR_OPTS_KNIT', None)
        if knitroptsknit:
            knitr.opts_knit[idx](**{str(k): v for k,v in knitroptsknit.items()})
        idx = knitr.opts_chunk.names.index('set')
        knitroptschunk = pelicanobj.settings.get('RMD_READER_KNITR_OPTS_CHUNK', None)
        if knitroptschunk:
            knitr.opts_chunk[idx](**{str(k): v for k,v in knitroptschunk.items()})
        rmd = True
    except ImportError as ex:
        rmd = False
    
class RmdReader(readers.BaseReader):
    file_extensions = ['Rmd', 'rmd']
    
    @property
    def enabled():
        return rmd

    # You need to have a read method, which takes a filename and returns
    # some content and the associated metadata.
    def read(self, filename):
        """Parse content and metadata of markdown files"""
        QUIET = self.settings.get('RMD_READER_KNITR_QUIET', True)
        ENCODING = self.settings.get('RMD_READER_KNITR_ENCODING', 'UTF-8')
        CLEANUP = self.settings.get('RMD_READER_CLEANUP', True)
        RENAME_PLOT = self.settings.get('RMD_READER_RENAME_PLOT', True)
        logger.debug("RMD_READER_KNITR_QUIET = %s", QUIET)
        logger.debug("RMD_READER_KNITR_ENCODING = %s", ENCODING)
        logger.debug("RMD_READER_CLEANUP = %s", CLEANUP)
        logger.debug("RMD_READER_RENAME_PLOT = %s", RENAME_PLOT)
        # replace single backslashes with double backslashes
        filename = filename.replace('\\', '\\\\')
        # parse Rmd file - generate md file
        md_filename = filename.replace('.Rmd', '.aux').replace('.rmd', '.aux')
        if RENAME_PLOT:
            chunk_label = os.path.splitext(os.path.basename(filename))[0]
            logger.debug('Chunk label: %s', chunk_label)
            robjects.r('''
opts_knit$set(unnamed.chunk.label="{unnamed_chunk_label}")
render_markdown()
hook_plot <- knit_hooks$get('plot')
knit_hooks$set(plot=function(x, options) hook_plot(paste0("{{filename}}/", x), options))
            '''.format(unnamed_chunk_label=chunk_label))
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
