# -*- coding: utf-8 -*-
"""
Pelican Comment System
======================

A Pelican plugin, which allows you to add comments to your articles.

Author: Bernhard Scheirle
"""
from __future__ import unicode_literals
import logging
import os
import copy

logger = logging.getLogger(__name__)

from itertools import chain
from pelican import signals
from pelican.readers import Readers
from pelican.writers import Writer

from . comment import Comment
from . import avatars


def pelican_initialized(pelican):
    from pelican.settings import DEFAULT_CONFIG
    DEFAULT_CONFIG.setdefault('PELICAN_COMMENT_SYSTEM', False)
    DEFAULT_CONFIG.setdefault('PELICAN_COMMENT_SYSTEM_DIR', 'comments')
    DEFAULT_CONFIG.setdefault(
        'PELICAN_COMMENT_SYSTEM_IDENTICON_OUTPUT_PATH' 'images/identicon')
    DEFAULT_CONFIG.setdefault('PELICAN_COMMENT_SYSTEM_IDENTICON_DATA', ())
    DEFAULT_CONFIG.setdefault('PELICAN_COMMENT_SYSTEM_IDENTICON_SIZE', 72)
    DEFAULT_CONFIG.setdefault('PELICAN_COMMENT_SYSTEM_AUTHORS', {})
    DEFAULT_CONFIG.setdefault(
        'PELICAN_COMMENT_SYSTEM_FEED', os.path.join('feeds', 'comment.%s.atom.xml'))
    DEFAULT_CONFIG.setdefault('COMMENT_URL', '#comment-{slug}')
    DEFAULT_CONFIG['PAGE_EXCLUDES'].append(
        DEFAULT_CONFIG['PELICAN_COMMENT_SYSTEM_DIR'])
    DEFAULT_CONFIG['ARTICLE_EXCLUDES'].append(
        DEFAULT_CONFIG['PELICAN_COMMENT_SYSTEM_DIR'])
    if pelican:
        pelican.settings.setdefault('PELICAN_COMMENT_SYSTEM', False)
        pelican.settings.setdefault('PELICAN_COMMENT_SYSTEM_DIR', 'comments')
        pelican.settings.setdefault(
            'PELICAN_COMMENT_SYSTEM_IDENTICON_OUTPUT_PATH', 'images/identicon')
        pelican.settings.setdefault(
            'PELICAN_COMMENT_SYSTEM_IDENTICON_DATA', ())
        pelican.settings.setdefault(
            'PELICAN_COMMENT_SYSTEM_IDENTICON_SIZE', 72)
        pelican.settings.setdefault('PELICAN_COMMENT_SYSTEM_AUTHORS', {})
        pelican.settings.setdefault(
            'PELICAN_COMMENT_SYSTEM_FEED', os.path.join('feeds', 'comment.%s.atom.xml'))
        pelican.settings.setdefault('COMMENT_URL', '#comment-{slug}')

        pelican.settings['PAGE_EXCLUDES'].append(
            pelican.settings['PELICAN_COMMENT_SYSTEM_DIR'])
        pelican.settings['ARTICLE_EXCLUDES'].append(
            pelican.settings['PELICAN_COMMENT_SYSTEM_DIR'])


def initialize(article_generator):
    avatars.init(
        article_generator.settings['OUTPUT_PATH'],
        article_generator.settings[
            'PELICAN_COMMENT_SYSTEM_IDENTICON_OUTPUT_PATH'],
        article_generator.settings['PELICAN_COMMENT_SYSTEM_IDENTICON_DATA'],
        article_generator.settings[
            'PELICAN_COMMENT_SYSTEM_IDENTICON_SIZE'] / 3,
        article_generator.settings['PELICAN_COMMENT_SYSTEM_AUTHORS'],
    )


def warn_on_slug_collision(items):
    slugs = {}
    for comment in items:
        if not comment.slug in slugs:
            slugs[comment.slug] = [comment]
        else:
            slugs[comment.slug].append(comment)

    for slug, itemList in slugs.items():
        len_ = len(itemList)
        if len_ > 1:
            logger.warning('There are %s comments with the same slug: %s' %
                           (len_, slug))
            for x in itemList:
                logger.warning('    %s' % x.source_path)


def write_feed(gen, items, context, slug):
    if gen.settings['PELICAN_COMMENT_SYSTEM_FEED'] is None:
        return

    path = gen.settings['PELICAN_COMMENT_SYSTEM_FEED'] % slug

    writer = Writer(gen.output_path, settings=gen.settings)
    writer.write_feed(items, context, path)


def add_static_comments(gen, content):
    if gen.settings['PELICAN_COMMENT_SYSTEM'] is not True:
        return

    content.comments_count = 0
    content.comments = []

    # Modify the local context, so we get proper values for the feed
    context = copy.copy(gen.context)
    context['SITEURL'] += "/" + content.url
    context['SITENAME'] += " - Comments: " + content.title
    context['SITESUBTITLE'] = ""

    folder = os.path.join(
        gen.settings['PATH'],
        gen.settings['PELICAN_COMMENT_SYSTEM_DIR'],
        content.slug
    )

    if not os.path.isdir(folder):
        logger.debug("No comments found for: " + content.slug)
        write_feed(gen, [], context, content.slug)
        return

    reader = Readers(gen.settings)
    comments = []
    replies = []

    for file in os.listdir(folder):
        name, extension = os.path.splitext(file)
        if extension[1:].lower() in reader.extensions:
            com = reader.read_file(
                base_path=folder, path=file,
                content_class=Comment, context=context)

            if hasattr(com, 'replyto'):
                replies.append(com)
            else:
                comments.append(com)

    warn_on_slug_collision(comments + replies)

    write_feed(gen, comments + replies, context, content.slug)

    # TODO: Fix this O(n²) loop
    for reply in replies:
        for comment in chain(comments, replies):
            if comment.slug == reply.replyto:
                comment.addReply(reply)

    count = 0
    for comment in comments:
        comment.sortReplies()
        count += comment.countReplies()

    comments = sorted(comments)

    content.comments_count = len(comments) + count
    content.comments = comments


def writeIdenticonsToDisk(gen, writer):
    avatars.generateAndSaveMissingAvatars()


def register():
    signals.initialized.connect(pelican_initialized)
    signals.article_generator_init.connect(initialize)
    signals.article_generator_write_article.connect(add_static_comments)
    signals.article_writer_finalized.connect(writeIdenticonsToDisk)
