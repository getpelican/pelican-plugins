import sys
import unittest

import pytest

from . import youtube


if "nosetests" in sys.argv[0]:
    raise unittest.SkipTest("Those tests are pytest-compatible only")


class configs:
    def __init__(self):
        self.config = {}

    def setConfig(self, name, value):
        self.config[name] = value

    def getConfig(self, name):
        try:
            out = self.config[name]
        except KeyError:
            out = ''

        return out


class fake_proc:
    def __init__(self):
        self.configs = configs()


@pytest.mark.parametrize('input,expected', [
    ('v78_WujMnVk', """<a
                    href="https://www.youtube.com/watch?v=v78_WujMnVk"
                class="youtube_video" alt="YouTube Video"
                title="Click to view on YouTube">
                    <img width="1280" height="720"
                        src="https://img.youtube.com/vi/v78_WujMnVk/maxresdefault.jpg">
                </a>""")])
def test_youtube(input, expected):
    fake_preproc = fake_proc()

    fake_preproc.configs.setConfig('YOUTUBE_THUMB_ONLY', True)
    fake_preproc.configs.setConfig('YOUTUBE_THUMB_SIZE', 'maxres')

    print(fake_preproc.configs.config)

    out = youtube.youtube(fake_preproc, '', input)

    assert out == expected
