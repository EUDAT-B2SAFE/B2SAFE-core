#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import requests
import json

import os
import logging
import logging.handlers
import argparse
import ConfigParser
import tempfile

from manifest import IRODSUtils
logger = logging.getLogger('create_md_schema')

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
        logger.setLevel(self.log_level[loglevel])
        rfh = logging.handlers.RotatingFileHandler(logfilepath, \
                                                   maxBytes=50000000, \
                                                   backupCount=10)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: '
                                    + '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)
        
        self.b2share_host_name = self._getConfOption('B2SHARE_HTTP_API', 'host_name')
        self.list_communities_endpoint = self._getConfOption('B2SHARE_HTTP_API', 'list_communities_endpoint')
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

def getAllCommunities(configuration):
    #get all community names and print/log them
    #warn the user that the script need community name
    
    
    host = configuration.b2share_host_name
    endpoint = configuration.list_communities_endpoint
    
    acces_part = configuration.access_parameter + "=" + configuration.access_token
    list_communities_url = host + endpoint + acces_part
    
    response = requests.get(url=list_communities_url)
    communities_list = response.json()["hits"]["hits"]
    communities = {}
    for community_object in communities_list:
        name = community_object["name"]
        id = community_object["id"]
        communities[name] = id
    
    return 	communities


def create_md_schema(args):
    commName = args.communityName
    
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    
    #get access_token from collection metadata
    irodsu = IRODSUtils(configuration.irods_home_dir, logger, configuration.irods_debug)
    access_token = irodsu.getMetadata(args.userName, "access_token", '-u')[0]
    configuration.access_token = access_token
    
    communities_list = getAllCommunities(configuration)
    
    if (commName is not None) and (commName != ''):
        logger.info ('Start creating metadata schema for the community'+str(commName))
        
        #get metadata schema
        #api/communities/
        community_id = communities_list[commName]
        host = configuration.b2share_host_name
        community_endpoint = configuration.list_communities_endpoint
        get_schema_endpoint = configuration.get_community_schema_endpoint
        acces_part = configuration.access_parameter + "=" + configuration.access_token
        get_community_schema_url = host + community_endpoint + community_id + get_schema_endpoint + acces_part
        
        response = requests.get(url=get_community_schema_url)
        #May be parsing for manifest extention
        #community_schema = response.json()["json_schema"]["allOf"][0]
        #print(response.json())
        #print(community_schema)
        #then ["properties"] dictianary with all properties objects
        #and ["required"] the list of required ones
        
        
        if args.dryrun:
            print(str(response.text))
        else:
            logger.info('Writing the metadata to a file')
            file_path = args.collectionName + "/" + "b2share_metadata.json" #TODO: config, argument?
            temp = tempfile.NamedTemporaryFile()
            try:
                temp.write(str(response.text))
                temp.flush()
                try: 
                    irodsu.putFile(temp.name, file_path, configuration.irods_resource)
                except:
                    out = irodsu.putFile(temp.name, file_path)
                    print(str(out))
            finally:
                temp.close()      
        
        logger.info ('Finish creating metadata schema for the community'+commName)
    else:
        logger.error("No communityName specified. Please select one of the communities names: " + str(communities_list.keys()))
        print(str(communities_list.keys()))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='B2SAFE B2SHARE client')
    parser.add_argument("--confpath", help="path to the configuration file")
    parser.add_argument("-c", "--communityName", help="B2Share user name")
    
    parser.add_argument("-dbg", "--debug", action="store_true", help="enable debug")
    parser.add_argument("-d", "--dryrun", action="store_true", help="run without performing any real change")
    parser.add_argument("-u", "--userName", help="B2Share user name")
    parser.add_argument("--collectionName", help="path to the collection where to create the metadata")
    
    parser.set_defaults(func=create_md_schema) 
    args = parser.parse_args()
    args.func(args)
