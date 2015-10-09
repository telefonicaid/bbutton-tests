#!/usr/bin/env python
# __author__ = 'xvc'

import subprocess
import sys
import os

# In case we are run from the source directory, we don't want to import the
# project from there:
sys.path.pop(0)

print ("Executing tests: \n")

cmd = "behave tests/ --tags=ft-smoke"
ret = subprocess.call(cmd)
