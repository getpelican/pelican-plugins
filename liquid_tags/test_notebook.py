import re
import sys
import unittest

if 'nosetests' in sys.argv[0]:
    raise unittest.SkipTest('Those tests are pytest-compatible only')

import pytest
pytest.skip("Test is currently broken, see pelican pr #1618", allow_module_level=True)

from pelican.tests.support import unittest

from . import notebook


class TestNotebookTagRegex(unittest.TestCase):

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
        markup = u'path/to/thing.ipynb'
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, u'path/to/thing.ipynb')
        self.assertIsNone(start)
        self.assertIsNone(end)
        self.assertIsNone(language)

    def test_basic_notebook_tag_insensitive_to_whitespace(self):
        markup = u'   path/to/thing.ipynb '
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, u'path/to/thing.ipynb')
        self.assertIsNone(start)
        self.assertIsNone(end)
        self.assertIsNone(language)

    def test_notebook_tag_with_cells(self):
        markup = u'path/to/thing.ipynb cells[1:5]'
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, u'path/to/thing.ipynb')
        self.assertEqual(start, u'1')
        self.assertEqual(end, u'5')
        self.assertIsNone(language)

    def test_notebook_tag_with_alphanumeric_language(self):
        markup = u'path/to/thing.ipynb language[python3]'
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, u'path/to/thing.ipynb')
        self.assertIsNone(start)
        self.assertIsNone(end)
        self.assertEqual(language, u'python3')

    def test_notebook_tag_with_symbol_in_name_language(self):
        for short_name in [u'c++', u'cpp-objdump', u'c++-objdumb', u'cxx-objdump']:
            markup = u'path/to/thing.ipynb language[{}]'.format(short_name)
            src, start, end, language = self.get_argdict(markup)

            self.assertEqual(src, u'path/to/thing.ipynb')
            self.assertIsNone(start)
            self.assertIsNone(end)
            self.assertEqual(language, short_name)

    def test_notebook_tag_with_language_and_cells(self):
        markup = u'path/to/thing.ipynb cells[1:5] language[julia]'
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, u'path/to/thing.ipynb')
        self.assertEqual(start, u'1')
        self.assertEqual(end, u'5')
        self.assertEqual(language, u'julia')

    def test_notebook_tag_with_language_and_cells_and_weird_spaces(self):
        markup = u'   path/to/thing.ipynb   cells[1:5]  language[julia]       '
        src, start, end, language = self.get_argdict(markup)

        self.assertEqual(src, u'path/to/thing.ipynb')
        self.assertEqual(start, u'1')
        self.assertEqual(end, u'5')
        self.assertEqual(language, u'julia')


if __name__ == '__main__':
    unittest.main()