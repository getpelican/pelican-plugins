# -*- coding: utf-8 -*-
"""
Disqus static comment plugin for Pelican
====================================
This plugin adds a disqus_comments property to all articles.          
Comments are fetched at generation time using disqus API.
"""

from disqusapi import DisqusAPI
from pelican import signals

def initialized(pelican):
    from pelican.settings import _DEFAULT_CONFIG
    _DEFAULT_CONFIG.setdefault('DISQUS_SECRET_KEY', '')
    _DEFAULT_CONFIG.setdefault('DISQUS_PUBLIC_KEY', '')
    if pelican:
        pelican.settings.setdefault('DISQUS_SECRET_KEY', '')
        pelican.settings.setdefault('DISQUS_PUBLIC_KEY', '')

def disqus_static(generator):
    disqus = DisqusAPI(generator.settings['DISQUS_SECRET_KEY'], 
                       generator.settings['DISQUS_PUBLIC_KEY'])
    threads = disqus.threads.list(forum=generator.settings['DISQUS_SITENAME'])
    thread_dict = {} # disqus thread id => title
    for thread in threads:
        thread_dict[thread['id']] = thread['title']
    posts = disqus.posts.list(forum=generator.settings['DISQUS_SITENAME'])
    post_dict = {} # title => [post1, post2, ...]
    for post in posts:
        if post['thread'] not in thread_dict.keys():
            continue
        if thread_dict[post['thread']] not in post_dict.keys():
            post_dict[thread_dict[post['thread']]] = []
        post_dict[thread_dict[post['thread']]].append(post)
    for article in generator.articles:
        if article.title in post_dict:
            article.disqus_comments = post_dict[article.title]

def register():
    signals.initialized.connect(initialized)
    signals.article_generator_finalized.connect(disqus_static)
