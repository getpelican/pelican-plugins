import unittest
from simple_footnotes import parse_for_footnotes

class PseudoArticleGenerator(object):
    articles = []
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
        self.assertEqual(art._content, expected_output)

    def test_simple(self):
        self._expect("words[ref]footnote[/ref]end",
        ('words<sup id="sf-article-1-back"><a title="footnote" '
         'href="#sf-article-1" class="simple-footnote">1</a></sup>end'
         '<ol class="simple-footnotes">'
         u'<li id="sf-article-1">footnote <a href="#sf-article-1-back" class="simple-footnote-back">\u21a9</a></li>'
         '</ol>'))

    def test_no_footnote_inside_code(self):
        self._expect("words<code>this is code[ref]footnote[/ref] end code </code> end",
            "words<code>this is code[ref]footnote[/ref] end code </code> end")

if __name__ == '__main__':
    unittest.main()