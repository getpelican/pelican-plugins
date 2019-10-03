"""
Author images plugin for Pelican
===========================

This plugin assigns the ``author.avatar`` and ``author.image`` variables to the
avatar and image of the author in question. Authors are identified by email
address, and avatars are images are stored in directories configured by
AUTHOR_AVATARS and AUTHOR_IMAGES.
"""

from pelican import signals
from hashlib import sha256
from os.path import exists

EXTENSIONS = ['jpg', 'png', 'svg']


def add_author_image(author, generator):
    hashsum = sha256(author.name.encode("UTF-8")).hexdigest()
    static = generator.settings['THEME'] + '/static/'
    if 'AUTHOR_AVATARS' in generator.settings.keys():
        avatar = generator.settings['AUTHOR_AVATARS'] + '/' + hashsum
        for ext in EXTENSIONS:
            if exists('%s%s.%s' % (static, avatar, ext)):
                author.avatar = '%s/%s.%s' % \
                    (generator.settings['THEME_STATIC_DIR'], avatar, ext)
                break

    if 'AUTHOR_IMAGES' in generator.settings.keys():
        image = generator.settings['AUTHOR_IMAGES'] + '/' + hashsum
        for ext in EXTENSIONS:
            if exists('%s%s.%s' % (static, image, ext)):
                author.image = '%s/%s.%s' % \
                    (generator.settings['THEME_STATIC_DIR'], image, ext)
                break


def add_author_images(generator):
    for article in generator.articles:
        for author in article.authors:
            add_author_image(author, generator)
    for author, _ in generator.authors:
        add_author_image(author, generator)


def register():
    signals.article_generator_finalized.connect(add_author_images)
