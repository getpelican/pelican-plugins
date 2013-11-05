#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

from docutils.parsers.rst import directives, Directive
from docutils import nodes

class Gist(Directive):
  """Embed gist in posts.

  Usage:
    .. gist:: GIST_ID GITHUB_USERNAME

  """
  required_arguments = 2
  has_content = False

  def run(self):
    gist_id = self.arguments[0].strip()
    user_name = self.arguments[1].strip()

    html = '<script src="https://gist.github.com/{}/{}.js"></script>'.format(user_name, gist_id)
    return [nodes.raw('', html, format='html')]
    

def register():
  directives.register_directive('gist', Gist)
