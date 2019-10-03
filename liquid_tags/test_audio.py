import re
import sys
import unittest
import pytest
from . import audio


if 'nosetests' in sys.argv[0]:
    raise unittest.SkipTest('Those tests are pytest-compatible only')


@pytest.mark.parametrize('input,expected', [
    ('http://foo.bar https://bar.foo',
     ('http://foo.bar', 'https://bar.foo', None)),
    ('http://test.foo',
     ('http://test.foo', None, None)),
    ('https://test.foo',
     ('https://test.foo', None, None)),
    ('http://foo.foo https://bar.bar http://zonk.zonk',
     ('http://foo.foo', 'https://bar.bar', 'http://zonk.zonk'))
])
def test_regex(input, expected):
    assert re.match(audio.AUDIO, input).groups() == expected


@pytest.mark.parametrize('input,expected', [
    ('http://foo.foo/foo.mp3',
     ('<audio controls>'
      '<source src="http://foo.foo/foo.mp3" type="audio/mpeg">'
      'Your browser does not support the audio element.</audio>')),
    ('https://foo.foo/foo.ogg http://bar.bar/bar.opus',
     ('<audio controls>'
      '<source src="https://foo.foo/foo.ogg" type="audio/ogg">'
      '<source src="http://bar.bar/bar.opus" type="audio/ogg">'
      'Your browser does not support the audio element.</audio>')),
    ('http://1.de/1.wav http://2.de/2.mp4 http://3.de/3.ogg',
     ('<audio controls>'
      '<source src="http://1.de/1.wav" type="audio/wav">'
      '<source src="http://2.de/2.mp4" type="audio/mp4">'
      '<source src="http://3.de/3.ogg" type="audio/ogg">'
      'Your browser does not support the audio element.</audio>'))
])
def test_create_html(input, expected):
    assert audio.create_html(input) == expected
