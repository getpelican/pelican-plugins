# -*- coding: utf-8 -*-
"""
@Author: Alistair Magee

Adds support for subcategories on pelican articles
"""
import os
from collections import defaultdict
from pelican import signals
from pelican.urlwrappers import URLWrapper, Category
from operator import attrgetter
from functools import partial

from six import text_type

class SubCategory(URLWrapper):
    def __init__(self, name, parent, *args, **kwargs):
        super(SubCategory, self).__init__(name, *args, **kwargs)
        self.parent = parent
        if isinstance(self.parent, SubCategory):
            self.savepath = os.path.join(self.parent.savepath, self.slug)
            self.fullurl = '{}/{}'.format(self.parent.fullurl, self.slug)
        else: #parent is a category
            self.savepath = os.path.join(self.parent.slug, self.slug)
            self.fullurl = '{}/{}'.format(self.parent.slug, self.slug)

    def as_dict(self):
        d = self.__dict__
        d['name'] = self.name
        d['savepath'] = self.savepath
        d['fullurl'] = self.fullurl
        d['parent'] = self.parent
        return d

def get_subcategories(generator, metadata):
    if 'SUBCATEGORY_SAVE_AS' not in generator.settings:
        generator.settings['SUBCATEGORY_SAVE_AS'] = os.path.join( 
                'subcategory', '{savepath}.html')
    if 'SUBCATEGORY_URL' not in generator.settings:
        generator.settings['SUBCATEGORY_URL'] = 'subcategory/{fullurl}.html'
    category_list = text_type(metadata.get('category')).split('/')
    category = (category_list.pop(0)).strip()
    category = Category(category, generator.settings)
    metadata['category'] = category
    #generate a list of subcategories with their parents
    sub_list = []
    parent = category
    for subcategory in category_list:
        subcategory.strip()
        subcategory = SubCategory(subcategory, parent, generator.settings)
        sub_list.append(subcategory)
        parent = subcategory
    metadata['subcategories'] = sub_list

def organize_subcategories(generator):
    generator.subcategories = defaultdict(list)
    for article in generator.articles:
        subcategories = article.metadata.get('subcategories')
        for cat in subcategories:
            generator.subcategories[cat].append(article)

def generate_subcategories(generator, writer):
    write = partial(writer.write_file,
            relative_urls=generator.settings['RELATIVE_URLS'])
    subcategory_template = generator.get_template('subcategory')
    for sub_cat, articles in generator.subcategories.items():
        articles.sort(key=attrgetter('date'), reverse=True)
        dates = [article for article in generator.dates if article in articles]
        write(sub_cat.save_as, subcategory_template, generator.context, 
                subcategory=sub_cat, articles=articles, dates=dates, 
                paginated={'articles': articles, 'dates': dates},
                page_name=sub_cat.page_name, all_articles=generator.articles)

def register():
    signals.article_generator_context.connect(get_subcategories)
    signals.article_generator_finalized.connect(organize_subcategories)
    signals.article_writer_finalized.connect(generate_subcategories)
