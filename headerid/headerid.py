from pelican import readers
from pelican.readers import PelicanHTMLTranslator
from pelican import signals
from docutils import nodes

LINK_CHAR = '*'


def init_headerid(sender):
    global LINK_CHAR
    char = sender.settings.get('HEADERID_LINK_CHAR')
    if char:
        LINK_CHAR = char

def register():
    signals.initialized.connect(init_headerid)


    class HeaderIDPatchedPelicanHTMLTranslator(PelicanHTMLTranslator):
        def depart_title(self, node):
            close_tag = self.context[-1]
            parent = node.parent
            if isinstance(parent, nodes.section) and parent.hasattr('ids') and parent['ids']:
                anchor_name = parent['ids'][0]
                # add permalink anchor
                if close_tag.startswith('</h'):
                    self.body.append(
                        '<a class="headerlink" href="#%s" title="Permalink to this headline">%s</a>' %
                        (anchor_name, LINK_CHAR))
            PelicanHTMLTranslator.depart_title(self, node)
    readers.PelicanHTMLTranslator = HeaderIDPatchedPelicanHTMLTranslator
