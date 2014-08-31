"""
Feed Footer Insert
"""

from __future__ import unicode_literals

from jinja2 import Markup
import six
if not six.PY3:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from pelican import signals
from pelican.writers import Writer
from pelican.utils import set_date_tzinfo

from .magic_set import magic_set


class FeedWriter(Writer):
    def _add_item_to_the_feed(self, feed, item):
        if 'FEED_FOOTER_INSERT_HTML' not in self.settings:
            super(FeedWriter, self)._add_item_to_the_feed(feed, item)
            return

        data_dict = {
            'title': item.title,
            'url': item.url,
            'author': item.author.name,
            'authors': ','.join([x.name for x in item.authors]),
            'slug': item.slug,
            'category': item.category,
            'summary': item.summary,
        }
        feed_foot_insert_html = self.settings['FEED_FOOTER_INSERT_HTML'] % data_dict

        title = Markup(item.title).striptags()
        description = item.get_content(self.site_url) + feed_foot_insert_html
        link = '%s/%s' % (self.site_url, item.url)
        feed.add_item(
            title=title,
            link=link,
            unique_id='tag:%s,%s:%s' % (urlparse(link).netloc,
                                        item.date.date(),
                                        urlparse(link).path.lstrip('/')),
            description=description,
            categories=item.tags if hasattr(item, 'tags') else None,
            author_name=getattr(item, 'author', ''),
            pubdate=set_date_tzinfo(
                item.modified if hasattr(item, 'modified') else item.date,
                self.settings.get('TIMEZONE', None)))


def patch_pelican_writer(pelican_object):
    @magic_set(pelican_object)
    def get_writer(self):
        return FeedWriter(self.output_path,settings=self.settings)


def register():
    signals.initialized.connect(patch_pelican_writer)
