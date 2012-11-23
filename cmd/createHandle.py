#!/usr/bin/env python

from epicclient import EpicClient
import uuid
import argparse
import sys

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser(description='Create a handle in the EPIC api')
    parser.add_argument("object", help="the location of the digital object instance")
    args = parser.parse_args()

    baseuri = 'https://epic.sara.nl/v2/handles/'
    username = 'XXXXX'
    password = 'YYYYYY'
    accept_format = 'application/json'
    
    debug_enabled = False
    
    prefix=username

    uid = uuid.uuid1();
    pid = prefix + "/" + str(uid)

    ec = EpicClient(baseuri,username,password,accept_format,debug=debug_enabled)
    result = ec.createHandle(pid,args.object)
    sys.stdout.write(result)
