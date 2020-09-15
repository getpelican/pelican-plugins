from pelican import signals

import logging
import os
import time


logger = logging.getLogger(__name__)


def set_file_utime(path, datetime):
    mtime = time.mktime(datetime.timetuple())
    logger.info('touching %s', path)
    os.utime(path, (mtime, mtime))


def touch_file(path, context):
    content = context.get('article', context.get('page'))
    page = context.get('articles_page')
    dates = context.get('dates')

    if content and hasattr(content, 'date'):
        set_file_utime(path, content.date)
    elif page:
        set_file_utime(path, max(x.date for x in page.object_list))
    elif dates:
        set_file_utime(path, max(x.date for x in dates))


def touch_feed(path, context, feed):
    set_file_utime(path, max(x['pubdate'] for x in feed.items))


def register():
    signals.content_written.connect(touch_file)
    signals.feed_written.connect(touch_feed)
