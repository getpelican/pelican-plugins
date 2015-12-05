# -*- coding: utf-8 -*-
"""
Static Discussion via Hubski plugin for Pelican
====================================
This plugin makes the following properties available to an article:
- hubski_comments: contains the all child publications (i.e. comments) fetched from the Hubski API.
- hubski_comment_count: contains the number of comments

The plugin cannot search Hubski for your post. Each post must
have a "Hubski_ID" property in the metadata which contains
the ID of the post on Hubski. Posts without an ID will be
skipped.

This plugin gets all its Hubski URLs from the Pelican conf file so that
they can easily be updated if the API changes. The following are the
valid URLs at the time of writing:
HUBSKI_URL = 'https://hubski.com'
HUBSKI_POST_URL = HUBSKI_URL + '/pub?id='
HUBSKI_USER_URL = HUBSKI_URL + '/user?id='
HUBSKI_API_URL = 'http://api.hubski.com'
HUBSKI_API_TREE_URL = HUBSKI_API_URL + '/publication/$id/tree'
"""

from __future__ import unicode_literals
from bs4 import BeautifulSoup
from datetime import date
from pelican import signals
import requests
from string import Template

def hubski_static(generator):
    # API end-points should be defined in the conf file so they can easily be changed
    tree_template = Template(generator.settings.get('HUBSKI_API_TREE_URL'))

    for article in generator.articles:
        post_id = getattr(article, 'hubski_id', None)
        if post_id is not None:
            post_tree_url = tree_template.safe_substitute(id=post_id)
            publication = requests.get(post_tree_url).json()

            # Perform any desired transformations on the comments
            comments, comment_count = hubski_alter_comments(generator, publication)

            # Make a count of top-level comments available in the templates
            article.hubski_comment_count = comment_count

            # Make the comments available to the templates
            article.hubski_comments = comments

def hubski_alter_comments(generator, publication):
    children = []
    children_count = 0
    if 'children' in publication:
        for child in publication['children']:
            soup = BeautifulSoup(child['text'])
            for a in soup.find_all('a'):
                # Update relative links with full paths
                if not a['href'].startswith('http'):
                    a['href'] = generator.settings.get('HUBSKI_URL') + '/' + a['href']
                # Also make them open in a new window
                a['target'] = '_blank'
            child['text'] = unicode(soup)

            # Human-readable date
            child['iso_date'] = date.fromtimestamp(child['time']).isoformat()

            # Recursively process the child's children
            child['children'], sub_children_count = hubski_alter_comments(generator, child)

            # Keep a running total of all children
            children_count = children_count + sub_children_count

            children.append(child)

    children_count = children_count + len(children)
    return [children, children_count]

def register():
    signals.article_generator_finalized.connect(hubski_static)
