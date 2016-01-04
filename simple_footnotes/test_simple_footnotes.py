# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import unittest

import html5lib
from html5lib.filters import alphabeticalattributes

from simple_footnotes import parse_for_footnotes


class PseudoArticleGenerator(object):
    articles = []
    drafts = []


class PseudoArticle(object):
    _content = ""
    slug = "article"


class TestFootnotes(unittest.TestCase):

    def _expect(self, input, expected_output):
        ag = PseudoArticleGenerator()
        art = PseudoArticle()
        art._content = input
        ag.articles = [art]
        parse_for_footnotes(ag)
        # Compare parsed output because strings may differ
        walker = html5lib.getTreeWalker("etree")
        cont = alphabeticalattributes.Filter(walker(html5lib.parse(art._content)))
        out = alphabeticalattributes.Filter(walker(html5lib.parse(expected_output)))
        s = html5lib.serializer.HTMLSerializer()
        cont = [e for e in s.serialize(cont)]
        out = [e for e in s.serialize(out)]
        self.assertEqual(cont, out)

    def test_simple(self):
        self.maxDiff = None
        self._expect("words[ref]footnote[/ref]end",
                     'words<sup id="sf-article-1-back"><a class="simple-footnote" title="footnote" href="#sf-article-1">1</a></sup>end<ol class="simple-footnotes"><li id="sf-article-1">footnote <a class="simple-footnote-back" href="#sf-article-1-back">↩</a></li></ol>')

    def test_no_footnote_inside_code(self):
        self._expect("words<code>this is code[ref]footnote[/ref] end code </code> end",
                     "words<code>this is code[ref]footnote[/ref] end code </code> end")

if __name__ == '__main__':
    unittest.main()
