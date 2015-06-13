from thumbnailer import _resizer
from unittest import TestCase, main
import os.path as path
from PIL import Image

class ThumbnailerTests(TestCase):

    def path(self, filename):
        return path.join(self.img_path, filename)

    def setUp(self):
        self.img_path = path.join(path.dirname(__file__), "test_data")
        self.img = Image.open(self.path("sample_image.jpg"))

    def testSquare(self):
        r = _resizer('square', '100', self.img_path)
        output = r.resize(self.img)
        self.assertEqual((100, 100), output.size)

    def testExact(self):
        r = _resizer('exact', '250x100', self.img_path)
        output = r.resize(self.img)
        self.assertEqual((250, 100), output.size)

    def testWidth(self):
        r = _resizer('aspect', '250x?', self.img_path)
        output = r.resize(self.img)
        self.assertEqual((250, 166), output.size)

    def testHeight(self):
        r = _resizer('aspect', '?x250', self.img_path)
        output = r.resize(self.img)
        self.assertEqual((375, 250), output.size)

class ThumbnailerFilenameTest(TestCase):

    def path(self, *parts):
        return path.join(self.img_path, *parts)

    def setUp(self):
        self.img_path = path.join(path.dirname(__file__), "test_data")

    def testRoot(self):
        """Test a file that is in the root of img_path."""

        r = _resizer('square', '100', self.img_path)
        new_name = r.get_thumbnail_name(self.path('sample_image.jpg'))
        self.assertEqual('sample_image_square.jpg', new_name)

    def testRootWithSlash(self):
        r = _resizer('square', '100', self.img_path + '/')
        new_name = r.get_thumbnail_name(self.path('sample_image.jpg'))
        self.assertEqual('sample_image_square.jpg', new_name)

    def testSubdir(self):
        """Test a file that is in a sub-directory of img_path."""

        r = _resizer('square', '100', self.img_path)
        new_name = r.get_thumbnail_name(self.path('subdir', 'sample_image.jpg'))
        self.assertEqual('subdir/sample_image_square.jpg', new_name)

if __name__=="__main__":
    main()
