#!/usr/bin/env python

from testB2SafeCmd.testLogManager import LogManagerTestCase
from testB2SafeCmd.testAuthzManager import AuthzManagerTestCase
from testB2SafeCmd.irodsintgtest import IrodsIntegrationTests
from testB2SafeCmd.irodsb2safetest import IrodsB2safeIntegrationTests
from testB2SafeCmd.epic2intgtest import EpicClient2IntegrationTests 
from testB2SafeCmd.msipidintgtest import MsiPidIntegrationTests

import argparse
import unittest
import sys

__author__ = 'lphan'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='epicclient2 (epic2), '
                                                 'msiPid (msipid), '
                                                 'logging manager (log), '
                                                 'authorization manager (auth), '
                                                 'iRODS (irods), '
                                                 'B2SAFE (b2safe), '
                                                 'and all scripts (all)')
    parser.add_argument('-test', action='store', dest='script',
                        help='[epic2, msipid, log, auth, irods, b2safe, all]')

    param = parser.parse_args()

    if param.script == "epic2":
        # test cases for B2safe-epicclient2#
        print "Test Epicclient2 Script"
        epic2_suite = unittest.TestLoader().loadTestsFromTestCase(
        EpicClient2IntegrationTests)
        ret = unittest.TextTestRunner(descriptions=2, verbosity=2).run(epic2_suite)

    elif param.script == "msipid":
        # test cases for B2safe-msipid#
        print "Test msiPid Script"
        msiPid_suite = unittest.TestLoader().loadTestsFromTestCase(
        MsiPidIntegrationTests)
        ret = unittest.TextTestRunner(descriptions=2, verbosity=2).run(msiPid_suite)

    elif param.script == "log":
        # Test cases for B2Safe-LogManager#
        print "Test Logging Script"
        log_suite = unittest.TestSuite()
        log_suite.addTest(LogManagerTestCase("test_case"))
        ret = unittest.TextTestRunner(descriptions=2, verbosity=2).run(log_suite)

    elif param.script == "auth":
        # Test cases for B2Safe-AuthorzManager#
        print "Test Authorization Script"
        authz_suite = unittest.TestSuite()
        authz_suite.addTest(AuthzManagerTestCase("test_case"))
        ret = unittest.TextTestRunner(descriptions=2, verbosity=2).run(authz_suite)

    elif param.script == "irods":
        # test cases for irods#
        print "Test irods"
        irods_suite = unittest.TestLoader().loadTestsFromTestCase(
        IrodsIntegrationTests)
        ret = unittest.TextTestRunner(descriptions=2, verbosity=2).run(irods_suite)

    elif param.script == "b2safe":
        # test cases for irods#
        print "Test b2safe"
        b2safe_suite = unittest.TestLoader().loadTestsFromTestCase(
        IrodsB2safeIntegrationTests)
        ret = unittest.TextTestRunner(descriptions=2, verbosity=2).run(b2safe_suite)


    elif param.script == "all":
        print "Test all scripts"
        print "run authZmanager.py - if true then run epicclient2beta and log "\
              "with logmanager.py"
        all_suite = unittest.TestSuite()
        all_suite.addTest(LogManagerTestCase("test_case"))
        all_suite.addTest(AuthzManagerTestCase("test_case"))
        all_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            IrodsIntegrationTests))
        all_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            IrodsB2safeIntegrationTests))
        ret = unittest.TextTestRunner(descriptions=2, verbosity=2).run(all_suite)
    else:
        print "Invalid Input; Valid example ./testB2SafeCmd -test epic2"
        sys.exit(8)
    if ret.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(8)
