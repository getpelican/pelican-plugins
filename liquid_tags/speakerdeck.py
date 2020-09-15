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
<script
    async
    class="speakerdeck-embed"
    data-id="82b209c0f181013106da6eb14261a8ef"
    data-ratio="1.33333333333333"
    src="//speakerdeck.com/assets/embed.js">
</script>
"""
import re

from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% speakerdeck id [ratio] %}"

REGEX = re.compile(r'([\S]+)(\s+(\d*\.?\d*))?')


@LiquidTags.register('speakerdeck')
def speakerdeck(preprocessor, tag, markup):
    ratio = 1.33333333333333
    id = None
    match = REGEX.search(markup)
    if match:
        groups = match.groups()
        id = groups[0]
        ratio = groups[2] or ratio
    if id:
        speakerdeck_out = """
<script async class="speakerdeck-embed" data-id="{id}"
data-ratio="{ratio}" src="//speakerdeck.com/assets/embed.js"></script>
        """.format(id=id, ratio=ratio)
    else:
        raise ValueError(
            "Error processing input, expected syntax: {0}".format(SYNTAX)
        )
    return speakerdeck_out


# ---------------------------------------------------
# This import allows speakerdeck tag to be a Pelican plugin
from liquid_tags import register  # noqa # isort:skip
