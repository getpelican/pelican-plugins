"""Libravatar plugin for Pelican"""

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


import hashlib
from pelican import signals


def initialize (pelicanobj):
    """Initialize the Libravatar plugin"""
    pelicanobj.settings.setdefault ('LIBRAVATAR_MISSING', None)
    pelicanobj.settings.setdefault ('LIBRAVATAR_SIZE', None)


def add_libravatar (generator, metadata):
    """Article generator connector for the Libravatar plugin"""
    missing = generator.settings.get ('LIBRAVATAR_MISSING')
    size = generator.settings.get ('LIBRAVATAR_SIZE')

    ## Check the presence of the Email header
    if 'email' not in metadata.keys ():
        try:
            metadata ['email'] = generator.settings.get ('AUTHOR_EMAIL')
        except:
            pass

    ## Add the Libravatar URL
    if metadata ['email']:

        ## Compose URL using the MD5 hash
        ## (the ascii encoding is necessary for Python3)
        email = metadata ['email'].lower ().encode ('ascii')
        md5 = hashlib.md5 (email).hexdigest ()
        url = 'http://cdn.libravatar.org/avatar/' + md5

        ## Add eventual "missing picture" option
        if missing or size:
            url = url + '?'
            if missing:
                url = url + 'd=' + missing
                if size:
                    url = url + '&'
            if size:
                url = url + 's=' + str (size)

        ## Add URL to the article's metadata
        metadata ['author_libravatar'] = url


def register ():
    """Register the Libravatar plugin with Pelican"""
    signals.initialized.connect (initialize)
    signals.article_generator_context.connect (add_libravatar)
