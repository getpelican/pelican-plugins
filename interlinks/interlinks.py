# -*- coding: utf-8 -*-
"""
Interlinks
=========================
This plugin allows you to include "interwiki" or shortcuts links into the blog,
as keyword>rest_of_url
"""
import re

from pelican import signals

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

interlinks = {}


def getSettings(generator):

    global interlinks

    interlinks = {'this': generator.settings['SITEURL']+"/"}
    if 'INTERLINKS' in generator.settings:
        for key, value in generator.settings['INTERLINKS'].items():
            interlinks[key] = value


def parse_links(instance):

    if instance._content is not None:
        content = instance._content

        if '<a' in content:
            text = BeautifulSoup(
                content, "html.parser", parse_only=SoupStrainer("a"))
            for link in text.find_all("a", href=re.compile("(.+?)>")):
                old_tag = link.decode()
                url = link.get('href')
                m = re.search(r"(.+?)>", url).groups()
                name = m[0]
                if name in interlinks:
                    hi = url.replace(name + ">", interlinks[name])
                    link['href'] = hi

                content = content.replace(old_tag, link.decode())

        if '<img' in content:
            text = BeautifulSoup(
                content, "html.parser", parse_only=SoupStrainer("img"))
            for img in text.find_all('img', src=re.compile("(.+?)>")):
                old_tag = img.decode()
                url = img.get('src')
                m = re.search(r"(.+?)>", url).groups()
                name = m[0]
                if name in interlinks:
                    hi = url.replace(name+">", interlinks[name])
                    img['src'] = hi

                # generated output has no trailing slash; match for replacement
                repaired_old_tag = old_tag.replace("/>", ">")

                content = content.replace(
                    repaired_old_tag,
                    img.decode()
                )


        instance._content = content


def register():
    signals.generator_init.connect(getSettings)
    signals.content_object_init.connect(parse_links)
