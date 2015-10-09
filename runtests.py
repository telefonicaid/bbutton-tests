#!/usr/bin/env python
# __author__ = 'xvc'

import subprocess
import sys
import os


def execute(cmd):
    process = subprocess.Popen(cmd.split())
    output = process.communicate()[0]


print ("Executing SMOKE tests: \n")
cmd = "behave tests/ --tags=ft-smoke"
execute(cmd)

print ("Executing HAPPY PATH tests: \n")
cmd = "behave tests/ --tags=ft-happypath"
execute(cmd)
