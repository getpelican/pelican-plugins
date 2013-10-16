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

import os

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
                # TODO: strip out {filename} explicitly, not using [10:]????
                # Should probably strip off {filename}, |filename| or /static
                src = instance.settings['PATH'] + os.path.split(img['src'])[0][10:] + '/' + os.path.split(img['src'])[1]

                logger.debug('Better Fig. PATH: %s', instance.settings['PATH'])
                logger.debug('Better Fig. img: %s', img['src'])
                logger.debug('Better Fig. src: %s', src)

                im = Image.open(src)
                extra_style = 'width: {}px; height: auto;'.format(im.size[0])

                if instance.settings['RESPONSIVE_IMAGES']:
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
