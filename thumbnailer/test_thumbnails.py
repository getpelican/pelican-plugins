from thumbnailer import _resizer
from unittest import TestCase, main
import os.path as path
from PIL import Image, ImageChops

class ThumbnailerTests(TestCase):

    def path(self, filename):
        return path.join(self.img_path, filename)

    def setUp(self):
        self.img_path = path.join(path.dirname(__file__), "test_data")
        self.img = Image.open(self.path("sample_image.jpg"))

    def testSquare(self):
        r = _resizer('square', '100')
        output = r.resize(self.img)
        self.assertEqual((100, 100), output.size)

    def testExact(self):
        r = _resizer('exact', '250x100')
        output = r.resize(self.img)
        self.assertEqual((250, 100), output.size)

    def testWidth(self):
        r = _resizer('aspect', '250x?')
        output = r.resize(self.img)
        self.assertEqual((250, 166), output.size)

    def testHeight(self):
        r = _resizer('aspect', '?x250')
        output = r.resize(self.img)
        self.assertEqual((375, 250), output.size)

if __name__=="__main__":
    main()