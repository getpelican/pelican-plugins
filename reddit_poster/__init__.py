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
import lxml.html

log = logging.getLogger(__name__)

def cross_post(reddit, submission, subs):
    subreddits = [] if subs is None else subs.split(' ')
    log.debug("Posting in marked subs: %s", subreddits)
    for sub in subreddits:
        if sub == '':
            continue
        log.debug("Posting in %s" % sub)
        subreddit = reddit.subreddit(sub)
        subreddit.subscribe() # must be subscribed to crosspost
        submission.crosspost(subreddit)

def make_posts(generator, metadata, url):
    """
    Make posts on reddit if it's not a draft, on whatever subs are specified
    """
    reddit = generator.get_reddit()
    title =  lxml.html.fromstring(metadata['title']).text_content()
    if reddit is None:
        log.info("Reddit plugin not enabled")
        return
    if metadata.get('status') == "draft": # people don't want to post drafts
        log.debug("ignoring draft %s" % title)
        return

    collection = generator.settings['REDDIT_POSTER_COLLECT_SUB']
    sub = reddit.subreddit(collection)
    results = sub.search(title)
    if len([result for result in results]) > 0:
        log.debug("ignoring %s because it is already on sub %s " % (title, collection))
        # post already was made to this sub
        return
    try:
        submission = sub.submit(title, url=url, resubmit=False)
        cross_post(reddit, submission, metadata.get('subreddit'))
    except praw.exceptions.APIException as e:
        log.error("got an api exception: %s", e)
    except AssertionError as e:
        log.error("Received an assertion error %s", e)


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
