import os
import logging
from six.moves.urllib.parse import urljoin
import six
from pelican import signals
from pelican.utils import pelican_open

if not six.PY3:
    from codecs import open

logger = logging.getLogger(__name__)
source_files = []
PROCESS = ['articles', 'pages', 'drafts']

def link_source_files(generator):
    """
    Processes each article/page object and formulates copy from and copy
    to destinations, as well as adding a source file URL as an attribute.
    """
    # Get all attributes from the generator that are articles or pages
    posts = [
        getattr(generator, attr, None) for attr in PROCESS
        if getattr(generator, attr, None) is not None]
    # Work on each item
    for post in posts[0]:
        if not 'SHOW_SOURCE_ON_SIDEBAR' in generator.settings and \
            not 'SHOW_SOURCE_IN_SECTION' in generator.settings:
            return
        # Only try this when specified in metadata or SHOW_SOURCE_ALL_POSTS
        # override is present in settings
        if 'SHOW_SOURCE_ALL_POSTS' in generator.settings or \
            'show_source' in post.metadata:
            # Source file name can be optionally set in config
            show_source_filename = generator.settings.get(
                'SHOW_SOURCE_FILENAME', '{}.txt'.format(post.slug)
                )
            try:
                # Get the full path to the original source file
                source_out = os.path.join(
                    post.settings['OUTPUT_PATH'], post.save_as
                    )
                # Get the path to the original source file
                source_out_path = os.path.split(source_out)[0]
                # Create 'copy to' destination for writing later
                copy_to = os.path.join(
                    source_out_path, show_source_filename
                    )
                # Add file to published path
                source_url = urljoin(
                    post.save_as, show_source_filename
                    )
            except Exception:
                return
            # Format post source dict & populate
            out = dict()
            out['copy_raw_from'] = post.source_path
            out['copy_raw_to'] = copy_to
            logger.debug('Linked %s to %s', post.source_path, copy_to)
            source_files.append(out)
            # Also add the source path to the post as an attribute for tpls
            post.show_source_url = source_url

def _copy_from_to(from_file, to_file):
    """
    A very rough and ready copy from / to function.
    """
    with pelican_open(from_file) as text_in:
        encoding = 'utf-8'
        with open(to_file, 'w', encoding=encoding) as text_out:
            text_out.write(text_in)
            logger.info('Writing %s', to_file)

def write_source_files(*args, **kwargs):
    """
    Called by the `page_writer_finalized` signal to process source files.
    """
    for source in source_files:
        _copy_from_to(source['copy_raw_from'], source['copy_raw_to'])

def register():
    """
    Calls the shots, based on signals
    """
    signals.article_generator_finalized.connect(link_source_files)
    signals.page_generator_finalized.connect(link_source_files)
    signals.page_writer_finalized.connect(write_source_files)
