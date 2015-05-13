"""Unit testing suite for the Libravatar Plugin"""

## Copyright (C) 2015  Rafael Laboissiere <rafael@laboissiere.net>
##
## This program is free software: you can redistribute it and/or modify it
## under the terms of the GNU General Affero Public License as published by
## the Free Software Foundation, either version 3 of the License, or (at
## your option) any later version.
##
## This program is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see http://www.gnu.org/licenses/.

import os
import re
import unittest
import hashlib
from tempfile import mkdtemp
from shutil import rmtree

from . import libravatar
from pelican import Pelican
from pelican.settings import read_settings


AUTHOR_EMAIL = 'bart.simpson@example.com'
MD5_HASH = hashlib.md5 (AUTHOR_EMAIL).hexdigest ()
LIBRAVATAR_BASE_URL = 'http://cdn.libravatar.org/avatar/'


class TestLibravatarURL (unittest.TestCase):
    """Class for testing the URL output of the Libravatar plugin"""

    def setUp (self, override = None):
        self.output_path = mkdtemp (prefix = 'pelicantests.')
        self.content_path = mkdtemp (prefix = 'pelicantests.')
        theme_path = os.path.join (os.path.dirname (os.path.abspath (__file__)),
                                   'test_data', 'theme')
        settings = {
            'PATH': self.content_path,
            'THEME': theme_path,
            'OUTPUT_PATH': self.output_path,
            'PLUGINS': [libravatar],
            'CACHE_CONTENT': False
        }
        if override:
            settings.update (override)

        fid = open (os.path.join (self.content_path, 'test.md'), 'w')
        fid.write ('Title: Test\nDate:\nEmail: ' + AUTHOR_EMAIL + '\n\n')
        fid.close ()

        self.settings = read_settings (override = settings)
        pelican = Pelican (settings = self.settings)
        pelican.run ()

    def tearDown (self):
        rmtree (self.output_path)
        rmtree (self.content_path)

    def test_url (self, options = ''):
        fid = open (os.path.join (self.output_path, 'test.html'), 'r')
        found = False
        for line in fid.readlines ():
            print line
            if re.search (LIBRAVATAR_BASE_URL + MD5_HASH + options, line):
                found = True
                break
        assert found

class TestLibravatarMissing (TestLibravatarURL):
    """Class for testing the Libravatar "missing picture" option"""

    def setUp (self, override = None):
        self.library = 'wavatar'
        TestLibravatarURL.setUp (self,
                                  override = {'LIBRAVATAR_MISSING':
                                              self.library})

    def test_url (self):
        TestLibravatarURL.test_url (self, '\?d=' + self.library)


class TestLibravatarSize (TestLibravatarURL):
    """Class for testing the Libravatar size option"""

    def setUp (self, override = None):
        self.size = 100
        TestLibravatarURL.setUp (self,
                                  override = {'LIBRAVATAR_SIZE': self.size})

    def test_url (self):
        TestLibravatarURL.test_url (self, '\?s=' + str (self.size))

