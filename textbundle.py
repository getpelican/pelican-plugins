#-*- conding: utf-8 -*-

import os
import logging
import shutil
from glob import glob

from pelican import readers
from pelican import signals
#from pelican.utils import pelican_open
from markdown import Markdown

logger = logging.getLogger(__name__)


class TextbundleReader(readers.MarkdownReader):
    enabled = Markdown
    path_mappings = {}
    file_extensions = ['textbundle']

    # You need to have a read method, which takes a filename and returns
    # some content and the associated metadata.
    def read(self, filename):
        md_filename = "{}/text.md".format(filename)
        logger.debug('Found textbundle {}'.format(filename))
        return super(TextbundleReader, self).read(md_filename)


def add_reader(readers):
    readers.reader_classes['textbundle'] = TextbundleReader


def copy_article_assets(generator):
    logging.debug('Copy Article textbundle assets')
    inspect_content_items(generator.articles, generator.output_path)


def copy_page_assets(generator):
    logging.debug('Copy Page textbundle assets')
    inspect_content_items(generator.pages, generator.output_path)


def inspect_content_items(content_items, output_path):
    for item in content_items:
        foldername = os.path.join(
            output_path,
            os.path.dirname(item.save_as),
            'assets'
        )
        assets = glob("{}/assets/*.*".format(os.path.dirname(item.source_path)))
        if len(assets) > 0:
            copy_assets_to_outputfolder(assets, foldername)


def copy_assets_to_outputfolder(assets, foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    for asset in assets:
        asset_path = os.path.join(foldername, os.path.basename(asset))
        if not os.path.exists(asset_path):
            logger.debug('copying asset {} to {}'.format(asset, foldername))
            shutil.copy2(asset, asset_path)
        else:
            logger.debug('skipping existing asset {}'.format(foldername))


def register():
    signals.readers_init.connect(add_reader)
    signals.article_generator_finalized.connect(copy_article_assets)
    signals.page_generator_finalized.connect(copy_page_assets)
