"""
collate_content.py
==================
(c) 2014 - Edward Stronge

Connects to the content generator finalized signal to combine
articles and pages sharing a category into lists that will be
available in the template context.

Thanks to #pelican member @kura for suggestions on creating this
plugin.
"""
from collections import defaultdict
import functools
import re

from pelican import signals


def group_content(generator, content_type):
    """
    Assembles articles and pages into lists based on each
    article or page's content. These lists are available
    through the global context passed to the template engine.

    When multiple categories are present, splits category names
    based on commas and trims whitespace surrounding a
    category's name. Thus, commas may not appear within a category
    but they can be used to delimit categories and may be surrounded by
    arbitrary amounts of whitespace.

    For each category, substitutes '_' for all whitespace and '-'
    characters, then creates a list named `SUBSTITUTED_CATEGORY_NAME`_articles
    or `SUBSTITUTED_CATEGORY_NAME`_pages for Articles or Pages,
    respectively.

    Note that the *original* category name must appear in the
    `CATEGORIES_TO_COLLATE` when using this plugin with category
    filtering enabled.
    """
    category_filter = generator.settings.get('CATEGORIES_TO_COLLATE', None)
    filtering_active = type(category_filter) in (list, tuple, set)

    collations = generator.context.get('collations', defaultdict(list))
    for content in generator.context[content_type]:
        category_list = [c.strip() for c in content.category.name.split(',')]
        for category in category_list:
            if filtering_active and category not in category_filter:
                continue
            category = substitute_category_name(category)
            collations['%s_%s' % (category, content_type)].append(content)
    generator.context['collations'] = collations


def substitute_category_name(category_name):
    """
    Replaces whitespace and '-' characters in `category_name`
    to allow category_name to be made into a valid Python
    identifier.

    Doesn't check all possible ways a string might be invalid;
    the user of the collate_content module is advised to use
    categories with Python-friendly names.
    """
    return re.sub(r'\s', '_', category_name).replace('-', '_').lower()

ARTICLE_GROUPER = functools.partial(group_content, content_type='articles')
PAGE_GROUPER = functools.partial(group_content, content_type='pages')


def register():
    """Register the new plugin"""
    signals.article_generator_finalized.connect(ARTICLE_GROUPER)
    signals.page_generator_finalized.connect(PAGE_GROUPER)
