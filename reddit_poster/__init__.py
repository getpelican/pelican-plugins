"""
Reddit poster posts articles to reddit
===================================

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


import praw
from functools import partial

def find_post(sub):
    pass


def make_posts(generator, metadata):
    """
    """
    reddit = generator.get_reddit()
    # TODO init once
    if metadata.get('status') == "draft": # people don't want to post drafts
        print("ignoring draft")
        return

    if 'subreddit' in metadata.keys():
        print("SUBMITTING TO REDDIT")
        print("SUBMITTING TO REDDIT")
        print("SUBMITTING TO REDDIT")
        print("SUBMITTING TO REDDIT")
        print(metadata)
        sub = reddit.subreddit('jappie')
        results = sub.search("title:%s" % metadata['title'])
        if len([result for result in results]) > 0:
            print("ignoring this one, already has")
            return
        sub.submit(metadata['title'], selftext="Attempts to make this work with the script")
        print(metadata['title'], sub)



def init_reddit(generator):
    """
    this is a hack to make sure the reddit object keeps track of a session
    trough article scanning, speeding up networking as the connection can be 
    kept alive.
    """
    reddit = praw.Reddit(**generator.settings['REDDIT_POSTER_AUTH'])
    generator.get_reddit = lambda: reddit # .. openworld has it's merrits
def content_written(generator, content):
    print('---- wirritgn some more!')
    print(content.title)
    print(content.filename)
    print(content.url)
    print(content.metadata)
    print(type(content))
    print('----')
def register():
    signals.article_generator_write_article.connect(content_written)
    signals.article_generator_init.connect(init_reddit)
    signals.article_generator_context.connect(make_posts)
