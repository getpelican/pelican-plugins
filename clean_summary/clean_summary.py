"""
Clean Summary
-------------

adds option to specify maximum number of images to appear in article summary
also adds option to include an image by default if one exists in your article
"""

from pelican import signals
from pelican.contents import Content, Article
from bs4 import BeautifulSoup
from six import text_type

def clean_summary(instance):
    if "CLEAN_SUMMARY_MAXIMUM" in instance.settings:
        maximum_images = instance.settings["CLEAN_SUMMARY_MAXIMUM"]
    else:
        maximum_images = 0
    if "CLEAN_SUMMARY_MINIMUM_ONE" in instance.settings:
        minimum_one = instance.settings['CLEAN_SUMMARY_MINIMUM_ONE']
    else:
        minimum_one = False
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

def register():
    signals.content_object_init.connect(clean_summary)
