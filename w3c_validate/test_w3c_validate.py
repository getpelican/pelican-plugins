import os

from pelican.tests.support import unittest

from w3c_validate import validate_files


CUR_DIR = os.path.dirname(__file__)
TEST_CONTENT_DIR = os.path.join(CUR_DIR, 'test_content')


class W3CValidateTest(unittest.TestCase):

    def test_validate_ok(self):
        with self.assertLogs('w3c_validate.wc3_validate', level='INFO') as logs:
            validate_files(PelicanMock({'OUTPUT_PATH': TEST_CONTENT_DIR}))

        self.assertEqual(logs.output, ['INFO:w3c_validate.wc3_validate:Validating: {}/getpelican.html'.format(TEST_CONTENT_DIR)])


class PelicanMock:
    'A dummy class exposing the only attribute needed by w3c_validate.validate_files'
    def __init__(self, settings):
        self.settings = settings
