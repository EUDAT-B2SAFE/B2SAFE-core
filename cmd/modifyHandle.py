#!/usr/bin/env python

from epicclient import EpicClient
import uuid
import argparse
import sys

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser(description='Create a handle in the EPIC api')
    parser.add_argument("pid", help="the pid <prefix/suffix> value")
    parser.add_argument("key", help="the key of the field to change in the pid record")
    parser.add_argument("value", help="the new value to store in the pid record identified with the supplied key")
    args = parser.parse_args()

    baseuri = 'https://epic.sara.nl/v2/handles/'
    username = 'XXXXX'
    password = 'YYYYYY'
    accept_format = 'application/json'
    
    debug_enabled = False
    
    prefix=username


    ec = EpicClient(baseuri,username,password,accept_format,debug=debug_enabled)
    result = ec.modifyHandle(args.pid,args.key,args.value)
    sys.stdout.write(str(result))
