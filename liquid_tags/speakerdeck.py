"""
Speakerdeck Tag
---------------
This implements a Liquid-style speakerdeck tag for Pelican.

Syntax
------
{% speakerdeck id %}

Example
-------
{% speakerdeck 82b209c0f181013106da6eb14261a8ef %}

Output
------
<script async class="speakerdeck-embed" data-id="82b209c0f181013106da6eb14261a8ef"
 data-ratio="1.33333333333333" src="//speakerdeck.com/assets/embed.js"></script>
"""
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% speakerdeck id %}"

@LiquidTags.register('speakerdeck')
def speakerdeck(preprocessor, tag, markup):
    speakerdeck_out = """
<script async class="speakerdeck-embed" data-id="{id}"
data-ratio="1.33333333333333" src="//speakerdeck.com/assets/embed.js"></script>
        """.format(id=markup)

    return speakerdeck_out


# ---------------------------------------------------
# This import allows speakerdeck tag to be a Pelican plugin
from liquid_tags import register  # noqa
