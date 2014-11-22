from pelican import signals

from bs4 import BeautifulSoup

import logging
logger = logging.getLogger(__name__)

HEADERS = ['h%d' % i for i in range (1, 7)]

def content_object_init(instance):

    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content)

        for headertag in HEADERS:
          if headertag in content:
            for header in soup(headertag):
              header['id'] = "".join(header.contents).lower().replace(" ", "")

        instance._content = soup.decode()


def register():
    signals.content_object_init.connect(content_object_init)
