"""
Org Reader
==========

Version 1.1.

Relevant Pelican settings:

- ORG_READER_EMACS_LOCATION: Required. Location of Emacs binary.

- ORG_READER_EMACS_SETTINGS: Optional. An absolute path to an Elisp file, to
  run per invocation. Useful for initializing the `package` Emacs library if
  that's where your Org mode comes from, or any modifications to Org Export-
  related variables.

- ORG_READER_BACKEND: Optional. A custom backend to provide to Org. Defaults
  to 'html.

To provide metadata to Pelican, the following properties can be defined in
the org file's header:

#+TITLE: The Title Of This BlogPost
#+DATE: 2001-01-01
#+CATEGORY: blog-category
#+AUTHOR: My Name
#+LANGUAGE: en
#+PROPERTY: SUMMARY hello, this is the description
#+PROPERTY: SLUG test_slug
#+PROPERTY: MODIFIED [2015-12-29 Di]
#+PROPERTY: TAGS my, first, tags
#+PROPERTY: SAVE_AS alternative_filename.html

- The TITLE is the only mandatory header property
- Timestamps (DATE and MODIFIED) are optional and can be either a string of
  %Y-%m-%d or an org timestamp
- The property names (SUMMARY, SLUG, MODIFIED, TAGS, SAVE_AS) can be either
  lower-case or upper-case
- The slug is automatically the filename of the Org file, if not explicitly
  specified
- It is not possible to pass an empty property to Pelican.  For this plugin,
  it makes no difference if a property is present in the Org file and left
  empty, or if it is not defined at all.

"""
import os
import json
import logging
import subprocess
from pelican import readers
from pelican import signals


ELISP = os.path.join(os.path.dirname(__file__), 'org_reader.el')
LOG = logging.getLogger(__name__)


class OrgReader(readers.BaseReader):
    enabled = True

    EMACS_ARGS = ["-Q", "--batch"]
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

        # get default slug from .org filename
        default_slug, _ = os.path.splitext(os.path.basename(filename))

        metadata = {'title': json_output['title'] or '',
                    'date': json_output['date'] or '',
                    'author': json_output['author'] or '',
                    'lang': json_output['language'] or '',
                    'category': json_output['category'] or '',
                    'slug': json_output['slug'] or default_slug,
                    'modified': json_output['modified'] or '',
                    'tags': json_output['tags'] or '',
                    'save_as': json_output['save_as'] or '',
                    'summary': json_output['summary'] or ''}

        # remove empty strings when necessary
        for key in ['save_as', 'modified', 'lang', 'summary']:
            if not metadata[key]:
                metadata.pop(key)

        parsed = {}
        for key, value in metadata.items():
            parsed[key] = self.process_metadata(key, value)

        content = json_output['post']

        return content, parsed


def add_reader(readers):
    readers.reader_classes['org'] = OrgReader


def register():
    signals.readers_init.connect(add_reader)
