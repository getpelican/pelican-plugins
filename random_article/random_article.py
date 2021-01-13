# -*- coding: utf-8 -*-
"""
Random Article Plugin For Pelican
========================

This plugin generates a html file which redirect to a random article
using javascript's window.location. The generated html file is 
saved at SITEURL.
"""

from __future__ import unicode_literals

import os.path
import logging

from codecs import open

from pelican import signals

log = logging.getLogger(__name__)

HTML_TOP = """
<!DOCTYPE html>
<head>
    <title>random</title>
    <script type="text/javascript">
        function redirect(){
            var urls = [
"""

HTML_BOTTOM = """
        ""];

        var index = Math.floor(Math.random() * (urls.length-1));
        window.location = urls[index];
    }
</script>
<body onload="redirect()">
</body>
</html>
"""

ARTICLE_URL = """ "{0}/{1}",
"""


class RandomArticleGenerator(object):
    """
        The structure is derived from sitemap plugin
    """

    def __init__(self, context, settings, path, theme, output_path, *null):

        self.output_path = output_path
        self.context = context
        self.siteurl = settings.get('SITEURL')
        self.randomurl = settings.get('RANDOM')

    def write_url(self, article, fd):
        if getattr(article, 'status', 'published') != 'published':
            return

        page_path = os.path.join(self.output_path, article.url)
        if not os.path.exists(page_path):
            return

        fd.write(ARTICLE_URL.format(self.siteurl, article.url))


    def generate_output(self, writer):
        path = os.path.join(self.output_path, self.randomurl)
        articles = self.context['articles']
        log.info('writing %r', path)

        if len(articles) == 0:
            return

        with open(path, 'w', encoding='utf-8') as fd:
            fd.write(HTML_TOP)

            for art in articles:
                self.write_url(art, fd)

            fd.write(HTML_BOTTOM)

def get_generators(generators):
    return RandomArticleGenerator


def register():
    signals.get_generators.connect(get_generators)
