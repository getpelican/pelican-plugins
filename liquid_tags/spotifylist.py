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

SYNTAX = "{% spotifylist id %}"

SPOTIFY = re.compile(r'\[A-Za-z0-9,\]+')

@LiquidTags.register('spotifylist')
def spotifylist(preprocessor, tag, markup):
    spotify_id = None

    spotify_id = markup

    if spotify_id:
        spotify_out = "<iframe src='https://embed.spotify.com/?uri=spotify:trackset:{}' width='300' height='380' frameborder='0' allowtransparency='true'></iframe>".format(spotify_id)
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    return spotify_out


#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
