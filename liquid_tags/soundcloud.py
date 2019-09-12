"""
Soundcloud Tag
--------------
This implements a Liquid-style soundcloud tag for Pelican.

It asks the official Soundcloud-API for the widget html code.

Syntax
------
`{% soundcloud track_url %}`

Example
-------
`{% soundcloud https://soundcloud.com/luftmentsh/hakotel %}`

Output
------
```
<iframe width="100%"
         height="400"
         scrolling="no"
         frameborder="no"
         src="https://w.soundcloud.com/player/?visual=true&url=http%3A%2F%2F\
             api.soundcloud.com%2Ftracks%2F33875102&show_artwork=true">
</iframe>
```
"""
import json
import re

# ---------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register

from .mdx_liquid_tags import LiquidTags

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


SYNTAX = "{% soundcloud track_url %}"
PARSE_SYNTAX = re.compile(r"(?P<track_url>https?://soundcloud.com/[\S]+)")
SOUNDCLOUD_API_URL = "https://soundcloud.com/oembed"


def get_widget(track_url):
    r = urlopen(
        SOUNDCLOUD_API_URL, data="format=json&url={}".format(track_url).encode("utf-8")
    )

    return json.loads(r.read().decode("utf-8"))["html"]


def match_it(markup):
    match = PARSE_SYNTAX.search(markup)
    if match:
        return match.groupdict()
    else:
        raise ValueError(
            "Error processing input. " "Expected syntax: {}".format(SYNTAX)
        )


@LiquidTags.register("soundcloud")
def soundcloud(preprocessor, tag, markup):
    track_url = match_it(markup)["track_url"]

    return get_widget(track_url)
