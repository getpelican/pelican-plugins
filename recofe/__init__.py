"""
Recofe is a REddit COmment FEtcher.
===================================

We look for the subreddit in the metadata.
Then try to find a post that has the same title as this article.
If we can't find a post we create it.
Finally we get the comment tree from said post.
We expose this to the templates.

So two things happen. 1 this thing can expose your posts to reddit. 
2 this thing exposes comments so you can put them somewhere in your articles.
"""

from collections import OrderedDict

from pelican import signals


def fetch_posts(generator, metadata):

    if 'subreddit' in metadata.keys():
        sub = metadata['subreddit']
        metadata['comments'] = [
            {'author': 'japjap', 'content': 'wow leuk howr'},
            {'author': 'henk', 'content': 'Ik ben mijn fiets kwijt'}
        ]
        print(sub)


def register():
    signals.article_generator_context.connect(fetch_posts)
