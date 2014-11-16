# -*- coding: utf-8 -*-
"""
Static Discussion via Hubski plugin for Pelican
====================================
This plugin makes the following properties available to an article:
- hubski_comments: contains the HTML of all comments screen-scraped
  from Hubski.
- hubski_comment_count: contains the number of comments
- hubski_post_url: the URL of this post on Hubski

The plugin cannot search Hubski for your post. Each post must
have a "Hubski_ID" property in the metadata which contains
the ID of the post on Hubski. Posts without an ID will be
skipped.

By default this plugin uses "https://hubski.com" as the Hubski URL,
and appends "/pub?id=" as the resource. If these change, the default
values can be overridden in the settings using HUBSKI_URL and
HUBSKI_POST_URL.
"""

from __future__ import unicode_literals
from bs4 import BeautifulSoup
from pelican import signals
import requests

def hubski_static(generator):
    # Get settings -- the defaults should work, but can be overridden
    # if Hubski changes its URL format
    hubski_url = generator.settings.get('HUBSKI_URL', 'https://hubski.com')
    hubski_post_url = generator.settings.get('HUBSKI_POST_URL', hubski_url + '/pub?id=')

    for article in generator.articles:
        post_id = getattr(article, 'hubski_id', None)
        if post_id:
            post = requests.get(hubski_post_url+post_id)
            soup = BeautifulSoup(post.text)

            # Get the smallest div we can that contains all the comments
            comments = soup.find('div', {'class': 'rightmenu'}).next_sibling

            # Scrape away the bits that aren't comments
            comments.find('div', {'class': 'sub'}).extract()
            comments.find('div', {'class': 'wholepub'}).extract()

            # Remove reply links and voting divs
            for links in comments.find_all('div', {'class': ['plusminus', 'underlink']}):
                links.extract()

            # Update relative links with full paths
            # Also make them open in a new window
            for a in comments.find_all('a'):
                if not a['href'].startswith('http'):
                    a['href'] = hubski_url + '/' + a['href']
                a['target'] = '_blank'

            # Make a count of comments available in the templates
            article.hubski_comment_count = len(comments.find_all('div', {'class': 'outercomm'}))

            # Convert the soup object to a string
            # and make it available to the templates
            article.hubski_comments = unicode(comments)

            # Create a link to this post on Hubski
            article.hubski_post_url = hubski_post_url + post_id

def register():
    signals.article_generator_finalized.connect(hubski_static)
