"""
jinja2content.py
----------------

Pelican plugin that processes Markdown files as jinja templates.

"""

from jinja2 import Environment, FileSystemLoader, ChoiceLoader
import os
from pelican import signals
from pelican.readers import MarkdownReader, HTMLReader, RstReader
from pelican.utils import pelican_open
from tempfile import NamedTemporaryFile

class JinjaContentMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # will look first in 'JINJA2CONTENT_TEMPLATES', by default the
        # content root path, then in the theme's templates
        local_dirs = self.settings.get('JINJA2CONTENT_TEMPLATES', ['.'])
        local_dirs = [os.path.join(self.settings['PATH'], folder)
                      for folder in local_dirs]
        theme_dir = os.path.join(self.settings['THEME'], 'templates')

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
        with pelican_open(source_path) as text:
            text = self.env.from_string(text).render()

        with NamedTemporaryFile(delete=False) as f:
            f.write(text.encode())
            f.close()
            content, metadata = super().read(f.name)
            os.unlink(f.name)
            return content, metadata


class JinjaMarkdownReader(JinjaContentMixin, MarkdownReader):
    pass

class JinjaRstReader(JinjaContentMixin, RstReader):
    pass

class JinjaHTMLReader(JinjaContentMixin, HTMLReader):
    pass

def add_reader(readers):
    for Reader in [JinjaMarkdownReader, JinjaRstReader, JinjaHTMLReader]:
        for ext in Reader.file_extensions:
            readers.reader_classes[ext] = Reader

def register():
    signals.readers_init.connect(add_reader)
