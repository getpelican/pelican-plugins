"""
Image Tag
---------
This implements a Liquid-style image tag for Pelican,
based on the octopress image tag [1]_

Syntax
------
{% img [class name(s)] [http[s]:/]/path/to/image [width [height]] [title text | "title text" ["alt text"]] %}

Examples
--------
{% img /images/ninja.png Ninja Attack! %}
{% img left half http://site.com/images/ninja.png Ninja Attack! %}
{% img left half http://site.com/images/ninja.png 150 150 "Ninja Attack!" "Ninja in attack posture" %}

Output
------
<img src="/images/ninja.png">
<img class="left half" src="http://site.com/images/ninja.png" title="Ninja Attack!" alt="Ninja Attack!">
<img class="left half" src="http://site.com/images/ninja.png" width="150" height="150" title="Ninja Attack!" alt="Ninja in attack posture">

[1] https://github.com/imathis/octopress/blob/master/plugins/image_tag.rb
"""
import os
import re
from .mdx_liquid_tags import LiquidTags
import six

SYNTAX = '{% img [class name(s)] [http[s]:/]/path/to/image [width [height]] [title text | "title text" ["alt text"]] %}'

# Regular expression to match the entire syntax
ReImg = re.compile(r'(?P<class>[-\w\s]+\s+)?(?P<src>(?P<scheme>[a-zA-Z]+://)?(?P<path>\S+))(?:\s+(?P<width>\d+))?(?:\s+(?P<height>\d+))?(?P<title>\s+.+)?')

# Regular expression to split the title and alt text
ReTitleAlt = re.compile("""(?:"|')(?P<title>[^"']+)?(?:"|')\s+(?:"|')(?P<alt>[^"']+)?(?:"|')""")

# Attributes to keep in the emmitted img tag
IMG_ATTRS = ['class', 'src', 'width', 'height', 'title',]

@LiquidTags.register('img')
def img(preprocessor, tag, markup):
    attrs = None

    # Parse the markup string
    match = ReImg.search(markup)
    if match:
        attrs = {k: v.strip() for k, v in match.groupdict().items() if v}
    else:
        raise ValueError('Error processing input. '
                         'Expected syntax: {0}'.format(SYNTAX))

    # Check if alt text is present -- if so, split it from title
    if 'title' in attrs:
        match = ReTitleAlt.search(attrs['title'])
        if match:
            attrs.update(match.groupdict())
        if not attrs.get('alt'):
            attrs['alt'] = attrs['title']

    # prepend site url to absolute paths
    if 'scheme' not in attrs and os.path.isabs(attrs['src']):
        siteurl = preprocessor.configs.getConfig('SITEURL')
        attrs['src'] = siteurl + attrs['path']

    # create tag
    img_attrs = ['{0!s}={1!r}'.format(k, attrs[k])
            for k in IMG_ATTRS if attrs.get(k)]
    s = "<img {0}>".format(' '.join(img_attrs))
    return s

#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from .liquid_tags import register

