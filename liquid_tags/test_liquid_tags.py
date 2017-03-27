# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import markdown
import re

from pelican.tests.support import unittest
from . import (mdx_liquid_tags, img, notebook)


# ------------------------------------------------------------------------------
# Tests for mdx_liquid_tags
# ------------------------------------------------------------------------------

class TestLiquidTagRegex(unittest.TestCase):
    """ Test if liquid tags are correctly parsed."""
    def get_liquid_tags(self, markup):
        liquid_tags = mdx_liquid_tags.LIQUID_TAG.findall(markup)
        if liquid_tags:
            for i, markup in enumerate(liquid_tags):
                # remove {% %}
                markup = markup[2:-2]
                self.tag = mdx_liquid_tags.EXTRACT_TAG.match(markup).groups()[0]
                self.markup = mdx_liquid_tags.EXTRACT_TAG.sub('', markup, 1)
                return self.tag, self.markup
        return None

    def test_basic_liquid_tag(self):
        markup = '{% tag arg1 arg2 ... argn %}'
        self.get_liquid_tags(markup)
        self.assertEqual(self.tag, 'tag')
        self.assertEqual(self.markup, 'arg1 arg2 ... argn ')

    def test_liquid_tag_in_text(self):
        markup = 'Some text, {% tag1 arg1 arg2 ... argn %}, and some more text'
        self.get_liquid_tags(markup)
        self.assertEqual(self.tag, 'tag1')
        self.assertEqual(self.markup, 'arg1 arg2 ... argn ')

# ------------------------------------------------------------------------------
# Tests for img
# ------------------------------------------------------------------------------


class TestImgTag(unittest.TestCase):
    """ Image Tag tests."""
    def md_img(self, markup):
        """Process markup with markdown LiquidTags img extension."""

        html = markdown.markdown(markup,
                                 extensions=[mdx_liquid_tags.LiquidTags(img)])
        # Remove surrounding <p> tags
        return re.sub('<p>(.*)</p>', '\\1', html)

    def test_basic_img_tag(self):
        markup = '{% img /images/ninja.png %}'
        expected = '<img src="/images/ninja.png">'
        output = self.md_img(markup)
        self.assertEqual(output, expected)

    def test_img_tag_with_title_text(self):
        markup = '{% img /images/ninja.png Ninja Attack! %}'
        expected = '<img alt="Ninja Attack!" src="/images/ninja.png" title="Ninja Attack!">'
        output = self.md_img(markup)
        self.assertEqual(output, expected)

    def test_img_tag_with_title_and_class(self):
        markup = '{% img left half http://site.com/images/ninja.png Ninja Attack! %}'
        expected = '<img alt="Ninja Attack!" class="left half" src="http://site.com/images/ninja.png" title="Ninja Attack!">'
        output = self.md_img(markup)
        self.assertEqual(output, expected)

    def test_img_tag_with_title_class_alt_and_size(self):
        markup = '{% img left half http://site.com/images/ninja.png 300 150 "Ninja Attack!" "Ninja in attack posture" %}'
        expected = '<img alt="Ninja in attack posture" class="left half" height="150" src="http://site.com/images/ninja.png" title="Ninja Attack!" width="300">'
        output = self.md_img(markup)
        self.assertEqual(output, expected)

# ------------------------------------------------------------------------------
# Tests for notebook
# ------------------------------------------------------------------------------


class TestNotebookTagRegex(unittest.TestCase):
    """ Test if notebook tags are correctly parsed."""
    def get_argdict(self, markup):

        match = notebook.FORMAT.search(markup)

        if match:
            argdict = match.groupdict()

            src = argdict['src']
            start = argdict['start']
            end = argdict['end']
            language = argdict['language']

            return src, start, end, language

        return None

    def test_basic_notebook_tag(self):
        markup = 'path/to/thing.ipynb'
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, 'path/to/thing.ipynb')
        self.assertIsNone(start)
        self.assertIsNone(end)
        self.assertIsNone(language)

    def test_basic_notebook_tag_insensitive_to_whitespace(self):
        markup = '   path/to/thing.ipynb '
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, 'path/to/thing.ipynb')
        self.assertIsNone(start)
        self.assertIsNone(end)
        self.assertIsNone(language)

    def test_notebook_tag_with_cells(self):
        markup = 'path/to/thing.ipynb cells[1:5]'
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, 'path/to/thing.ipynb')
        self.assertEqual(start, '1')
        self.assertEqual(end, '5')
        self.assertIsNone(language)

    def test_notebook_tag_with_alphanumeric_language(self):
        markup = 'path/to/thing.ipynb language[python3]'
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, 'path/to/thing.ipynb')
        self.assertIsNone(start)
        self.assertIsNone(end)
        self.assertEqual(language, 'python3')

    def test_notebook_tag_with_symbol_in_name_language(self):
        for short_name in ['c++', 'cpp-objdump', 'c++-objdumb', 'cxx-objdump']:
            markup = 'path/to/thing.ipynb language[{}]'.format(short_name)
            src, start, end, language = self.get_argdict(markup)

            self.assertEqual(src, 'path/to/thing.ipynb')
            self.assertIsNone(start)
            self.assertIsNone(end)
            self.assertEqual(language, short_name)

    def test_notebook_tag_with_language_and_cells(self):
        markup = 'path/to/thing.ipynb cells[1:5] language[julia]'
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, 'path/to/thing.ipynb')
        self.assertEqual(start, '1')
        self.assertEqual(end, '5')
        self.assertEqual(language, 'julia')

    def test_notebook_tag_with_language_and_cells_and_weird_spaces(self):
        markup = '   path/to/thing.ipynb   cells[1:5]  language[julia]       '
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, 'path/to/thing.ipynb')
        self.assertEqual(start, '1')
        self.assertEqual(end, '5')
        self.assertEqual(language, 'julia')


if __name__ == '__main__':
    unittest.main()
