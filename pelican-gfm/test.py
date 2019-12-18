#!/usr/bin/python -B

import unittest

# python2 and python3 differ on how to do this it seems
try:
    from .gfm import *
except ImportError:
    import gfm

class gfmTest(unittest.TestCase):

    def test_for_gfm(self):
        self.assertTrue(gfm.register())

if __name__ == '__main__':
    unittest.main()
