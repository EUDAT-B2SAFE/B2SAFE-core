#!/usr/bin/env python
#
#   * use 4 spaces!!! not tabs
#   * See PEP-8 Python style guide http://www.python.org/dev/peps/pep-0008/
#   * use pylint
#

import json

user_map_file="/etc/irods/user_map.json"

def parseUserMap():
    """Parse the user map file"""

    with open(user_map_file, 'r') as f:
        user_map = json.load(f)
        jstr = json.dumps(user_map, ensure_ascii=True, indent=4)
        print(jstr)


if __name__ == "__main__":
 
    parseUserMap()
