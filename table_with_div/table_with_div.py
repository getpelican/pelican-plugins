"""
Footer Insert
"""

from pelican import signals
from pelican.contents import Content, Article

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def add_table_div(instance):
    if not isinstance(instance, Article):
        return
    content = instance._content
    if not '<table' in content:
        return

    soup = BeautifulSoup(content, "html.parser")
    for table in soup.find_all("table"):
        div = soup.new_tag('div')
        div['style'] = 'overflow-x: auto;'
        table.wrap(div)

    instance._content = str(soup)

def register():
    signals.content_object_init.connect(add_table_div)
