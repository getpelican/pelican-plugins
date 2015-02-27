from pelican import readers
from pelican.readers import PelicanHTMLTranslator
from pelican import signals
from docutils import nodes

def register():
    class HeaderIDPatchedPelicanHTMLTranslator(PelicanHTMLTranslator):
        def depart_title(self, node):
            close_tag = self.context[-1]
            parent = node.parent
            if isinstance(parent, nodes.section) and parent.hasattr('ids') and parent['ids']:
                anchor_name = parent['ids'][0]
                # add permalink anchor
                if close_tag.startswith('</h'):
                    self.body.append(
                        '<a class="headerlink" href="#%s" title="Permalink to this headline">*</a>' % anchor_name
                    )
            PelicanHTMLTranslator.depart_title(self, node)
    readers.PelicanHTMLTranslator = HeaderIDPatchedPelicanHTMLTranslator
