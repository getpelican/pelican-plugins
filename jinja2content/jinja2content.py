import os

from pelican import signals
from pelican.readers import Markdown, MarkdownReader
from pelican.utils import pelican_open
from jinja2 import Environment, FileSystemLoader


class JinjaMarkdownReader(MarkdownReader):

    def __init__(self, *args, **kwargs):
        super(JinjaMarkdownReader, self).__init__(*args, **kwargs)

        templates_dir = os.path.join(self.settings['THEME'], 'templates')
        self._env = Environment(
            trim_blocks=True, lstrip_blocks=True,
            loader=FileSystemLoader(templates_dir),
            extensions=self.settings['JINJA_EXTENSIONS'])

    def read(self, source_path):
        """Parse content and metadata of markdown files.

        Rendering them as jinja templates first.

        """

        self._source_path = source_path
        self._md = Markdown(extensions=self.extensions)
        with pelican_open(source_path) as text:
            text = self._env.from_string(text).render()
            content = self._md.convert(text)

        metadata = self._parse_metadata(self._md.Meta)
        return content, metadata


def add_reader(readers):
    for ext in MarkdownReader.file_extensions:
        readers.reader_classes[ext] = JinjaMarkdownReader


def register():
    signals.readers_init.connect(add_reader)
