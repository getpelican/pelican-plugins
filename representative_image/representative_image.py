import six
from bs4 import BeautifulSoup

from pelican import signals
from pelican.contents import Article, Page
from pelican.generators import ArticlesGenerator, PagesGenerator


def images_extraction(instance):
    representativeImage = None
    if type(instance) in (Article, Page):
        if 'image' in instance.metadata:
            representativeImage = instance.metadata['image']

        # Process Summary:
        # If summary contains images, extract one to be the representativeImage
        # and remove images from summary
        soup = BeautifulSoup(instance.summary, 'html.parser')
        images = soup.find_all('img')
        for i in images:
            if not representativeImage:
                representativeImage = i['src']
            i.extract()
        if len(images) > 0:
            # set _summary field which is based on metadata. summary field is
            # only based on article's content and not settable
            instance._summary = six.text_type(soup)

        # If there are no image in summary, look for it in the content body
        if not representativeImage:
            soup = BeautifulSoup(instance._content, 'html.parser')
            imageTag = soup.find('img')
            if imageTag:
                representativeImage = imageTag['src']

        # Set the attribute to content instance
        instance.featured_image = representativeImage
        instance.featured_alt = instance.metadata.get('alt', None)
        instance.featured_link = instance.metadata.get('link', None)
        instance.featured_caption = instance.metadata.get('caption', None)


def run_plugin(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                images_extraction(article)
                for translation in article.translations:
                    images_extraction(translation)
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                images_extraction(page)
                for translation in page.translations:
                    images_extraction(translation)


def register():
    try:
        signals.all_generators_finalized.connect(run_plugin)
    except AttributeError:
        # NOTE: This results in #314 so shouldn't really be relied on
        # https://github.com/getpelican/pelican-plugins/issues/314
        signals.content_object_init.connect(images_extraction)
