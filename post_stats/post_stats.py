# -*- coding: utf-8 -*-
"""
Post Statistics
========================

This plugin calculates various Statistics about a post and stores them in an article.stats disctionary.

wc: how many words
read_minutes: how many minutes to read this article, based on 250 wpm (http://en.wikipedia.org/wiki/Words_per_minute#Reading_and_comprehension)
word_count: frquency count of all the words in the article; can be used for tag/word clouds/

"""

from pelican import signals
# import math

# import nltk

from bs4 import BeautifulSoup

# import lxml.html
# from lxml.html.clean import Cleaner

import re
from collections import Counter


def calculate_stats(instance):

    # How fast do average people read?
    WPM = 250

    if instance._content is not None:
        stats = {}
        content = instance._content

        # print content
        entities = r'\&\#?.+?;'
        content = content.replace('&nbsp;', ' ')
        content = re.sub(entities, '', content)
        # print content

        # Pre-process the text to remove punctuation
        drop = u'.,?!@#$%^&*()_+-=\|/[]{}`~:;\'\"‘’—…“”'
        content = content.translate(dict((ord(c), u'') for c in drop))

        # nltk
        # raw_text = nltk.clean_html(content)

        # BeautifulSoup
        raw_text = BeautifulSoup(content).getText()
        # raw_text = ''.join(BeautifulSoup(content).findAll(text=True))

        # lxml
        # cleaner = Cleaner(style=True)
        # html = lxml.html.fromstring(content)
        # raw_text = cleaner.clean_html(html).text_content()

        # stats['wc'] = len(re.findall(r'\b', raw_text)) >> 1

        # print raw_text

        words = raw_text.lower().split()
        word_count = Counter(words)
        # print word_count

        stats['word_counts'] = word_count
        stats['wc'] = sum(word_count.values())
        # stats['read_minutes'] = math.ceil(float(stats['wc']) / float(WPM))
        stats['read_minutes'] = (stats['wc'] + WPM - 1) // WPM
        if stats['read_minutes'] == 0:
            stats['read_minutes'] = 1

        instance.stats = stats
        instance.raw_text = raw_text


def register():
    signals.content_object_init.connect(calculate_stats)
