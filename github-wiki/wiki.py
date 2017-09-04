from pelican import signals, utils
from collections import namedtuple, OrderedDict
import os
import re
import logging

def add_to_structure(structure, path_list):
    folders = structure["folders"]
    articles = structure["articles"]
    subdir = path_list[0]
    rest = path_list[1:]

    if len(rest) > 1:
        if subdir in folders:
            folders[subdir] = add_to_structure(folders[subdir], rest)
        else:
            folders[subdir] = add_to_structure({"folders":{},"articles":[]}, rest)
    else:
       if subdir in folders:
           folders[subdir]["articles"] += rest
       else:
           folders[subdir] = { "folders": {}, "articles": rest }

    return { "folders": folders, "articles": articles }

def parse_wiki_pages(generator):
    settings = generator.settings
    readers = generator.readers
    contentpath = settings.get("PATH", "content")

    root = os.path.realpath(
        os.path.abspath(os.path.join(contentpath, "wiki", "")))

    wikilist = []
    structure = {"folders":{}, "articles":[]}
    for (dirname, dirnames, filenames) in os.walk(root):
        for filename in filenames:
            if ".git" not in dirname and ".git" not in filename:
                parsedfile = readers.read_file(dirname, filename)
                metadata = parsedfile.metadata
                try:
                    path = metadata["path"]
                    org = metadata["path"].split("/")
                except KeyError:
                    path = ""
                    org = []
                org.append(filename)
                structure = add_to_structure(structure, org)
                wikilist.append((path,filename,parsedfile))

    structure = { "articles": structure["folders"]['']["articles"], "folders":structure["folders"] }

    del(structure["folders"][""])
    wikilist.sort()
    generator.context['wikilist'] = wikilist
    generator.context['wiki'] = structure


def parse_dict(structure, level, nice_list):
    folders = OrderedDict(sorted(structure["folders"].items(), key=lambda t: t[0]))
    articles = sorted(structure["articles"])
    for key in folders.keys():
        if key + ".md" in articles:
            nice_list.append((key, "indexdir", level))
            articles.remove(key + ".md")
        else:
            nice_list.append((key, "noindexdir", level))
        nice_list = parse_dict(folders[key], level + 1, nice_list)
    for item in articles:
        nice_list.append((item, "article", level))
    return nice_list

def generate_wiki_pages(generator, writer):
    wiki_list = generator.context['wikilist']
    structure = generator.context['wiki']
    template = generator.get_template('wikiarticle')
    nice_list = parse_dict(structure, 0, [])

    for page in wiki_list:
        filename = os.path.join('wiki', page[1].replace('.md', '.html'))
        content = page[2].content
        metadata = page[2].metadata
        path = page[0]
        breadcrumbs = []
        for name in path.split('/'):
            name_match = [item[1] for item in nice_list if item[0] == name]
            if len(name_match) > 0 and name_match[0] == "indexdir":
                breadcrumbs.append((name, "a"))
            else:
                breadcrumbs.append((name, "p"))
        file = page[1]
        writer.write_file(filename, template, generator.context,
                          meta=metadata, content=content, file=file, path=path, links=nice_list, breadcrumbs=breadcrumbs)


def register():
    signals.article_generator_finalized.connect(parse_wiki_pages)
    signals.article_writer_finalized.connect(generate_wiki_pages)
