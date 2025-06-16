# -*- coding: utf-8 -*-
"""
Section number plugin for Pelican
================================
Adds section numbers to section titles of the article
"""

import pelican.contents
from pelican import signals
from bs4 import BeautifulSoup


def _insert_title_number(text: str, level_max: int) -> str:
    levels_count = dict()
    soup = BeautifulSoup(text, 'html.parser')
    previous_level = 0

    for head_tag in soup.find_all([f'h{i}' for i in range(1, level_max)],
                                  recursive=True):
        level = int(head_tag.name.replace('h', ''))

        if level < previous_level:
            for k in levels_count.keys():
                if k > level:
                    levels_count[k] = 0

        levels_count.setdefault(level, 0)
        levels_count[level] += 1

        top_head_string = ''
        for top_level, top_level_count in levels_count.items():
            if top_level < level and top_level_count != 0:
                top_head_string = f'{top_head_string}{top_level_count}.'

        head_tag.string = f'{top_head_string}{levels_count[level]}' \
                          f' {head_tag.string}'
        previous_level = level

    return soup.decode(formatter='html')


def process_content(content: pelican.contents.Article):
    if content._content is None:
        return

    level_max = content.settings.get('SECTION_NUMBER_MAX', 3)

    if level_max <= 0:
        return

    content._content = _insert_title_number(content._content, level_max)


def register():
    signals.content_object_init.connect(process_content)
