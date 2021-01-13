'''
tag_cloud
===================================

This plugin generates a tag cloud from available tags
'''
from __future__ import unicode_literals

from collections import defaultdict
from operator import itemgetter

import logging
import math
import random

from pelican import signals

logger = logging.getLogger(__name__)


def set_default_settings(settings):
    settings.setdefault('TAG_CLOUD_STEPS', 4)
    settings.setdefault('TAG_CLOUD_MAX_ITEMS', 100)
    settings.setdefault('TAG_CLOUD_SORTING', 'random')
    settings.setdefault('TAG_CLOUD_BADGE', False)


def init_default_config(pelican):
    from pelican.settings import DEFAULT_CONFIG
    set_default_settings(DEFAULT_CONFIG)
    if(pelican):
            set_default_settings(pelican.settings)


def generate_tag_cloud(generator):
    tag_cloud = defaultdict(int)
    for article in generator.articles:
        for tag in getattr(article, 'tags', []):
            tag_cloud[tag] += 1

    tag_cloud = sorted(tag_cloud.items(), key=itemgetter(1), reverse=True)
    tag_cloud = tag_cloud[:generator.settings.get('TAG_CLOUD_MAX_ITEMS')]

    tags = list(map(itemgetter(1), tag_cloud))
    if tags:
        max_count = tags[0]
        min_count = tags[-1]
    steps = generator.settings.get('TAG_CLOUD_STEPS')

    # calculate word sizes
    def generate_tag(tag, count):
        tag = (
            tag,
            int(math.floor(steps - (steps - 1) * math.log(count - min_count + 1)
                / (math.log(max_count - min_count + 1) or 1)))
        )
        if generator.settings.get('TAG_CLOUD_BADGE'):
            tag += (count,)
        return tag

    tag_cloud = [
        generate_tag(tag, count)
        for tag, count in tag_cloud
    ]

    sorting = generator.settings.get('TAG_CLOUD_SORTING')

    if sorting == 'alphabetically':
        tag_cloud.sort(key=lambda elem: elem[0].name)
    elif sorting == 'alphabetically-rev':
        tag_cloud.sort(key=lambda elem: elem[0].name, reverse=True)
    elif sorting == 'size':
        tag_cloud.sort(key=lambda elem: elem[1])
    elif sorting == 'size-rev':
        tag_cloud.sort(key=lambda elem: elem[1], reverse=True)
    elif sorting == 'random':
        random.shuffle(tag_cloud)
    else:
        logger.warning("setting for TAG_CLOUD_SORTING not recognized: %s, "
                       "falling back to 'random'", sorting)
        random.shuffle(tag_cloud)

    # make available in context
    generator.tag_cloud = tag_cloud
    generator._update_context(['tag_cloud'])


def register():
    signals.initialized.connect(init_default_config)
    signals.article_generator_finalized.connect(generate_tag_cloud)
