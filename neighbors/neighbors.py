# -*- coding: utf-8 -*-
"""
Neighbor Articles Plugin for Pelican
====================================

This plugin adds ``next_article`` (newer) and ``prev_article`` (older) 
variables to the article's context
"""

from pelican import signals

def iter3(seq):
    it = iter(seq)
    nxt = None
    cur = next(it)
    for prv in it:
        yield nxt, cur, prv
        nxt, cur = cur, prv
    yield nxt, cur, None

def neighbors(generator):
    for nxt, cur, prv in iter3(generator.articles):
        cur.next_article = nxt
        cur.prev_article = prv

def register():
    signals.article_generator_finalized.connect(neighbors)
