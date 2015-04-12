#!/usr/bin/env python
# encoding: utf-8
import os
import subprocess

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'tox.ini')
subprocess.call(['tox', '-c', CONFIG_FILE])
