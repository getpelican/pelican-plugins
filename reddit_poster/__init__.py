"""
Reddit poster posts articles to reddit
===================================

You can use the 'subreddit' attribute in you articles to specify which 
subbreddit the article should be post in aside of your default sub.

We look for the subreddit in the metadata.
Then try to find a post that has the same title as this article.
If we can't find a post we create it.

## Usage
I followed these steps for praw: https://praw.readthedocs.io/en/latest/getting_started/authentication.html#script-application
Summeraized:
+ Go to https://www.reddit.com/prefs/apps/ 
+ create a script for example named 'reddit-poster'.
+ redirect uri is unused so can be http://localhost:8080
+ about uri is probably some page on your website, not important either I think

This will create an 'application', ie it let's reddit know you have a script by 
using the secret generated.
Interesting from this screen is the secret and the app id. copy those over 
somewhere.

We need 4 pieces of information from you which you must *not* commit to source 
code. These should all be considered private.
This script will expect these values to be set in the settings.
You should store them for real in either an ignored file, environment variables,
or pass them each time as command line options.
Also make sure to set your SITEURL, for proper backlinks

https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html#praw.models.Subreddit.search
https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html#praw.models.Subreddit.submit

## Dependencies
+ praw 5.4

On fedora the praw in yum is too old, however the pip requests doesn't 
work for some reason, so I installed praw with pip and requests with dnf 
which seems to work (requests probably needed some sys lib or something)
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
