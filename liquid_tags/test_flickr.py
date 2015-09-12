from . import flickr
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
import os
import pytest
import re


PLUGIN_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(PLUGIN_DIR, 'test_data')


@pytest.mark.parametrize('input,expected', [
    ('18873146680 large "test 1"',
     dict(photo_id='18873146680',
          size='large',
          alt='test 1')),
    ('18873146680 large \'test 1\'',
     dict(photo_id='18873146680',
          size='large',
          alt='test 1')),
    ('18873143536360 medium "test number two"',
     dict(photo_id='18873143536360',
          size='medium',
          alt='test number two')),
    ('18873143536360 small "test number 3"',
     dict(photo_id='18873143536360',
          size='small',
          alt='test number 3')),
    ('18873143536360 "test 4"',
     dict(photo_id='18873143536360',
          size=None,
          alt='test 4')),
    ('18873143536360',
     dict(photo_id='18873143536360',
          size=None,
          alt=None)),
    ('123456 small',
     dict(photo_id='123456',
          size='small',
          alt=None))
])
def test_regex(input, expected):
    assert re.match(flickr.PARSE_SYNTAX, input).groupdict() == expected


@pytest.mark.parametrize('input,expected', [
    (['1', 'server1', '1', 'secret1', 'small'],
     'https://farm1.staticflickr.com/server1/1_secret1_n.jpg'),
    (['2', 'server2', '2', 'secret2', 'medium'],
     'https://farm2.staticflickr.com/server2/2_secret2_c.jpg'),
    (['3', 'server3', '3', 'secret3', 'large'],
     'https://farm3.staticflickr.com/server3/3_secret3_b.jpg')
])
def test_source_url(input, expected):
    assert flickr.source_url(
        input[0], input[1], input[2], input[3], input[4]) == expected


@patch('liquid_tags.flickr.urlopen')
def test_generage_html(mock_urlopen):
    # mock the return to deliver the flickr.json file instead
    with open(TEST_DATA_DIR + '/flickr.json', 'rb') as f:
        mock_urlopen.return_value.read.return_value = f.read()

        attrs = dict(
            photo_id='1234567',
            size='large',
            alt='this is a test'
        )

        expected = ('<a href="https://www.flickr.com/photos/'
                    'marvinxsteadfast/18841055371/">'
                    '<img src="https://farm6.staticflickr.com/5552/1234567_'
                    '17ac287217_b.jpg" alt="this is a test"></a>')

        assert flickr.generate_html(attrs, 'abcdef') == expected
