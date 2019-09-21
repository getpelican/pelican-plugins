# -*- coding: utf-8 -*-
import os, shutil
from tempfile import TemporaryDirectory
from unittest.mock import patch, Mock

from pelican.tests.support import get_settings, unittest

from .shaarli_poster import build_article_generator, upload_new_articles


CUR_DIR = os.path.dirname(__file__)
TEST_CONTENT_DIR = os.path.join(CUR_DIR, 'test_content')


class ShaarliPosterTest(unittest.TestCase):

    @patch('shaarli_poster.shaarli_poster.get_credentials')  # avoid ~/.config/shaarli/client.ini parsing, which may not exist in CI
    @patch('shaarli_poster.shaarli_poster.ShaarliV1Client')
    def test_upload_new_article(self, ShaarliClientClassMock, _):
        ShaarliClientClassMock.return_value.request.side_effect = [
            ResponseMock([{'url': '/other-dummy-article.html'}]),  # get-links
            ResponseMock()  # post-link
        ]
        with TemporaryDirectory() as tmpdirname:
            upload_new_articles([build_article_generator(get_settings(filenames={}), TEST_CONTENT_DIR, tmpdirname)])
            self.assertEqual(ShaarliClientClassMock.return_value.request.call_count, 2)  # 1 get-links + 1 post-link

class ResponseMock:
    def __init__(self, json=None):
        self._json = json
    def json(self):
        return self._json
    def raise_for_status(self):
        pass
