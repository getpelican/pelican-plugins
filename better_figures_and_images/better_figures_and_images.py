"""
Better Figures & Images
-------

This plugin:

- Adds a style="width: ???px;" to each image in the content
- Also adds the width of the contained image to any parent div.figures.


<div class="figure">
    <img alt="map to buried treasure" src="/static/images/dunc_smiling_192x192.jpg" />
    <p class="caption">
        This is the caption of the figure (a simple&nbsp;paragraph).
    </p>
    <div class="legend">
        The legend consists of all elements after the caption. In this
        case, the legend consists of this paragraph.
    </div>
</div>

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
                src = instance.settings['PATH'] + '/images/' + os.path.split(img['src'])[1]
                im = Image.open(src)
                extra_style = 'width: {}px;'.format(im.size[0])
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
