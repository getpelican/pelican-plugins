# -*- coding: utf-8 -*-

import unittest

from jinja2.utils import generate_lorem_ipsum

# generate one paragraph, enclosed with <p>
TEST_CONTENT = str(generate_lorem_ipsum(n=1))
TEST_SUMMARY = generate_lorem_ipsum(n=1, html=False)


from pelican.contents import Page
import pelican.settings

import summary

class TestSummary(unittest.TestCase):
    def setUp(self):
        super(TestSummary, self).setUp()
        pelican.settings.DEFAULT_CONFIG['SUMMARY_MAX_LENGTH'] = None
        pelican.settings.DEFAULT_CONFIG['SUMMARY_USE_FIRST_PARAGRAPH'] = False

        summary.register()
        summary.initialized(None)
        self.page_kwargs = {
            'content': TEST_CONTENT,
            'context': {
                'localsiteurl': '',
            },
            'metadata': {
                'summary': TEST_SUMMARY,
                'title': 'foo bar',
                'author': 'Blogger',
            },
        }

    def _copy_page_kwargs(self):
        # make a deep copy of page_kwargs
        page_kwargs = dict([(key, self.page_kwargs[key]) for key in
                            self.page_kwargs])
        for key in page_kwargs:
            if not isinstance(page_kwargs[key], dict):
                break
            page_kwargs[key] = dict([(subkey, page_kwargs[key][subkey])
                                     for subkey in page_kwargs[key]])

        return page_kwargs

    def test_end_summary(self):
        page_kwargs = self._copy_page_kwargs()
        del page_kwargs['metadata']['summary']
        page_kwargs['content'] = (
            TEST_SUMMARY + '<!-- PELICAN_END_SUMMARY -->' + TEST_CONTENT)
        page = Page(**page_kwargs)
        summary.extract_summary(page)
        # test both the summary and the marker removal
        self.assertEqual(page.summary, TEST_SUMMARY)
        self.assertEqual(page.content, TEST_SUMMARY + TEST_CONTENT)

    def test_begin_summary(self):
        page_kwargs = self._copy_page_kwargs()
        del page_kwargs['metadata']['summary']
        page_kwargs['content'] = (
            'FOOBAR<!-- PELICAN_BEGIN_SUMMARY -->' + TEST_CONTENT)
        page = Page(**page_kwargs)
        summary.extract_summary(page)
        # test both the summary and the marker removal
        self.assertEqual(page.summary, TEST_CONTENT)
        self.assertEqual(page.content, 'FOOBAR' + TEST_CONTENT)

    def test_begin_end_summary(self):
        page_kwargs = self._copy_page_kwargs()
        del page_kwargs['metadata']['summary']
        page_kwargs['content'] = (
                'FOOBAR<!-- PELICAN_BEGIN_SUMMARY -->' + TEST_SUMMARY +
                '<!-- PELICAN_END_SUMMARY -->' + TEST_CONTENT)
        page = Page(**page_kwargs)
        summary.extract_summary(page)
        # test both the summary and the marker removal
        self.assertEqual(page.summary, TEST_SUMMARY)
        self.assertEqual(page.content, 'FOOBAR' + TEST_SUMMARY + TEST_CONTENT)

    def test_use_first_paragraph(self):
        page_kwargs = self._copy_page_kwargs()
        del page_kwargs['metadata']['summary']
        pelican.settings.DEFAULT_CONFIG['SUMMARY_USE_FIRST_PARAGRAPH'] = True
        page_kwargs['content'] = '<p>' + TEST_SUMMARY + '</p>' + TEST_CONTENT
        page = Page(**page_kwargs)
        summary.extract_summary(page)
        # test both the summary and the marker removal
        self.assertEqual(page.summary, TEST_SUMMARY)
        self.assertEqual(page.content, '<p>' + TEST_SUMMARY + '</p>' + TEST_CONTENT)

    def test_correct_malformed_markup(self):
        page_kwargs = self._copy_page_kwargs()
        del page_kwargs['metadata']['summary']
        malformed = '<article><div><h2>Title</h2><p>Some content</article>'
        wellformed = (
            '<article><div><h2>Title</h2>'
            '<p>Some content</p></div></article>')
        page_kwargs['content'] = (
            '<!-- PELICAN_BEGIN_SUMMARY -->' + malformed +
            '<!-- PELICAN_END_SUMMARY -->')
        page = Page(**page_kwargs)
        summary.extract_summary(page)
        self.assertEqual(page.summary, wellformed)


if __name__ == '__main__':
    unittest.main()
