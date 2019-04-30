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

<span class="videobox">
    <iframe
        width="640" height="480"
        src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0"
        webkitAllowFullScreen mozallowfullscreen allowFullScreen>
    </iframe>
</span>

[1] https://gist.github.com/jamieowen/2063748
"""
import re
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% youtube id [width height] %}"

YOUTUBE = re.compile(r'([\S]+)(\s+([\d%]+)\s([\d%]+))?')


@LiquidTags.register('youtube')
def youtube(preprocessor, tag, markup):
    width = 640
    height = 390
    youtube_id = None

    config_thumb_only = preprocessor.configs.getConfig('YOUTUBE_THUMB_ONLY')
    config_thumb_size = preprocessor.configs.getConfig('YOUTUBE_THUMB_SIZE')

    thumb_sizes = {
        'maxres': [1280, 720],
        'sd': [640, 480],
        'hq': [480, 360],
        'mq': [320, 180]
    }

    if config_thumb_only:
        if not config_thumb_size:
            config_thumb_size = 'sd'

        try:
            width = thumb_sizes[config_thumb_size][0]
            height = thumb_sizes[config_thumb_size][1]
        except KeyError:
            pass

    match = YOUTUBE.search(markup)
    if match:
        groups = match.groups()
        youtube_id = groups[0]
        width = groups[2] or width
        height = groups[3] or height

    if youtube_id:
        if config_thumb_only:
            thumb_url = 'https://img.youtube.com/vi/{youtube_id}'.format(
                youtube_id=youtube_id)

            youtube_out = """<a
                    href="https://www.youtube.com/watch?v={youtube_id}"
                class="youtube_video" alt="YouTube Video"
                title="Click to view on YouTube">
                    <img width="{width}" height="{height}"
                        src="{thumb_url}/{size}default.jpg">
                </a>""".format(width=width, height=height,
                               youtube_id=youtube_id,
                               size=config_thumb_size,
                               thumb_url=thumb_url)
        else:
            youtube_out = """
                <span class="videobox">
                    <iframe width="{width}" height="{height}"
                        src='https://www.youtube.com/embed/{youtube_id}'
                        frameborder='0' webkitAllowFullScreen
                        mozallowfullscreen allowFullScreen>
                    </iframe>
                </span>
            """.format(width=width, height=height,
                       youtube_id=youtube_id).strip()
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    return youtube_out


# ---------------------------------------------------
# This import allows youtube tag to be a Pelican plugin
from liquid_tags import register  # noqa
