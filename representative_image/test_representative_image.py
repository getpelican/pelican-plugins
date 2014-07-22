#!/bin/sh
import unittest

from jinja2.utils import generate_lorem_ipsum

# Generate content with image 
TEST_CONTENT_IMAGE_URL = 'https://testimage.com/test.jpg' 
TEST_CONTENT = str(generate_lorem_ipsum(n=3, html=True)) + '<img src="' + TEST_CONTENT_IMAGE_URL + '"/>'+ str(generate_lorem_ipsum(n=2,html=True))
TEST_SUMMARY_IMAGE_URL = 'https://testimage.com/summary.jpg'
TEST_SUMMARY_WITHOUTIMAGE = str(generate_lorem_ipsum(n=1, html=True))
TEST_SUMMARY_WITHIMAGE = TEST_SUMMARY_WITHOUTIMAGE + '<img src="' + TEST_SUMMARY_IMAGE_URL + '"/>'
TEST_CUSTOM_IMAGE_URL = 'https://testimage.com/custom.jpg' 


from pelican.contents import Article
import representative_image

class TestRepresentativeImage(unittest.TestCase):

    def setUp(self):
        super(TestRepresentativeImage, self).setUp()
        representative_image.register()

    def test_extract_image_from_content(self): 
        args = {
            'content': TEST_CONTENT,
            'metadata': {
                'summary': TEST_SUMMARY_WITHOUTIMAGE,
            },
        }

        article = Article(**args)
        self.assertEqual(article.featured_image, TEST_CONTENT_IMAGE_URL)

    def test_extract_image_from_summary(self):
        args = {
            'content': TEST_CONTENT,
            'metadata': {
                'summary': TEST_SUMMARY_WITHIMAGE,
            },
        }

        article = Article(**args)
        self.assertEqual(article.featured_image, TEST_SUMMARY_IMAGE_URL)
        self.assertEqual(article.summary, TEST_SUMMARY_WITHOUTIMAGE)

    def test_extract_image_from_summary_with_custom_image(self):
        args = {
            'content': TEST_CONTENT,
            'metadata': {
                'summary': TEST_SUMMARY_WITHIMAGE,
                'image': TEST_CUSTOM_IMAGE_URL,
            },
        }

        article = Article(**args)
        self.assertEqual(article.featured_image, TEST_CUSTOM_IMAGE_URL)
        self.assertEqual(article.summary, TEST_SUMMARY_WITHOUTIMAGE)

if __name__ == '__main__':
    unittest.main()
        






