"""
jinja2htmlcontent.py
----------------

Pelican plugin that processes HTML files as Jinja templates.

"""

from os import path
from pelican import signals
from pelican.readers import HTMLReader
from pelican.utils import pelican_open
from jinja2 import Environment, FileSystemLoader, ChoiceLoader


class JinjaHTMLReader(HTMLReader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        if 'JINJA_FILTERS' in self.settings:
            custom_filters = self.settings['JINJA_FILTERS']
            self.env.filters.update(custom_filters)

    def read(self, filename):
        """
        Parse HTML content files with Jinja templates inside
        """
        with pelican_open(filename) as content:
            jinjad_content = self.env.from_string(content).render()
            parser = self._HTMLParser(self.settings, filename)
            parser.feed(jinjad_content)
            parser.close()

        metadata = {}
        for k in parser.metadata:
            metadata[k] = self.process_metadata(k, parser.metadata[k])
        return parser.body, metadata


def add_reader(readers):
    for ext in HTMLReader.file_extensions:
        readers.reader_classes[ext] = JinjaHTMLReader


def register():
    signals.readers_init.connect(add_reader)
