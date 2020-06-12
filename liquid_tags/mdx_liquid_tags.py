"""
Markdown Extension for Liquid-style Tags
----------------------------------------
A markdown extension to allow user-defined tags of the form::

    {% tag arg1 arg2 ... argn %}

Where "tag" is associated with some user-defined extension.
These result in a preprocess step within markdown that produces
either markdown or html.
"""
import warnings
import markdown
import itertools
import re
import os
from functools import wraps

LT_CONFIG = { 'CODE_DIR': 'code',
              'NOTEBOOK_DIR': 'notebooks',
              'FLICKR_API_KEY': 'flickr',
              'GIPHY_API_KEY': 'giphy',
              'LT_DELIMITERS': ('{%', '%}'),
}
LT_HELP = { 'CODE_DIR' : 'Code directory for include_code subplugin',
            'NOTEBOOK_DIR' : 'Notebook directory for notebook subplugin',
            'FLICKR_API_KEY': 'Flickr key for accessing the API',
            'GIPHY_API_KEY': 'Giphy key for accessing the API',
            'LT_DELIMITERS': 'Alternative set of Liquid Tags block delimiters',
}

class _LiquidTagsPreprocessor(markdown.preprocessors.Preprocessor):
    LT_FMT = r'{0}(?:\s*)(?P<tag>\S+)(?:\s*)(?P<markup>.*?)(?:\s*){1}'
    LT_RE_FLAGS = re.MULTILINE | re.DOTALL | re.UNICODE
    _tags = {}

    def __init__(self, configs):
        cls = self.__class__
        liquid_tag_re = cls.LT_FMT.format(
                *map(re.escape, configs.getConfig('LT_DELIMITERS')))
        self.liquid_tag = re.compile(liquid_tag_re, cls.LT_RE_FLAGS)
        self.configs = configs

    def expand_tag(self, match):
        tag, markup = match.groups()
        if tag in self.__class__._tags:
            return self.__class__._tags[tag](self, tag, markup)
        else:
            return match[0]

    def run(self, lines):
        page = '\n'.join(lines)
        page = self.liquid_tag.sub(self.expand_tag, page)
        return page.splitlines()


class LiquidTags(markdown.Extension):
    """Wrapper for MDPreprocessor"""
    def __init__(self, config):
        try:
            # Needed for markdown versions >= 2.5
            for key,value in LT_CONFIG.items():
                self.config[key] = [value,LT_HELP[key]]
            super(LiquidTags,self).__init__(**config)
        except AttributeError:
            # Markdown versions < 2.5
            for key,value in LT_CONFIG.items():
                config[key] = [config[key],LT_HELP[key]]
            super(LiquidTags,self).__init__(config)

    @classmethod
    def register(cls, tag):
        """Decorator to register a new include tag"""
        def dec(func):
            if tag in _LiquidTagsPreprocessor._tags:
                warnings.warn("Enhanced Markdown: overriding tag '%s'" % tag)
            _LiquidTagsPreprocessor._tags[tag] = func
            return func
        return dec

    def extendMarkdown(self, md, md_globals):
        self.htmlStash = md.htmlStash
        md.registerExtension(self)
        if 'include_code' in _LiquidTagsPreprocessor._tags:
            # For the include_code preprocessor, we need to re-run the
            # fenced code block preprocessor after substituting the code.
            # Because the fenced code processor is run before, {% %} tags
            # within equations will not be parsed as an include.
            md.preprocessors.add('mdincludes',
                    _LiquidTagsPreprocessor(self), ">html_block")


def makeExtension(configs=None):
    """Wrapper for a MarkDown extension"""
    return LiquidTags(configs=configs)
