#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import unittest
import os
from os.path import dirname
from os.path import abspath
import logging
import sys

logger = logging.getLogger('ConfigurationTest')

sys.path.insert(0,
                os.path.join(dirname(dirname(dirname(dirname(abspath(__file__))))),
                             "cmd"))

from configuration import Configuration

class ConfigurationTest(unittest.TestCase):
    def setUp(self):
        # create tmp file with correct configs
        self.conffile = os.getcwd() + os.sep + "ConfigurationTestTMPconfigFile.txt"
        with open(self.conffile, 'w') as tmpConfFile:
            tmpConfFile.write("[Logging]" + os.linesep + \
                                "log_file=../../log/b2share_connection.log" + os.linesep + \
                                "[B2SHARE_HTTP_API]" +  os.linesep + \
                                "host_name=https://trng-b2share.eudat.eu/ " +  os.linesep + \
                                "access_parameter=?access_token " +  os.linesep + \
                                "list_communities_endpoint=api/communities/ " +  os.linesep + \
                                "get_community_schema_endpoint=/schemas/last " +  os.linesep + \
                                "records_endpoint=api/records/ " +  os.linesep + \
                                "log_level=DEBUG " +  os.linesep + \
                                "[iRODS] " +  os.linesep + \
                                "irods_home_dir=/BasZone/home/ " +  os.linesep + \
                                "irods_debug=False")
        logger.setLevel('DEBUG')
        defaultLogPath = Configuration.defaultLogDir
        if os.path.exists(defaultLogPath):
            configurationTestsLogfilepath = defaultLogPath + os.sep + "ConfigurationTest.log"
        else:
            configurationTestsLogfilepath = os.getcwd() + os.sep + "ConfigurationTest.log"
        rfh = logging.handlers.RotatingFileHandler(configurationTestsLogfilepath, \
                                                   maxBytes=8388608, \
                                                   backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: '+ '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)
        
        self.configurationMock = Configuration(self.conffile, True, False, logger)
        pass

    def tearDown(self):
        # delete tmp file with configs
        if os.path.exists(self.conffile):
            os.remove(self.conffile)
        else:
            print("The file does not exist")
        # defaulting only if was not existing before so delete default logs after the test
        # to save the logs for the test add existing log file path
        logging.shutdown()
        logfilepath = Configuration.defaultLogDir + Configuration.defaultLogFileName
        if os.path.exists(logfilepath):
            os.remove(logfilepath)
        logfilepath =  os.getcwd()+ Configuration.defaultLogFileName
        if os.path.exists(logfilepath):
            os.remove(logfilepath)
        pass


    def testParseConf(self):
        # run parseConf to fill the configurationMock with mock options
        self.configurationMock.parseConf()
        
        # test _init_
        self.assertEqual(self.conffile, self.configurationMock.conffile)
        
        # test an option read from the config file
        self.assertEqual("https://trng-b2share.eudat.eu/", self.configurationMock.b2share_host_name)
    
    def test_getConfOption(self):
        with open(self.configurationMock.conffile, "r") as confFile:
            try:
                self.configurationMock.config.readfp(confFile)
            except Exception as e:
                self.assertTrue(False, "Error during reading conf file for the test")
            irodsDebugOption = self.configurationMock._getConfOption('iRODS', 'irods_debug', True)
            self.assertNotEqual(None, irodsDebugOption, "Reading existing boolean option from configuration file.")
        
            irodsHomeDirOption = self.configurationMock._getConfOption('iRODS', 'irods_home_dir')
            self.assertNotEqual(None, irodsHomeDirOption, "Reading existing not boolean option from configuration file.")
        
    def test_getConfOption_error(self):
        try:
            self.configurationMock._getConfOption("unknown", "option", True)
        except Exception as e:
            self.assertNotEqual(None, e, "Reading not existing boolean option from configuration file.")
        try:
            self.configurationMock._getConfOption("unknown", "option")
        except Exception as ex:
            self.assertNotEqual(None, ex, "Reading not existing not boolean option from configuration file.")
        
    def testParseConfError(self):
        # write error containing config file
        with open(self.conffile, 'w') as tmpConfFile:
            tmpConfFile.write("[Logging]" + os.linesep + \
                                "log_file=../../log/b2share_connection.log " + os.linesep + \
                                "[B2SHARE_HTTP_API" +  os.linesep + \
                                "host_name=https://trng-b2share.eudat.eu/ " +  os.linesep + \
                                "access_parameter=?access_token " +  os.linesep + \
                                "list_communities_endpoint=api/communities/ " +  os.linesep + \
                                "get_community_schema_endpoint=/schemas/last " +  os.linesep + \
                                "records_endpoint=api/records/ " +  os.linesep + \
                                "log_level=DEBUG " +  os.linesep + \
                                "[iRODS] " +  os.linesep + \
                                "irods_home_dir=/BasZone/home/ " +  os.linesep + \
                                "irods_debug=False")
        # run parseConf to fill the configurationMock with mock options with incorrect configuration file
        self.configurationMock = Configuration(self.conffile, True, False, logger)
        try:
            self.configurationMock.parseConf()
            
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)
        
if __name__ == "__main__":
    unittest.main()
