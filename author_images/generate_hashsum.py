#!/usr/bin/env python2

from __future__ import print_function
import hashlib
import sys

print(hashlib.sha256(sys.argv[1]).hexdigest())
