from pelican import signals

import logging
import os
import time


logger = logging.getLogger(__name__)


def touch_file(path, context):
    content = context.get('article', context.get('page'))
    if content and hasattr(content, 'date'):
        mtime = time.mktime(content.date.timetuple())
        logger.info('touching %s', path)
        os.utime(path, (mtime, mtime))


def register():
    signals.content_written.connect(touch_file)
