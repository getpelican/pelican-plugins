"""
Youtube Tag
---------
This implements a Liquid-style youtube tag in a bootstrap responsive iframe
for Pelican, based on the jekyll / octopress youtube tag [1]_

Syntax
------
{% bootstrap_youtube id %}

Example
-------
{% bootstrap_youtube dQw4w9WgXcQ %}

Output
------

<span class="videobox">
    <div class="embed-responsive embed-responsive-16by9">
        <iframe class="embed-responsive-item"
            src="https://www.youtube.com/embed/dQw4w9WgXcQ"
            frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen>
        </iframe>
    </div>
</span>
"""
import re
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% bootstrap_youtube id %}"

YOUTUBE = re.compile(r'([\S]+)(\s+([\d%]+)\s([\d%]+))?')


@LiquidTags.register('bootstrap_youtube')
def bootstrap_youtube(preprocessor, tag, markup):
    youtube_id = None

    match = YOUTUBE.search(markup)
    if match:
        groups = match.groups()
        youtube_id = groups[0]

    if youtube_id:
        youtube_out = """
            <span class="videobox">
              <div class="embed-responsive embed-responsive-16by9">
                <iframe class="embed-responsive-item"
                    src='https://www.youtube.com/embed/{youtube_id}'
                    frameborder='0' webkitAllowFullScreen mozallowfullscreen
                    allowFullScreen>
                </iframe>
              </div>
            </span>
        """.format(youtube_id=youtube_id).strip()
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    return youtube_out


# ---------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register  # noqa
