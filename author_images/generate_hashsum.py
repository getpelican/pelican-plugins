#!/usr/bin/env python

from __future__ import print_function
import hashlib
import sys

print(hashlib.sha256(sys.argv[1].encode("utf-8")).hexdigest())
