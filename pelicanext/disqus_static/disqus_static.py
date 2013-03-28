# -*- coding: utf-8 -*-
"""
Disqus static comment plugin for Pelican
====================================
This plugin adds a disqus_comments property to all articles.          
Comments are fetched at generation time using disqus API.
"""

from disqusapi import DisqusAPI, Paginator
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
    # first retrieve the threads
    threads = Paginator(disqus.threads.list, 
                        forum=generator.settings['DISQUS_SITENAME'])
    # build a {thread_id: title} dict
    thread_dict = {}
    for thread in threads:
        thread_dict[thread['id']] = thread['title']

    # now retrieve the posts
    posts = Paginator(disqus.posts.list, 
                      forum=generator.settings['DISQUS_SITENAME'])

    # build a {post_id: [child_post1, child_post2, ...]} dict
    child_dict = {}
    for post in posts:
        if post['id'] not in child_dict.keys():
            child_dict[post['id']] = []
        if post['parent'] is not None:
            if str(post['parent']) not in child_dict.keys():
                child_dict[str(post['parent'])] = []
            child_dict[str(post['parent'])].append(post)

    # build a {title: [post1, post2, ...]} dict
    post_dict = {}
    for post in posts:
        build_post_dict(post_dict, child_dict, thread_dict, post)

    for article in generator.articles:
        if article.title in post_dict:
            article.disqus_comments = post_dict[article.title]
            article.disqus_comment_count = sum([
                postcounter(post) for post in post_dict[article.title]])

def postcounter(node):
    return 1 + sum([postcounter(n) for n in node['children']])

def build_post_dict(post_dict, child_dict, thread_dict, post):
    if post['thread'] not in thread_dict.keys():
        return # invalid thread, should never happen

    build_child_dict(child_dict, post)

    if post['parent'] is not None:
        return # this is a child post, don't want to display it here

    if thread_dict[post['thread']] not in post_dict.keys():
        post_dict[thread_dict[post['thread']]] = []
    post_dict[thread_dict[post['thread']]].append(post)

def build_child_dict(child_dict, post):
    post['children'] = child_dict[post['id']]
    for child in child_dict[post['id']]:
        build_child_dict(child_dict, child)

def register():
    signals.initialized.connect(initialized)
    signals.article_generator_finalized.connect(disqus_static)
