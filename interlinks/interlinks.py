# -*- coding: utf-8 -*-

"""
Interlinks
=========================

This plugin allows you to include "interwiki" or shortcuts links into the blog, as keyword>rest_of_url

"""

from bs4 import BeautifulSoup
from pelican import signals
import re

interlinks = {}

def getSettings (generator):

	global interlinks

	interlinks = {'this': generator.settings['SITEURL']+"/"}
	if 'INTERLINKS' in generator.settings:
		for key, value in generator.settings['INTERLINKS'].items():
			interlinks[key] = value

def content_object_init(instance):

	if instance._content is not None:
		content = instance._content
		# use Python's built-in parser so no duplicated html & body tags appear, or use tag.unwrap()
		text = BeautifulSoup(content, "html.parser")
		
		if 'a' in content:
			for link in text.find_all(href=re.compile("(.+?)>")):
				url = link.get('href')
				m = re.search(r"(.+?)>", url).groups()
				name = m[0]
				if name in interlinks:
					hi = url.replace(name+">",interlinks[name])
					link['href'] = hi

		instance._content = text.decode()

def register():
	signals.generator_init.connect(getSettings)
	signals.content_object_init.connect(content_object_init)