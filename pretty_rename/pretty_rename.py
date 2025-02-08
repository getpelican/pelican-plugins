# -*- coding: utf-8 -*-
"""
Auto Rename

This plugin will auto rename content files to the format:
	YYYY-MM-DD-<slug>.ext
	
========================

"""

from os import path, rename
from time import strftime, strptime
from pelican import signals

def rename_content(generator):

	for article in generator.articles:
		(a_filepath, a_filename) = path.split(article.source_path)
		a_extension = path.splitext(article.source_path)[1]
		a_date_struct = strptime(str(article.date), "%Y-%m-%d %H:%M:%S")
		a_new_filename = a_filepath + "/" + strftime("%Y-%m-%d-", a_date_struct) + article.slug + a_extension

		if not (article.source_path == a_new_filename):
			rename(article.source_path, a_new_filename)
				
def register():
	signals.article_generator_finalized.connect(rename_content)
