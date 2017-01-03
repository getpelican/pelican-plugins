# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import itertools
import json
import logging
import multiprocessing
import os
import pprint
import re
import sys

from pelican.generators import ArticlesGenerator
from pelican.generators import PagesGenerator
from pelican.settings import DEFAULT_CONFIG
from pelican import signals
from pelican.utils import pelican_open

logger = logging.getLogger(__name__)

try:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageEnhance
    from PIL import ImageFont
except ImportError:
    logger.error('PIL/Pillow not found')

try:
    import piexif
except ImportError:
    ispiexif = False
    logger.warning('piexif not found! Cannot use exif manipulation features')
else:
    ispiexif = True
    logger.debug('piexif found.')


def initialized(pelican):

    p = os.path.expanduser('~/Pictures')

    DEFAULT_CONFIG.setdefault('PHOTO_LIBRARY', p)
    DEFAULT_CONFIG.setdefault('PHOTO_GALLERY', (1024, 768, 80))
    DEFAULT_CONFIG.setdefault('PHOTO_ARTICLE', (760, 506, 80))
    DEFAULT_CONFIG.setdefault('PHOTO_THUMB', (192, 144, 60))
    DEFAULT_CONFIG.setdefault('PHOTO_GALLERY_TITLE', '')
    DEFAULT_CONFIG.setdefault('PHOTO_ALPHA_BACKGROUND_COLOR', (255, 255, 255))
    DEFAULT_CONFIG.setdefault('PHOTO_WATERMARK', False)
    DEFAULT_CONFIG.setdefault('PHOTO_WATERMARK_THUMB', False)
    DEFAULT_CONFIG.setdefault('PHOTO_WATERMARK_TEXT', DEFAULT_CONFIG['SITENAME'])
    DEFAULT_CONFIG.setdefault('PHOTO_WATERMARK_TEXT_COLOR', (255, 255, 255))
    DEFAULT_CONFIG.setdefault('PHOTO_WATERMARK_IMG', '')
    DEFAULT_CONFIG.setdefault('PHOTO_WATERMARK_IMG_SIZE', False)
    DEFAULT_CONFIG.setdefault('PHOTO_RESIZE_JOBS', 1)
    DEFAULT_CONFIG.setdefault('PHOTO_EXIF_KEEP', False)
    DEFAULT_CONFIG.setdefault('PHOTO_EXIF_REMOVE_GPS', False)
    DEFAULT_CONFIG.setdefault('PHOTO_EXIF_AUTOROTATE', True)
    DEFAULT_CONFIG.setdefault('PHOTO_EXIF_COPYRIGHT', False)
    DEFAULT_CONFIG.setdefault('PHOTO_EXIF_COPYRIGHT_AUTHOR', DEFAULT_CONFIG['SITENAME'])
    DEFAULT_CONFIG.setdefault('PHOTO_LIGHTBOX_GALLERY_ATTR', 'data-lightbox')
    DEFAULT_CONFIG.setdefault('PHOTO_LIGHTBOX_CAPTION_ATTR', 'data-title')

    DEFAULT_CONFIG['queue_resize'] = {}
    DEFAULT_CONFIG['created_galleries'] = {}
    DEFAULT_CONFIG['plugin_dir'] = os.path.dirname(os.path.realpath(__file__))

    if pelican:
        pelican.settings.setdefault('PHOTO_LIBRARY', p)
        pelican.settings.setdefault('PHOTO_GALLERY', (1024, 768, 80))
        pelican.settings.setdefault('PHOTO_ARTICLE', (760, 506, 80))
        pelican.settings.setdefault('PHOTO_THUMB', (192, 144, 60))
        pelican.settings.setdefault('PHOTO_GALLERY_TITLE', '')
        pelican.settings.setdefault('PHOTO_ALPHA_BACKGROUND_COLOR', (255, 255, 255))
        pelican.settings.setdefault('PHOTO_WATERMARK', False)
        pelican.settings.setdefault('PHOTO_WATERMARK_THUMB', False)
        pelican.settings.setdefault('PHOTO_WATERMARK_TEXT', pelican.settings['SITENAME'])
        pelican.settings.setdefault('PHOTO_WATERMARK_TEXT_COLOR', (255, 255, 255))
        pelican.settings.setdefault('PHOTO_WATERMARK_IMG', '')
        pelican.settings.setdefault('PHOTO_WATERMARK_IMG_SIZE', False)
        pelican.settings.setdefault('PHOTO_RESIZE_JOBS', 1)
        pelican.settings.setdefault('PHOTO_EXIF_KEEP', False)
        pelican.settings.setdefault('PHOTO_EXIF_REMOVE_GPS', False)
        pelican.settings.setdefault('PHOTO_EXIF_AUTOROTATE', True)
        pelican.settings.setdefault('PHOTO_EXIF_COPYRIGHT', False)
        pelican.settings.setdefault('PHOTO_EXIF_COPYRIGHT_AUTHOR', pelican.settings['AUTHOR'])
        pelican.settings.setdefault('PHOTO_LIGHTBOX_GALLERY_ATTR', 'data-lightbox')
        pelican.settings.setdefault('PHOTO_LIGHTBOX_CAPTION_ATTR', 'data-title')


def read_notes(filename, msg=None):
    notes = {}
    try:
        with pelican_open(filename) as text:
            for line in text.splitlines():
                if line.startswith('#'):
                    continue

                m = line.split(':', 1)
                if len(m) > 1:
                    pic = m[0].strip()
                    note = m[1].strip()
                    if pic and note:
                        notes[pic] = note
                else:
                    notes[line] = ''
    except Exception as e:
        if msg:
            logger.warning('{} at file {}'.format(msg, filename))
        logger.debug('read_notes issue: {} at file {}. Debug message:{}'.format(msg, filename, e))
    return notes


def enqueue_resize(orig, resized, spec=(640, 480, 80)):
    if resized not in DEFAULT_CONFIG['queue_resize']:
        DEFAULT_CONFIG['queue_resize'][resized] = (orig, spec)
    elif DEFAULT_CONFIG['queue_resize'][resized] != (orig, spec):
        logger.error('photos: resize conflict for {}, {}-{} is not {}-{}'.format(resized, DEFAULT_CONFIG['queue_resize'][resized][0], DEFAULT_CONFIG['queue_resize'][resized][1], orig, spec))


def isalpha(img):
    return True if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info) else False


def remove_alpha(img, bg_color):
    background = Image.new("RGB", img.size, bg_color)
    background.paste(img, mask=img.split()[3])  # 3 is the alpha channel

    return background


def ReduceOpacity(im, opacity):
    """Reduces Opacity.

    Returns an image with reduced opacity.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879
    """
    assert opacity >= 0 and opacity <= 1
    if isalpha(im):
        im = im.copy()
    else:
        im = im.convert('RGBA')

    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def watermark_photo(image, settings):

    margin = [10, 10]
    opacity = 0.6

    watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw_watermark = ImageDraw.Draw(watermark_layer)
    text_reducer = 32
    image_reducer = 8
    text_size = [0, 0]
    mark_size = [0, 0]
    text_position = [0, 0]

    if settings['PHOTO_WATERMARK_TEXT']:
        font_name = 'SourceCodePro-Bold.otf'
        default_font = os.path.join(DEFAULT_CONFIG['plugin_dir'], font_name)
        font = ImageFont.FreeTypeFont(default_font, watermark_layer.size[0] // text_reducer)
        text_size = draw_watermark.textsize(settings['PHOTO_WATERMARK_TEXT'], font)
        text_position = [image.size[i] - text_size[i] - margin[i] for i in [0, 1]]
        draw_watermark.text(text_position, settings['PHOTO_WATERMARK_TEXT'], settings['PHOTO_WATERMARK_TEXT_COLOR'], font=font)

    if settings['PHOTO_WATERMARK_IMG']:
        mark_image = Image.open(settings['PHOTO_WATERMARK_IMG'])
        mark_image_size = [watermark_layer.size[0] // image_reducer for size in mark_size]
        mark_image_size = settings['PHOTO_WATERMARK_IMG_SIZE'] if settings['PHOTO_WATERMARK_IMG_SIZE'] else mark_image_size
        mark_image.thumbnail(mark_image_size, Image.ANTIALIAS)
        mark_position = [watermark_layer.size[i] - mark_image.size[i] - margin[i] for i in [0, 1]]
        mark_position = tuple([mark_position[0] - (text_size[0] // 2) + (mark_image_size[0] // 2), mark_position[1] - text_size[1]])

        if not isalpha(mark_image):
            mark_image = mark_image.convert('RGBA')

        watermark_layer.paste(mark_image, mark_position, mark_image)

    watermark_layer = ReduceOpacity(watermark_layer, opacity)
    image.paste(watermark_layer, (0, 0), watermark_layer)

    return image


def rotate_image(img, exif_dict):

    if "exif" in img.info and piexif.ImageIFD.Orientation in exif_dict["0th"]:
        orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
        if orientation == 2:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            img = img.rotate(180)
        elif orientation == 4:
            img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 5:
            img = img.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
            img = img.rotate(-90)
        elif orientation == 7:
            img = img.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
            img = img.rotate(90)

    return (img, exif_dict)


def build_license(license, author):

    year = datetime.datetime.now().year
    license_file = os.path.join(DEFAULT_CONFIG['plugin_dir'], 'licenses.json')

    with open(license_file) as data_file:
        licenses = json.load(data_file)

    if any(license in k for k in licenses):
        return licenses[license]['Text'].format(Author=author, Year=year, URL=licenses[license]['URL'])
    else:
        return 'Copyright {Year} {Author}, All Rights Reserved'.format(Author=author, Year=year)


def manipulate_exif(img, settings):

    try:
        exif = piexif.load(img.info['exif'])
    except Exception:
        logger.debug('EXIF information not found')
        exif = {}

    if settings['PHOTO_EXIF_AUTOROTATE']:
        img, exif = rotate_image(img, exif)

    if settings['PHOTO_EXIF_REMOVE_GPS']:
        exif.pop('GPS')

    if settings['PHOTO_EXIF_COPYRIGHT']:

        # We want to be minimally destructive to any preset exif author or copyright information.
        # If there is copyright or author information prefer that over everything else.
        if not exif['0th'].get(piexif.ImageIFD.Artist):
            exif['0th'][piexif.ImageIFD.Artist] = settings['PHOTO_EXIF_COPYRIGHT_AUTHOR']
            author = settings['PHOTO_EXIF_COPYRIGHT_AUTHOR']

        if not exif['0th'].get(piexif.ImageIFD.Copyright):
            license = build_license(settings['PHOTO_EXIF_COPYRIGHT'], author)
            exif['0th'][piexif.ImageIFD.Copyright] = license

    return (img, piexif.dump(exif))


def resize_worker(orig, resized, spec, settings):

    logger.info('photos: make photo {} -> {}'.format(orig, resized))
    im = Image.open(orig)

    if ispiexif and settings['PHOTO_EXIF_KEEP'] and im.format == 'JPEG':  # Only works with JPEG exif for sure.
        im, exif_copy = manipulate_exif(im, settings)
    else:
        exif_copy = b''

    icc_profile = im.info.get("icc_profile", None)
    im.thumbnail((spec[0], spec[1]), Image.ANTIALIAS)
    directory = os.path.split(resized)[0]

    if isalpha(im):
        im = remove_alpha(im, settings['PHOTO_ALPHA_BACKGROUND_COLOR'])

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception:
            logger.exception('Could not create {}'.format(directory))
    else:
        logger.debug('Directory already exists at {}'.format(os.path.split(resized)[0]))

    if settings['PHOTO_WATERMARK']:
        isthumb = True if spec == settings['PHOTO_THUMB'] else False
        if not isthumb or (isthumb and settings['PHOTO_WATERMARK_THUMB']):
            im = watermark_photo(im, settings)

    im.save(resized, 'JPEG', quality=spec[2], icc_profile=icc_profile, exif=exif_copy)


def resize_photos(generator, writer):
    if generator.settings['PHOTO_RESIZE_JOBS'] == -1:
        debug = True
        generator.settings['PHOTO_RESIZE_JOBS'] = 1
    else:
        debug = False

    pool = multiprocessing.Pool(generator.settings['PHOTO_RESIZE_JOBS'])
    logger.debug('Debug Status: {}'.format(debug))
    for resized, what in DEFAULT_CONFIG['queue_resize'].items():
        resized = os.path.join(generator.output_path, resized)
        orig, spec = what
        if (not os.path.isfile(resized) or os.path.getmtime(orig) > os.path.getmtime(resized)):
            if debug:
                resize_worker(orig, resized, spec, generator.settings)
            else:
                pool.apply_async(resize_worker, (orig, resized, spec, generator.settings))

    pool.close()
    pool.join()


def detect_content(content):

    hrefs = None

    def replacer(m):
        what = m.group('what')
        value = m.group('value')
        tag = m.group('tag')
        output = m.group(0)

        if what in ('photo', 'lightbox'):
            if value.startswith('/'):
                value = value[1:]

            path = os.path.join(
                os.path.expanduser(settings['PHOTO_LIBRARY']),
                value
            )

            if os.path.isfile(path):
                photo_prefix = os.path.splitext(value)[0].lower()

                if what == 'photo':
                    photo_article = photo_prefix + 'a.jpg'
                    enqueue_resize(
                        path,
                        os.path.join('photos', photo_article),
                        settings['PHOTO_ARTICLE']
                    )

                    output = ''.join((
                        '<',
                        m.group('tag'),
                        m.group('attrs_before'),
                        m.group('src'),
                        '=',
                        m.group('quote'),
                        os.path.join(settings['SITEURL'], 'photos', photo_article),
                        m.group('quote'),
                        m.group('attrs_after'),
                    ))

                elif what == 'lightbox' and tag == 'img':
                    photo_gallery = photo_prefix + '.jpg'
                    enqueue_resize(
                        path,
                        os.path.join('photos', photo_gallery),
                        settings['PHOTO_GALLERY']
                    )

                    photo_thumb = photo_prefix + 't.jpg'
                    enqueue_resize(
                        path,
                        os.path.join('photos', photo_thumb),
                        settings['PHOTO_THUMB']
                    )

                    lightbox_attr_list = ['']

                    gallery_name = value.split('/')[0]
                    lightbox_attr_list.append('{}="{}"'.format(
                        settings['PHOTO_LIGHTBOX_GALLERY_ATTR'],
                        gallery_name
                    ))

                    captions = read_notes(
                        os.path.join(os.path.dirname(path), 'captions.txt'),
                        msg = 'photos: No captions for gallery'
                    )
                    caption = captions.get(os.path.basename(path)) if captions else None
                    if caption:
                        lightbox_attr_list.append('{}="{}"'.format(
                            settings['PHOTO_LIGHTBOX_CAPTION_ATTR'],
                            caption
                        ))

                    lightbox_attrs = ' '.join(lightbox_attr_list)

                    output = ''.join((
                        '<a href=',
                        m.group('quote'),
                        os.path.join(settings['SITEURL'], 'photos', photo_gallery),
                        m.group('quote'),
                        lightbox_attrs,
                        '><img',
                        m.group('attrs_before'),
                        'src=',
                        m.group('quote'),
                        os.path.join(settings['SITEURL'], 'photos', photo_thumb),
                        m.group('quote'),
                        m.group('attrs_after'),
                        '</a>'
                    ))

            else:
                logger.error('photos: No photo %s', path)

        return output

    if hrefs is None:
        regex = r"""
            <\s*
            (?P<tag>[^\s\>]+)  # detect the tag
            (?P<attrs_before>[^\>]*)
            (?P<src>href|src)  # match tag with src and href attr
            \s*=
            (?P<quote>["\'])  # require value to be quoted
            (?P<path>{0}(?P<value>.*?))  # the url value
            (?P=quote)
            (?P<attrs_after>[^\>]*>)
        """.format(
            content.settings['INTRASITE_LINK_REGEX']
        )
        hrefs = re.compile(regex, re.X)

    if content._content and ('{photo}' in content._content or '{lightbox}' in content._content):
        settings = content.settings
        content._content = hrefs.sub(replacer, content._content)


def galleries_string_decompose(gallery_string):
    splitter_regex = re.compile(r'[\s,]*?({photo}|{filename})')
    title_regex = re.compile(r'{(.+)}')
    galleries = map(unicode.strip if sys.version_info.major == 2 else str.strip, filter(None, splitter_regex.split(gallery_string)))
    galleries = [gallery[1:] if gallery.startswith('/') else gallery for gallery in galleries]
    if len(galleries) % 2 == 0 and ' ' not in galleries:
        galleries = zip(zip(['type'] * len(galleries[0::2]), galleries[0::2]), zip(['location'] * len(galleries[0::2]), galleries[1::2]))
        galleries = [dict(gallery) for gallery in galleries]
        for gallery in galleries:
            title = re.search(title_regex, gallery['location'])
            if title:
                gallery['title'] = title.group(1)
                gallery['location'] = re.sub(title_regex, '', gallery['location']).strip()
            else:
                gallery['title'] = DEFAULT_CONFIG['PHOTO_GALLERY_TITLE']
        return galleries
    else:
        logger.error('Unexpected gallery location format! \n{}'.format(pprint.pformat(galleries)))


def process_gallery(generator, content, location):

    content.photo_gallery = []

    galleries = galleries_string_decompose(location)

    for gallery in galleries:

        if gallery['location'] in DEFAULT_CONFIG['created_galleries']:
            content.photo_gallery.append((gallery['location'], DEFAULT_CONFIG['created_galleries'][gallery]))
            continue

        if gallery['type'] == '{photo}':
            dir_gallery = os.path.join(os.path.expanduser(generator.settings['PHOTO_LIBRARY']), gallery['location'])
            rel_gallery = gallery['location']
        elif gallery['type'] == '{filename}':
            base_path = os.path.join(generator.path, content.relative_dir)
            dir_gallery = os.path.join(base_path, gallery['location'])
            rel_gallery = os.path.join(content.relative_dir, gallery['location'])

        if os.path.isdir(dir_gallery):
            logger.info('photos: Gallery detected: {}'.format(rel_gallery))
            dir_photo = os.path.join('photos', rel_gallery.lower())
            dir_thumb = os.path.join('photos', rel_gallery.lower())
            exifs = read_notes(os.path.join(dir_gallery, 'exif.txt'),
                               msg='photos: No EXIF for gallery')
            captions = read_notes(os.path.join(dir_gallery, 'captions.txt'), msg='photos: No captions for gallery')
            blacklist = read_notes(os.path.join(dir_gallery, 'blacklist.txt'), msg='photos: No blacklist for gallery')
            content_gallery = []

            title = gallery['title']
            for pic in sorted(os.listdir(dir_gallery)):
                if pic.startswith('.'):
                    continue
                if pic.endswith('.txt'):
                    continue
                if pic in blacklist:
                    continue
                photo = os.path.splitext(pic)[0].lower() + '.jpg'
                thumb = os.path.splitext(pic)[0].lower() + 't.jpg'
                content_gallery.append((
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

            content.photo_gallery.append((title, content_gallery))
            logger.debug('Gallery Data: '.format(pprint.pformat(content.photo_gallery)))
            DEFAULT_CONFIG['created_galleries']['gallery'] = content_gallery
        else:
            logger.error('photos: Gallery does not exist: {} at {}'.format(gallery['location'], dir_gallery))


def detect_gallery(generator, content):
    if 'gallery' in content.metadata:
        gallery = content.metadata.get('gallery')
        if gallery.startswith('{photo}') or gallery.startswith('{filename}'):
            process_gallery(generator, content, gallery)
        elif gallery:
            logger.error('photos: Gallery tag not recognized: {}'.format(gallery))


def image_clipper(x):
    return x[8:] if x[8] == '/' else x[7:]


def file_clipper(x):
    return x[11:] if x[10] == '/' else x[10:]


def process_image(generator, content, image):

    if image.startswith('{photo}'):
        path = os.path.join(os.path.expanduser(generator.settings['PHOTO_LIBRARY']), image_clipper(image))
        image = image_clipper(image)
    elif image.startswith('{filename}'):
        path = os.path.join(content.relative_dir, file_clipper(image))
        image = file_clipper(image)

    if os.path.isfile(path):
        photo = os.path.splitext(image)[0].lower() + 'a.jpg'
        thumb = os.path.splitext(image)[0].lower() + 't.jpg'
        content.photo_image = (
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
        logger.error('photo: No photo for {} at {}'.format(content.source_path, path))


def detect_image(generator, content):
    image = content.metadata.get('image', None)
    if image:
        if image.startswith('{photo}') or image.startswith('{filename}'):
            process_image(generator, content, image)
        else:
            logger.error('photos: Image tag not recognized: {}'.format(image))


def detect_images_and_galleries(generators):
    """Runs generator on both pages and articles."""
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in itertools.chain(generator.articles, generator.translations, generator.drafts):
                detect_image(generator, article)
                detect_gallery(generator, article)
        elif isinstance(generator, PagesGenerator):
            for page in itertools.chain(generator.pages, generator.translations, generator.hidden_pages):
                detect_image(generator, page)
                detect_gallery(generator, page)


def register():
    """Uses the new style of registration based on GitHub Pelican issue #314."""
    signals.initialized.connect(initialized)
    try:
        signals.content_object_init.connect(detect_content)
        signals.all_generators_finalized.connect(detect_images_and_galleries)
        signals.article_writer_finalized.connect(resize_photos)
    except Exception as e:
        logger.exception('Plugin failed to execute: {}'.format(pprint.pformat(e)))
