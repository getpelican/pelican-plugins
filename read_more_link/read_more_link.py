# -*- coding: utf-8 -*-
"""
Read More Link
===========================

This plugin inserts an inline "read more" or "continue" link into the last html element of the object summary.

For more information, please visit: http://vuongnguyen.com/creating-inline-read-more-link-python-pelican-lxml.html

"""

from pelican import signals, contents
from pelican.utils import truncate_html_words
from pelican.generators import ArticlesGenerator

try:
    from lxml.html import fragment_fromstring, fragments_fromstring, tostring
    from lxml.etree import ParserError
except ImportError:
    raise Exception("Unable to find lxml. To use READ_MORE_LINK, you need lxml")


def insert_into_last_element(html, element):
    """
    function to insert an html element into another html fragment
    example:
        html = '<p>paragraph1</p><p>paragraph2...</p>'
        element = '<a href="/read-more/">read more</a>'
        ---> '<p>paragraph1</p><p>paragraph2...<a href="/read-more/">read more</a></p>'
    """
    try:
        item = fragment_fromstring(element)
    except (ParserError, TypeError) as e:
        item = fragment_fromstring('<span></span>')

    try:
        doc = fragments_fromstring(html)
        doc[-1].append(item)

        return ''.join(tostring(e) for e in doc)
    except (ParserError, TypeError) as e:
        return ''

def insert_read_more_link(instance):
    """
    Insert an inline "read more" link into the last element of the summary
    :param instance:
    :return:
    """

    # only deals with Article type
    if type(instance) != contents.Article: return


    SUMMARY_MAX_LENGTH = instance.settings.get('SUMMARY_MAX_LENGTH')
    READ_MORE_LINK = instance.settings.get('READ_MORE_LINK', None)
    READ_MORE_LINK_FORMAT = instance.settings.get('READ_MORE_LINK_FORMAT',
                                                  '<a class="read-more" href="/{url}">{text}</a>')

    if not (SUMMARY_MAX_LENGTH and READ_MORE_LINK and READ_MORE_LINK_FORMAT): return

    if hasattr(instance, '_summary') and instance._summary:
        summary = instance._summary
    else:
        summary = truncate_html_words(instance.content, SUMMARY_MAX_LENGTH)

    if summary != instance.content:
        read_more_link = READ_MORE_LINK_FORMAT.format(url=instance.url, text=READ_MORE_LINK)
        instance._summary = insert_into_last_element(summary, read_more_link)


def run_plugin(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                insert_read_more_link(article)


def register():
    try:
        signals.all_generators_finalized.connect(run_plugin)
    except AttributeError:
        # NOTE: This may result in #314 so shouldn't really be relied on
        # https://github.com/getpelican/pelican-plugins/issues/314
        signals.content_object_init.connect(insert_read_more_link)
