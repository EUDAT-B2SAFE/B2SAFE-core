#!/usr/bin/env python
#
#   authZmanager.py
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

    def __init__(self, mapfilepath, debug):
        """Initialize object with connection parameters.
        :rtype : object
        """

        self.mapfile = mapfilepath
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
            print "authZ assertions from %s" % self.mapfile

    def checkauth(self, username, action, target, credential):
        """1. check the authorization (credential) of user, action = read
        for credential """
        i = 0
        for assertion in self.map:
            for subjectVal in self.map[assertion]['subject']:
                subjectMatch = fnmatch.fnmatch(username, subjectVal)
                if subjectMatch:
                    break
            for actionVal in self.map[assertion]['action']:
                actionAuth = fnmatch.fnmatch("read", actionVal)
                actionMatch = fnmatch.fnmatch(action, actionVal)
                if actionAuth or actionMatch:
                    break
            for targetVal in self.map[assertion]['target']:
                targetAuth = fnmatch.fnmatch(credential, targetVal)
                targetMatch = fnmatch.fnmatch(target, targetVal)
                if targetAuth or targetMatch:
                    break
            if subjectMatch and actionAuth and targetAuth:
                i += 1
                if self.debug:
                    print "matched authZ assertion (%s %s %s %s)" \
                          % (username, "read", target, credential)
                    #print "i=", i
            if subjectMatch and actionMatch and targetMatch:
                i += 1
                if self.debug:
                    print "matched action assertion (%s %s %s %s)" \
                          % (username, action, target, credential)
                    #print "i=", i
            if i == 2:
                #print "TRUE"
                return True

        return False

    def checkRequest(self, username, action, target):
        """check the request against the list of assertions."""

        for assertion in self.map:
            for subjectVal in self.map[assertion]['subject']:
                subjectMatch = fnmatch.fnmatch(username, subjectVal)
                if subjectMatch:
                    break
            for actionVal in self.map[assertion]['action']:
                actionMatch = fnmatch.fnmatch(action, actionVal)
                if actionMatch:
                    break
            for targetVal in self.map[assertion]['target']:
                targetMatch = fnmatch.fnmatch(target, targetVal)
                if targetMatch:
                    break
            if subjectMatch and actionMatch and targetMatch:
                if self.debug:
                    print "matched authZ assertion (%s %s %s)" \
                          % (username, action, target)
                return True

        if self.debug:
            print "failed to match authZ assertion (%s %s %s)" \
                  % (username, action, target)

        return False


###############################################################################
# EUDAT AuthZ Client Command Line Interface #
###############################################################################

def check(args):
    """perform check action"""

    authzclient = AuthZClient(args.mapfilepath, args.debug)
    authzclient.parse()

    result = authzclient.checkauth(args.username, args.action, args.target,
                                   args.credential)
    #	result = authzclient.checkRequest(args.username, args.action,
    # args.target)
    sys.stdout.write(str(result))


def test(args):
    """do a series of tests"""

    def test_result(result, testval):
        """local helper func: print OK/FAIL for testB2SafeCmd result
        Returns 0 on OK, 1 on failure"""

        if type(result) != type(testval):
            print "FAIL (wrong type; testB2SafeCmd is bad)"
            return 1

        if result == testval:
            print "OK"
            return 0
        else:
            print "FAIL"
            return 1

    authzclient = AuthZClient(args.mapfilepath, args.debug)
    authzclient.parse()

    fail = 0

    print
    print ("Checking request (testuser, read, path/to/creds) against "
           "assertions contained in " + args.mapfilepath)
    #fail += test_result(authZclient.checkRequest('testuser#testzone', 'read',
    #                                             'path/to/creds'), True)
    fail += test_result(authzclient.checkauth('testuser#testzone',
                        'epicclient2beta.py', '* delete *',
                        'path/to/creds'), True)

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
    parser_read.add_argument("credential", help="the Credential value")
    parser_read.set_defaults(func=check)

    parser_test = subparsers.add_parser('test', help='Run test suite')
    parser_test.set_defaults(func=test)

    _args = parser.parse_args()
    _args.func(_args)
