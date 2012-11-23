#!/usr/bin/env python

from epicclient import EpicClient
import uuid
import argparse
import sys

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser(description='Update a handle 10320/LOC field in the EPIC api')
    parser.add_argument("ppid", help="the parent pid <prefix/suffix> value")
    parser.add_argument("cpid", help="the child pid <prefix/suffix> value")
    args = parser.parse_args()

    baseuri = 'https://epic.sara.nl/v2/handles/'
    username = 'XXXXX'
    password = 'YYYYYY'
    accept_format = 'application/json'
    
    debug_enabled = False
    
    prefix=username


    ec = EpicClient(baseuri,username,password,accept_format,debug=debug_enabled)
    result = ec.updateHandleWithLocation(args.ppid[:42],args.cpid[:42])
    sys.stdout.write(str(result))
