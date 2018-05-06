# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Bootstrap RST
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from docutils import nodes, utils
from docutils.parsers.rst import roles

class h1(nodes.Inline, nodes.TextElement): pass
class h2(nodes.Inline, nodes.TextElement): pass
class h3(nodes.Inline, nodes.TextElement): pass
class h4(nodes.Inline, nodes.TextElement): pass
class h5(nodes.Inline, nodes.TextElement): pass
class h6(nodes.Inline, nodes.TextElement): pass

class label_default(nodes.Inline, nodes.TextElement): pass
class label_muted(nodes.Inline, nodes.TextElement): pass
class label_primary(nodes.Inline, nodes.TextElement): pass
class label_success(nodes.Inline, nodes.TextElement): pass
class label_info(nodes.Inline, nodes.TextElement): pass
class label_warning(nodes.Inline, nodes.TextElement): pass
class label_danger(nodes.Inline, nodes.TextElement): pass


roles.register_generic_role('h1',h1)
roles.register_generic_role('h2',h2)
roles.register_generic_role('h3',h3)
roles.register_generic_role('h4',h4)
roles.register_generic_role('h5',h5)
roles.register_generic_role('h6',h6)

roles.register_generic_role('label-default',label_default)
roles.register_generic_role('label-muted',label_muted)
roles.register_generic_role('label-primary',label_primary)
roles.register_generic_role('label-success',label_success)
roles.register_generic_role('label-info',label_info)
roles.register_generic_role('label-warning',label_warning)
roles.register_generic_role('label-danger',label_danger)
