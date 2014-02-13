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

from os import path, access, R_OK

from pelican import signals

from bs4 import BeautifulSoup
from PIL import Image

import logging
logger = logging.getLogger(__name__)

def content_object_init(instance):

    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content)

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
                else:
                    logger.warning('Better Fig. Error: img_path should start with either {filename}, |filename| or /static')

                # Build the source image filename
                src = instance.settings['PATH'] + img_path + '/' + img_filename

                logger.debug('Better Fig. src: %s', src)
                if not (path.isfile(src) and access(src, R_OK)):
                    logger.error('Better Fig. Error: image not found: {}'.format(src))

                if instance.settings['RESPONSIVE_IMAGES']:
                    new_style = 'max-width:100%;'
                    extra_style = 'max-width:100%;'
                else:
                    new_style = ''
                    extra_style = ''

                # Pull all of the style tags out, so they can be modified
                if img.get('style'):
                    style_tags = dict([tag.replace(' ', '').split(':') for tag in img.get('style').split(';') if ':' in tag])
                else:
                    style_tags = dict()
                
                # Only open and decode the image if neither width nor height are given
                if 'width' not in style_tags and 'height' not in style_tags:
                    style_tags['width'] = '{}px'.format(Image.open(src).size[0])
                    style_tags['height'] = 'auto'
                elif 'height' not in style_tags:
                    style_tags['height'] = 'auto'
                elif 'width' not in style_tags:
                    style_tags['width'] = 'auto'

                for k, v in style_tags.iteritems():
                    new_style += '%s;' % ':'.join([k, v])

                extra_style += 'width:%s;height:%s;' % (style_tags['width'], style_tags['height'])

                img['style'] = new_style

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
