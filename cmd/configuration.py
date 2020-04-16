#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging.handlers
import os
from irodsUtility import IRODSUtils


class Configuration():
    def __init__(self, logger):
        self.logger = logger
        self.log_level = {'INFO': logging.INFO,
                          'DEBUG': logging.DEBUG,
                          'ERROR': logging.ERROR,
                          'WARNING': logging.WARNING,
                          'CRITICAL': logging.CRITICAL}
        self.access_token = ""
        self.config_path = ""
        self.record_id = ""
        self.dryrun = None
        self.user = None
        self.collection_path = None
        self.title = None
        self.community = None

    def loadConfigurarionsFrom(self, configuration_file_path):
        with open(configuration_file_path, 'r') as json_file:
            data = json.load(json_file)
            loglevel = data["configurations"]["logging"]["loglevel"]
            self.logger.setLevel(self.log_level[loglevel])
            logfilepath = data["configurations"]["logging"]["logfile"]
            # if logfile does not exist and not possible to create
            # stop execution with ERROR
            if not os.path.exists(logfilepath):
                try:
                    logDir = os.path.dirname(logfilepath)
                    os.mkdir(logDir)
                except OSError:
                    return "Log file directory: " + logfilepath +\
                           "specified in config file: " +\
                           configuration_file_path +\
                           " does NOT exist."
            rfh = logging.handlers.RotatingFileHandler(logfilepath,
                                                       maxBytes=8388608,
                                                       backupCount=9)
            formatter = logging.Formatter('%(asctime)s %(levelname)s: ' +
                                          '[%(funcName)s] %(message)s')
            rfh.setFormatter(formatter)
            self.logger.addHandler(rfh)

            b2share_http_api = data["configurations"]["b2share_http_api"]
            self.b2share_host_name = b2share_http_api["host_name"]
            self.list_communities_endpoint =\
                b2share_http_api["list_communities_endpoint"]
            self.records_endpoint = b2share_http_api["records_endpoint"]
            self.access_parameter = b2share_http_api["access_parameter"]
            self.get_community_schema_endpoint =\
                b2share_http_api["get_community_schema_endpoint"]

            irods = data["configurations"]["irods"]
            self.irodsenv = irods["irods_env"]
            if self.irodsenv:
                self.irodsu = IRODSUtils(self.logger, irods_env=self.irodsenv)
            self.irods_resources = irods["resources"]
            self.irods_home_dir = irods["irods_home_dir"]
            self.irods_debug = irods["irods_debug"]
        return ""