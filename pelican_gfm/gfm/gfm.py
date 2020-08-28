#!/usr/bin/python -B

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#
# gfm_reader.py -- GitHub-Flavored Markdown reader for Pelican
#
from __future__ import absolute_import
import sys
import os
import ctypes
import time
import re
import pelican.utils
import pelican.signals
import pelican.readers

from gfm import gfmSetup
from gfm import Settings

_LIBDIR = Settings.LIBCMARKLOCATION
_LIBCMARK = 'libcmark-gfm.so'
_LIBEXT = 'libcmark-gfmextensions.so'
try:
    cmark = ctypes.CDLL(os.path.join(_LIBDIR, _LIBCMARK))
    cmark_ext = ctypes.CDLL(os.path.join(_LIBDIR, _LIBEXT))
except OSError:
    raise ImportError(
                      '%s not found. run python3 gfmSetup.py as a\
 user with write permisions to %s or change LIBCMARKLOCATION\
 in Settings.py'
                      % (_LIBCMARK, _LIBDIR)
                      )

# Use ctypes to access the functions in libcmark-gfm
F_cmark_parser_new = cmark.cmark_parser_new
F_cmark_parser_new.restype = ctypes.c_void_p
F_cmark_parser_new.argtypes = (ctypes.c_int,)

F_cmark_parser_feed = cmark.cmark_parser_feed
F_cmark_parser_feed.restype = None
F_cmark_parser_feed.argtypes = (
                                ctypes.c_void_p,
                                ctypes.c_char_p,
                                ctypes.c_size_t
                                )

F_cmark_parser_finish = cmark.cmark_parser_finish
F_cmark_parser_finish.restype = ctypes.c_void_p
F_cmark_parser_finish.argtypes = (ctypes.c_void_p,)

F_cmark_parser_attach_syntax_extension = cmark.cmark_parser_attach_syntax_extension
F_cmark_parser_attach_syntax_extension.restype = ctypes.c_int
F_cmark_parser_attach_syntax_extension.argtypes = (
                                                    ctypes.c_void_p,
                                                    ctypes.c_void_p
                                                    )

F_cmark_parser_get_syntax_extensions = cmark.cmark_parser_get_syntax_extensions
F_cmark_parser_get_syntax_extensions.restype = ctypes.c_void_p
F_cmark_parser_get_syntax_extensions.argtypes = (ctypes.c_void_p,)

F_cmark_parser_free = cmark.cmark_parser_free
F_cmark_parser_free.restype = None
F_cmark_parser_free.argtypes = (ctypes.c_void_p,)

F_cmark_node_free = cmark.cmark_node_free
F_cmark_node_free.restype = None
F_cmark_node_free.argtypes = (ctypes.c_void_p,)

F_cmark_find_syntax_extension = cmark.cmark_find_syntax_extension
F_cmark_find_syntax_extension.restype = ctypes.c_void_p
F_cmark_find_syntax_extension.argtypes = (ctypes.c_char_p,)

F_cmark_render_html = cmark.cmark_render_html
F_cmark_render_html.restype = ctypes.c_char_p
F_cmark_render_html.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)


# Set up the libcmark-gfm library and its extensions
F_register = cmark_ext.core_extensions_ensure_registered
F_register.restype = None
F_register.argtypes = ()
F_register()

# technically, maybe install an atexit() to release the plugins


class GFMReader(pelican.readers.BaseReader):
    enabled = True
    """GitHub Flavored Markdown Reader for the Pelican system.

    Pelican looks for all subclasses of BaseReader, and automatically
    registers them for the file extensions listed below. Thus, nothing
    further is required by users of this Reader.
    """

    # NOTE: the builtin MarkdownReader must be disabled. Otherwise, it will be
    #       non-deterministic which Reader will be used for these files.
    #       See settings for the list of extensions.
    file_extensions = Settings.FILE_EXTENSIONS

    # Metadata is specified as a single, colon-separated line, such as:
    #
    # Title: this is the title
    #
    # Note: name starts in column 0, no whitespace before colon, will be
    #       made lower-case, and value will be stripped
    #
    RE_METADATA = re.compile('^([A-za-z]+): (.*)$')

    def read(self, source_path):
        # Prepare the "slug", which is the target file name.
        # It will be the same as the source file, minus the leading
        # ".../content/(articles|pages)"
        # and with the extension removed (Pelican will add .html)
        relpath = os.path.relpath(source_path, self.settings['PATH'])
        parts = relpath.split(os.sep)

        # split off ext, keep base
        parts[-1] = os.path.splitext(parts[-1])[0]
        slug = os.sep.join(parts[1:])

        metadata = {
            'slug': slug,
        }

        # Fetch the source content, with a few appropriate tweaks
        with pelican.utils.pelican_open(source_path) as text:

            # Extract the metadata from the header of the text
            lines = text.splitlines()
            for i in range(len(lines)):
                line = lines[i]
                match = GFMReader.RE_METADATA.match(line)
                if match:
                    name = match.group(1).strip().lower()
                    if name != 'slug':
                        value = match.group(2).strip()
                        if name == 'date':
                            value = pelican.utils.get_date(value)
                    metadata[name] = value
                    # if name != 'title':
                    #  print 'META:', name, value
                elif not line.strip():
                    # blank line
                    continue
                else:
                    # reached actual content
                    break

            # Reassemble content, minus the metadata
            text = '\n'.join(lines[i:])

            # Render the markdown into HTML
            if sys.version_info >= (3, 0):
                text = text.encode('utf-8')
                content = self.render(text).decode('utf-8')
            else:
                content = self.render(text)

        # Redo the slug for articles.
        if parts[0] == 'articles' and 'title' in metadata:
            metadata['slug'] = pelican.utils.slugify(
                                metadata['title'],
                                self.settings.get(
                                 'SLUG_SUBSTITUTIONS',
                                 ()
                                 )
                                )

        return content, metadata

    def render(self, text):
        "Use cmark-gfm to render the Markdown into an HTML fragment."

        parser = F_cmark_parser_new(Settings.OPTS)
        assert parser
        for name in Settings.EXTENSIONS:
            ext = F_cmark_find_syntax_extension(name.encode('utf-8'))
            assert ext
            rv = F_cmark_parser_attach_syntax_extension(parser, ext)
            assert rv
        exts = F_cmark_parser_get_syntax_extensions(parser)
        F_cmark_parser_feed(parser, text, len(text))
        doc = F_cmark_parser_finish(parser)
        assert doc
        output = F_cmark_render_html(doc, Settings.OPTS, exts)
        F_cmark_parser_free(parser)
        F_cmark_node_free(doc)
        return output


def add_readers(readers):
    msg = "GFM plugin cannot find the required libcmark files.\
 Please run python3 gfmSetup.py as a user with write permission \
 to the directory into which the libcmark files will be placed."
    if gfmSetup.test_configuration():
        readers.reader_classes['md'] = GFMReader
        return True
    else:
        raise Exception(msg)


def register():
    reader = pelican.signals.readers_init.connect(add_readers)
    return(reader)
