import logging

import time

from pelican import signals



logger = logging.getLogger(__name__)

try:
    from git import Repo
except ImportError:
    logger.warning("Could not import git!")



def get_commit_id(gen):
    p = gen.settings.get('PATH')
    r = Repo(p, search_parent_directories=True)
    c = r.head.commit
    gen.settings["COMMITID"] = c.hexsha
    gen.settings["COMMITDATE"] = time.ctime(c.committed_date)
    logger.info("found commit id %s from %s" % (c.hexsha,time.ctime(c.committed_date) ))


def register():
    signals.initialized.connect(get_commit_id)
