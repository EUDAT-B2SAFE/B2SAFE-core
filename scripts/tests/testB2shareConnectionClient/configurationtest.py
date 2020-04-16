#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import unittest
import os
from os.path import dirname
from os.path import abspath
import logging
import sys

logger = logging.getLogger('ConfigurationTest')

sys.path.insert(0, os.path.join(dirname(dirname(dirname(dirname(abspath(__file__))))), "cmd"))

from configuration import Configuration

class ConfigurationTest(unittest.TestCase):
    def setUp(self):
        # create tmp file with correct configs
        self.conffilePath = os.getcwd() + os.sep + "ConfigurationTestTMPconfigFile.txt"
        self.testLogFilePath = os.getcwd() + os.sep + "logs/ConfigurationTest.log"
        self.irodsEnvPath = "/home/irods/.irods/irods_environment.json"
        self.irodsZoneName = "JULK_ZONE"
        with open(self.conffilePath, 'w') as tmpConfFile:
            tmpConfFile.write('{"configurations": ' + os.linesep + 
                                '{' + os.linesep +
                                '"b2share_http_api": {' +  os.linesep +
                                    '"host_name": "https://trng-b2share.eudat.eu/",' +  os.linesep +
                                    '"access_parameter": "?access_token",' +  os.linesep +
                                    '"list_communities_endpoint": "api/communities/",' +  os.linesep +
                                    '"get_community_schema_endpoint": "/schemas/last",' +  os.linesep +
                                    '"records_endpoint": "api/records/"' +  os.linesep +
                                '} ,' + os.linesep +
                                '"irods": {' + os.linesep +
                                    '"zone_name": "' + self.irodsZoneName + '",' + os.linesep +
                                    '"irods_env": "' + self.irodsEnvPath + '",' + os.linesep +
                                    '"resources": "",' + os.linesep +
                                    '"irods_home_dir": "",' + os.linesep +
                                    '"irods_debug": ""' + os.linesep +
                                '},' + os.linesep +
                                '"logging": {' + os.linesep +
                                    '"loglevel": "DEBUG",' + os.linesep +
                                    '"logfile": "' + self.testLogFilePath + '"'+ os.linesep +
                                 '}' + os.linesep +
	                            '}' + os.linesep +
                              "}")
        self.configurationMock = Configuration(logger)
        pass

    def tearDown(self):
        # delete tmp file with configs
        if os.path.exists(self.conffilePath):
            os.remove(self.conffilePath)
        else:
            print("The file does not exist: " + self.conffilePath)
        # defaulting only if was not existing before so delete default logs after the test
        # to save the logs for the test add existing log file path
        logging.shutdown()
        if os.path.exists(self.testLogFilePath):
            os.remove(self.testLogFilePath)
            logDir = os.path.dirname(self.testLogFilePath)
            os.rmdir(logDir)
        else:
            print("The file does not exist: " + self.testLogFilePath)
        pass

    def testLoadConfigurarionsFrom(self):
        # run parseConf to fill the configurationMock with mock options
        self.configurationMock.loadConfigurarionsFrom(self.conffilePath)
        
        # test _init_
        self.assertEqual(self.conffilePath, self.configurationMock.config_path)
        
        # test an option read from the config file
        self.assertEqual("https://trng-b2share.eudat.eu/", self.configurationMock.b2share_host_name)
        
    def testLoadConfigurarionsFromError(self):
        # write error containing config file
        with open(self.conffilePath, 'w') as tmpConfFile:
            tmpConfFile.write('{"configurations": ' + os.linesep + 
                                '{' + os.linesep +
                                '"b2share_http_api": {' +  os.linesep +
                                    '"host_name": "https://trng-b2share.eudat.eu/",' +  os.linesep +
                                    '"access_parameter": "?access_token",' +  os.linesep +
                                    '"list_communities_endpoint": "api/communities/",' +  os.linesep +
                                    '"get_community_schema_endpoint": "/schemas/last",' +  os.linesep +
                                    '"records_endpoint": "api/records/"' +  os.linesep +
                                #'} ,' + os.linesep +
                                '"irods": {' + os.linesep +
                                    '"zone_name": "' + self.irodsZoneName + '",' + os.linesep +
                                    '"irods_env": "' + self.irodsEnvPath + '",' + os.linesep +
                                    '"resources": "",' + os.linesep +
                                    '"irods_home_dir": "",' + os.linesep +
                                    '"irods_debug": ""' + os.linesep +
                                '},' + os.linesep +
                                '"logging": {' + os.linesep +
                                    '"loglevel": "DEBUG",' + os.linesep +
                                    '"logfile": "' + self.testLogFilePath + '"'+ os.linesep +
                                 '}' + os.linesep +
	                            '}' + os.linesep +
                              "}")
        # run parseConf to fill the configurationMock with mock options with incorrect configuration file
        self.configurationMock = Configuration(logger)
        try:
            self.configurationMock.loadConfigurarionsFrom(self.conffilePath)
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)
        
if __name__ == "__main__":
    unittest.main()
