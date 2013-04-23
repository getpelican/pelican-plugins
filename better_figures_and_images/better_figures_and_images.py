"""
Better Figures & Images
-------

This plugin:

- Adds a style="width: ???px;" to each image in the content
- Also adds the width of the contained image to any parent div.figures.

TODO: Need to add a test.py for this plugin.

"""

import types
import os

from pelican import signals

from bs4 import BeautifulSoup
from PIL import Image


def content_object_init(instance):

    def _get_content(self):
        content = self._content
        return content

    instance._get_content = types.MethodType(_get_content, instance)

    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content)

        if 'img' in content:
            for img in soup('img'):
                # TODO: Pretty sure this isn't the right way to do this, too hard coded.
                # There must be a setting that I should be using?
                src = instance.settings['PATH'] + '/images/' + os.path.split(img['src'])[1]
                im = Image.open(src)
                extra_style = 'width: {}px; height: auto;'.format(im.size[0])
                if img.get('style'):
                    img['style'] += extra_style
                else:
                    img['style'] = extra_style
                fig = img.find_parent('div', 'figure')
                if fig:
                    if fig.get('style'):
                        fig['style'] += extra_style
                    else:
                        fig['style'] = extra_style

        instance._content = soup.decode()


def register():
    signals.content_object_init.connect(content_object_init)
