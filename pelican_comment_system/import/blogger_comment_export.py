#! python3.6
"""
Export Comments from BLogger XML

Takes in a Blogger export XML file and spits out each comment in a seperate
file, such that can be used with the [Pelican Comment System]
(https://bernhard.scheirle.de/posts/2014/March/29/static-comments-via-email/).

May be simple to extend to export posts as well.

For a more detailed desciption, read my blog post at
    http://blog.minchin.ca/2016/12/blogger-comments-exported.html

Author: Wm. Minchin -- minchinweb@gmail.com
License: MIT
Changes:

 - 2016.12.29 -- initial release
 - 2017.01.10 -- clean-up for addition in Pelican Comment System repo
"""

from pathlib import Path

import untangle

###############################################################################
# Constants                                                                   #
###############################################################################

BLOGGER_EXPORT = r'c:\tmp\blog.xml'
COMMENTS_DIR = 'comments'
COMMENT_EXT = '.md'
AUTHORS_FILENAME = 'authors.txt'

###############################################################################
# Main Code Body                                                              #
###############################################################################

authors_and_pics = []


def main():
    obj = untangle.parse(BLOGGER_EXPORT)

    templates = 0
    posts = 0
    comments = 0
    settings = 0
    others = 0

    for entry in obj.feed.entry:
        try:
            full_type = entry.category['term']
        except TypeError:
            # if a post is under multiple categories
            for my_category in entry.category:
                full_type = my_category['term']
                # str.find() uses a return of `-1` to denote failure
                if full_type.find('#') != -1:
                    break
            else:
                others += 1

        simple_type = full_type[full_type.find('#')+1:]

        if 'settings' == simple_type:
            settings += 1
        elif 'post' == simple_type:
            posts += 1
            # process posts here
        elif 'comment' == simple_type:
            comments += 1
            process_comment(entry, obj)
        elif 'template' == simple_type:
            templates += 1
        else:
            others += 1

    export_authors()

    print('''
            {} template
            {} posts (including drafts)
            {} comments
            {} settings
            {} other entries'''.format(templates,
                                       posts,
                                       comments,
                                       settings,
                                       others))


def process_comment(entry, obj):
    # e.g. "tag:blogger.com,1999:blog-26967745.post-4115122471434984978"
    comment_id = entry.id.cdata
    # in ISO 8601 format, usable as is
    comment_published = entry.published.cdata
    comment_body = entry.content.cdata
    comment_post_id = entry.thr_in_reply_to['ref']
    comment_author = entry.author.name.cdata
    comment_author_pic = entry.author.gd_image['src']
    comment_author_email = entry.author.email.cdata

    # add author and pic to global list
    global authors_and_pics
    authors_and_pics.append((comment_author, comment_author_pic))

    # use this for a filename for the comment
    # e.g. "4115122471434984978"
    comment_short_id = comment_id[comment_id.find('post-')+5:]

    comment_text = "date: {}\nauthor: {}\nemail: {}\n\n{}\n"\
                        .format(comment_published,
                                comment_author,
                                comment_author_email,
                                comment_body)

    # article
    for entry in obj.feed.entry:
        entry_id = entry.id.cdata
        if entry_id == comment_post_id:
            article_entry = entry
            break
    else:
        print("No matching article for comment", comment_id, comment_post_id)
        # don't process comment further
        return

    # article slug
    for link in article_entry.link:
        if link['rel'] == 'alternate':
            article_link = link['href']
            break
    else:
        article_title = article_entry.title.cdata
        print('Could not find slug for', article_title)
        article_link = article_title.lower().replace(' ', '-')

    article_slug = article_link[article_link.rfind('/')+1:
                                                    article_link.find('.html')]

    comment_filename = Path(COMMENTS_DIR).resolve()
    # folder; if it doesn't exist, create it
    comment_filename = comment_filename / article_slug
    comment_filename.mkdir(parents=True, exist_ok=True)
    # write the comment file
    comment_filename = comment_filename / (comment_short_id + COMMENT_EXT)
    comment_filename.write_text(comment_text)


def export_authors():
    to_export = set(authors_and_pics)
    to_export = list(to_export)
    to_export.sort()

    str_export = ''
    for i in to_export:
        str_export += (i[0] + '\t\t' + i[1] + '\n')

    authors_filename = Path(COMMENTS_DIR).resolve() / AUTHORS_FILENAME
    authors_filename.write_text(str_export)


if __name__ == "__main__":
    main()
