"""
Youtube Tag
---------
This implements a Liquid-style youtube tag for Pelican,
based on the jekyll / octopress youtube tag [1]_

Syntax
------
{% youtube id [width height align] %}

Example
-------
{% youtube dQw4w9WgXcQ 640 480 center %}

Output
------
<div style="text-align:center"><iframe width="640" height="480" src="http://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe></div>

[1] https://gist.github.com/jamieowen/2063748
"""
import os
import re
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% youtube id [width height align] %}"

YOUTUBE = re.compile(r'(?P<id>\w+)'
    r'( (?P<width>\d+))?'
    r'( (?P<height>\d+))?')

ALIGN = re.compile(r'(?P<align>left|right|center|justify)')

@LiquidTags.register('youtube')
def youtube(preprocessor, tag, markup):
    width = 640
    height = 390
    align = 'left'
    youtube_id = None

    match = YOUTUBE.search(markup)
    align_match = ALIGN.search(markup)

    if match:
        youtube_id = match.group('id')
        width = match.group('width') or width
        height = match.group('height') or height
        align = align_match.group('align') or align

    if youtube_id:
        youtube_out = "<div style='text-align:{align}'><iframe width='{width}' height='{height}' display='block' src='http://www.youtube.com/embed/{youtube_id}' frameborder='0' webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe></div>".format(width=width, height=height, align=align, youtube_id=youtube_id)
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    return youtube_out


#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
