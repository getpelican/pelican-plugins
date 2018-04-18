import unittest
import os

from __init__ import CommonMarkReader

CUR_DIR = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(CUR_DIR, 'test_data')


class CommonMarkSmokeTest(unittest.TestCase):
    EXPECTED_METADATA = {'key1': 'value1',
                         'key2': 'value2'}
    EXPECTED_HTML = '''<div>
<div>
<h2>header</h2>
<p>paragraph</p>
</div>
<div>
<p>paragraph</p>
</div>
</div>
'''

    def setUp(self):
        self.reader = CommonMarkReader({})
        source_path = os.path.join(CONTENT_PATH, 'markdown_in_html.md')
        self.content, self.metadata = self.reader.read(source_path)

    def test_metadata_should_be_parsed(self):
        self.assertEqual(self.metadata, self.EXPECTED_METADATA)

    def test_markdown_in_block_tags_should_be_parsed(self):
        self.assertEqual(self.content, self.EXPECTED_HTML)
