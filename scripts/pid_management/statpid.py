#!/usr/bin/python

import httplib2
import json
import argparse
import base64
from epicclient import Credentials

class PIDManagement():
	""" Class implementing different operations for PID Management."""
	
	def __init__(self, cred):
		self.cred = cred
		self.http = httplib2.Http(disable_ssl_certificate_validation=True)
		self.http.add_credentials(cred.username, cred.password)
		# do not throw exceptions for connection errors
		self.http.force_exception_to_status_code = True

	def requestPID(self, cred, typepid, searchfield):
		'''
		get a list of all pids for a prefix
		'''
		path = self.getURI(cred,typepid,searchfield)
		hdrs = self.getHeader(cred)
		response, content = self.http.request(str(path), method='GET', headers=hdrs)
	    
		if (response.status != 200):
			print '--- status ', response.status, 'from epic, exit'
			exit(2)
		
		pids = json.loads(content)
		#for pid in pids:
		#	print pid	
		return pids

	def getURI(self, cred, key, value):
		if self.cred.baseuri.endswith('/'):
			uri = cred.baseuri + cred.prefix + '/?' + key + '=' + value
		else:
			uri = cred.baseuri + '/' + cred.prefix + '/?' + key + '=' + value
		return uri	
	
	def getHeader(self, cred):
		hdrs = None
		auth = base64.encodestring(cred.username + ':' +cred.password)
		if cred.accept_format:
			hdrs = {'Accept': cred.accept_format,'Authorization': 'Basic ' + auth}
		return hdrs
   
###############################################################################
# PID management Command Line Interface #
###############################################################################
def countPIDprefix(args):
	cred = Credentials('os',args.credpath)
	cred.parse()    
	pidm = PIDManagement(cred)
	result = pidm.requestPID(cred,"limit","0")
	print "Number of PIDs = ", len(result)

def countPIDtype(args):
	cred = Credentials('os',args.credpath)
	cred.parse()
	pidm = PIDManagement(cred)    
	result = pidm.requestPID(cred,args.typepid,args.searchfield)
	print "Number of PIDs = ", len(result)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='EUDAT PID Management: return number of PIDs followed by Prefix and Type')
	parser.add_argument("credpath",default="NULL",help="path to the credentials")
	
	subparsers = parser.add_subparsers(title='Actions', description='Operations for management of PID', help='additional help') 
	
	parser_countPIDprefix = subparsers.add_parser('count_prefix',help='get number of PIDs with default Prefix from credential')
	parser_countPIDprefix.set_defaults(func=countPIDprefix)
	
	parser_countPIDtype = subparsers.add_parser('count_type',help='get number of PIDs with specific type.' )
	parser_countPIDtype.add_argument("typepid",help="Input corresponding Type in PID to search (URL, 10320/LOC, CHECKSUM, EUDAT/ROR, EUDAT/PPID)")
	parser_countPIDtype.add_argument("searchfield",help="search-key for typepid, using wildcard * if necessary")
	parser_countPIDtype.set_defaults(func=countPIDtype)
	
	args = parser.parse_args()
	args.func(args)
