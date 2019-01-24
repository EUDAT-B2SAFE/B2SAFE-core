#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from testB2shareConnectionClient.configurationtest import ConfigurationTest
from testB2shareConnectionClient.b2shareclienttest import B2shareClientTest
from testB2shareConnectionClient.b2shareclient_cli_test import B2shareClientCLITest

def getSuite():
    # first test the configurations class that loads the configurations for the B2shareClient, that is not working without
    # than test the B2shareClient doing the requests to the B2SHARE
    # as b2shareclientCLI is only a wrapper calling the B2shareClient and connecting to the iRODS
    configurationTests = unittest.TestLoader().loadTestsFromTestCase(ConfigurationTest)
    b2shareClientTests = unittest.TestLoader().loadTestsFromTestCase(B2shareClientTest)
    b2shareClientCLITests = unittest.TestLoader().loadTestsFromTestCase(B2shareClientCLITest)
    return unittest.TestSuite([configurationTests, b2shareClientTests, b2shareClientCLITests])

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(getSuite())