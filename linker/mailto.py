# -*- coding: utf-8 -*-
from __future__ import absolute_import

import codecs

from pelican import signals
from pelican.generators import Generator

from linker import linker

def encode_mailto_link(mailto):
    return 'mailto/' + codecs.encode(mailto, 'rot_13') + '/'

class MailtoLinker(linker.LinkerBase):
    commands = ['mailto']

    def link(self, link):
        mailto = link.path

        link.path = '/' + encode_mailto_link(mailto) # a.href for JS parsing
        link.context['mailtos'].add(mailto) # remember mail address for fallback


class MailtoFallbackGenerator(Generator):
    def generate_context(self):
        self.context['mailtos'] = set() # populated on {mailto} link processing

    def generate_output(self, writer):
        for mailto in self.context['mailtos']:
            save_as = encode_mailto_link(mailto) + 'index.html'

            writer.write_file(save_as, self.get_template('mailto_fallback'),
                              self.context, mailto=mailto)


def return_mailto_fallback_generator(generators):
    return MailtoFallbackGenerator

def register():
    linker.register()
    signals.get_generators.connect(return_mailto_fallback_generator)
