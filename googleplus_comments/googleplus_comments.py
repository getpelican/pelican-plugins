# -*- coding: utf-8 -*-
"""
Google Comments Plugin For Pelican
==================================

Adds Google comments to Pelican
"""

from pelican import signals

googleplus_comments_snippet = """
    <script src="https://apis.google.com/js/plusone.js"></script>
    <script>
        $(document).ready(function () {
            gapi.comments.render('comments', {
                href: window.location,
                width: '600',
                first_party_property: 'BLOGGER',
                view_type: 'FILTERED_POSTMOD'
            });
    });
    </script>
"""

def add_googleplus_comments(generator, metadata):
    metadata["googleplus_comments"] = googleplus_comments_snippet

def register():
    signals.article_generator_context.connect(add_googleplus_comments)
