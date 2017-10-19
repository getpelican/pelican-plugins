# Copyright (C) 2017  Sébastien Gendre

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import re
from orgpython import org_to_html
from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open

class OrgReader(BaseReader):
    """Reader for Org files"""
    enabled = True
    file_extensions = ['org']

    def _separate_header_and_content(self, text_lines):
        """
        From a given Org text, return the header separate from the content.
        The given text must be separate line by line and be a list.
        The return is a list of two items: header and content.
        Theses two items are text separate line by line in format of a list
        Keyword Arguments:
        text_lines -- A list, each item is a line of the texte
        Return:
        [
          header   -- A list, each item is a line of the texte
          content  -- A list, each item is a line of the texte
        ]
        """
        pass

    def _parse_metadata(self, text_lines):
        """
        From a given Org text, return the metadatas 
        Keyword Arguments:
        text_lines -- A list, each item is a line of the texte
        Return:
        A dict containing metadatas
        """
        pass
    
