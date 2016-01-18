#-*- conding: utf-8 -*-

import os
import warnings

from pelican import readers
from pelican import signals
from pelican import settings
from pelican.utils import pelican_open
from markdown import Markdown

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from rpy2.robjects.packages import importr
    knitr = importr('knitr')
    idx = knitr.opts_knit.names.index('set')
    knitr.opts_knit[idx](**{'base.dir': '{0}/content'.format(settings.DEFAULT_CONFIG.get('PATH'))})
    rmd = True
except ImportError:
    rmd = False

class RmdReader(readers.BaseReader):
    enabled = rmd
    file_extensions = ['Rmd', 'rmd']

    # You need to have a read method, which takes a filename and returns
    # some content and the associated metadata.
    def read(self, filename):
        """Parse content and metadata of markdown files"""
        # replace single backslashes with double backslashes
        filename = filename.replace('\\', '\\\\')
        # parse Rmd file - generate md file
        md_filename = filename.replace('.Rmd', '.aux').replace('.rmd', '.aux')
        knitr.knit(filename, md_filename, quiet=True, encoding='UTF-8')
        # read md file - create a MarkdownReader
        md_reader = readers.MarkdownReader(self.settings)
        content, metadata = md_reader.read(md_filename)
        # remove md file
        os.remove(md_filename)
        return content, metadata

def add_reader(readers):
    readers.reader_classes['rmd'] = RmdReader

def register():
    signals.readers_init.connect(add_reader)
