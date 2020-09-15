#!/usr/bin/env python3

import hashlib
import sys

print(hashlib.sha256(sys.argv[1].encode("UTF-8")).hexdigest())
