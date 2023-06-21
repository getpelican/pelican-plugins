# -*- coding: utf-8 -*-

"""
Yaml plugin for pelican
=======================
Ian Barton: ian@manor-farm.org
Based on my original code:
See: http://www.ian-barton.com/posts/2013/Apr/06/blogging-with-emacs-org-mode-and-pelican/

Thanks to bas@baslab, who turned my original code into a plugin and also to
contact@saimon.org, who fixed the problems I was having with unicode.
"""

from __future__ import unicode_literals

import os
import logging
import datetime
import six

from pelican import signals
from pelican.readers import EXTENSIONS, Reader
from pelican.utils import pelican_open

try:
    import yaml
    Yaml = True # NOQA
except ImportError:
    Yaml = False # NOQA

class YamlReader(Reader):
    enabled = bool(yaml)
    file_extensions = ['yml']

    def read(self, filename):
        """Parse content and metadata of YAML files"""

        with pelican_open(filename) as source:
            _, yml_meta, content = source.split('---', 2)

        md = yaml.load(yml_meta)
        metadata = {}

        for key, value in md.items():
            name = key.lower()

            if name == "tags":
                if isinstance(value, list):
                    value = ",".join(value)

                metadata[name] = self.process_metadata(name, value)
            elif name == 'date':
                # yaml returns date as a datetime.date object.
                if isinstance(name, six.string_types):
                    metadata[name] = self.process_metadata(name, unicode(value))
                elif isinstance(name, datetime.date):
                    metadata[name] = datetime.combine(value, datetime.time(0))
                elif isinstance(name, datetime.datetime):
                    metadata[name] = value
                # else: TODO
                #     logger.warning
            else:
                metadata[name] = self.process_metadata(name, unicode(value))

        return content, metadata


def get_generators(generators):
    # define a new generator here if you need to
    return generators

def add_reader(arg):
    EXTENSIONS['yml'] = YamlReader

def register():
    signals.get_generators.connect(get_generators)
    signals.initialized.connect(add_reader)
