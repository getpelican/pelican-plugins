"""
Literal Tag
-----------
This implements a tag that allows explicitly showing commands which would
otherwise be interpreted as a liquid tag.

For example, the line

    {% literal video arg1 arg2 %}

would result in the following line:

    {% video arg1 arg2 %}

This is useful when the resulting line would be interpreted as another
liquid-style tag.
"""
from .mdx_liquid_tags import LiquidTags

@LiquidTags.register('literal')
def literal(preprocessor, tag, markup):
    return '{%% %s %%}' % markup

#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register

