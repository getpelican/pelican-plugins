# -*- coding: utf-8 -*-
"""
AsciiDoc Reader
===============

This plugin allows you to use AsciiDoc to write your posts.
File extension should be ``.asc``, ``.adoc``, or ``asciidoc``.
"""

from pelican.readers import BaseReader
from pelican import signals
import os
import re
import subprocess
import sys
import tempfile

import logging
logger = logging.getLogger(__name__)


def encoding():
    """Return encoding used to decode shell output in call function"""
    if os.name == 'nt':
        from ctypes import cdll
        return 'cp' + str(cdll.kernel32.GetOEMCP())
    return 'utf-8'

def call(cmd):
    """Calls a CLI command and returns the stdout as string."""
    logger.debug('AsciiDocReader: Running: %s', cmd)
    stdoutdata, stderrdata = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    if stderrdata:
        logger.warning('AsciiDocReader: strderr: %s', stderrdata)
    return stdoutdata.decode(encoding())

def default():
    """Attempt to find the default AsciiDoc utility."""
    for cmd in ALLOWED_CMDS:
        if len(call(cmd + " --help")):
            logger.debug('AsciiDocReader: Using cmd: %s', cmd)
            return cmd

ALLOWED_CMDS = ["asciidoc", "asciidoctor"]

ENABLED = None != default()

class AsciiDocReader(BaseReader):
    """Reader for AsciiDoc files."""

    enabled = ENABLED
    file_extensions = ['asc', 'adoc', 'asciidoc']
    default_options = ['--no-header-footer']

    def read(self, source_path):
        """Parse content and metadata of AsciiDoc files."""
        cmd = self._get_cmd()
        content = ""
        if cmd:
            logger.debug('AsciiDocReader: Reading: %s', source_path)
            optlist = self.settings.get('ASCIIDOC_OPTIONS', []) + self.default_options
            options = " ".join(optlist)
            # Beware! # Don't use tempfile.NamedTemporaryFile under Windows: https://bugs.python.org/issue14243
            # Also, use mkstemp correctly (Linux and Windows): https://www.logilab.org/blogentry/17873
            fd, temp_name = tempfile.mkstemp()
            content = call("%s %s -o %s \"%s\"" % (cmd, options, temp_name, source_path))
            with open(temp_name, encoding='utf-8') as f:
                content = f.read()
            os.close(fd)
            os.unlink(temp_name)
        metadata = self._read_metadata(source_path)
        logger.debug('AsciiDocReader: Got content (showing first 50 chars): %s', (content[:50] + '...') if len(content) > 50 else content)
        return content, metadata

    def _get_cmd(self):
        """Returns the AsciiDoc utility command to use for rendering or None if
        one cannot be found."""
        if self.settings.get('ASCIIDOC_CMD') in ALLOWED_CMDS:
            return self.settings.get('ASCIIDOC_CMD')
        return default()

    def _read_metadata(self, source_path):
        """Parses the AsciiDoc file at the given `source_path` and returns found
        metadata."""
        metadata = {}
        with open(source_path, encoding='utf-8') as fi:
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
                        metadata['title'] = self.process_metadata('title', title)

                # Parse for other metadata.
                regexp = re.compile(r"^:\w+:")
                if regexp.search(line):
                    toks = line.split(":", 2)
                    key = toks[1].strip().lower()
                    val = toks[2].strip()
                    metadata[key] = self.process_metadata(key, val)
                prev = line
        logger.debug('AsciiDocReader: Found metadata: %s', metadata)
        return metadata

def add_reader(readers):
    for ext in AsciiDocReader.file_extensions:
        readers.reader_classes[ext] = AsciiDocReader

def register():
    signals.readers_init.connect(add_reader)
