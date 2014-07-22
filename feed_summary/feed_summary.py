# -*- coding: utf-8 -*-
"""
Feed Summary
============

This plugin allows summaries to be used in feeds instead of the full length article.
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

class FeedSummaryWriter(Writer):
    def _add_item_to_the_feed(self, feed, item):
        if self.settings['FEED_USE_SUMMARY']:
            title = Markup(item.title).striptags()
            link = '%s/%s' % (self.site_url, item.url)
            feed.add_item(
                title=title,
                link=link,
                unique_id='tag:%s,%s:%s' % (urlparse(link).netloc,
                                            item.date.date(),
                                            urlparse(link).path.lstrip('/')),
                description=item.summary if hasattr(item, 'summary') else item.get_content(self.site_url),
                categories=item.tags if hasattr(item, 'tags') else None,
                author_name=getattr(item, 'author', ''),
                pubdate=set_date_tzinfo(item.modified if hasattr(item, 'modified') else item.date,
                    self.settings.get('TIMEZONE', None)))
        else:
            super(FeedSummaryWriter, self)._add_item_to_the_feed(feed, item)

def set_feed_use_summary_default(pelican_object):
    # modifying DEFAULT_CONFIG doesn't have any effect at this point in pelican setup
    # everybody who uses DEFAULT_CONFIG is already used/copied it or uses the pelican_object.settings copy.

    pelican_object.settings.setdefault('FEED_USE_SUMMARY', False)

def patch_pelican_writer(pelican_object):
    @magic_set(pelican_object)
    def get_writer(self):
        return FeedSummaryWriter(self.output_path,settings=self.settings)

def register():
    signals.initialized.connect(set_feed_use_summary_default)
    signals.initialized.connect(patch_pelican_writer)
