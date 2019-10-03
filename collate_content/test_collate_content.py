"""
test_collate_content.py
=======================

(c) 2014 - Edward J. Stronge

Tests for the collate_content module
"""
from collections import defaultdict, namedtuple
import os
import random
import tempfile
import shutil
import string
import unittest

from pelican import Pelican
from pelican import ArticlesGenerator, PagesGenerator
from pelican.settings import read_settings

import collate_content as cc

TEMP_PAGE_TEMPLATE = """Title: {title}
Category: {category}
"""

Content = namedtuple('Content', ['title', 'path', 'category'])
# Characters likely to appear in blog titles/categories. Could eventually
# extend support to more characters that can't appear in a Python identifier
BLOG_CHARACTERS = string.ascii_letters + ' -:'


def make_content(directory, categories, count=5, categories_per_content=1):
    """
    make_content --> {(processed_category, original_category): articles, ...}

    Writes random titles and categories into `count` temporary
    files in `directory`. If desired, specify `categories_per_content`
    to assign multiple categories to each written file.

    Returns a dictionary whose keys are in `categories` with values
    that are (title, path, category) tuples for the generated
    content files.
    """
    new_content = defaultdict(list)
    for _ in range(count):
        title = get_random_text_and_whitespace()
        category_choice = random.sample(categories, categories_per_content)
        categories_string = ', '.join(category_choice)
        output = TEMP_PAGE_TEMPLATE.format(
            title=title, category=categories_string)
        with tempfile.NamedTemporaryFile(
                dir=directory, mode='w', suffix='.md', delete=False) as tmp:
            tmp.write(output)
            path = os.path.join(directory, tmp.name)

        for each_cat in category_choice:
            new_content[(cc.substitute_category_name(each_cat), each_cat)]\
                .append(Content(title, path, categories_string))
    return new_content


def get_random_text_and_whitespace(length=10):
    """
    Returns at most `length` randomly-generated letters and/or
    whitespace. The returned string will not begin or end in whitespace.
    """
    return "".join(random.sample(BLOG_CHARACTERS, length)).strip()


def modified_pelican_run(self):
    """Runs the generators and returns the context object

    Modified from the Pelican object's run methods.
    """

    context = self.settings.copy()
    context['filenames'] = {}  # share the dict between all the generators
    context['localsiteurl'] = self.settings['SITEURL']  # share
    context['generated_content'] = dict()
    context['static_links'] = set()
    generators = [
        cls(
            context=context,
            settings=self.settings,
            path=self.path,
            theme=self.theme,
            output_path=self.output_path,
        ) for cls in self.get_generator_classes()
    ]

    for p in generators:
        if hasattr(p, 'generate_context'):
            p.generate_context()

    writer = self.get_writer()

    for p in generators:
        if hasattr(p, 'generate_output'):
            p.generate_output(writer)

    next(g for g in generators if isinstance(g, ArticlesGenerator))
    next(g for g in generators if isinstance(g, PagesGenerator))
    return context


class ContentCollationTester(unittest.TestCase):
    """Test generation of lists of content based on their Category metadata"""

    def setUp(self, settings_overrides=None, count=5,
              categories_per_content=1, categories=None):
        self.temp_input_dir = tempfile.mkdtemp(prefix="cc-input-")
        page_directory = os.path.join(self.temp_input_dir, 'pages')
        os.mkdir(page_directory)
        self.temp_output_dir = tempfile.mkdtemp(prefix="cc-output-")

        if categories is None:
            categories = [get_random_text_and_whitespace() for _ in range(5)]

        self.articles = make_content(
            self.temp_input_dir, categories, count=count,
            categories_per_content=categories_per_content)
        self.pages = make_content(
            page_directory, categories, count=count,
            categories_per_content=categories_per_content)
        settings = {
            'PATH': self.temp_input_dir,
            'PAGE_DIR': 'pages',
            'OUTPUT_PATH': self.temp_output_dir,
            'PLUGINS': [cc],
            'DEFAULT_DATE': (2014, 6, 8),
            }
        if settings_overrides is not None:
            settings.update(settings_overrides)
        settings = read_settings(override=settings)
        pelican = Pelican(settings=settings)
        pelican.modified_run = modified_pelican_run
        self.collations = pelican.modified_run(pelican)['collations']

    def tearDown(self):
        shutil.rmtree(self.temp_input_dir)
        shutil.rmtree(self.temp_output_dir)


class TestCollation(ContentCollationTester):
    """Test generation of lists of content based on their Category metadata"""

    def test_articles_with_one_category(self):

        for substituted_category, original_category in self.articles.keys():
            collation_key = '%s_articles' % substituted_category
            self.assertIn(collation_key, self.collations)

            collated_titles = [a.title for a in self.collations[collation_key]]

            for title, _, _ in self.articles[
                    (substituted_category, original_category)]:
                self.assertIn(title, collated_titles)

    def test_pages_with_one_category(self):

        for substituted_category, original_category in self.pages.keys():
            collation_key = '%s_pages' % substituted_category
            self.assertIn(collation_key, self.collations)

            collated_titles = [a.title for a in self.collations[collation_key]]

            for title, _, _ in self.pages[
                    (substituted_category, original_category)]:
                self.assertIn(title, collated_titles)


class TestCollationAndMultipleCategories(TestCollation):
    """
    Test collate_content with multiple categories specified in each
    article and each page.
    """
    def setUp(self):
        categories = [get_random_text_and_whitespace() for _ in range(5)]

        ContentCollationTester.setUp(
            self, categories=categories, categories_per_content=3)


class TestFilteredCategories(ContentCollationTester):
    """
    Test collate_content with the `CATEGORIES_TO_COLLATE` setting
    in effect
    """

    def setUp(self):
        categories = [get_random_text_and_whitespace() for _ in range(5)]
        self.retained_categories = categories[:2]
        override = {'CATEGORIES_TO_COLLATE': self.retained_categories}

        ContentCollationTester.setUp(
            self, settings_overrides=override, categories=categories)

    def test_articles_with_one_category_after_filtering(self):

        for substituted_category, original_category in self.articles.keys():
            collation_key = '%s_articles' % substituted_category

            if original_category not in self.retained_categories:
                self.assertNotIn(collation_key, self.collations)
                continue

            self.assertIn(collation_key, self.collations)

            collated_titles = [a.title for a in self.collations[collation_key]]

            for title, _, _ in self.articles[
                    (substituted_category, original_category)]:
                self.assertIn(title, collated_titles)

    def test_pages_with_one_category_after_filtering(self):

        for substituted_category, original_category in self.pages.keys():
            collation_key = '%s_pages' % substituted_category

            if original_category not in self.retained_categories:
                self.assertNotIn(collation_key, self.collations)
                continue

            self.assertIn(collation_key, self.collations)

            collated_titles = [a.title for a in self.collations[collation_key]]

            for title, _, _ in self.pages[
                    (substituted_category, original_category)]:
                self.assertIn(title, collated_titles)


class TestFilteredAndMultipleCategories(TestFilteredCategories):
    """
    Test collate_content with the `CATEGORIES_TO_COLLATE` setting
    in effect as well as with multiple categories specified in each
    article and each page.
    """
    def setUp(self):
        categories = [get_random_text_and_whitespace() for _ in range(5)]
        self.retained_categories = categories[:2]
        override = {'CATEGORIES_TO_COLLATE': self.retained_categories}

        ContentCollationTester.setUp(
            self, settings_overrides=override, categories=categories,
            categories_per_content=3)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromNames(['test_collate_content'])
    unittest.TextTestRunner(verbosity=1).run(suite)
