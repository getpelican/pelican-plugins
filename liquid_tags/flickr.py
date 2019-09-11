"""
Flickr Tag
----------
This implements a Liquid-style flickr tag for Pelican.

IMPORTANT: You have to create a API key to access the flickr api.
You can do this `here <https://www.flickr.com/services/apps/create/apply>`_.
Add the created key to your config under FLICKR_API_KEY.

Syntax
------
{% flickr image_id [small|medium|large] ["alt text"|'alt text'] %}

Example
--------
{% flickr 18841055371 large "Fichte"}

Output
------
<a href="https://www.flickr.com/photos/marvinxsteadfast/18841055371/"><img src="https://farm6.staticflickr.com/5552/18841055371_17ac287217_b.jpg" alt="Fichte"></a>
"""
import json
import re
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen, urlencode
from .mdx_liquid_tags import LiquidTags


SYNTAX = '''{% flickr image_id [small|medium|large] ["alt text"|'alt text'] %}'''
PARSE_SYNTAX = re.compile((r'''(?P<photo_id>\S+)'''
                           r'''(?:\s+(?P<size>large|medium|small))?'''
                           r'''(?:\s+(['"]{0,1})(?P<alt>.+)(\3))?'''))


def get_info(photo_id, api_key):
    ''' Get photo informations from flickr api. '''
    query = urlencode({
        'method': 'flickr.photos.getInfo',
        'api_key': api_key,
        'photo_id': photo_id,
        'format': 'json',
        'nojsoncallback': '1'
    })

    r = urlopen('https://api.flickr.com/services/rest/?' + query)
    info = json.loads(r.read().decode('utf-8'))

    if info['stat'] == 'fail':
        raise ValueError(info['message'])

    return info


def source_url(farm, server, id, secret, size):
    ''' Url for direct jpg use. '''
    if size == 'small':
        img_size = 'n'
    elif size == 'medium':
        img_size = 'c'
    elif size == 'large':
        img_size = 'b'

    return 'https://farm{}.staticflickr.com/{}/{}_{}_{}.jpg'.format(
        farm, server, id, secret, img_size)


def generate_html(attrs, api_key):
    ''' Returns html code. '''
    # getting flickr api data
    flickr_data = get_info(attrs['photo_id'], api_key)

    # if size is not defined it will use large as image size
    if 'size' not in attrs.keys():
        attrs['size'] = 'large'

    # if no alt is defined it will use the flickr image title
    if 'alt' not in attrs.keys():
        attrs['alt'] = flickr_data['photo']['title']['_content']

    # return final html code
    return '<a href="{}"><img src="{}" alt="{}"></a>'.format(
        flickr_data['photo']['urls']['url'][0]['_content'],
        source_url(flickr_data['photo']['farm'],
                   flickr_data['photo']['server'],
                   attrs['photo_id'],
                   flickr_data['photo']['secret'],
                   attrs['size']),
        attrs['alt'])


@LiquidTags.register('flickr')
def flickr(preprocessor, tag, markup):
    # getting flickr api key out of config
    api_key = preprocessor.configs.getConfig('FLICKR_API_KEY')

    # parse markup and extract data
    attrs = None

    match = PARSE_SYNTAX.search(markup)
    if match:
        attrs = dict(
            [(key, value.strip())
             for (key, value) in match.groupdict().items() if value])
    else:
        raise ValueError('Error processing input. '
                         'Expected syntax: {}'.format(SYNTAX))

    return generate_html(attrs, api_key)


# ---------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
