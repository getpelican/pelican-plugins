"""
Reddit poster posts articles to reddit
===================================

We look for the subreddit in the metadata.
Then try to find a post that has the same title as this article.
If we can't find a post we create it.
"""

from collections import OrderedDict

from pelican import signals

def find_post(sub):
    pass


def fetch_posts(generator, metadata):
    if metadata.get('status') == "draft": # people don't want to post drafts
        print("ignoring draft")
        return

    if 'subreddit' in metadata.keys():
        sub = metadata['subreddit']
        print(metadata['title'], sub)



def register():
    signals.article_generator_context.connect(fetch_posts)
