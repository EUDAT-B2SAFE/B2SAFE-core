#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from testB2shareConnectionClient.configurationtest import ConfigurationTest
from testB2shareConnectionClient.b2shareclienttest import B2shareClientTest

def getSuite():
    # first test the configurations class that loads the configurations for the B2shareClient, that is not working without
    # than test the B2shareClient from the b2shareclientworker.py doing the requests to the B2Share
    # as b2shareclient.py is only a wrapper calling the B2shareClient and connecting to the iRODS
    configurationTests = unittest.TestLoader().loadTestsFromTestCase(ConfigurationTest)
    b2shareClientTests = unittest.TestLoader().loadTestsFromTestCase(B2shareClientTest)
    # TODO: at the end call the tests for the b2shareclient.py
    return unittest.TestSuite([configurationTests, b2shareClientTests])

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(getSuite())