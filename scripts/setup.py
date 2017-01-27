#!/usr/bin/env python3

import sys

if sys.version_info < (3, 0):
    raise SystemExit("Sorry, this code need Python 3.0 or higher")
else:
    from setup_lib.setup_prompt import setup
    setup()

