import os
import os.path

from pelican import signals


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

def test(article_generator):
    settings = article_generator.settings
    readers = article_generator.readers
    path = settings.get("AUTHOR_PAGE_PATH", "authors")

    author_pages = {}
    for filename in yield_files(path):
        base_path, filename = os.path.split(filename)
        page = readers.read_file(base_path, filename)
        slug, _ = os.path.splitext(filename)
        author_pages[slug] = page

    for author, _ in article_generator.authors:
        print "set author.page for %s to %r" % (author.slug, author_pages.get(author.slug, ""))
        author.page = author_pages.get(author.slug, "")

def register():
    signals.article_generator_finalized.connect(test)
