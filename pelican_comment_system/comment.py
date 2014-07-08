# -*- coding: utf-8 -*-
"""
Author: Bernhard Scheirle
"""
from __future__ import unicode_literals
from pelican import contents
from pelican.contents import Content

class Comment(Content):
	mandatory_properties = ('author', 'date')
	default_template = 'None'

	def __init__(self, id, avatar, content, metadata, settings, source_path, context):
		super(Comment,self).__init__( content, metadata, settings, source_path, context )
		self.id = id
		self.replies = []
		self.avatar = avatar
		self.title = "Posted by:  {}".format(metadata['author'])

	def addReply(self, comment):
		self.replies.append(comment)

	def getReply(self, id):
		for reply in self.replies:
			if reply.id == id:
				return reply
			else:
				deepReply = reply.getReply(id)
				if deepReply != None:
					return deepReply
		return None

	def __lt__(self, other):
		return self.metadata['date'] < other.metadata['date']

	def sortReplies(self):
		for r in self.replies:
			r.sortReplies()
		self.replies = sorted(self.replies)

	def countReplies(self):
		amount = 0
		for r in self.replies:
			amount += r.countReplies()
		return amount + len(self.replies)
