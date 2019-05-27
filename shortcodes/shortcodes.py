"""
shortcodes.py
=============
Copyright: AGPLv3 <Bernardas Ališauskas @ bernardas.alisauskas@pm.me>

This plugin allows to define macros called shortcodes in content pages that will be expanded as jinja2 templates.
The purpose of this plugin is to allow explicit and quick jinja2 templating in your content without compromising markdown/rst.

Example:

    #pelicanconf.py

    SHORTCODES = {
        'image': "<img src=/images/{{src}}>{{desc|title}}<img>"
    }

Then in your content:

    [% image src=foo.png desc="this is a test" %]

will become:

    <img src=/images/foo.png>This Is A Test<img>
"""
import re
from typing import Match, Dict

from jinja2 import Template
from pelican import signals
from pelican.contents import Content

SETTINGS_NAME = 'SHORTCODES'


def expand_shortcodes(text: str, shortcodes: Dict[str, str]) -> str:
    def repl(group: Match):
        """replace shortocodes with evaluated templates"""
        match = group.groups()[0]
        func, args = match.split(' ', 1)
        args = re.split('(\w+=)', args)
        args = [a.strip("""'" """) for a in args if a]
        kwargs = {args[i].strip('='): args[i + 1] for i in range(0, len(args), 2)}
        try:
            return Template(shortcodes[func]).render(**kwargs)
        except KeyError:
            raise KeyError('shortcode {} not found'.format(func))

    return re.sub(r'\[% (.+?) %\]', repl, text)


def content_object_init(instance: Content):
    shortcodes = instance.settings.get(SETTINGS_NAME)
    if not shortcodes or not instance._content:
        return
    instance._content = expand_shortcodes(instance._content, shortcodes)


def register():
    signals.content_object_init.connect(content_object_init)
