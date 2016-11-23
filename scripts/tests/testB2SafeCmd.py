#!/usr/bin/env python

from testB2SafeCmd.epicapitest import EpicClientAPITestCase
from testB2SafeCmd.epiccredtest import EpicClientCredentialsTestCase
from testB2SafeCmd.epicclitest import EpicClientCLITestCase
from testB2SafeCmd.epicintgtest import EpicClientIntegrationTests
from testB2SafeCmd.testLogManager import LogManagerTestCase
from testB2SafeCmd.testAuthzManager import AuthzManagerTestCase
from testB2SafeCmd.irodsintgtest import IrodsIntegrationTests
from testB2SafeCmd.irodsb2safetest import IrodsB2safeIntegrationTests
from testB2SafeCmd.epic2intgtest import EpicClient2IntegrationTests 

import argparse
import unittest

__author__ = 'lphan'

def create_epic_test_suite():
    epic_api_suite = unittest.TestLoader().loadTestsFromTestCase(
        EpicClientAPITestCase)
    epic_cred_suite = unittest.TestLoader().loadTestsFromTestCase(
        EpicClientCredentialsTestCase)
    epic_cli_suite = unittest.TestLoader().loadTestsFromTestCase(
        EpicClientCLITestCase)
    epic_it_suite = unittest.TestLoader().loadTestsFromTestCase(
        EpicClientIntegrationTests)
    return unittest.TestSuite(
        [epic_api_suite, epic_cred_suite, epic_cli_suite, epic_it_suite])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test script for epicclient '
                                                 '(epic), '
                                                 'epicclient2 (epic2), '
                                                 'logging manager (log), '
                                                 'authorization manager (auth), '
                                                 'iRODS (irods), '
                                                 'B2SAFE (b2safe), '
                                                 'and all scripts (all)')
    parser.add_argument('-test', action='store', dest='script',
                        help='[epic, epic2, log, auth, irods, b2safe, all]')

    param = parser.parse_args()

    if param.script == "epic":
        # Test cases for B2Safe-Epicclient#
        print "Test Epicclient Script"
        epic_suite = create_epic_test_suite()
        unittest.TextTestRunner(descriptions=2, verbosity=2).run(epic_suite)

    elif param.script == "epic2":
        # test cases for B2safe-epicclient2#
        print "Test Epicclient2 Script"
        epic2_suite = unittest.TestLoader().loadTestsFromTestCase(
        EpicClient2IntegrationTests)
        unittest.TextTestRunner(descriptions=2, verbosity=2).run(epic2_suite)

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

    elif param.script == "irods":
        # test cases for irods#
        print "Test irods"
        irods_suite = unittest.TestLoader().loadTestsFromTestCase(
        IrodsIntegrationTests)
        unittest.TextTestRunner(descriptions=2, verbosity=2).run(irods_suite)

    elif param.script == "b2safe":
        # test cases for irods#
        print "Test b2safe"
        b2safe_suite = unittest.TestLoader().loadTestsFromTestCase(
        IrodsB2safeIntegrationTests)
        unittest.TextTestRunner(descriptions=2, verbosity=2).run(b2safe_suite)


    elif param.script == "all":
        print "Test all scripts"
        print "run authZmanager.py - if true then run epicclient2beta and log "\
              "with logmanager.py"
        all_suite = unittest.TestSuite()
        all_suite.addTest(create_epic_test_suite())
        all_suite.addTest(LogManagerTestCase("test_case"))
        all_suite.addTest(AuthzManagerTestCase("test_case"))
        unittest.TextTestRunner(descriptions=2, verbosity=2).run(all_suite)

    else:
        print "Invalid Input; Valid example ./testB2SafeCmd -test epic"
