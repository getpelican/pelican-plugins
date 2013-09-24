# -*- coding: utf-8 -*-

# NEEDS WORK
"""
Copyright (c) Marco Milanesi <kpanic@gnufunk.org>

Github Activity
---------------
A plugin to list your Github Activity
"""

from __future__ import unicode_literals, print_function

import logging
logger = logging.getLogger(__name__)

from pelican import signals


class GitHubActivity():
    """
        A class created to fetch github activity with feedparser
    """
    def __init__(self, generator):
        import feedparser
        self.activities = feedparser.parse(
            generator.settings['GITHUB_ACTIVITY_FEED'])

    def fetch(self):
        """
            returns a list of html snippets fetched from github actitivy feed
        """

        entries = []
        for activity in self.activities['entries']:
            entries.append(
                    [element for element in [activity['title'],
                        activity['content'][0]['value']]])

        return entries


def fetch_github_activity(gen, metadata):
    """
        registered handler for the github activity plugin
        it puts in generator.context the html needed to be displayed on a
        template
    """

    if 'GITHUB_ACTIVITY_FEED' in gen.settings.keys():
        gen.context['github_activity'] = gen.plugin_instance.fetch()


def feed_parser_initialization(generator):
    """
        Initialization of feed parser
    """

    generator.plugin_instance = GitHubActivity(generator)


def register():
    """
        Plugin registration
    """
    try:
        signals.article_generator_init.connect(feed_parser_initialization)
        signals.article_generator_context.connect(fetch_github_activity)
    except ImportError:
        logger.warning('`github_activity` failed to load dependency `feedparser`.'
                       '`github_activity` plugin not loaded.')
