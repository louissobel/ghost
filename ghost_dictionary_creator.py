"""
This script takes the name of a file on the command line, and will remove words
that have a duplicate word stem.
"""
import sys

from ghost_utils import *

try:
    file_name = sys.argv[1]
    file_handle = open(file_name)
except IndexError:
    file_handle = sys.stdin
except IOError:
    print "IO error opening file"
    sys.exit(1)




