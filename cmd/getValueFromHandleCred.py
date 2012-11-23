#!/usr/bin/env python

from epicclient import EpicClient
from epicclient import credential_parser
import uuid
import argparse
import sys

if __name__ == "__main__":
	debug_enabled = False
    
	parser = argparse.ArgumentParser(description='Get a value from a handle in the EPIC api')
	parser.add_argument("pid", help="the pid <prefix/suffix> value")
	parser.add_argument("key", help="the key of the field to change in the pid record")
	parser.add_argument("--credstore",default="NULL", help="the used credential storage (os=filespace,irods=iRODS storage)")
	parser.add_argument("--credpath",default="NULL", help="path to the credentials")
	args = parser.parse_args()
    
	credentials = credential_parser(args.credstore,args.credpath,debug_enabled)
	baseuri = credentials[0]
	username = credentials[1]
	password = credentials[2]
	accept_format = credentials[3]
    
	ec = EpicClient(baseuri,username,password,accept_format,debug=debug_enabled)
	result = ec.getValueFromHandle(args.pid,args.key)
	sys.stdout.write(str(result))
