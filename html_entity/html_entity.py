from docutils import nodes, utils
from docutils.parsers.rst import roles
from pelican.readers import PelicanHTMLTranslator

class html_entity(nodes.Inline, nodes.Node):
    def __init__(self, rawsource, text):
        self.rawsource = rawsource
        self.text = text
        self.children = []
        self.attributes = {}

    def astext(self):
        return self.text


def entity_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    entity_code = text
    try:
        entity_code = "#{}".format(unicode(int(entity_code)))
    except ValueError:
        pass
    entity_code = "&{};".format(entity_code)
    return [html_entity(text, entity_code)], []


def register():
    roles.register_local_role('html_entity', entity_role)

PelicanHTMLTranslator.visit_html_entity = lambda self, node: self.body.append(node.astext())
PelicanHTMLTranslator.depart_html_entity = lambda self, node: None
