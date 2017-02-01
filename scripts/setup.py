#!/usr/bin/env python3
import os
import sys

from pathlib import Path

if sys.version_info < (3, 0):
    raise SystemExit("Sorry, this code need Python 3.0 or higher")
else:
    from lib import setup
    try:
        next(filter(lambda file: file.name == "docker-compose.yml", Path(os.getcwd()).glob("*")))
    except StopIteration as e:
        print("ERROR: You must execute this script in the root lecture viewer directory")
        sys.exit(1)
    setup()

