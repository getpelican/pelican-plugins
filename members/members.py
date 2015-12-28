"""
Members info plugin for Pelican
===============================

This plugin looks for a ``members`` metadata header containing key/value pairs
and makes them available for use in templates

The first line of the members metadata defines each key, and the following
lines contain corresponding values for each member.

:members: nome, email, twitter, github, site_nome, site_href
    Danilo Shiga, daniloshiga@gmail.com, @daneoshiga, daneoshiga, Danilo Shiga, http://daniloshiga.com
"""

from collections import OrderedDict

from pelican import signals


def add_members(generator, metadata):

    if 'members' in metadata.keys():
        # Dealing with differences on metadata for md and rst content
        if type(metadata['members']) == list:
            members = metadata['members']
        else:
            members = metadata['members'].splitlines()

        metadata['members'] = OrderedDict()
        keys = map(unicode.strip, members[0].split(','))
        for member in members[1:]:
            values = map(unicode.strip, member.split(','))
            member_dict = dict(zip(keys, values))
            metadata['members'][member_dict['nome']] = member_dict


def register():
    signals.page_generator_context.connect(add_members)
