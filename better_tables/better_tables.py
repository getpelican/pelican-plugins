# Copyright (c) 2015 Alex Waite
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

''' Better Tables: Restore sanity to rst->html tables

This pelican plugin removes the excess attributes and elements in the HTML
tables generated from RST. Trimming this fat allows them to pass HTML5
validation. Hopefully rst2html5 will be merged into pelican at some point, but
until then, this hacky approach is needed.

This approach has the advantage of restoring sanity to tables, and allows their
column with to flow normally. All styling is default and must be styled by CSS
rather than in HTML attributes.

I make no claim that /all/ HTML table crimes generated are corrected, merely
the ones which I have stumbled across.

Usage:
    Enable the plugin in your pelicanconf.py

    PLUGINS = [
        # ...
        'better_tables',
        # ...
    ]

    And that's it. Life's simple like that sometimes.
'''

from pelican import signals, contents
from bs4 import BeautifulSoup

def better_tables(content):
    if isinstance(content, contents.Static):
        return

    soup = BeautifulSoup(content._content, 'html.parser')

    for table in soup.findAll('table'):
        # table's "border" is so 1996
        del(table['border'])

        # col widths. not only /infuriating/ it's also not in HTML5
        for tag in table.findAll('colgroup'):
            tag.extract()

        # tbody and thead's valign
        for tag in table.findAll(['tbody', 'thead']):
            del(tag['valign'])

    soup.renderContents()
    content._content = soup.decode()

def register():
    signals.content_object_init.connect(better_tables)
