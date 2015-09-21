# -*- coding: utf-8 -*-
"""
Add_cname
--------

Add CNAME file in your output directory.

"""

import os
from pelican import signals

def add_cname(p):
    """ 
    :param p: pelican instance
    :return: None
    """

    cname_path = os.path.join(p.output_path, 'CNAME')
    siteurl = p.settings.get('SITEURL', "127.0.0.1:8000")
    siteurl = siteurl.replace("http://", "")
    with open(cname_path, 'w') as cname_file:
        cname_file.write(siteurl)    

def register():
    signals.finalized.connect(add_cname)
