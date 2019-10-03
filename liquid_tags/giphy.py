"""
Giphy Tag
---------

This implements a Liquid-style Giphy tag for Pelican.

IMPORTANT: You have to request a production API key from giphy `here <https://api.giphy.com/submit>`.
For the first runs you could also use the public beta key you can get `here <https://github.com/giphy/GiphyAPI>`.

Syntax
------
{% giphy gif_id ["alt text"|'alt text'] %}

Example
-------
{% giphy aMSJFS6oFX0fC 'ive had some free time' %}

Output
------
<a href="http://giphy.com/gifs/veronica-mars-aMSJFS6oFX0fC"><img src="http://media4.giphy.com/media/aMSJFS6oFX0fC/giphy.gif" alt="ive had some free time"></a>
"""
import json
import re
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
from .mdx_liquid_tags import LiquidTags


SYNTAX = '''{% giphy gif_id ["alt text"|'alt text'] %}'''
GIPHY = re.compile(r'''(?P<gif_id>[\S+]+)(?:\s+(['"]{0,1})(?P<alt>.+)(\\2))?''')


def get_gif(api_key, gif_id):
    '''Returns dict with gif informations from the API.'''
    url = 'http://api.giphy.com/v1/gifs/{}?api_key={}'.format(gif_id, api_key)
    r = urlopen(url)

    return json.loads(r.read().decode('utf-8'))


def create_html(api_key, attrs):
    '''Returns complete html tag string.'''
    gif = get_gif(api_key, attrs['gif_id'])

    if 'alt' not in attrs.keys():
        attrs['alt'] = 'source: {}'.format(gif['data']['source'])

    html_out = '<a href="{}">'.format(gif['data']['url'])
    html_out += '<img src="{}" alt="{}">'.format(
        gif['data']['images']['original']['url'],
        attrs['alt'])
    html_out += '</a>'

    return html_out


def main(api_key, markup):
    '''Doing the regex parsing and running the create_html function.'''
    match = GIPHY.search(markup)

    attrs = None

    if match:
        attrs = dict(
            [(key, value.strip())
             for (key, value) in match.groupdict().items() if value])

    else:
        raise ValueError('Error processing input. '
                         'Expected syntax: {}'.format(SYNTAX))

    return create_html(api_key, attrs)


@LiquidTags.register('giphy')
def giphy(preprocessor, tag, markup):
    api_key = preprocessor.configs.getConfig('GIPHY_API_KEY')

    if api_key is None:
        raise ValueError('Please set GIPHY_API_KEY.')

    return main(api_key, markup)


# ---------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register
