# -*- coding: utf-8 -*-

import codecs
import logging
import markdown
import os

logger = logging.getLogger(__name__)

from pelican import signals


def initialized(pelican):
    from pelican.settings import DEFAULT_CONFIG
    DEFAULT_CONFIG.setdefault('STATIC_COMMENTS', False)
    DEFAULT_CONFIG.setdefault('STATIC_COMMENTS_DIR' 'comments')
    if pelican:
        pelican.settings.setdefault('STATIC_COMMENTS', False)
        pelican.settings.setdefault('STATIC_COMMENTS_DIR', 'comments')


def add_static_comments(gen, metadata):
    if gen.settings['STATIC_COMMENTS'] != True:
        return

    if not 'slug' in metadata:
        logger.warning("static_comments: "
                "cant't locate comments file without slug tag in the article")
        return

    fname = os.path.join(gen.settings['STATIC_COMMENTS_DIR'],
            metadata['slug'] + ".md")

    if not os.path.exists(fname):
        return

    input_file = codecs.open(fname, mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text)

    metadata['static_comments'] = html


def register():
    signals.initialized.connect(initialized)
    signals.article_generator_context.connect(add_static_comments)
