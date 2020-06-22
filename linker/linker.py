# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import re

from six.moves.urllib.parse import urlparse, urlunparse

from pelican import signals, contents

from linker import content_objects

logger = logging.getLogger("linker")

class Link(object):
    """Represents an HTML link including a linker command.

    Typically, the Link is constructed from an SRE_Match after applying the
    provided Link.regex pattern to the HTML content of a content object.

    """
    # regex based on the one used in contents.py from pelican version 3.6.3
    regex = re.compile(
        r""" # EXAMPLE: <a rel="nofollow" href="{mailto}webmaster"

        (?P<markup><\s*[^\>]*   # <a rel="nofollow" href=   --> markup
            (?:href|src|poster|data|cite|formaction|action)\s*=)

        (?P<quote>["\'])        # "                         --> quote
        \{(?P<cmd>.*?)\}        # {mailto}                  --> cmd
        (?P<url>.*?)            # webmaster                 --> __url (see path)
        \2                      # "                         <-- quote

        """, re.X)

    def __init__(self, context, content_object, match):
        """Construct a Link from an SRE_Match.

        :param context: The shared context between generators.
        :param content_object: The associated pelican.contents.Content.
        :param match: An SRE_Match obtained by applying the regex to my content.

        """
        self.context = context
        self.content_object = content_object

        self.markup = match.group('markup')
        self.quote = match.group('quote')
        self.cmd = match.group('cmd')
        self.__url = urlparse(match.group('url'))
        self.path = self.__url.path

    def href(self): # rebuild matched URL using (possibly updated) self.path
        return urlunparse( self.__url._replace(path=self.path) )

    def html_code(self): # rebuild matched pattern from (possibly updated) self
        return ''.join((self.markup, self.quote, self.href(), self.quote))


class LinkerBase(object):
    """Base class for performing the linker command magic.

    In order to provide the linker command 'foo' as in '<a href="{foo}contact',
    a responsible Linker class (e.g., FooLinker) should derive from LinkerBase
    and set FooLinker.commands to ['foo']. The linker command is processed when
    the overridden Linker.link(Link) is called.

    """
    commands = [] # link commands handled by the Linker. EXAMPLE: ['mailto']
    builtins = ['attach', 'author', 'category', 'filename', 'index', 'static', 'tag']


    def __init__(self, settings):
        self.settings = settings

    def link(self, link):
        raise NotImplementedError


class Linkers(object):
    """Interface for all Linkers.

    This class contains a mapping of {cmd1: linker1, cmd2: linker2} to apply any
    registered linker command by passing the Link to the responsible Linker.

    (Idea based on pelican.readers.Readers, but with less customization options.)

    """
    def __init__(self, settings):
        self.settings = settings
        self.linkers = {}

        for linker_class in [LinkerBase] + LinkerBase.__subclasses__():
            for cmd in linker_class.commands:
                self.register_linker(cmd, linker_class)

    def register_linker(self, cmd, linker_class):
        if cmd in self.linkers: # check for existing registration of that cmd
            current_linker_class = self.linkers[cmd].__class__
            logger.warning(
                "%s is stealing the linker command %s from %s.",
                linker_class.__name__, cmd, current_linker_class.__name__
            )
        self.linkers[cmd] = linker_class(self.settings)

    def handle_links_in_content_object(self, context, content_object):
        # replace Link matches (with side effects on content and content_object)
        def replace_link_match(match):
            link = Link(context, content_object, match)

            if link.cmd in LinkerBase.builtins:
                return match.group(0)  # builtin commands not handled here
            elif link.cmd in self.linkers:
                self.linkers[link.cmd].link(link) # let Linker process the Link
            else:
                logger.warning("Ignoring unknown linker command %s", link.cmd)

            return link.html_code() # return HTML to replace the matched link

        content_object._content = Link.regex.sub( # match, process and replace
            replace_link_match, content_object._content)


def feed_context_to_linkers(generators):
    settings = generators[0].settings
    linkers = Linkers(settings)

    context = generators[0].context
    for co in context['content_objects']: # provided by plugin 'content_objects'
        if isinstance(co, contents.Static): continue
        if not co._content: continue
        linkers.handle_links_in_content_object(context, co)

def register():
    content_objects.register()
    signals.all_generators_finalized.connect(feed_context_to_linkers)
