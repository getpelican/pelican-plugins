# -*- coding: utf-8 -*-
"""
Slug collisions avoidance for Pelican
=====================================
When {slug} is the only parameter used for ARTICLE_URL, this plugin
prevents that different articles generates the same slug, by adding
a numerical increment at the end

Author: leonardo http://github.com/leofiore
"""

from pelican import signals
from pelican import contents
import re

slugs = set()
pattern = re.compile("-[0-9]+$")


def deslug(sender, instance=None):
    if type(sender) != contents.Article:
        return
    slug = sender.slug
    newslug = pattern.sub("", slug)
    i = 1
    while newslug in slugs:
        newslug = "%s-%d" % (slug, i)
        i = i + 1
    slugs.add(newslug)
    sender.slug = newslug


def register():
    signals.content_object_init.connect(deslug)
