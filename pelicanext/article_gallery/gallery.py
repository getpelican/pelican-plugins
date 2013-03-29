# -*- encoding: utf-8 -*-
'''
Article gallery plugin for Pelican
==================================
This plugin adds a gallery property to all articles to store an associated
list of images. The images are retrieved from a specific folder based on the
article's slug.
'''


from pelican import signals
import mimetypes
import exceptions
import logging
import os
import Image as PILImage


logger = logging.getLogger(__name__)


class Image(object):
    '''
    Implements an object to store all the information on an image.
    '''
    def __init__(self, name, mime, url, thumbnail, thumbnail_url):
        self.name = name
        self.mime = mime
        self.url = url
        self.thumbnail_url = thumbnail_url
        self.thumbnail = thumbnail


def resize_image(image_in, image_out=None, width=800, height=600):
    '''
        Resizes an image.

        ``resize_image`` takes a path to an image to resize it to the specified
        size. If the no output path is given, the original image will be
        overwritten.
    '''
    if image_out is None:
        image_out = image_in
    img = PILImage.open(image_in)
    img.thumbnail((width, height), PILImage.ANTIALIAS)
    img.save(image_out, 'JPEG', quality=90)


def initialized(pelican):
    '''
        Gets and sets settings of the plugin then executes initializations.

        The initialization process needs to resize the original images and
        generates thumbnails to make them available before the generation of
        the static files.
    '''

    # set up pelican with required article gallery parameters
    gallery = pelican.settings.get('ARTICLE_GALLERY', 'gallery')
    thumbnails = pelican.settings.get('ARTICLE_GALLERY_THUMBNAILS', True)
    directory = pelican.settings.get('ARTICLE_GALLERY_THUMBNAIL_DIR', '.min')
    thumb_w = pelican.settings.get('ARTICLE_GALLERY_THUMBNAIL_WIDTH', 800)
    thumb_h = pelican.settings.get('ARTICLE_GALLERY_THUMBNAIL_HEIGHT', 600)
    resize = pelican.settings.get('ARTICLE_GALLERY_RESIZE', False)
    resize_w = pelican.settings.get('ARTICLE_GALLERY_RESIZE_WIDTH', 800)
    resize_h = pelican.settings.get('ARTICLE_GALLERY_RESIZE_HEIGHT', 600)

    pelican.settings.setdefault('ARTICLE_GALLERY', gallery)
    pelican.settings.setdefault('ARTICLE_GALLERY_THUMBNAIL_DIR', directory)
    pelican.settings.setdefault('ARTICLE_GALLERY_THUMBNAILS', thumbnails)
    pelican.settings.setdefault('ARTICLE_GALLERY_THUMBNAIL_WIDTH', thumb_w)
    pelican.settings.setdefault('ARTICLE_GALLERY_THUMBNAIL_HEIGHT', thumb_h)
    pelican.settings.setdefault('ARTICLE_GALLERY_RESIZE_', resize)
    pelican.settings.setdefault('ARTICLE_GALLERY_RESIZE_WIDTH', resize_w)
    pelican.settings.setdefault('ARTICLE_GALLERY_RESIZE_HEIGHT', resize_h)
    if gallery not in pelican.settings['STATIC_PATHS']:
        pelican.settings['STATIC_PATHS'].append(gallery)


    # if the original images need to be manipulated
    if thumbnails or resize:

        content = pelican.settings.get('PATH')
        for root, _, files in os.walk(os.path.join(content, gallery)):
            # skip thumbnail directory
            if root.endswith(directory):
                continue

            for img in files:
                # skip files which are not pictures
                mime, _ = mimetypes.guess_type(img)
                if mime is None or not mime.startswith('image'):
                    continue

                original_path = os.path.join(root, img)
                # create thumbnails and their hosting directory if necessary
                if thumbnails:
                    thumbnail_dir = os.path.join(root, directory)
                    if not os.path.exists(thumbnail_dir):
                        os.makedirs(thumbnail_dir)

                    img_root, _ = os.path.splitext(img)
                    thumb_path = os.path.join(thumbnail_dir,
                                              '{}{}'.format(img_root, '.jpg'))
                    resize_image(original_path, thumb_path, thumb_w, thumb_h)

                # resize original pictures if necessary
                if resize:
                    resize_image(original_path, width=resize_w, height=resize_h)


def article_gallery(generator):

    # get required parameters to build the object
    content = generator.settings.get('PATH')
    gallery = generator.settings['ARTICLE_GALLERY']
    thumbnails = generator.settings['ARTICLE_GALLERY_THUMBNAILS']
    directory = generator.settings['ARTICLE_GALLERY_THUMBNAIL_DIR']

    for article in generator.articles:
        article.gallery = []

        source_path = os.path.join(content, gallery, article.slug)
        root_url = os.path.join('/static', gallery, article.slug)
        thumbnail_root_url = os.path.join(root_url, directory)

        try:

            for img in os.listdir(source_path):

                mime, _ = mimetypes.guess_type(img)
                if mime is None or not mime.startswith('image'):
                    continue

                file_root, _ = os.path.splitext(img)
                thumbnail_url = os.path.join(thumbnail_root_url,
                                             '{}{}'.format(file_root, '.jpg'))
                original_url = os.path.join(root_url, img)
                article.gallery.append(Image(img, mime, original_url,
                                             thumbnails, thumbnail_url))

        except exceptions.OSError:
            logger.warning('No gallery found for the article "{}".'
                           .format(article.slug))


def register():
    signals.initialized.connect(initialized)
    signals.article_generator_finalized.connect(article_gallery)
