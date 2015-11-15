# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
import logging
from pelican import signals
from pelican.utils import pelican_open
from PIL import Image, ExifTags
from itertools import chain

logger = logging.getLogger(__name__)
queue_resize = dict()
hrefs = None


def initialized(pelican):
    p = os.path.expanduser('~/Pictures')
    from pelican.settings import DEFAULT_CONFIG
    DEFAULT_CONFIG.setdefault('PHOTO_LIBRARY', p)
    DEFAULT_CONFIG.setdefault('PHOTO_GALLERY', (1024, 768, 80))
    DEFAULT_CONFIG.setdefault('PHOTO_ARTICLE', ( 760, 506, 80))
    DEFAULT_CONFIG.setdefault('PHOTO_THUMB',   ( 192, 144, 60))
    if pelican:
        pelican.settings.setdefault('PHOTO_LIBRARY', p)
        pelican.settings.setdefault('PHOTO_GALLERY', (1024, 768, 80))
        pelican.settings.setdefault('PHOTO_ARTICLE', ( 760, 506, 80))
        pelican.settings.setdefault('PHOTO_THUMB',   ( 192, 144, 60))


def read_notes(filename, msg=None):
    notes = {}
    try:
        with pelican_open(filename) as text:
            for line in text.splitlines():
                m = line.split(':', 1)
                if len(m) > 1:
                    pic = m[0].strip()
                    note = m[1].strip()
                    if pic and note:
                        notes[pic] = note
    except:
        if msg:
            logger.warning(msg, filename)
    return notes


def enqueue_resize(orig, resized, spec=(640, 480, 80)):
    global queue_resize
    if resized not in queue_resize:
        queue_resize[resized] = (orig, spec)
    elif queue_resize[resized] != (orig, spec):
        logger.error('photos: resize conflict for {}, {}-{} is not {}-{}',
                     resized,
                     queue_resize[resized][0], queue_resize[resized][1],
                     orig, spec)


def resize_photos(generator, writer):
    print('photos: {} photo resizes to consider.'
          .format(len(queue_resize.items())))
    for resized, what in queue_resize.items():
        resized = os.path.join(generator.output_path, resized)
        orig, spec = what
        if (not os.path.isfile(resized) or
                os.path.getmtime(orig) > os.path.getmtime(resized)):
            logger.info('photos: make photo %s -> %s', orig, resized)
            im = Image.open(orig)
            try:
                exif = im._getexif()
            except Exception:
                exif = None
            try:
                icc_profile = im.info.get("icc_profile")
            except Exception:
                icc_profile = None
            if exif:
                for tag, value in exif.items():
                    decoded = ExifTags.TAGS.get(tag, tag)
                    if decoded == 'Orientation':
                        if   value == 3: im = im.rotate(180)
                        elif value == 6: im = im.rotate(270)
                        elif value == 8: im = im.rotate(90)
                        break
            im.thumbnail((spec[0], spec[1]), Image.ANTIALIAS)
            try:
                os.makedirs(os.path.split(resized)[0])
            except:
                pass
            im.save(resized, 'JPEG', quality=spec[2], icc_profile=icc_profile)

def detect_content(content):

    def replacer(m):
        what = m.group('what')
        value = m.group('value')
        origin = m.group('path')

        if what == 'photo':
            if value.startswith('/'):
                value = value[1:]
            path = os.path.join(
                        os.path.expanduser(settings['PHOTO_LIBRARY']),
                        value)
            if not os.path.isfile(path):
                logger.error('photos: No photo %s', path)
            else:
                photo = os.path.splitext(value)[0].lower() + 'a.jpg'
                origin = os.path.join('/photos', photo)
                enqueue_resize(
                    path,
                    os.path.join('photos', photo),
                    settings['PHOTO_ARTICLE'])
        return ''.join((m.group('markup'), m.group('quote'), origin,
                        m.group('quote')))

    global hrefs
    if hrefs is None:
        regex = r"""
            (?P<markup><\s*[^\>]*  # match tag with src and href attr
                (?:href|src)\s*=)

            (?P<quote>["\'])      # require value to be quoted
            (?P<path>{0}(?P<value>.*?))  # the url value
            \2""".format(content.settings['INTRASITE_LINK_REGEX'])
        hrefs = re.compile(regex, re.X)

    if content._content and '{photo}' in content._content:
        settings = content.settings
        content._content = hrefs.sub(replacer, content._content)


def process_gallery_photo(generator, article, gallery):
    if gallery.startswith('/'):
        gallery = gallery[1:]
    dir_gallery = os.path.join(
                    os.path.expanduser(generator.settings['PHOTO_LIBRARY']),
                    gallery)
    if os.path.isdir(dir_gallery):
        logger.info('photos: Gallery detected: %s', gallery)
        dir_photo = os.path.join('photos', gallery.lower())
        dir_thumb = os.path.join('photos', gallery.lower())
        exifs = read_notes(os.path.join(dir_gallery, 'exif.txt'),
                           msg='photos: No EXIF for gallery %s')
        captions = read_notes(os.path.join(dir_gallery, 'captions.txt'))
        article.photo_gallery = []
        for pic in sorted(os.listdir(dir_gallery)):
            if pic.startswith('.'): continue
            if pic.endswith('.txt'): continue
            photo = os.path.splitext(pic)[0].lower() + '.jpg'
            thumb = os.path.splitext(pic)[0].lower() + 't.jpg'
            article.photo_gallery.append((
                pic,
                os.path.join(dir_photo, photo),
                os.path.join(dir_thumb, thumb),
                exifs.get(pic, ''),
                captions.get(pic, '')))
            enqueue_resize(
                os.path.join(dir_gallery, pic),
                os.path.join(dir_photo, photo),
                generator.settings['PHOTO_GALLERY'])
            enqueue_resize(
                os.path.join(dir_gallery, pic),
                os.path.join(dir_thumb, thumb),
                generator.settings['PHOTO_THUMB'])
    else:
        logger.error('photos: Gallery does not exist: %s at %s', gallery, dir_gallery)


def process_gallery_filename(generator, article, gallery):
    if gallery.startswith('/'):
        gallery = gallery[1:]
    else:
        gallery = os.path.join(article.relative_dir, gallery)
    dir_gallery = os.path.join(
                    os.path.expanduser(generator.settings['PHOTO_LIBRARY']),
                    gallery)
    if os.path.isdir(dir_gallery):
        logger.info('photos: Gallery detected: %s', gallery)
        dir_photo = gallery.lower()
        dir_thumb = os.path.join('photos', gallery.lower())
        exifs = read_notes(os.path.join(dir_gallery, 'exif.txt'),
                           msg='photos: No EXIF for gallery %s')
        captions = read_notes(os.path.join(dir_gallery, 'captions.txt'))
        article.photo_gallery = []
        for pic in sorted(os.listdir(dir_gallery)):
            if pic.startswith('.'): continue
            if pic.endswith('.txt'): continue
            photo = pic.lower()
            thumb = os.path.splitext(pic)[0].lower() + 't.jpg'
            article.photo_gallery.append((
                pic,
                os.path.join(dir_photo, photo),
                os.path.join(dir_thumb, thumb),
                exifs.get(pic, ''),
                captions.get(pic, '')))
            enqueue_resize(
                os.path.join(dir_gallery, pic),
                os.path.join(dir_thumb, thumb),
                generator.settings['PHOTO_THUMB'])
    else:
        logger.error('photos: Gallery does not exist: %s at %s', gallery, dir_gallery)


def detect_gallery(generator):
    for article in chain(generator.articles, generator.drafts):
        if 'gallery' in article.metadata:
            gallery = article.metadata.get('gallery')
            if gallery.startswith('{photo}'):
                process_gallery_photo(generator, article, gallery[7:])
            elif gallery.startswith('{filename}'):
                process_gallery_filename(generator, article, gallery[10:])
            elif gallery:
                logger.error('photos: Gallery tag not recognized: %s', gallery)


def process_image_photo(generator, article, image):
    if image.startswith('/'):
        image = image[1:]
    path = os.path.join(
                os.path.expanduser(generator.settings['PHOTO_LIBRARY']),
                image)
    if os.path.isfile(path):
        photo = os.path.splitext(image)[0].lower() + 'a.jpg'
        thumb = os.path.splitext(image)[0].lower() + 't.jpg'
        article.photo_image = (
            os.path.basename(image).lower(),
            os.path.join('photos', photo),
            os.path.join('photos', thumb))
        enqueue_resize(
            path,
            os.path.join('photos', photo),
            generator.settings['PHOTO_ARTICLE'])
        enqueue_resize(
            path,
            os.path.join('photos', thumb),
            generator.settings['PHOTO_THUMB'])
    else:
        logger.error('photo: No photo for %s at %s', article.source_path, path)


def process_image_filename(generator, article, image):
    if image.startswith('/'):
        image = image[1:]
    else:
        image = os.path.join(article.relative_dir, image)
    path = os.path.join(generator.path, image)
    if os.path.isfile(path):
        small = os.path.splitext(image)[0].lower() + 't.jpg'
        article.photo_image = (
            os.path.basename(image),
            image.lower(),
            os.path.join('photos', small))
        enqueue_resize(
            path,
            os.path.join('photos', small),
            generator.settings['PHOTO_THUMB'])
    else:
        logger.error('photos: No photo at %s', path)


def detect_image(generator):
    for article in chain(generator.articles, generator.drafts):
        image = article.metadata.get('image', None)
        if image:
            if image.startswith('{photo}'):
                process_image_photo(generator, article, image[7:])
            elif image.startswith('{filename}'):
                process_image_filename(generator, article, image[10:])
            else:
                logger.error('photos: Image tag not recognized: %s', image)


def register():
    signals.initialized.connect(initialized)
    signals.content_object_init.connect(detect_content)
    signals.article_generator_finalized.connect(detect_gallery)
    signals.article_generator_finalized.connect(detect_image)
    signals.article_writer_finalized.connect(resize_photos)
