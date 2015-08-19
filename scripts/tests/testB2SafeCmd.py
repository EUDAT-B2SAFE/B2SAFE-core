#!/usr/bin/env python

from testB2SafeCmd.epicapitest import EpicClientAPITestCase
from testB2SafeCmd.epiccredtest import EpicClientCredentialsTestCase
from testB2SafeCmd.epicclitest import EpicClientCLITestCase
from testB2SafeCmd.epicintgtest import EpicClientIntegrationTests
from testB2SafeCmd.testLogManager import LogManagerTestCase
from testB2SafeCmd.testAuthzManager import AuthzManagerTestCase
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
        print "Test Epicclient Script"
        epic_api_suite = unittest.TestLoader().loadTestsFromTestCase(
            EpicClientAPITestCase)
        epic_cred_suite = unittest.TestLoader().loadTestsFromTestCase(
            EpicClientCredentialsTestCase)
        epic_cli_suite = unittest.TestLoader().loadTestsFromTestCase(
            EpicClientCLITestCase)
        epic_it_suite = unittest.TestLoader().loadTestsFromTestCase(
            EpicClientIntegrationTests)
        epic_suite = unittest.TestSuite(
            [epic_api_suite, epic_cred_suite, epic_cli_suite, epic_it_suite])
        unittest.TextTestRunner(descriptions=2, verbosity=2).run(epic_suite)

    elif param.script == "log":
        # Test cases for B2Safe-LogManager#
        print "Test Logging Script"
        log_suite = unittest.TestSuite()
        log_suite.addTest(LogManagerTestCase("test_case"))
        unittest.TextTestRunner(descriptions=2, verbosity=2).run(log_suite)

    elif param.script == "auth":
        # Test cases for B2Safe-AuthorzManager#
        print "Test Authorization Script"
        authz_suite = unittest.TestSuite()
        authz_suite.addTest(AuthzManagerTestCase("test_case"))
        unittest.TextTestRunner(descriptions=2, verbosity=2).run(authz_suite)

    elif param.script == "all":
        print "Test all scripts"
        print "run authZmanager.py - if true then run epicclient2beta and log "\
              "with logmanager.py"
        all_suite = unittest.TestSuite()
        all_suite.addTest(AuthzManagerTestCase("test_case"))
        all_suite.addTest(EpicClientTestCase("test_case"))
        all_suite.addTest(LogManagerTestCase("test_case"))
        unittest.TextTestRunner(descriptions=2, verbosity=2).run(all_suite)

    else:
        print "Invalid Input; Valid example ./testB2SafeCmd -test epic"