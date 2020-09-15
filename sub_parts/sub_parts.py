# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pelican import signals
import logging

logger = logging.getLogger(__name__)


def patch_subparts(generator):
    generator.subparts = []
    slugs = {}
    for article in generator.articles:
        slugs[article.slug] = article
        if '--' in article.slug:
            generator.subparts.append(article)
    for article in generator.subparts:
        logger.info('sub_part: Detected %s', article.slug)
        (pslug, _) = article.slug.rsplit('--', 1)
        if pslug in slugs:
            parent = slugs[pslug]
            if not hasattr(parent, 'subparts'):
                parent.subparts = []
            parent.subparts.append(article)
            article.subpart_of = parent
            article.subtitle = article.title
            article.title = article.title + ", " + parent.title
            generator.dates.remove(article)
            generator.articles.remove(article)
            if article.category:
                for cat, arts in generator.categories:
                    if cat.name == article.category.name:
                        arts.remove(article)
                        break
                else:
                    logger.error(
                        'sub_part: Cannot remove sub-part from category %s',
                        article.category)
            if (hasattr(article, 'subphotos') or
                    hasattr(article, 'photo_gallery')):
                parent.subphotos = (
                    getattr(parent, 'subphotos',
                            len(getattr(parent, 'photo_gallery', []))) +
                    getattr(article, 'subphotos', 0) +
                    len(getattr(article, 'photo_gallery', [])))
        else:
            logger.error('sub_part: No parent for %s', pslug)
        generator._update_context(('articles', 'dates', 'subparts'))


def write_subparts(generator, writer):
    for article in generator.subparts:
        signals.article_generator_write_article.send(generator,
                                                     content=article)
        writer.write_file(
            article.save_as, generator.get_template(article.template),
            generator.context, article=article, category=article.category,
            override_output=hasattr(article, 'override_save_as'),
            relative_urls=generator.settings['RELATIVE_URLS'])
    if len(generator.subparts) > 0:
        print('sub_part: processed {} sub-parts.'.format(
            len(generator.subparts)))


def register():
    signals.article_generator_finalized.connect(patch_subparts)
    signals.article_writer_finalized.connect(write_subparts)
