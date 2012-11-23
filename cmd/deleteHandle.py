#!/usr/bin/env python

from epicclient import EpicClient
import uuid
import argparse
import sys

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser(description='Delete a handle in the EPIC api')
    parser.add_argument("object", help="the PID of the digital object instance")
    args = parser.parse_args()

    baseuri = 'https://epic.sara.nl/v2/handles/'
    username = 'XXXXX'
    password = 'YYYYYY'
    accept_format = 'application/json'
    
    debug_enabled = False
    
    prefix=username
    pid = str(args.object)

    ec = EpicClient(baseuri,username,password,accept_format,debug=debug_enabled)
    result = ec.deleteHandle(pid)
    sys.stdout.write(str(result))
