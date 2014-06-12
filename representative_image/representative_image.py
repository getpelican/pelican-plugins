from pelican import signals
from pelican.contents import Content, Article
from bs4 import BeautifulSoup

def images_extraction(instance):
    representativeImage = None
    if type(instance) == Article:
        if 'image' in instance.metadata:
            representativeImage = instance.metadata['image']

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
            instance._summary = unicode(soup)
        
        # If there are no image in summary, look for it in the content body
        if not representativeImage:
            soup = BeautifulSoup(instance.content, 'html.parser')
            imageTag = soup.find('img')
            if imageTag:
                representativeImage = imageTag['src']
        
        # Set the attribute to content instance
        instance.featured_image = representativeImage

def register():
    signals.content_object_init.connect(images_extraction)
