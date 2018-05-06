# -*- coding: utf-8 -*-
"""
Section number plugin for Pelican
================================
Adds section numbers to section titles of the article
"""

from pelican import signals


def _extract_level(text, idx):
    end = text.find(">", idx)

    if end == -1:
        return (idx, -1)

    try:
        level = int(text[idx: end])
        return (end, level)

    except:
        return (idx, -1)


def _level_str(level_nums, level_max):
    ret = u''

    if len(level_nums) > level_max:
        return ret

    for n in level_nums:
        ret += str(n) + '.'

    return ret[:-1]


def _insert_title_number(text, level_max):
    idx = 0
    levels = []
    level_nums = []

    while True:
        idx = text.find("<h", idx)
        if idx == -1:
            break

        (idx, level) = _extract_level(text, idx + 2)

        if level == -1:
            continue

        if not levels:
            levels += [level]
            level_nums += [1]

        elif level == levels[-1]:
            level_nums[-1] += 1

        elif level < levels[-1]:
            while level < levels[-1]:
                levels.pop()
                level_nums.pop()
            level_nums[-1] += 1

        else:
            while level > levels[-1]:
                levels += [levels[-1] + 1]
                level_nums += [1]

        text = text[:idx + 1] + \
            _level_str(level_nums, level_max) + '. ' + text[idx + 1:]

    # print text.encode('gb2312')
    return text


def process_content(content):
    if content._content is None:
        return

    level_max = content.settings.get('SECTION_NUMBER_MAX', 3)

    if level_max <= 0:
        return

    content._content = _insert_title_number(content._content, level_max)


def register():
    signals.content_object_init.connect(process_content)
