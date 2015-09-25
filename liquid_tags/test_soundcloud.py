from . import soundcloud
import pytest


@pytest.mark.parametrize('input,expected', [
    ('https://soundcloud.com/forss/in-paradisum',
     dict(track_url='https://soundcloud.com/forss/in-paradisum')),
    ('http://soundcloud.com/forss/in-paradisum',
     dict(track_url='http://soundcloud.com/forss/in-paradisum')),
    ('https://soundcloud.com/toroymoi/real-love-ft-kool-ad',
     dict(track_url='https://soundcloud.com/toroymoi/real-love-ft-kool-ad')),
    ('https://soundcloud.com/capturedtracks/sets/wild-nothing-nocturne',
     dict(track_url=('https://soundcloud.com/capturedtracks/'
                     'sets/wild-nothing-nocturne')))
])
def test_match_it(input, expected):
    assert soundcloud.match_it(input) == expected


@pytest.mark.parametrize('input', [
    'http://foobar.com',
    'foobar',
    'https://google.com'
])
def test_match_it_exception(input):
    with pytest.raises(ValueError):
        soundcloud.match_it(input)
