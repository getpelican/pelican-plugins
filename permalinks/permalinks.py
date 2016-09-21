# -*- coding: utf-8 -*-
"""
This plugin enables a kind of permalink which can be used to refer to a piece
of content which is resistant to the file being moved or renamed.
"""
import logging
import itertools
import os
import os.path
from pelican import signals
from pelican.generators import Generator
from pelican.utils import mkdir_p
from pelican.utils import clean_output_dir

logger = logging.getLogger(__name__)


def article_url(content):
    '''
    Get the URL for an item of content
    '''
    return '{content.settings[SITEURL]}/{content.url}'.format(
        content=content).encode('utf-8')


REDIRECT_STRING = '''
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0;url={url}">
        <script type="text/javascript">
            window.location.href = "{url}"
        </script>
        <title>Page Redirection to {title}</title>
    </head>
    <body>
        If you are not redirected automatically, follow the
        <a href='{url}'>link to {title}</a>
    </body>
</html>
'''


class PermalinkGenerator(Generator):
    '''
    Generate a redirect page for every item of content with a
    permalink_id metadata
    '''
    def generate_context(self):
        '''
        Setup context
        '''
        self.permalink_output_path = os.path.join(
            self.output_path, self.settings['PERMALINK_PATH'])
        self.permalink_id_metadata_key = self.settings['PERMALINK_ID_METADATA_KEY']

    def generate_output(self, writer=None):
        '''
        Generate redirect files
        '''
        logger.info(
            'Generating permalink files in %r', self.permalink_output_path)

        clean_output_dir(self.permalink_output_path, [])
        mkdir_p(self.permalink_output_path)
        for content in itertools.chain(
                self.context['articles'], self.context['pages']):

            for permalink_id in content.get_permalink_ids_iter():
                permalink_path = os.path.join(
                    self.permalink_output_path, permalink_id) + '.html'

                redirect_string = REDIRECT_STRING.format(
                    url=article_url(content),
                    title=content.title)
                open(permalink_path, 'w').write(redirect_string)


def get_permalink_ids_iter(self):
    '''
    Method to get permalink ids from content. To be bound to the class last thing
    '''
    permalink_id_key = self.settings['PERMALINK_ID_METADATA_KEY']
    permalink_ids_raw = self.metadata.get(permalink_id_key, '')

    for permalink_id in permalink_ids_raw.split(','):
        if permalink_id:
            yield permalink_id.strip()


def get_permalink_ids(self):
    '''
    Method to get permalink ids from content. To be bound to the class last thing
    '''
    return list(self.get_permalink_ids_iter())

def get_permalink_path(self):
    """Get just path component of permalink."""
    try:
        first_permalink_id = self.get_permalink_ids_iter().next()
    except StopIteration:
        return None

    return '/{settings[PERMALINK_PATH]}/{first_permalink}'.format(
        settings=self.settings, first_permalink=first_permalink_id)


def get_permalink_url(self):
    '''
    Get a permalink URL
    '''
    return "/".join((self.settings['SITEURL'], self.get_permalink_path()))


PERMALINK_METHODS = (
    get_permalink_ids_iter,
    get_permalink_ids,
    get_permalink_url,
    get_permalink_path,
)


def add_permalink_methods(content_inst):
    '''
    Add permalink methods to object
    '''
    for permalink_method in PERMALINK_METHODS:
        setattr(
            content_inst,
            permalink_method.__name__,
            permalink_method.__get__(content_inst, content_inst.__class__))

def add_permalink_option_defaults(pelicon_inst):
    '''
    Add perlican defaults
    '''
    pelicon_inst.settings.setdefault('PERMALINK_PATH', 'permalinks')
    pelicon_inst.settings.setdefault('PERMALINK_ID_METADATA_KEY', 'permalink_id')


def get_generators(_pelican_object):
    return PermalinkGenerator


def register():
    signals.get_generators.connect(get_generators)
    signals.content_object_init.connect(add_permalink_methods)
    signals.initialized.connect(add_permalink_option_defaults)
