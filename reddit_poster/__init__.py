"""
Reddit poster posts articles to reddit

You can use the 'subreddit' attribute in you articles to specify which 
subbreddit the article should be post in aside of your default sub.
"""

from collections import OrderedDict

from pelican import signals
from pelican.generators import Generator
from functools import partial
import logging
import praw

log = logging.getLogger(__name__)

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

    subreddits = metadata.get('subreddit')
    subreddits = [] if subreddits is None else subreddits.split(' ')
    subreddits.add(generator.settings['REDDIT_POSTER_COLLECT_SUB'])

    log.debug("Posting in marked subs: %s", subreddits)
    for subreddit in subreddits:
        log.debug("Posting in %s" % subreddit)
        sub = reddit.subreddit(subreddit)
        try:
            sub.submit(metadata['title'], url=url, resubmit=False)
        except praw.exceptions.APIException as e:
            log.error("got an api exception: %s", e)



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
