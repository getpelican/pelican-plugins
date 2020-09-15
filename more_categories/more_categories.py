# -*- coding: utf-8 -*-
"""
Title: More Categories
Description: adds support for multiple categories per article and nested
categories
Requirements: Pelican 3.8 or higher
"""

from pelican import signals
from pelican.urlwrappers import URLWrapper
from pelican.utils import slugify

from collections import defaultdict
from six import text_type

class Category(URLWrapper):
    @property
    def _name(self):
        if self.parent:
            return self.parent._name + '/' + self.shortname
        return self.shortname

    @_name.setter
    def _name(self, val):
        if '/' in val:
            parentname, val = val.rsplit('/', 1)
            self.parent = self.__class__(parentname, self.settings)
        else:
            self.parent = None
        self.shortname = val.strip()

    @URLWrapper.name.setter
    def name(self, val):
        self._name = val

    @property
    def slug(self):
        if self._slug is None:
            if 'CATEGORY_REGEX_SUBSTITUTIONS' in self.settings:
                subs = self.settings['CATEGORY_REGEX_SUBSTITUTIONS']
            else:
                subs = self.settings.get('SLUG_REGEX_SUBSTITUTIONS', [])
            self._slug = slugify(self.shortname, regex_subs=subs)
            if self.parent:
                self._slug = self.parent.slug + '/' + self._slug
        return self._slug

    @property
    def ancestors(self):
        if self.parent:
            return self.parent.ancestors + [self]
        return [self]

    def as_dict(self):
        d = super(Category, self).as_dict()
        d['shortname'] = self.shortname
        return d


def get_categories(generator, metadata):
    categories = text_type(metadata.get('category')).split(',')
    metadata['categories'] = [
        Category(name, generator.settings) for name in categories]
    metadata['category'] = metadata['categories'][0]


def create_categories(generator):
    generator.categories = []
    cat_dct = defaultdict(list)
    for article in generator.articles:
        for cat in {a for c in article.categories for a in c.ancestors}:
            cat_dct[cat].append(article)

    generator.categories = sorted(
        list(cat_dct.items()),
        reverse=generator.settings.get('REVERSE_CATEGORY_ORDER') or False)
    generator._update_context(['categories'])


def register():
    signals.article_generator_context.connect(get_categories)
    signals.article_generator_finalized.connect(create_categories)
