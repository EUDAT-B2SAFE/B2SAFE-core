#!/usr/bin/env python

from epicclient import EpicClient
from epicclient import credential_parser
import argparse
import sys

if __name__ == "__main__":
	debug_enabled = False
	
	parser = argparse.ArgumentParser(description='Update a handle 10320/LOC field in the EPIC api')
	parser.add_argument("ppid", help="the parent pid <prefix/suffix> value")
	parser.add_argument("cpid", help="the child pid <prefix/suffix> value")
	parser.add_argument("--credstore",default="NULL", help="the used credential storage (os=filespace,irods=iRODS storage)")
	parser.add_argument("--credpath",default="NULL", help="path to the credentials")
	args = parser.parse_args()

	credentials = credential_parser(args.credstore,args.credpath,debug_enabled)
	baseuri=credentials[0]
	username=credentials[1]
	password=credentials[2]
	accept_format=credentials[3]
	
	ec = EpicClient(baseuri,username,password,accept_format,debug_enabled)
	result = ec.updateHandleWithLocation(args.ppid[:40],args.cpid[:40])
	sys.stdout.write(str(result))