"""
Reddit poster posts articles to reddit

You can use the 'subreddit' attribute in you articles to specify which 
subbreddit the article should be post in aside of your default sub.
"""

from collections import OrderedDict

from pelican import signals
from pelican.generators import Generator
import logging
log = logging.getLogger(__name__)


import praw
from functools import partial

def find_post(sub):
    pass


def make_posts(generator, metadata, url):
    """
    Make posts on reddit if it's not a draft, on whatever subs are specified
    """
    reddit = generator.get_reddit()
    if reddit is None:
        log.info("Reddit plugin not enabled")
        return
    if metadata.get('status') == "draft": # people don't want to post drafts
        log.debug("ignoring draft %s" % metadata['title'])
        return

    sub = reddit.subreddit(generator.settings['REDDIT_POSTER_COLLECT_SUB'])
    results = sub.search("title:%s" % metadata['title'])
    if len([result for result in results]) > 0:
        log.debug("ignoring %s because it is already on reddit" % metadata['title'])
        # post already was made to this sub
        return
    log.debug("Putting in collect sub")
    sub.submit(metadata['title'], url=url)
    if not 'subreddit' in metadata.keys():
        log.debug("stopping %s because it has no subreddit key" % metadata['title'])
        return

    log.debug("Posting in marked subs")
    for subreddit in metadata['subreddit'].split(' '):
        log.debug("Posting in %s" % subreddit)
        sub = reddit.subreddit(subreddit)
        try:
            sub.submit(metadata['title'], url=url)
        except praw.exceptions.APIException as e:
            log.error("got an api exception: ", e)



def init_reddit(generator):
    """
    this is a hack to make sure the reddit object keeps track of a session
    trough article scanning, speeding up networking as the connection can be 
    kept alive.
    """
    auth_dict = generator.settings.get('REDDIT_POSTER_AUTH')
    if auth_dict is None:
        log.info("Could not find REDDIT_POSTER_AUTH key in settings, reddit plugin won't function")
        generator.get_reddit = lambda: None
        return

    reddit = praw.Reddit(**auth_dict)
    generator.get_reddit = lambda: reddit # .. openworld has it's merrits

def content_written(generator, content):
    """
    create a url and call make posts (which has less information)
    """
    url = "%s/%s" % (generator.settings.get('SITEURL', 'http://localhost:8000'), content.url)
    make_posts(generator, content.metadata, url)

def register():
    signals.article_generator_write_article.connect(content_written)
    signals.article_generator_init.connect(init_reddit)
