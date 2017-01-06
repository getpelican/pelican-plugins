"""
jinja2content.py
----------------

Pelican plugin that processes Markdown files as jinja templates.

"""

from os import path
from pelican import signals
from pelican.readers import Markdown, MarkdownReader
from pelican.utils import pelican_open
from jinja2 import Environment, FileSystemLoader, ChoiceLoader


class JinjaMarkdownReader(MarkdownReader):

    def __init__(self, *args, **kwargs):
        super(JinjaMarkdownReader, self).__init__(*args, **kwargs)

        # will look first in 'JINJA2CONTENT_TEMPLATES', by default the
        # content root path, then in the theme's templates
        # local_templates_dirs = self.settings.get('JINJA2CONTENT_TEMPLATES', ['.'])
        # local_templates_dirs = path.join(self.settings['PATH'], local_templates_dirs)
        local_dirs = self.settings.get('JINJA2CONTENT_TEMPLATES', ['.'])
        local_dirs = [path.join(self.settings['PATH'], folder)
                      for folder in local_dirs]
        theme_dir = path.join(self.settings['THEME'], 'templates')

        loaders = [FileSystemLoader(_dir) for _dir
                   in local_dirs + [theme_dir]]
        if 'JINJA_ENVIRONMENT' in self.settings: # pelican 3.7
            jinja_environment = self.settings['JINJA_ENVIRONMENT']
        else:
            jinja_environment = {
                'trim_blocks': True,
                'lstrip_blocks': True,
                'extensions': self.settings['JINJA_EXTENSIONS']
            }
        self.env = Environment(
            loader=ChoiceLoader(loaders),
            **jinja_environment)

    def read(self, source_path):
        """Parse content and metadata of markdown files.

        Rendering them as jinja templates first.

        """

        self._source_path = source_path
        self._md = Markdown(extensions=self.settings['MARKDOWN']['extensions'])

        with pelican_open(source_path) as text:
            text = self.env.from_string(text).render()
            content = self._md.convert(text)

        metadata = self._parse_metadata(self._md.Meta)
        return content, metadata


def add_reader(readers):
    for ext in MarkdownReader.file_extensions:
        readers.reader_classes[ext] = JinjaMarkdownReader


def register():
    signals.readers_init.connect(add_reader)
