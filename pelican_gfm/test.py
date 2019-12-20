#!/usr/bin/python -B
from __future__ import absolute_import
import unittest
from gfm import gfm

class gfmTest(unittest.TestCase):

    def test_for_gfm(self):
        self.assertTrue(gfm.register())

if __name__ == '__main__':
    unittest.main()
