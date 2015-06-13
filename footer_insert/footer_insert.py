"""
Footer Insert
"""

from pelican import signals
from pelican.contents import Content, Article


def add_footer(content):
    if not isinstance(content, Article):
        return
    
    if 'FOOTER_INSERT_HTML' not in content.settings:
        return
    data_dict = {
        'title': content.title,
        'url': content.url,
        'author': content.author.name,
        'authors': ','.join([x.name for x in content.authors]),
        'slug': content.slug,
        'category': content.category,
        'summary': content.summary,
    }
    if hasattr(content, 'date'):
        data_dict['date'] = content.date
    foot_insert_html = content.settings['FOOTER_INSERT_HTML'] % data_dict
    content.footer_insert_html = foot_insert_html

def register():
    signals.content_object_init.connect(add_footer)
