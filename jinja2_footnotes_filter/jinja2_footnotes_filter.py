# -*- coding: utf-8 -*-
"""

"""

from pelican import signals

def rename_footnote_link():
	return "I've hacked you"

class RenameFootnoteLink(object):

	def __init__(self):
		print "Hello"
	
	def __call__(self, content):
		return "Hacked."

def register():
    signals.initialized.connect(RenameFootnoteLink)
    