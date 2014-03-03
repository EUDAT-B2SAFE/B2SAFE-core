#!/usr/bin/env python
#
#   authZ.manager.py
#
#   * use 4 spaces!!! not tabs
#   * See PEP-8 Python style guide http://www.python.org/dev/peps/pep-0008/
#   * use pylint
#

"""EUDAT authorization client API. 

simplejson
download from http://pypi.python.org/pypi/simplejson/
python setup.py install

apt-get install pylint

"""

import argparse
import sys
import simplejson
import fnmatch

###############################################################################
# AuthZ Client Class #
###############################################################################

class AuthZClient(object):
    """Class implementing an EPIC client."""

    def __init__(self, mapFilePath, debug):
        """Initialize object with connection parameters."""
        
        self.mapfile  = mapFilePath
        self.debug = debug

    def _debugMsg(self, method, msg):
        """Internal: Print a debug message if debug is enabled."""

        if self.debug:
            print "[", method, "]", msg
            
    def parse(self):
        """parse authorization assertions from json file.

        This method terminates the program on error

        """

        try:
            filehandle = open(self.mapfile, "r")
        except IOError as err:
            print "error: failed to open %s: %s" % (self.mapfile,
                                                        err.strerror)
            sys.exit(-1)

        with filehandle:
            self.map = simplejson.loads(filehandle.read())

        if self.debug:
            print "authZ assertions from %s" % (self.mapfile)
            
    def checkRequest(self, username, action, target):
        """check the request against the list of assertions."""

        for assertion in self.map:
            for subjectVal in self.map[assertion]['subject']:
                subjectMatch = fnmatch.fnmatch(username, subjectVal)
                if subjectMatch: break
            for actionVal in self.map[assertion]['action']:
                actionMatch = fnmatch.fnmatch(action, actionVal)
                if actionMatch: break                
            for targetVal in self.map[assertion]['target']:
                targetMatch = fnmatch.fnmatch(target, targetVal)
                if targetMatch: break
            if subjectMatch and actionMatch and targetMatch:
                if self.debug:
                    print "matched authZ assertion (%s %s %s)" % (username,
                                                                    action,
                                                                    target)
                return True
        
        if self.debug:
            print "failed to match authZ assertion (%s %s %s)" % (username,
                                                                    action,
                                                                    target)            
            
        return False
        
        
###############################################################################
# EUDAT AuthZ Client Command Line Interface #
###############################################################################

def check(args):
    '''perform check action'''

    authZclient = AuthZClient(args.mapfilepath, args.debug)
    authZclient.parse()

    result = authZclient.checkRequest(args.username, args.action, args.target)

    sys.stdout.write(str(result))
    
def test(args):
    '''do a series of tests'''

    def test_result(result, testval):
        '''local helper func: print OK/FAIL for test result
        Returns 0 on OK, 1 on failure'''
        
        if type(result) != type(testval):
            print "FAIL (wrong type; test is bad)"
            return 1
            
        if result == testval:
            print "OK"
            return 0
        else:
            print "FAIL"
            return 1
            
    authZclient = AuthZClient(args.mapfilepath, args.debug)
    authZclient.parse()
    
    fail = 0
    
    print
    print ("Checking request (testuser, read, path/to/creds) against "
           "assertions contained in " + args.mapfilepath)
    fail += test_result(authZclient.checkRequest('testuser#testzone', 'read', 
                                                 'path/to/creds'),True)
    
    print
    if fail == 0:
        print "All tests passed OK"
    else:
        print "%d tests failed" % fail


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='EUDAT AuthZ client API. ')
    parser.add_argument("mapfilepath", default="NULL",
                        help="path to the authorization map file")
    parser.add_argument("-d", "--debug", help="Show debug output", 
                        action="store_true")

    subparsers = parser.add_subparsers(title='Actions',
                                       description='Handle authz management '
                                                   'actions',
                                       help='additional help')

    parser_read = subparsers.add_parser('check', help='Check authz assertions')
    parser_read.add_argument("username", help='the iRODS user name value '
                                              '(user#zone)')
    parser_read.add_argument("action", help="the action value")
    parser_read.add_argument("target", help="the target value")
    parser_read.set_defaults(func=check)

    parser_test = subparsers.add_parser('test', help='Run test suite')
    parser_test.set_defaults(func=test)

    _args = parser.parse_args()
    _args.func(_args)            
