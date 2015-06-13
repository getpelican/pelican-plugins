"""
Instagram Image Tag
-------------------

By `Tom Spalding <https://github.com/digitalvapor>`_

You can see a working example at `antivapor.net/instagram-tag.html <http://antivapor.net/instagram-tag.html>`_.

Based on `Liquid Image Tag <https://github.com/getpelican/pelican-plugins/blob/master/liquid_tags/img.py>`_ by `Jake Vanderplas <https://github.com/jakevdp>`_.

Optional Todo:
* Query JSON to automatically include descriptions.
  http://api.instagram.com/oembed?url=http://instagr.am/p/olw8jXiz1_/
  and option to add wrapping anchor link to original http://instagram.com/p/olw8jXiz1_
* Default to size m
  http://instagr.am/p/olw8jXiz1_/media/?size=t
  http://instagr.am/p/olw8jXiz1_/media
* Provide examples using with [Better Figures and Images](https://github.com/getpelican/pelican-plugins/tree/master/better_figures_and_images).

Syntax
------

    {% gram shortcode [size] [width] [class name(s)] [title text | "title text" ["alt text"]] %}

where size is t, m, or l, and it defaults to m. see http://instagram.com/developer/embedding.

Examples
--------

    {% gram pFG7naIZkr t %}
    {% gram pFJE11IZnx %}
    {% gram pFI0CAIZna l 400 figure 'pretty turkey tail fungus' %}
    {% gram rOru21oZpe l 450 test_class instagram 'warehouse window title' 'alt text' %}

Output
------

    <img src="http://photos-c.ak.instagram.com/hphotos-ak-xaf1/t51.2885-15/917172_604907902963826_254280879_n.jpg" width="450" title="warehouse window title" alt="alt text" class="test_class instagram">
"""
import re
import urllib
from .mdx_liquid_tags import LiquidTags

SYNTAX = '{% gram shortcode [size] [width] [class name(s)] [title text | "title text" ["alt text"]] %}'

# Regular expression for full syntax
# ReGram = re.compile("""(?P<shortcode>\S+)(?:\s+(?P<size>[tml]?))?(?:\s+(?P<width>\d*))?(?:\s+(?P<class>\S*))?(?P<title>\s+.+)?""")
ReGram = re.compile("""(?P<shortcode>\S+)(?:\s+(?P<size>[tml]?))?(?:\s+(?P<width>\d*))?(?:\s+(?P<class>[^']*))?(?P<title>.+)?""")

# Regular expression to split the title and alt text
ReTitleAlt = re.compile("""(?:"|')(?P<title>[^"']+)?(?:"|')\s+(?:"|')(?P<alt>[^"']+)?(?:"|')""")

@LiquidTags.register('gram')
def gram(preprocessor, tag, markup):

    attrs = None

    # Parse the markup string
    match = ReGram.search(markup)
    if match:
        attrs = dict([(key, val.strip())
                      for (key, val) in match.groupdict().iteritems() if val])
    else:
        raise ValueError('Error processing input. '
                         'Expected syntax: {0}'.format(SYNTAX))

    # Construct URI
    #print(attrs)
    shortcode = attrs['shortcode']
    url = 'http://instagr.am/p/'+shortcode+'/media/'
    del attrs['shortcode']

    if 'size' in attrs:
        size = '?size={0}'.format(attrs['size'])
        url = url+size
        del attrs['size']

    r = urllib.urlopen(url)

    if(r.getcode()==404):
        raise ValueError('%s isnt a photo.'%shortcode)

    gram_url = r.geturl()

    # Check if alt text is present -- if so, split it from title
    if 'title' in attrs:
        match = ReTitleAlt.search(attrs['title'])
        if match:
            attrs.update(match.groupdict())
        if not attrs.get('alt'):
            attrs['alt'] = attrs['title']

    #print('updated dict: '+repr(attrs))

    # Return the formatted text
    return '<img src="{0}"{1}>'.format(gram_url,' '.join(' {0}="{1}"'.format(key,val) for (key,val) in attrs.iteritems()))

#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
