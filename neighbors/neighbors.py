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

def get_translation(article, prefered_language):
    if not article:
        return None
    for translation in article.translations:
        if translation.lang == prefered_language:
            return translation
    return article

def neighbors(generator):
    for nxt, cur, prv in iter3(generator.articles):
        cur.next_article = nxt
        cur.prev_article = prv

        for translation in cur.translations:
            translation.next_article = get_translation(nxt, translation.lang)
            translation.prev_article = get_translation(prv, translation.lang)

def register():
    signals.article_generator_finalized.connect(neighbors)
