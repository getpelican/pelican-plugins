"""
Builds a glossary page containing definition lists found in articles
and pages, and adds a `definitions` variable visible to all page templates.

"""

from pelican import signals, contents
from bs4 import BeautifulSoup


class Definitions():
    definitions = []
    exclude = []


def extract_definitions(content):
    soup = BeautifulSoup(content.content, 'html.parser')

    for def_list in soup.find_all('dl'):
        defns = []
        for def_title in def_list.find_all('dt'):
            if def_title.text not in Definitions.exclude:
                defns.append(
                    {'title': get_title(def_title),
                     'link': get_link(def_title, content.url),
                     'definition': get_def(def_title),
                     'source': content})

        for defn in defns:
            defn['see_also'] = [also for also in defns if also is not defn]

        Definitions.definitions += defns


def get_title(def_title):
    return def_title.text


def get_link(def_title, url):
    a_tag = def_title.findChild('a')
    if a_tag and a_tag['href']:
        return url + a_tag['href']
    else:
        return None


def get_def(def_title):
    return ''.join(str(t) for t in def_title.find_next('dd').contents)


def parse_content(content):
    if isinstance(content, contents.Static) or not content.content:
        return
    else:
        return extract_definitions(content)


def set_definitions(generator, metadata):
    generator.context['definitions'] = Definitions.definitions


def get_excludes(generator, metadata):
    Definitions.exclude = generator.context.get('GLOSSARY_EXCLUDE', [])


def register():
    signals.article_generator_context.connect(get_excludes)
    signals.content_object_init.connect(parse_content)
    signals.page_generator_context.connect(set_definitions)
