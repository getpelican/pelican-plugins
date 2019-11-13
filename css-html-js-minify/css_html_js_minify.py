# -*- coding: utf-8 -*-
"""
css-html-js-minify wrapper for Pelican
"""

import glob
import os
import sys

from css_html_js_minify import (
    process_single_css_file,
    process_single_html_file,
    process_single_js_file,
)
from pelican import signals

def main(pelican):
    for f in glob.iglob(pelican.output_path + '/**/*.htm*', recursive=True):
        process_single_html_file(f, overwrite=True)
    for f in glob.iglob(pelican.output_path + '/**/*.css', recursive=True):
        process_single_css_file(f, overwrite=True)
    for f in glob.iglob(pelican.output_path + '/**/*.js', recursive=True):
        process_single_js_file(f, overwrite=True)

def register():
    signals.finalized.connect(main)
