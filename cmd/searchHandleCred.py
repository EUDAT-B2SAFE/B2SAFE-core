#!/usr/bin/env python

from epicclient import EpicClient
from epicclient import credential_parser
import argparse
import sys

if __name__ == "__main__":
    debug_enabled = False
        
    parser = argparse.ArgumentParser(description='Create a handle in the EPIC api')
    parser.add_argument("object", help="the location of the digital object instance")
    parser.add_argument("--credstore",default="NULL", help="the used credential storage (os=filespace,irods=iRODS storage)")
    parser.add_argument("--credpath",default="NULL", help="path to the credentials")
    args = parser.parse_args()

    credentials = credential_parser(args.credstore,args.credpath,debug_enabled)
    baseuri=credentials[0]
    username=credentials[1]
    password=credentials[2]
    accept_format=credentials[3]
    prefix=username

    ec = EpicClient(baseuri,username,password,accept_format,debug=debug_enabled)
    result = ec.searchHandle(prefix,args.object)
    sys.stdout.write(str(result))