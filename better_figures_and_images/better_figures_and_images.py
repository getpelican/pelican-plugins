"""
Better Figures & Images
------------------------

This plugin:

- Adds a style="width: ???px; height: auto;" to each image in the content
- Also adds the width of the contained image to any parent div.figures.
    - If RESPONSIVE_IMAGES == True, also adds style="max-width: 100%;"
- Corrects alt text: if alt == image filename, set alt = ''

TODO: Need to add a test.py for this plugin.

"""

from __future__ import unicode_literals
from os import path, access, R_OK
import os

from pelican import signals

from bs4 import BeautifulSoup
from PIL import Image
import pysvg.parser
import cssutils

import logging
logger = logging.getLogger(__name__)

def content_object_init(instance):

    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, 'html.parser')

        for img in soup(['img', 'object']):
            logger.debug('Better Fig. PATH: %s', instance.settings['PATH'])
            if img.name == 'img':
                logger.debug('Better Fig. img.src: %s', img['src'])
                img_path, img_filename = path.split(img['src'])
            else:
                logger.debug('Better Fig. img.data: %s', img['data'])
                img_path, img_filename = path.split(img['data'])
            logger.debug('Better Fig. img_path: %s', img_path)
            logger.debug('Better Fig. img_fname: %s', img_filename)

            # If the image already has attributes... then we can skip it. Assuming it's already optimised
            if 'style' in img.attrs:
                sheet = cssutils.parseStyle(img['style'])
                if len(sheet.width) > 0 or len(sheet.height) > 0:
                    continue

            # Pelican 3.5+ supports {attach} macro for auto copy, in this use case the content does not exist in output
            # due to the fact it has not been copied, hence we take it from the source (same as current document)
            src = None
            if img_filename.startswith('{attach}'):
                img_path = os.path.dirname(instance.source_path)
                img_filename = img_filename[8:]
                src = os.path.join(img_path, img_filename)
            elif img_path.startswith(('{filename}', '|filename|')):
                # Strip off {filename}, |filename| or /static
                img_path = img_path[10:]
            elif img_path.startswith('{static}'):
                img_path = img_path[8:]
            elif img_path.startswith('/static'):
                img_path = img_path[7:]
            elif img_path.startswith('data:image'):
                # Image is encoded in-line (not a file).
                continue
            else:
                # Check the location in the output as some plugins create them there.
                output_path = path.dirname(instance.save_as)
                image_output_location = path.join(instance.settings['OUTPUT_PATH'], output_path, img_filename)
                if path.isfile(image_output_location):
                    src = image_output_location
                    logger.info('{src} located in output, missing from content.'.format(src=img_filename))
                else:
                    logger.warning('Better Fig. Error: img_path should start with either {attach}, {filename}, |filename|, {static} or /static')

            if src is None:
                # search src path list
                # 1. Build the source image filename from PATH
                # 2. Build the source image filename from STATIC_PATHS

                # if img_path start with '/', remove it.
                img_path = os.path.sep.join([el for el in img_path.split("/") if len(el) > 0])

                # style: {filename}/static/foo/bar.png
                src = os.path.join(instance.settings['PATH'], img_path, img_filename)
                src_candidates = [src]

                # style: {filename}../static/foo/bar.png
                src_candidates += [os.path.join(instance.settings['PATH'], static_path, img_path, img_filename) for static_path in instance.settings['STATIC_PATHS']]

                src_candidates = [f for f in src_candidates if path.isfile(f) and access(f, R_OK)]

                if not src_candidates:
                    logger.error('Better Fig. Error: image not found: %s', src)
                    logger.debug('Better Fig. Skip src: %s', img_path + '/' + img_filename)
                    continue

                src = src_candidates[0]
            logger.debug('Better Fig. src: %s', src)

            # Open the source image and query dimensions; build style string
            try:
                if img.name == 'img':
                    im = Image.open(src)
                    extra_style = 'width: {}px; height: auto;'.format(im.size[0])
                else:
                    svg = pysvg.parser.parse(src)
                    extra_style = 'width: {}px; height: auto;'.format(svg.get_width())
            except IOError as e:
                logger.debug('Better Fig. Failed to open: %s', src)
                extra_style = 'width: 100%; height: auto;'

            if 'RESPONSIVE_IMAGES' in instance.settings and instance.settings['RESPONSIVE_IMAGES']:
                extra_style += ' max-width: 100%;'

            if img.get('style'):
                img['style'] += extra_style
            else:
                img['style'] = extra_style

            if img.name == 'img':
                if img['alt'] == img['src']:
                    img['alt'] = ''

            fig = img.find_parent('div', 'figure')
            if fig:
                if fig.get('style'):
                    fig['style'] += extra_style
                else:
                    fig['style'] = extra_style

        instance._content = soup.decode()


def register():
    signals.content_object_init.connect(content_object_init)
