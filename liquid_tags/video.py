"""
Video Tag
---------
This implements a Liquid-style video tag for Pelican,
based on the octopress video tag [1]_

Syntax
------
{% video url/to/video [width height] [url/to/poster] %}

Example
-------
{% video http://site.com/video.mp4 720 480 http://site.com/poster-frame.jpg %}

Output
------
<video width='720' height='480' preload='none' controls poster='http://site.com/poster-frame.jpg'>
   <source src='http://site.com/video.mp4' type='video/mp4; codecs=\"avc1.42E01E, mp4a.40.2\"'/>
</video>

[1] https://github.com/imathis/octopress/blob/master/plugins/video_tag.rb
"""
import os
import re
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% video url/to/video [url/to/video] [url/to/video] [width height] [url/to/poster] %}"

VIDEO = re.compile(r'(/\S+|https?:\S+)(\s+(/\S+|https?:\S+))?(\s+(/\S+|https?:\S+))?(\s+(\d+)\s(\d+))?(\s+(/\S+|https?:\S+))?')

VID_TYPEDICT = {'.mp4':"type='video/mp4; codecs=\"avc1.42E01E, mp4a.40.2\"'",
                '.ogv':"type='video/ogg; codecs=theora, vorbis'",
                '.webm':"type='video/webm; codecs=vp8, vorbis'"}


@LiquidTags.register('video')
def video(preprocessor, tag, markup):
    videos = []
    width = None
    height = None
    poster = None

    match = VIDEO.search(markup)
    if match:
        groups = match.groups()
        videos = [g for g in groups[0:6:2] if g]
        width = groups[6]
        height = groups[7]
        poster = groups[9]

    if any(videos):
        video_out = """
        <div class="videobox">
            <video width="{width}" height="{height}" preload="none" controls poster="{poster}">
        """.format(width=width, height=height, poster=poster).strip()

        for vid in videos:
            base, ext = os.path.splitext(vid)
            if ext not in VID_TYPEDICT:
                raise ValueError("Unrecognized video extension: "
                                 "{0}".format(ext))
            video_out += ("<source src='{0}' "
                          "{1}>".format(vid, VID_TYPEDICT[ext]))
        video_out += "</video></div>"
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    return video_out


#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
