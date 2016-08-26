# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest

from pelican import contents

from right_quoter import right_quoter


class PseudoContent(contents.Content):

    def __init__(self, content='content', title='title', summary=None):
        self._content = content
        self.title = title
        if summary:
            self._summary = summary


class TestRightQuoter(unittest.TestCase):

    def test_title(self):
        expected = 'The &#8217;80s'
        content = PseudoContent(title='The &#8216;80s')
        right_quoter(content)
        self.assertEqual(content.title, expected)

    def test_summary(self):
        expected = '&#8217;Twas the night...'
        content = PseudoContent(summary='&#8216;Twas the night...')
        right_quoter(content)
        self.assertEqual(content._summary, expected)

    def test_two_digit_year(self):
        expected = '&#8216;7 &#8217;78 &#8216;789'
        content = PseudoContent(content='&#8216;7 &#8216;78 &#8216;789')
        right_quoter(content)
        self.assertEqual(content._content, expected)

    def test_decade(self):
        expected = '&#8217;90s &#8216;90ss &#8216;95s'
        content = PseudoContent(
            content='&#8216;90s &#8216;90ss &#8216;95s'
        )
        right_quoter(content)
        self.assertEqual(content._content, expected)

    def test_quote_span(self):
        expected = '<span class="quo">&#8217;</span>Tis but a test.'
        content = PseudoContent(
            content='<span class="quo">&#8216;</span>Tis but a test.'
        )
        right_quoter(content)
        self.assertEqual(content._content, expected)

    def test_caps_span(self):
        expected = '&#8217;<span class="caps">EM</span>'
        content = PseudoContent(
            content='&#8216;<span class="caps">EM</span>'
        )
        right_quoter(content)
        self.assertEqual(content._content, expected)

    def test_quote_and_caps_spans(self):
        expected = ('<span class="quo">&#8217;</span>'
                    '<span class="caps">TIS</span>')
        content = PseudoContent(
            content=('<span class="quo">&#8216;</span>'
                     '<span class="caps">TIS</span>')
        )
        right_quoter(content)
        self.assertEqual(content._content, expected)

    def test_word_boundary(self):
        expected = '&#8217;em &#8216;emphasis&#8217;'
        content = PseudoContent(
            content='&#8216;em &#8216;emphasis&#8217;'
        )
        right_quoter(content)
        self.assertEqual(content._content, expected)

    def test_misc_non_matching(self):
        expected = (
            '<span class="quo">&#8216;</span>Blah blah blah'
            '&#8216;<span class="caps">HELLO</span>Spam spam spam'
            '<span class="quo">&#8216;</span>'
            '<span class="caps">HONK</span> &#8216;tissue&#8217;'
        )
        content = PseudoContent(
            content='<span class="quo">&#8216;</span>Blah blah blah'
            '&#8216;<span class="caps">HELLO</span>Spam spam spam'
            '<span class="quo">&#8216;</span>'
            '<span class="caps">HONK</span> &#8216;tissue&#8217;'
        )
        right_quoter(content)
        self.assertEqual(content._content, expected)

if __name__ == '__main__':
    unittest.main()
