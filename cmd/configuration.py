#!/usr/bin/env python 
# -*- coding: utf-8 -*-

################################################################################
# Configuration Class #
################################################################################
import logging.handlers
import ConfigParser

class Configuration():
    """ 
    Get properties from filesystem
    """

    def __init__(self, conffile, debug, dryrun, logger):
        
        self.conffile = conffile
        self.debug = debug
        self.dryrun = dryrun
        self.logger = logger
        self.access_token = ""
        self.log_level = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, \
                          'ERROR': logging.ERROR, 'WARNING': logging.WARNING, \
                          'CRITICAL': logging.CRITICAL}

    def parseConf(self):
        """Parse the configuration file."""

        self.config = ConfigParser.RawConfigParser()
        with open(self.conffile, "r") as confFile:
            self.config.readfp(confFile)

        logfilepath = self._getConfOption('Logging', 'log_file')
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
        
        self.irods_zone_name = self._getConfOption('iRODS', 'zone_name')
        self.irods_res = self._getConfOption('iRODS', 'resources')
        self.irods_home_dir = self._getConfOption('iRODS', 'irods_home_dir')
        self.irods_debug = self._getConfOption('iRODS', 'irods_debug', True)

    def _getConfOption(self, section, option, boolean=False):
        """
        get the options from the configuration file
        """
        if (self.config.has_option(section, option)):
            opt = self.config.get(section, option)
            if boolean:
                if opt in ['True', 'true']: return True
                else: return False
            return opt
        else:
            self.logger.warning('missing parameter %s:%s' % (section,option))
            return None
    