#-*- conding: utf-8 -*-

import os

from pelican import readers
from pelican import signals
from pelican import settings
from pelican.utils import pelican_open
from markdown import Markdown
try:
    from rpy2 import robjects
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
        robjects.r("""
require(knitr);
opts_knit$set(base.dir='{2}/content');
knit('{0}', '{1}', quiet=TRUE, encoding='UTF-8');
""".format(filename, md_filename, settings.DEFAULT_CONFIG.get('PATH')))
        md_reader = readers.MarkdownReader(self.settings)
        content, metadata = md_reader.read(md_filename)
        os.remove(md_filename)
        return content, metadata

def add_reader(readers):
    readers.reader_classes['rmd'] = RmdReader

def register():
    signals.readers_init.connect(add_reader)
