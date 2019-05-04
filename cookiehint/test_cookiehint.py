import unittest
import os

import cookiehint 


class TestCookieHint(unittest.TestCase):

     def setUp(self):
        os.system('cp ./test_data/test.html ./test_data/test-current.html')


     def tearDown(self):
        os.system('rm ./test_data/test-current.html')


     def test_text_replace(self):
        """
        Test behaviour if text ws written to the html file
        """
        cookiehint.add_cookie_hint('./test_data/test-current.html', None)
        with open('./test_data/test-current.html', 'r') as file:
           content = file.read()
        
        self.assertTrue(content.find(cookiehint.plugin_content['text']) > -1)
        self.assertTrue(content.find('<head>') > -1)        
        self.assertTrue(content.find('</head>') > -1)
        self.assertTrue(content.find('<body>') > -1)
        self.assertTrue(content.find('</body>') > -1)


if __name__ == "__main__":
    unittest.main()
