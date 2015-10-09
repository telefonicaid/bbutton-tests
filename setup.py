# -*- coding: utf-8 -*
"""
Setup script for behave.

USAGE:
    python setup.py install
    python setup.py behave_test     # -- XFAIL on Windows (currently).
    python setup.py nosetests
"""

import sys
import os.path
import re

HERE0 = os.path.dirname(__file__) or os.curdir
os.chdir(HERE0)
HERE = os.curdir
sys.path.insert(0, HERE)

from setuptools import find_packages, setup
from setuptools_behave import behave_test

# -----------------------------------------------------------------------------
# CONFIGURATION:
# -----------------------------------------------------------------------------
python_version = float("%s.%s" % sys.version_info[:2])
requirements = ["parse>=1.6.3", "parse_type>=0.3.4", "six"]
py26_extra = ["argparse", "importlib", "ordereddict"]
if python_version < 2.7:
    requirements.extend(py26_extra)
if python_version < 2.6:
    requirements.append("simplejson")

BEHAVE = os.path.join(HERE, "behave")
README = os.path.join(HERE, "README.md")
description = "".join(open(README).readlines()[4:])


# -----------------------------------------------------------------------------
# UTILITY:
# -----------------------------------------------------------------------------
def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        elif re.match(r'\s*-r\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

requirements = parse_requirements('requirements.txt'),

# -----------------------------------------------------------------------------
# SETUP:
# -----------------------------------------------------------------------------
setup(
    name="bbutton-tests",
    version="0.1.0-dev",
    description="bbuton tests",
    long_description=description,
    author="XVC",
    author_email="behave-users@googlegroups.com",
    url="aaa",
    provides=["bbutton"],
    py_modules=["setuptools_behave"],
    entry_points={
        "console_scripts": [
            "behave = behave.__main__:main"
        ],
        "distutils.commands": [
            "behave_test = setuptools_behave:behave_test"
        ]
    },
    install_requires=requirements,
    test_suite="nose.collector",
    tests_require=["nose>=1.3", "behave>=1.2.5"],
    cmdclass={
        "behave_test": behave_test,
    },
    use_2to3=bool(python_version >= 3.0),
    license="GNU",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: BSD License",
    ],
    zip_safe=True,
)
