#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import json
import requests
import logging.handlers
import argparse
import ConfigParser
import jsonpatch
from manifest import IRODSUtils

logger = logging.getLogger('B2shareClient')

################################################################################
# B2SHARE client #
################################################################################

class B2shareClient():

    def __init__(self, conf):

        self.configuration = conf
        #self.b2share_url = ( conf.b2share_scheme + "://" + conf.b2share_addr + conf.b2share_path)

################################################################################
    def createDraft(self, community_name, title):
        """
        Create a new record, in the draft state.
        """
        if (community_name is None) | (community_name == ''):
            communities_list = self.getAllCommunities()
            logger.error("No communityName specified. Please select one of the communities names: " + str(communities_list.keys()))
            print("No communityName specified. Please select one of the communities names: " + str(communities_list.keys()))
            return None
        
        community_id = self.getCommunityIDByName(community_name)
        record_id = None
        if community_id:
            logger.debug("title: " + str(title) + ", token: " + self.configuration.access_token + ", community: " + str(community_id))
            acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
            create_draft_url = self.configuration.b2share_host_name + self.configuration.records_endpoint + acces_part
            data = '{"titles":[{"title":"' + title + '"}], "community":"' \
                   + community_id + '", "open_access":true, "community_specific": {}}'
            headers = {"Content-Type":"application/json"}
            print(create_draft_url + " : " + str(headers) + " : " + data)
            draft = requests.post(url=create_draft_url, headers=headers, data=data)
            print(str(draft.json()))
            logger.debug("status code: " + str(draft.status_code))
            if (str(draft.status_code) == "200") | (str(draft.status_code) == "201"): 
                record_id = draft.json()['id']
                logger.info("Record created with id: " + record_id) 
                return record_id
        logger.error("No record created: " + str(draft.json()))
        return None
        
    def getCommunityIDByName(self, community_name):
        host = self.configuration.b2share_host_name
        endpoint = self.configuration.list_communities_endpoint
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        list_communities_url = host + endpoint + acces_part
        
        response = requests.get(url=list_communities_url)
        communities_list = response.json()["hits"]["hits"]
        id = None
        for community_object in communities_list:
            name = community_object["name"]
            if community_name == name:
                id = community_object["id"]
        return id

################################################################################
    
    # Get iRODS metadata
    def getB2safeMetadata(self):
        """Get system metadata"""
        return None

    # Patch the draft with extra metadata
    def addB2shareMetadata(self, record_id, communityName, metadata_path, irodsu):
        """
        This action updates the draft record with new information.
        """
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        patch_url = self.configuration.b2share_host_name + self.configuration.records_endpoint + record_id \
                    + "/draft" + acces_part
        
        #NOT WORKING
        # JSON object from community schema
        #src = self.getCommunitySchema(communityName)
        # JSON object from the metadata file = community schema filled by user with data
        #dst = str(irodsu.getFile(metadata_path))
        #NOT WORKING
        
        
        #ONLY FOR TEST, works with empty keywords field
        src = {}
        dst = {'keywords': ["keyword1", "keyword2"]}
        #ONLY FOR TEST
        
        #get draft metadata as src and metadata file as dst
        #src1 = self.getDraftMetadata(record_id)
        #testsrc = src1['keywords']
        #src = {'keywords': src1['keywords']}
        #print(testsrc)
        #dst1 = str(irodsu.getFile(metadata_path))
        
        patch = jsonpatch.make_patch(src, dst)
        #print(patch)
        headers = {"Content-Type": "application/json-patch+json"}
        response = requests.patch(url=patch_url, headers=headers, data=str(patch))
        print(response.text)
    
    def getDraftMetadata(self, record_id):
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        get_draft_metadata = self.configuration.b2share_host_name + self.configuration.records_endpoint + record_id \
                    + "/draft" + acces_part
        
        response = requests.get(url=get_draft_metadata)
        return response.json()["metadata"]
        
    def getCommunitySchema(self, communityName):
        communities_list = self.getAllCommunities()
        community_id = communities_list[communityName]
        community_endpoint = self.configuration.list_communities_endpoint
        get_schema_endpoint = self.configuration.get_community_schema_endpoint
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token		
        get_community_schema_url = self.configuration.b2share_host_name + community_endpoint\
                                   + community_id + get_schema_endpoint + acces_part
        response = requests.get(url=get_community_schema_url)
        return response.text
    
################################################################################   
   # Publish the record
    def publishRecord(self, record_id):
        """Publish a record in B2SHARE"""
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        publish_record_url = self.configuration.b2share_host_name + self.configuration.records_endpoint + record_id \
                             + "/draft" + acces_part
        patch = '[{"op":"add", "path":"/publication_state", "value":"submitted"}]'
        headers = {"Content-Type": "application/json-patch+json"}
        response = requests.patch(url=publish_record_url, headers=headers, data=patch)
        print(response.text)

################################################################################
    
    def addFilesToDraft(self, record_id, collectionPath):
        self.logger.info("addFilesToDraft not possible now")
        #TODO: collect PIDs from files imeta in the colleciton
        #TODO: send the REST request to B2Share with the list of PIDs to update the record with record_id		
    
################################################################################
    #TODO add the function "Search drafts"
    def getDraftByID(self, draft_id):
        logger.info('')
    
    #TODO add the function "delete drafts"
    def deleteDraft(self, draft_id):
        logger.info('')
        
    def getAllCommunities(self):
        host = self.configuration.b2share_host_name
        endpoint = self.configuration.list_communities_endpoint
        
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        list_communities_url = host + endpoint + acces_part
        
        response = requests.get(url=list_communities_url)
        communities_list = response.json()["hits"]["hits"]
        communities = {}
        for community_object in communities_list:
            name = community_object["name"]
            id = community_object["id"]
            communities[name] = id
        
        return 	communities

################################################################################
# Configuration Class #
################################################################################

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
                                                   maxBytes=8388608, \
                                                   backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: '
                                    + '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)

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


################################################################################
# B2SAFE B2SHARE client Command Line Interface                                 #
################################################################################

def draft(args):

    logger.info("Drafting ...")
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    configuration.access_token = getAccessTokenWithConfigs(configuration)
    
    b2shcl = B2shareClient(configuration)
    record_id = b2shcl.createDraft(args.communityName, args.title)
    logger.info("Drafting END")


def addMetadata(args):

    logger.info("Adding metadata ...")
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    irodsu = IRODSUtils(configuration.irods_home_dir, logger, configuration.irods_debug)
    configuration.access_token = irodsu.getMetadata(args.userName, "access_token", '-u')[0]
    
    b2shcl = B2shareClient(configuration)
    #system_metadata = b2shcl.getB2safeMetadata()
    b2shcl.addB2shareMetadata(args.record_id, args.commName, args.metadata, irodsu)
    logger.info("Added metadata")

def addFilePIDsToDraft(args):
    
    logger.info("Adding file names to the draft ...")
    #get files list from collection name specified in args
    files = ''
    
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    configuration.access_token = getAccessTokenWithConfigs(configuration)
    
    #update draft with the files names/path's? list
    #B2Share REST API endpoint needed
    b2shcl = B2shareClient(configuration)
    record_id = b2shcl.addFilesToDraft(files, args.rec_id, args.collectionPath)
    
    logger.info("File names successfully added to draft.")

def publish(args):

    logger.info("Publishing ...")
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    configuration.access_token = getAccessTokenWithConfigs(configuration)
    
    b2shcl = B2shareClient(configuration)
    b2shcl.publishRecord(args.rec_id)        
    logger.info("Published")

def getAccessTokenWithConfigs(configuration):
    #get access_token from users metadata in iRODS
    irodsu = IRODSUtils(configuration.irods_home_dir, logger, configuration.irods_debug)
    access_token = irodsu.getMetadata(args.userName, "access_token", '-u')[0]  #TODO: "access_token" as config variable?
    return access_token

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='B2SAFE B2SHARE client')
    parser.add_argument("--confpath", help="path to the configuration file")
    parser.add_argument("-dbg", "--debug", action="store_true",
                        help="enable debug")
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="run without performing any real change")
    parser.add_argument("-u", "--userName", help="iRODS user name")

    subparsers = parser.add_subparsers(help='sub-command help', dest='subcmd')
    parser_draft = subparsers.add_parser('draft', help='Create a draft record')
    parser_draft.add_argument('-c', '--communityName', required=True, help='B2Share community name')
    parser_draft.add_argument('-ti', '--title', help='title of the record')
    parser_draft.set_defaults(func=draft)

    parser_meta = subparsers.add_parser('meta', help='Add metadata to the draft')
    parser_meta.add_argument('-id', '--record_id', required=True, help='the b2share id of the record')
    parser_meta.add_argument('--commName', required=True, help='B2Share community name')
    parser_meta.add_argument('-md', '--metadata', required=True, help='path to the metadata JSON file of the record')
    parser_meta.set_defaults(func=addMetadata)

    parser_file_pids = subparsers.add_parser('addFilePIDs', help='add file PIDs to the draft')
    parser_file_pids.add_argument('-pi', '--rec_id', required=True, help='the b2share id of the record')
    parser_file_pids.add_argument('-cn', '--collectionPath', required=True, help='path to the collection in iRODS with files')
    parser_file_pids.set_defaults(func=addFilePIDsToDraft)

    parser_pub = subparsers.add_parser('pub', help='publish the draft')
    parser_pub.add_argument('-pi', '--rec_id', required=True, help='the b2share id of the record')
    parser_pub.set_defaults(func=publish)

    args = parser.parse_args()
    args.func(args)

