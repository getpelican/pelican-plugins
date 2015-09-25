"""
Audio Tag
---------
This implements a Liquid-style audio tag for Pelican,
based on the pelican video plugin [1]_

Syntax
------
{% audio url/to/audio [url/to/audio] [/url/to/audio] %}

Example
-------
{% audio http://example.tld/foo.mp3 http://example.tld/foo.ogg %}

Output
------
<audio controls><source src="http://example.tld/foo.mp3" type="audio/mpeg"><source src="http://example.tld/foo.ogg" type="audio/ogg">Your browser does not support the audio element.</audio>

[1] https://github.com/getpelican/pelican-plugins/blob/master/liquid_tags/video.py
"""
import os
import re
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% audio url/to/audio [url/to/audio] [/url/to/audio] %}"
AUDIO = re.compile(r'(/\S+|https?:\S+)(?:\s+(/\S+|https?:\S+))?(?:\s+(/\S+|https?:\S+))?')

AUDIO_TYPEDICT = {'.mp3': 'audio/mpeg',
                  '.ogg': 'audio/ogg',
                  '.oga': 'audio/ogg',
                  '.opus': 'audio/ogg',
                  '.wav': 'audio/wav',
                  '.mp4': 'audio/mp4'}


def create_html(markup):
    match = AUDIO.search(markup)
    if match:
        groups = match.groups()
        audio_files = [g for g in groups if g]

    if any(audio_files):
        audio_out = '<audio controls>'

        for audio_file in audio_files:

            base, ext = os.path.splitext(audio_file)

            if ext not in AUDIO_TYPEDICT:
                raise ValueError("Unrecognized audio extension: "
                                 "{0}".format(ext))

            # add audio source
            audio_out += '<source src="{}" type="{}">'.format(
                audio_file, AUDIO_TYPEDICT[ext])

        # close audio tag
        audio_out += 'Your browser does not support the audio element.'
        audio_out += '</audio>'

    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    return audio_out


@LiquidTags.register('audio')
def audio(preprocessor, tag, markup):
    return create_html(markup)


# ---------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
