"""
Youtube Tag
---------
This implements a Liquid-style youtube tag for Pelican,
based on the jekyll / octopress youtube tag [1]_

Syntax
------
{% youtube id [width height] %}

Example
-------
{% youtube dQw4w9WgXcQ 640 480 %}

Output
------
<iframe width="640" height="480" src="http://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>

[1] https://gist.github.com/jamieowen/2063748
"""
import os
import re
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% youtube id [width height] %}"

YOUTUBE = re.compile(r'([\S]+)(\s+(\d+)\s(\d+))?')

@LiquidTags.register('youtube')
def youtube(preprocessor, tag, markup):
    width = 640
    height = 390
    youtube_id = None

    match = YOUTUBE.search(markup)
    if match:
        groups = match.groups()
        youtube_id = groups[0]
        width = groups[2] or width
        height = groups[3] or height

    if youtube_id:
        youtube_out = """
            <div class="videobox">
                <iframe width="{width}" height="{height}"
                        src='http://www.youtube.com/v/{youtube_id}'
                        frameborder='0'
                        webkitAllowFullScreen mozallowfullscreen allowFullScreen>
                </iframe>
            </div>
        """.format(width=width, height=height, youtube_id=youtube_id).strip()
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    return youtube_out


#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
