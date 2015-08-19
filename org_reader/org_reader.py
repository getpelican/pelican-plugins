"""
Org Reader
==========

Version 1.0.

Relevant Pelican settings:

- ORG_READER_EMACS_LOCATION: Required. Location of Emacs binary.

- ORG_READER_EMACS_SETTINGS: Optional. An absolute path to an Elisp file, to
  run per invocation. Useful for initializing the `package` Emacs library if
  that's where your Org mode comes from, or any modifications to Org Export-
  related variables.

- ORG_READER_BACKEND: Optional. A custom backend to provide to Org. Defaults
  to 'html.

To provide metadata to Pelican, provide the following header in your Org file:

#+TITLE: The Title Of This BlogPost
#+DATE: 2001-01-01
#+CATEGORY: comma, separated, list, of, tags

The slug is automatically the filename of the Org file.
"""
import os
import json
import logging
import subprocess
from pelican import readers
from pelican import signals
from pelican import settings


ELISP = os.path.join(os.path.dirname(__file__), 'org_reader.el')
LOG = logging.getLogger(__name__)

class OrgReader(readers.BaseReader):
    enabled = True

    EMACS_ARGS = ["--batch"]
    ELISP_EXEC = "(org->pelican \"{0}\" {1})"

    file_extensions = ['org']

    def __init__(self, settings):
        super(OrgReader, self).__init__(settings)
        assert 'ORG_READER_EMACS_LOCATION' in self.settings, \
            "No ORG_READER_EMACS_LOCATION specified in settings"

    def read(self, filename):
        LOG.info("Reading Org file {0}".format(filename))
        cmd = [self.settings['ORG_READER_EMACS_LOCATION']]
        cmd.extend(self.EMACS_ARGS)

        if 'ORG_READER_EMACS_SETTINGS' in self.settings:
            cmd.append('-l')
            cmd.append(self.settings['ORG_READER_EMACS_SETTINGS'])

        backend = self.settings.get('ORG_READER_BACKEND', "'html")

        cmd.append('-l')
        cmd.append(ELISP)

        cmd.append('--eval')
        cmd.append(self.ELISP_EXEC.format(filename, backend))

        LOG.debug("OrgReader: running command `{0}`".format(cmd))

        json_result = subprocess.check_output(cmd, universal_newlines=True)
        json_output = json.loads(json_result)

        slug, e = os.path.splitext(os.path.basename(filename))

        metadata = {'title': json_output['title'],
                    'tags': json_output['category'] or '',
                    'slug': slug,
                    'author': json_output['author'],
                    'date': json_output['date']}

        parsed = {}
        for key, value in metadata.items():
            parsed[key] = self.process_metadata(key, value)

        return json_output['post'], parsed

def add_reader(readers):
    readers.reader_classes['org'] = OrgReader

def register():
    signals.readers_init.connect(add_reader)
