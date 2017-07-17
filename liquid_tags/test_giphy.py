from . import giphy
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
import os
import pytest


PLUGIN_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(PLUGIN_DIR, 'test_data')


@pytest.mark.parametrize('input,expected', [
    (dict(gif_id='abc123'),
     ('<a href="http://giphy.com/gifs/veronica-mars-aMSJFS6oFX0fC">'
      '<img src="http://media2.giphy.com/media/'
      'aMSJFS6oFX0fC/giphy.gif" alt="source: http://www.tumblr.com"></a>')),
    (dict(gif_id='abc123', alt='ive had some free time'),
     ('<a href="http://giphy.com/gifs/veronica-mars-aMSJFS6oFX0fC">'
      '<img src="http://media2.giphy.com/media/'
      'aMSJFS6oFX0fC/giphy.gif" alt="ive had some free time"></a>'))
])
@patch('liquid_tags.giphy.urlopen')
def test_create_html(mock_urlopen, input, expected):
    with open(TEST_DATA_DIR + '/giphy.json', 'rb') as f:
        mock_urlopen.return_value.read.return_value = f.read()

        assert giphy.create_html('test_api_key', input) == expected
