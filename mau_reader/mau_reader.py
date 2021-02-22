# -*- coding: utf-8 -*-
"""
Mau Reader
==========

This plugin allows you to use Mau to write your posts. 
File extension should be ``.mau``
"""

from pelican.readers import BaseReader
from pelican.utils import pelican_open
from pelican import signals

try:
    from mau import Mau
    from mau.visitors.html_visitor import DEFAULT_TEMPLATES as mau_default_templates

    mau_enabled = True
except ImportError:
    mau_enabled = False  # NOQA


class MauReader(BaseReader):
    enabled = mau_enabled
    file_extensions = ["mau"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(self, source_path):
        config = self.settings["MAU"].get("config", {})
        config["no_document"] = True

        output_format = self.settings["MAU"].get("output_format", "html")
        custom_templates = self.settings["MAU"].get("custom_templates", {})
        mau_default_templates.update(custom_templates)

        self._source_path = source_path
        self._mau = Mau(config, output_format, default_templates=mau_default_templates)
        with pelican_open(source_path) as text:
            content = self._mau.process(text)

        metadata = self._parse_metadata(self._mau.variables["pelican"])

        return content, metadata

    def _parse_metadata(self, meta):
        """Return the dict containing document metadata"""
        formatted_fields = self.settings["FORMATTED_FIELDS"]

        output = {}
        for name, value in meta.items():
            name = name.lower()
            if name in formatted_fields:
                formatted = self._mau.process(value)
                output[name] = self.process_metadata(name, formatted)
            elif len(value) > 1:
                # handle list metadata as list of string
                output[name] = self.process_metadata(name, value)
            else:
                # otherwise, handle metadata as single string
                output[name] = self.process_metadata(name, value[0])

        return output


def add_reader(readers):
    for ext in MauReader.file_extensions:
        readers.reader_classes[ext] = MauReader


def register():
    signals.readers_init.connect(add_reader)
