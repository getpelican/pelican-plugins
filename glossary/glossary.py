"""
Builds a glossary page containing definition lists found in articles
and pages, and adds a `definitions` variable visible to all page templates.

"""

import bs4
from pelican import signals


class Definitions():
    definitions = []
    exclude = []


def make_title(def_title):
    return def_title.text


def make_def(def_title):
    return ''.join(str(t) for t in def_title.find_next('dd').contents)


def make_anchor(def_title):
    return def_title.text.lower().replace(' ', '-')


def set_definitions(generator, metadata):
    generator.context['definitions'] = Definitions.definitions


def get_excludes(pelican):
    Definitions.exclude = pelican.settings.get('GLOSSARY_EXCLUDE', [])


def parse_content(content):
    soup = bs4.BeautifulSoup(content._content, 'html.parser')

    for def_list in soup.find_all('dl'):
        defns = []
        for def_title in def_list.find_all('dt'):
            if def_title.text not in Definitions.exclude:
                anchor_name = make_anchor(def_title)
                anchor_tag = bs4.Tag(name="a", attrs={'name': anchor_name})
                index = def_list.parent.index(def_list)-1
                def_list.parent.insert(index, anchor_tag)

                defns.append(
                    {'title': make_title(def_title),
                     'definition': make_def(def_title),
                     'anchor': anchor_name,
                     'source': content})

        for defn in defns:
            defn['see_also'] = [d for d in defns if d is not defn]

        Definitions.definitions += defns

    content._content = str(soup)


def parse_articles(generator):
    for article in generator.articles:
        parse_content(article)


def register():
    signals.initialized.connect(get_excludes)
    signals.article_generator_finalized.connect(parse_articles)
    signals.page_generator_context.connect(set_definitions)
