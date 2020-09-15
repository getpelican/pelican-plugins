import unittest
from .video import video


class TestVideoTag(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.preprocessor = None
        self.tag = 'video'

    def test_normal_example(self):
        markup = 'http://site.com/video.mp4 720 480 http://site.com/poster-frame.jpg'
        expected = (
            '<video width="720" height="480" preload="none" controls poster="http://site.com/poster-frame.jpg">'
            "<source src='http://site.com/video.mp4' type='video/mp4; codecs=\"avc1.42E01E, mp4a.40.2\"'>"
            "</video>")
        actual = video(self.preprocessor, self.tag, markup)
        self.assertIn(expected, actual)

    def test_relative_path(self):
        markup = 'files/video.mp4 720 480 images/poster-frame.jpg'
        expected = (
            '<video width="720" height="480" preload="none" controls poster="images/poster-frame.jpg">'
            "<source src='files/video.mp4' type='video/mp4; codecs=\"avc1.42E01E, mp4a.40.2\"'>"
            "</video>")
        actual = video(self.preprocessor, self.tag, markup)
        self.assertIn(expected, actual)

    def test_internal_content(self):
        markup = '{filename}../files/video.mp4 720 480 {filename}../images/poster-frame.jpg'
        expected = (
            '<video width="720" height="480" preload="none" controls poster="{filename}../images/poster-frame.jpg">'
            "<source src='{filename}../files/video.mp4' type='video/mp4; codecs=\"avc1.42E01E, mp4a.40.2\"'>"
            "</video>")
        actual = video(self.preprocessor, self.tag, markup)
        self.assertIn(expected, actual)


if __name__ == '__main__':
    unittest.main()
