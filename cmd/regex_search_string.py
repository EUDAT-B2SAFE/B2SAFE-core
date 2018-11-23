#!/usr/bin/env python

import re
import sys

def search_pattern_in_string(pattern, string):
    """
    search_pattern_in_string. Search if a pattern matches in a string.
    return match in string if found.
    return "no match found!" if not found
    """
    searchObj = re.search(pattern, string, re.U|re.I)
    if searchObj:
        print searchObj.group()
    else:
        print "no match found!"

if __name__ == "__main__":

     search_pattern_in_string(sys.argv[1], sys.argv[2])

