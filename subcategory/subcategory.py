# -*- coding: utf-8 -*-
"""
@Author: Alistair Magee

Adds support for subcategories on pelican articles
"""

from pelican import signals
from pelican.urlwrappers import URLWrapper
from pelican.utils import (slugify, python_2_unicode_compatible)

from six import text_type


class Category(URLWrapper):
    def __init__(self, name, parent, settings):
        super(Category, self).__init__(name, settings)
        self.parent = parent
        self.shortname = name.split('/')
        self.shortname = self.shortname.pop()
        substitutions = self.settings.get('SLUG_SUBSTITUTIONS', ())
        substitutions += tuple(self.settings.get('CATEGORY_SUBSTITUTIONS', ()))
        self.slug = slugify(self.shortname, substitutions)
        if self.parent:
            self.slug = '{}/{}'.format(self.parent.slug, self.slug)

    def as_dict(self):
        d = super(Category, self).as_dict()
        d['shortname'] = self.shortname
        d['parent'] = self.parent
        return d


def get_categories(generator, metadata):

    if 'category_path' in metadata:
        category_list = text_type(metadata.get('category_path')).split('/')
    else:
        category_list = text_type(metadata.get('category')).split('/')

    # generate a list of subcategories with their parents
    cat_list = []
    parent = None
    for category in category_list:
        category.strip()
        if parent:
            category = parent + '/' + category
        cat_list.append(category)
        parent = category
    metadata['category_branch'] = cat_list


def create_categories(generator):
    generator.categories = []
    for article in generator.articles:
        parent = None
        actual_categories = []
        for category in article.category_branch:
            # following line returns a list of items, tuples in this case
            cat = [item for item in generator.categories if item[0].name == category]
            if cat:
                cat[0][1].append(article)
                parent = cat[0][0]
                actual_categories.append(parent)
            else:
                new_cat = Category(category, parent, generator.settings)
                generator.categories.append((new_cat, [article, ]))
                parent = new_cat
                actual_categories.append(parent)
        article.category_branch = actual_categories
        article.category = actual_categories[-1]

    generator.categories.sort(reverse=generator.settings.get('REVERSE_CATEGORY_ORDER') or False)
    generator._update_context(['categories'])


def register():
    signals.article_generator_context.connect(get_categories)
    signals.article_generator_finalized.connect(create_categories)
