"""
Better Figures
-------

This plugin adds the width of the contained image to .figures.


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


def initialized(pelican):
    pass


def content_object_init(instance):

    def _get_content(self):
        content = self._content
        return content

    instance._get_content = types.MethodType(_get_content, instance)

    if instance._content is not None:
        content = instance._content
        if 'figure' in content:
            soup = BeautifulSoup(content)
            fig = soup.find("div", {"class": "figure"})
            img = instance.settings['PATH'] + '/images/' + os.path.split(fig.img['src'])[1]
            im = Image.open(img)
            # if im.size[0] >= 500 and im.size[1] >= 500:

            style = 'width: {}px;'.format(im.size[0])
            fig['style'] = style
            fig.img['style'] = style

            instance._content = soup.decode()


def register():
    signals.initialized.connect(initialized)
    signals.content_object_init.connect(content_object_init)
