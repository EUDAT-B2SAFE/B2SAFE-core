#!/usr/bin/env python
from testB2SafeCmd.testEpicClient import EpicClientTestCase
import argparse
import unittest

__author__ = 'lphan'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test script for epicclient '
                                                 '(epic), '
                                                 'logging manager (log), '
                                                 'authorization manager (auth)'
                                                 'and all scripts (all)')
    parser.add_argument('-test', action='store', dest='script',
                        help='[epic, log, auth, all]')

    param = parser.parse_args()

    if param.script == "epic":
        # Test cases for B2Safe-Epicclient#
        epic_suite = unittest.TestSuite()
        print "Test Epicclient Script"
        epic_suite.addTest(EpicClientTestCase("test_case"))
        unittest.TextTestRunner(descriptions=2, verbosity=2).run(epic_suite)
    elif param.script == "log":
        print "Test Logging Script"
    elif param.script == "auth":
        print "Test Authorization Script"
    elif param.script == "all":
        print "Test all scripts"
    else:
        print "Invalid Input; Valid example ./testB2SafeCmd -test epic"