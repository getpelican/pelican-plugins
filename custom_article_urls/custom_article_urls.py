# -*- coding: utf-8 -*-
"""
@Author: Alistair Magee

Adds ability to specify custom urls for different categories 
(or subcategories if using subcategory plugin) of article
using a dictionary stored in pelican settings file as
{category: {article_url_structure: stirng, article_save_as: string}}
"""
from pelican import signals
from pelican.contents import Article, Category
from six import text_type

def custom_url(generator, metadata):
    if 'CUSTOM_ARTICLE_URLS' in generator.settings:
        custom_urls = generator.settings['CUSTOM_ARTICLE_URLS']
        category = text_type(metadata['category'])
        pattern_matched = {}
        
        if category in custom_urls:
            pattern_matched = custom_urls[category]

        if 'subcategories' in metadata: #using subcategory plugin
            for subcategory in metadata['subcategories']:
                if subcategory in custom_urls:
                    pattern_matched = custom_urls[subcategory]

        if pattern_matched:
            #only alter url if hasn't been set in the metdata
            if ('url', 'save_as') in metadata:
                """ if both url and save_as are set in the metadata already
                then there is already a custom url set, skip this one
                """
                pass
            else:
                temp_article = Article("", metadata=metadata)
                url_format = pattern_matched['URL']
                save_as_format = pattern_matched['SAVE_AS']
                url = url_format.format(**temp_article.url_format)
                save_as = save_as_format.format(**temp_article.url_format)
                metadata.update({'url': url, 'save_as': save_as})

        
def register():
    signals.article_generator_context.connect(custom_url)
