# -*- coding: utf-8 -*-

import os

from pelican import signals


CTAGS_TEMPLATE = '''{% for tag, articles in tags_articles %}
{% for article in articles %}
{{tag}}\t{{article}}\t0;"\ttag
{% endfor %}
{% endfor %}
'''


def generate_ctags(article_generator, writer):
    tags_file_path = os.path.join(article_generator.path, 'tags')
    if article_generator.settings.get('WRITE_SELECTED'):
        article_generator.settings['WRITE_SELECTED'].append(tags_file_path)
    writer.output_path = article_generator.path
    try:
        writer.write_file('tags', article_generator.env.from_string(CTAGS_TEMPLATE), article_generator.context,
                          tags_articles=sorted(article_generator.tags.items()))
    finally:
        writer.output_path = article_generator.output_path


def register():
    signals.article_writer_finalized.connect(generate_ctags)
