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

import logging
logger = logging.getLogger(__name__)

def content_object_init(instance):

    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, 'html.parser')

        if 'img' in content:
            for img in soup('img'):
                logger.debug('Better Fig. PATH: %s', instance.settings['PATH'])
                logger.debug('Better Fig. img.src: %s', img['src'])

                img_path, img_filename = path.split(img['src'])

                logger.debug('Better Fig. img_path: %s', img_path)
                logger.debug('Better Fig. img_fname: %s', img_filename)

                # Strip off {filename}, |filename| or /static
                if img_path.startswith(('{filename}', '|filename|')):
                    img_path = img_path[10:]
                elif img_path.startswith('/static'):
                    img_path = img_path[7:]
                elif img_path.startswith('data:image'):
                    # Image is encoded in-line (not a file).
                    continue
                else:
                    logger.warning('Better Fig. Error: img_path should start with either {filename}, |filename| or /static')

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
                im = Image.open(src)
                extra_style = 'width: {}px; height: auto;'.format(im.size[0])

                if 'RESPONSIVE_IMAGES' in instance.settings and instance.settings['RESPONSIVE_IMAGES']:
                    extra_style += ' max-width: 100%;'

                if img.get('style'):
                    img['style'] += extra_style
                else:
                    img['style'] = extra_style

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
