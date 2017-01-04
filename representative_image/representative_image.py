import six
from pelican import signals
from pelican.contents import Article, Draft, Page
from pelican.generators import ArticlesGenerator
from bs4 import BeautifulSoup


def images_extraction(instance):
    representativeImage = None
    if type(instance) in (Article, Draft, Page):
        if 'image' in instance.metadata:
            try:
                ix = int(instance.metadata['image'])
            except ValueError:
                representativeImage = instance.metadata['image']
        else:
            ix = 0
        # Process Summary:
        # If summary contains images, extract one to be the representativeImage and remove images from summary
        soup = BeautifulSoup(instance.summary, 'html.parser')
        images = soup.find_all('img')
        for i in images:
            if not representativeImage:
                representativeImage = i['src']
            i.extract()
        if len(images) > 0:
            # set _summary field which is based on metadata. summary field is only based on article's content and not settable
            instance._summary = six.text_type(soup)

        # If there are no image in summary, look for it in the content body
        if not representativeImage:
            soup = BeautifulSoup(instance._content, 'html.parser')
            imageTag = soup.find_all('img')
            if imageTag:
                if len(imageTag) < (ix + 1):
                    raise ValueError('Image index exceeds number of images in document')
                representativeImage = imageTag[ix]['src']

        # Set the attribute to content instance
        instance.featured_image = representativeImage


def run_plugin(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                images_extraction(article)


def register():
    try:
        signals.all_generators_finalized.connect(run_plugin)
    except AttributeError:
        # NOTE: This results in #314 so shouldn't really be relied on
        # https://github.com/getpelican/pelican-plugins/issues/314
        signals.content_object_init.connect(images_extraction)
