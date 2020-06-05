# -*- coding: utf-8 -*-
"""
AsciiDoc3 Reader
================

This plugin allows you to use AsciiDoc3 to write your posts.
File extension should be ``.ad3``.
"""

import os
import re
import subprocess
import sys
from pelican.readers import BaseReader
from pelican import signals

def call(cmd):
    """Calls a CLI command and returns the stdout as string."""
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
                            shell=True).communicate()[0].decode('utf-8')

def default():
    """Attempt to find the default AsciiDoc3 utility."""
    for cmd in ALLOWED_CMDS:
        if call(cmd + " --help"):
            return cmd

def fix_unicode(val):
    if sys.version_info[0] < 3:
        val = unicode(val.decode("utf-8"))
    else:
        # This fixes an issue with character substitutions, e.g. 'ñ' to 'Ã±'.
        val = str.encode(val, "latin-1").decode("utf-8")
    return val

ALLOWED_CMDS = ["asciidoc3"]

ENABLED = None != default()

class AsciiDoc3Reader(BaseReader):
    """Reader for AsciiDoc3 files."""

    enabled = ENABLED
    file_extensions = ['ad3']
    default_options = ['--no-header-footer']

    def read(self, source_path):
        """Parse content and metadata of AsciiDoc3 files."""
        cmd = self._get_cmd()
        content = ""
        if cmd:
            optlist = self.settings.get('ASCIIDOC3_OPTIONS', []) + self.default_options
            options = " ".join(optlist)
            content = call("%s %s -o - %s" % (cmd, options, source_path))
        metadata = self._read_metadata(source_path)
        return content, metadata

    def _get_cmd(self):
        """Returns the AsciiDoc3 utility command to use for rendering or None if
        one cannot be found."""
        if self.settings.get('ASCIIDOC3_CMD') in ALLOWED_CMDS:
            return self.settings.get('ASCIIDOC3_CMD')
        return default()

    def _read_metadata(self, source_path):
        """Parses the AsciiDoc3 file at the given `source_path` and returns found
        metadata."""
        metadata = {}
        with open(source_path) as fi:
            prev = ""
            for line in fi.readlines():
                # Parse for doc title.
                if 'title' not in metadata.keys():
                    title = ""
                    if line.startswith("= "):
                        title = line[2:].strip()
                    elif line.count("=") == len(prev.strip()):
                        title = prev.strip()
                    if title:
                        metadata['title'] = self.process_metadata('title', fix_unicode(title))

                # Parse for other metadata.
                regexp = re.compile(r"^:[A-z]+:\s*[A-z0-9]")
                if regexp.search(line):
                    toks = line.split(":", 2)
                    key = toks[1].strip().lower()
                    val = toks[2].strip()
                    metadata[key] = self.process_metadata(key, fix_unicode(val))
                prev = line
        return metadata

def add_reader(readers):
    for ext in AsciiDoc3Reader.file_extensions:
        readers.reader_classes[ext] = AsciiDoc3Reader

def register():
    signals.readers_init.connect(add_reader)
