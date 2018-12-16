#!/usr/bin/env python 
# -*- coding: utf-8 -*-

################################################################################
# Configuration Class #
################################################################################
import ConfigParser
import logging.handlers
import os

class Configuration():
    """ 
    Get properties from filesystem
    """
    defaultLogDir = os.getcwd() + os.sep + "logs"
    defaultLogFileName = os.sep + "b2share_connection.log"
    
    def __init__(self, conffile, debug, dryrun, logger):
        self.conffile = conffile
        self.debug = debug
        self.dryrun = dryrun
        self.logger = logger
        self.access_token = ""
        self.log_level = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, \
                          'ERROR': logging.ERROR, 'WARNING': logging.WARNING, \
                          'CRITICAL': logging.CRITICAL}
        self.config = ConfigParser.RawConfigParser()
    
    # return configuration missing exception if expected config is not in the config file
    def parseConf(self):
        """Parse the configuration file."""
        
        #self.config = ConfigParser.RawConfigParser()
        if not os.path.exists(self.conffile):
            self.logger.error('missing configuration file %s:%s' % (self.conffile))
            return # error config file not found
        
        with open(self.conffile, "r") as confFile:
            try:
                self.config.readfp(confFile)
            except Exception as e:
                self.configuration.logger.error(e)
                return

        logfilepath = self._getConfOption('Logging', 'log_file')
        if not os.path.exists(logfilepath):
            # if user did not specified a path for log file default to current dir + b2share_connection.log
            # self.logger.error("no location for log file is specified, so try to default to <currend directory>/logs/b2share_connection.log")
            try:  
                os.mkdir(self.defaultLogDir)
                logfilepath =  self.defaultLogDir + self.defaultLogFileName
            except OSError: 
                # self.logger.error("no location for log file is specified, so try to default to <currend directory>/logs/b2share_connection.log")
                logfilepath =  os.getcwd()+ self.defaultLogFileName
                #print("Creation of the directory %s failed, so defaulting to <currend directory>/b2share_connection.log" % defaultLogDir)
        
        loglevel = self._getConfOption('Logging', 'log_level')
        if self.debug:
            loglevel = 'DEBUG'
        self.logger.setLevel(self.log_level[loglevel])
        
        rfh = logging.handlers.RotatingFileHandler(logfilepath, \
                                                   maxBytes=8388608, \
                                                   backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: '
                                    + '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        self.logger.addHandler(rfh)

        self.b2share_scheme = self._getConfOption('B2SHARE', 'scheme')
        self.b2share_addr = self._getConfOption('B2SHARE', 'address')
        self.b2share_path = self._getConfOption('B2SHARE', 'path')

        self.b2share_host_name = self._getConfOption('B2SHARE_HTTP_API', 'host_name')
        self.list_communities_endpoint = self._getConfOption('B2SHARE_HTTP_API', 'list_communities_endpoint')
        self.records_endpoint = self._getConfOption('B2SHARE_HTTP_API', 'records_endpoint')
        self.access_parameter = self._getConfOption('B2SHARE_HTTP_API', 'access_parameter')
        self.get_community_schema_endpoint = self._getConfOption('B2SHARE_HTTP_API', 'get_community_schema_endpoint')
        
        self.irods_home_dir = self._getConfOption('iRODS', 'irods_home_dir')
        self.irods_debug = self._getConfOption('iRODS', 'irods_debug', True)

    def _getConfOption(self, section, option, boolean=False):
        """
        get the options from the configuration file
        """
        if self.config.has_section(section):
            if (self.config.has_option(section, option)):
                opt = self.config.get(section, option)
                if boolean:
                    if opt in ['True', 'true']:
                        return True
                    else: 
                        return False
                return opt
            else:
                self.logger.error('missing parameter %s: in section %s' % (section, option))
        else: 
            self.logger.error('missing section %s: with parameter %s' % (section, option))
        return None
    