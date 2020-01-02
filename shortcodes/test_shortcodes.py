import pytest

from .shortcodes import expand_shortcodes


def test_expand_shortcodes():
    shortcode_map = {
        'image': """<img src={{src}} title={{title}}> {{desc}}</img>"""
    }
    text = """
    This is a test foo

    {} 
    
    more text
    """

    expected = {
        """[% image src="image_nice.png" desc='meow meow' title=woof %]""":
            "<img src=image_nice.png title=woof> meow meow</img>",
        """[% image src=src desc=desc title=title %]""":
            "<img src=src title=title> desc</img>",
        """[% image src="src " desc=" desc" title=''' title ''' %]""":
            "<img src=src title=title> desc</img>",
    }
    for short_code, exp in expected.items():
        assert expand_shortcodes(text.format(short_code), shortcode_map) == text.format(exp)

    expected_errors = {
        """[% short_code_not_there src="src " desc=" desc" title=''' title ''' %]""":
        KeyError,
    }
    with pytest.raises(KeyError):
        for short_code, exp in expected_errors.items():
            assert expand_shortcodes(text.format(short_code), shortcode_map)
