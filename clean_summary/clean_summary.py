"""
Clean Summary
-------------

adds option to specify maximum number of images to appear in article summary
also adds option to include an image by default if one exists in your article
"""

from pelican import signals
from pelican.contents import Content, Article
from pelican.generators import ArticlesGenerator
from bs4 import BeautifulSoup
from six import text_type

def init(pelican):
    global maximum_images
    global minimum_one
    maximum_images = pelican.settings.get('CLEAN_SUMMARY_MAXIMUM', 0)
    minimum_one = pelican.settings.get('CLEAN_SUMMARY_MINIMUM_ONE', False)


def clean_summary(instance):
    if type(instance) == Article:
        summary = instance.summary
        summary = BeautifulSoup(instance.summary, 'html.parser')
        images = summary.findAll('img')
        if (len(images) > maximum_images):
            for image in images[maximum_images:]:
                image.extract()
        if len(images) < 1 and minimum_one: #try to find one
            content = BeautifulSoup(instance.content, 'html.parser')
            first_image = content.find('img')
            if first_image:
                summary.insert(0, first_image)
        instance._summary = text_type(summary)


def run_plugin(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                clean_summary(article)


def register():
    signals.initialized.connect(init)
    try:
        signals.all_generators_finalized.connect(run_plugin)
    except AttributeError:
        # NOTE: This may result in #314 so shouldn't really be relied on
        # https://github.com/getpelican/pelican-plugins/issues/314
        signals.content_object_init.connect(clean_summary)
