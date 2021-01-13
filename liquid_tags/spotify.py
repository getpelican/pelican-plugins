"""
Spotify Tag
---------
This implements a Liquid-style spotify tag for Pelican,
based on the jekyll / octopress youtube tag [1]_

Syntax
------
{% spotify id %}

Example
-------
{% spotify 1HNZcRFlIKwHAJD3LxvX4d %}

Output
------
<iframe
    src='https://embed.spotify.com/?uri=spotify:track:1HNZcRFlIKwHAJD3LxvX4d'
    width='300' height='380' frameborder='0' allowtransparency='true'>
</iframe>
"""
import re
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% spotify id %}"

SPOTIFY = re.compile(r'(\w+)(\s+(\d+)\s(\d+))?')


@LiquidTags.register('spotify')
def spotify(preprocessor, tag, markup):
    spotify_id = None

    match = SPOTIFY.search(markup)
    if match:
        groups = match.groups()
        spotify_id = groups[0]

    if spotify_id:
        spotify_out = """
        <iframe src='https://embed.spotify.com/?uri=spotify:track:{}'
          width='300'
          height='380'
          frameborder='0'
          allowtransparency='true'></iframe>""".format(spotify_id).strip()
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    return spotify_out


# ---------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register  # noqa
