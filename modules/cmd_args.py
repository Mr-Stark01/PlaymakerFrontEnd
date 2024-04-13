import argparse
import json
import os

parser = argparse.ArgumentParser()

parser.add_argument("--loglevel", type=str, help="log level; one of: CRITICAL, ERROR, WARNING, INFO, DEBUG", default=None)
parser.add_argument("--skip-install", action='store_true', help="launch.py argument: skip installation of packages")
parser.add_argument("--skip-python-version-check", action='store_true', help="launch.py argument: do not check python version")
parser.add_argument("--dump-sysinfo", action='store_true', help="launch.py argument: dump limited sysinfo file (without information about extensions, options) to disk and quit")
