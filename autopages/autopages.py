import logging
import os
import os.path

from pelican import signals
from pelican.contents import Page


logger = logging.getLogger("autopages")

def yield_files(root):
    root = os.path.realpath(os.path.abspath(root))
    for dirpath, dirnames, filenames in os.walk(root):
        for dirname in list(dirnames):
            try:
                if dirname.startswith("."):
                    dirnames.remove(dirname)
            except IndexError:
                # duplicate already removed?
                pass
        for filename in filenames:
            if filename.startswith("."):
                continue
            yield os.path.join(dirpath, filename)

def make_page(readers, context, filename):
    base_path, filename = os.path.split(filename)
    page = readers.read_file(base_path, filename, Page, None, context)
    slug, _ = os.path.splitext(filename)
    return slug, page

def make_pages(readers, context, path):
    pages = {}
    for filename in yield_files(path):
        try:
            slug, page = make_page(readers, context, filename)
        except Exception:
            logger.exception("Could not make autopage for %r", filename)
            continue
        pages[slug] = page
    return pages

def create_autopages(article_generator):
    settings = article_generator.settings
    readers = article_generator.readers
    context = article_generator.context

    authors_path = settings.get("AUTHOR_PAGE_PATH", "authors")
    categories_path = settings.get("CATEGORY_PAGE_PATH", "categories")
    tags_path = settings.get("TAG_PAGE_PATH", "tags")

    author_pages = make_pages(readers, context, authors_path)
    category_pages = make_pages(readers, context, categories_path)
    tag_pages = make_pages(readers, context, tags_path)

    for author, _ in article_generator.authors:
        author.page = author_pages.get(author.slug, "")
    for category, _ in article_generator.categories:
        category.page = category_pages.get(category.slug, "")
    for tag in article_generator.tags:
        tag.page = tag_pages.get(tag.slug, "")

def register():
    signals.article_generator_finalized.connect(create_autopages)
