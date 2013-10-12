# -*- encoding: UTF-8 -*-
# @author: wilbur.ma@foxmail.com
# @date: 2013-10-11
# @license: BSD 3-Clause Licencse
'''
A simple pelican plugin which can
    1) use the value of `update' metadata as update date
    2) use filesystem's mtime value as update date if the `update' metadata is not defined

New variables:
    1) article.updatedate
    2) page.updatedate
'''

import os, logging
from datetime import datetime
from pelican import signals
from pelican.utils import get_date

def set_update_date(content):
    '''read `update' metadata or filesysystem's mtime
    '''

    if not content._context:
        return

    content.updatedate = content.date

    for k, v in content.metadata.items():
        if "update" == k.lower():
            content.updatedate = get_date(v)
            return

    try:
        content.updatedate = datetime.fromtimestamp(os.path.getmtime(content.source_path))
        content.updatedate = content.updatedate.replace(microsecond = 0)
    except os.error:
        logging.error("{} not exists or not readable".format(content.source_path))

def register():
    signals.content_object_init.connect(set_update_date)

