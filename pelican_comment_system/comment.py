# -*- coding: utf-8 -*-
"""
Author: Bernhard Scheirle
"""
from __future__ import unicode_literals
import os

from pelican.contents import Content
from pelican.utils import slugify

from . import avatars


class Comment(Content):
    mandatory_properties = ('author', 'date')
    default_template = 'None'

    article = None

    def __init__(self, content, metadata, settings, source_path, context):
        # Strip the path off the full filename.
        name = os.path.split(source_path)[1]

        if not hasattr(self, 'slug'):
            # compute the slug before initializing the base Content object, so
            # it doesn't get set there
            # This is required because we need a slug containing the file
            # extension.
            self.slug = slugify(name, settings.get('SLUG_SUBSTITUTIONS', ()))

        super(Comment, self).__init__(content, metadata, settings, source_path,
                                      context)

        self.replies = []

        # Strip the extension from the filename.
        name = os.path.splitext(name)[0]
        self.avatar = avatars.getAvatarPath(name, metadata)
        self.title = "Posted by:  {}".format(metadata['author'])

    def addReply(self, comment):
        self.replies.append(comment)

    def getReply(self, slug):
        for reply in self.replies:
            if reply.slug == slug:
                return reply
            else:
                deepReply = reply.getReply(slug)
                if deepReply is not None:
                    return deepReply
        return None

    def __lt__(self, other):
        return self.date < other.date

    def sortReplies(self):
        for r in self.replies:
            r.sortReplies()
        self.replies = sorted(self.replies)

    def countReplies(self):
        amount = 0
        for r in self.replies:
            amount += r.countReplies()
        return amount + len(self.replies)
