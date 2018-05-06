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
"""

from collections import OrderedDict

from pelican import signals
from pelican.generators import Generator


import praw
from functools import partial

def find_post(sub):
    pass


def fetch_posts(generator, metadata):
    reddit = generator.get_reddit()
    print("reddit is")
    print(reddit)
    # TODO init once
    if metadata.get('status') == "draft": # people don't want to post drafts
        print("ignoring draft")
        return

    if 'subreddit' in metadata.keys():
        print("SUBMITTING TO REDDIT")
        print("SUBMITTING TO REDDIT")
        print("SUBMITTING TO REDDIT")
        print("SUBMITTING TO REDDIT")
        sub = reddit.subreddit('jappie')
        sub.submit(metadata['title'], selftext="Attempts to make this work with the script")
        print(metadata['title'], sub)



def init_reddit(generator):
    print("reddit initialized")
    print(generator.settings['REDDIT_POSTER_AUTH'])
    reddit = praw.Reddit(**generator.settings['REDDIT_POSTER_AUTH'])
    print("read only %s " % reddit.read_only)
    generator.get_reddit = lambda: reddit # .. openworld has it's merrits

def register():
    signals.article_generator_init.connect(init_reddit)
    signals.article_generator_context.connect(fetch_posts)
