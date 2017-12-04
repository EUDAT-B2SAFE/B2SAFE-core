#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import os
import pprint
import json
import simplejson
import requests
import logging.handlers
import argparse
import ConfigParser
import jsonpatch
from manifest import IRODSUtils
#from pyxb.binding.basis import element

logger = logging.getLogger('B2shareClient')

################################################################################
# B2SHARE client #
################################################################################

class B2shareClient():

    def __init__(self, conf):

        self.configuration = conf
        #self.b2share_url = ( conf.b2share_scheme + "://" + conf.b2share_addr + conf.b2share_path)
    
    def createDraft(self, community_id, title, filePIDsList):
        """
        Create a new record, in the draft state.
        """
        record_id = None
        if community_id:
            logger.debug("title: " + str(title) + ", token: " + self.configuration.access_token + ", community: " + str(community_id))
            acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
            create_draft_url = self.configuration.b2share_host_name + self.configuration.records_endpoint + acces_part
            # For the new B2SHARE API
            # data = '{"titles":[{"title":"' + title + '"}], ' + \
            #       '"community":"' + community_id + '", ' + \
            #       '"file_pids:"' + filePIDsList + '", ' + \
            #       '"open_access":true, "community_specific": {}}'
            data = '{"titles":[{"title":"' + title + '"}], ' + \
                   '"community":"' + community_id + '", ' + \
                   '"open_access":true, "community_specific": {}}'
            headers = {"Content-Type":"application/json"}
            
            draft = requests.post(url=create_draft_url, headers=headers, data=data)
            logger.debug("status code: " + str(draft.status_code))
            if (str(draft.status_code) == "200") | (str(draft.status_code) == "201"): 
                record_id = draft.json()['id']
                logger.info("Record created with id: " + record_id) 
                return record_id
        logger.error("No record created: " + str(draft.json()))
        return None
    
    # Get iRODS metadata
    def getB2safeMetadata(self):
        """Get system metadata"""
        return None

    # Patch the draft with extra metadata
    def addB2shareMetadata(self, record_id, metadata_path, irodsu):
        """
        This action updates the draft record with new information.
        """
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        patch_url = self.configuration.b2share_host_name + self.configuration.records_endpoint + record_id \
                    + "/draft" + acces_part
        
        
        # JSON object from the metadata file = community schema filled by user with data
        metadata_lines = irodsu.getFile(metadata_path).split('\n\n')
        draft_metadata = self.getDraftMetadata(record_id)
        src = {}
        dst = {}
        for line in metadata_lines[1:]:
            line_content = line.split('\n')
            if len(line_content) == 2:
                option_name = line_content[0]
                if option_name == 'community' or option_name == '':
                    logger.info("ignore the value for the 'community' as it's immutable and empty lines from meta data file")
                else:
                    if option_name in draft_metadata.keys():
                        # src[option_name] = draft_metadata[option_name]
                        src[option_name] = ''
                    value = line_content[1]
                    if value.startswith('['):
                        value = value.replace('[','').replace(']','')
                        values_array = []
                        if value.startswith('{') :
                            if '},' in value:
                                #many objects in array
                                delimiter = '}'
                                arr = value.split(delimiter)
                                values_array.append(arr[0]+'}')
                                for elem in value.split(delimiter)[1:]:
                                    values_array.append(elem[1:].strip()+'}')
                            else:
                                #one element in array
                                values_array.append(value)
                        else:
                            values_array = value.split(',')
                        array_of_objects = []
                        for array_element in values_array:
                            if '{' in array_element:
                                array_of_objects.append(self.valueToObject(array_element))
                        if array_of_objects:
                            values_array = array_of_objects
                        dst[option_name] = values_array
                    else:
                        if value.startswith('{'):
                            #object
                            value = self.valueToObject(value)
                        else:
                            #string
                            if value.lower() == "true":
                                value = True
                            else: 
                                if value.lower() == "false":
                                    value = False
                        dst[option_name] = value
        
        patch = jsonpatch.make_patch(src, dst)
        headers = {"Content-Type": "application/json-patch+json"}
        response = requests.patch(url=patch_url, headers=headers, data=str(patch))
        logger.debug("responce: " + str(response.text))
        
    def valueToObject(self, value):
        v = json.loads(value)
        return v
    
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
        logger.debug("responce: " + str(response.text))
        
################################################################################
    #TODO add the function "Search drafts"
    def getDraftByID(self, draft_id):
        logger.info('')
    
    #TODO add the function "delete drafts"
    def deleteDraft(self, draft_id):
        logger.info('')

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
            logger.warning('missing parameter %s:%s' % (section,option))
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
    filePIDsList = collectPIDsForCollection(args.collectionPath, configuration)
    if args.communityID:
        record_id = b2shcl.createDraft(args.communityID, args.title, filePIDsList)
    else:
        commID = getCommunityIDByName(configuration, args.communityName)
        record_id = b2shcl.createDraft(commID, args.title, filePIDsList)
    if record_id is not None:
        logger.info("Drafting for record"+record_id+"END")
    else:
        logger.error("Drafting FAILED")

def getCommunityIDByName(configuration, community_name):
    host = configuration.b2share_host_name
    endpoint = configuration.list_communities_endpoint
    acces_part = configuration.access_parameter + "=" + configuration.access_token
    list_communities_url = host + endpoint + acces_part
    
    response = requests.get(url=list_communities_url)
    communities_list = response.json()["hits"]["hits"]
    community_id = None
    for community_object in communities_list:
        name = community_object["name"]
        if community_name == name:
            community_id = community_object["id"]
    return community_id

def getAllCommunities(args):
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    configuration.access_token = getAccessTokenWithConfigs(configuration)
    
    host = configuration.b2share_host_name
    endpoint = configuration.list_communities_endpoint
    
    acces_part = configuration.access_parameter + "=" + configuration.access_token
    list_communities_url = host + endpoint + acces_part
    
    response = requests.get(url=list_communities_url)
    communities_list = response.json()["hits"]["hits"]
    communities = {}
    for community_object in communities_list:
        name = community_object["name"]
        community_id = community_object["id"]
        communities[name] = community_id
    print("List of communities and their id's: \n"+ pprint.pformat(communities))

def collectPIDsForCollection(collectionPath, configuration):
    PIDobjects = []
    irodsu = IRODSUtils(configuration.irods_home_dir, logger, configuration.irods_debug)
    rc, res = irodsu.deepListDir(collectionPath)
    if res:
        filePathsMap = collectFilePathsFromTree(res)
    for filePath in filePathsMap.keys():
        print(filePath)
        filePID = irodsu.getMetadata(filePath, "PID")
        print(str(filePID))
        if filePID : 
            pidObject = '{"'+filePath+'":"'+filePID[0]+'"}'
            PIDobjects.append(pidObject)
    return PIDobjects

def collectFilePathsFromTree(filesTree):
    filePaths = {}
    for coll in filesTree:
        for fp in filesTree[coll]['__files__']:
            # loop over the files of the collection
            if ":" in fp:
                fp = fp.replace(":", "___")
            filePaths[coll + os.sep + fp] = fp
        if len(filesTree[coll]) > 1:
                # there are also subdirs
                del filesTree[coll]['__files__']
                fm = collectFilePathsFromTree(filesTree[coll])
                # merge the map dictionaries
                temp = fm.copy()
                temp.update(filePaths)
                filePaths = temp  
    return filePaths

def addMetadata(args):
    logger.info("Adding metadata ...")
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    irodsu = IRODSUtils(configuration.irods_home_dir, logger, configuration.irods_debug)
    configuration.access_token = irodsu.getMetadata(args.userName, "access_token", '-u')[0]
    
    b2shcl = B2shareClient(configuration)
    b2shcl.addB2shareMetadata(args.record_id, args.metadata, irodsu)
    logger.info("Added metadata")

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
    access_token = irodsu.getMetadata(args.userName, "access_token", '-u')[0]
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
    
    parser_list_comm = subparsers.add_parser('listCommunities', help="List all communities with their names and id's")
    parser_list_comm.set_defaults(func=getAllCommunities)
    
    parser_draft = subparsers.add_parser('draft', help='Create a draft record')
    input_group = parser_draft.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-c", "--communityName", help="B2Share community name")
    input_group.add_argument("-i", "--communityID", help="B2Share community id")
    parser_draft.add_argument('-ti', '--title', help='title of the record')
    parser_draft.add_argument('-cp', '--collectionPath', required=True, help='path to the collection in iRODS with files')
    parser_draft.set_defaults(func=draft)

    parser_meta = subparsers.add_parser('meta', help='Add metadata to the draft')
    parser_meta.add_argument('-id', '--record_id', required=True, help='the b2share id of the record')
    input_group = parser_meta.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-cn", "--commName", help="B2Share community name")
    input_group.add_argument("-ci", "--commID", help="B2Share community id")
    parser_meta.add_argument('-md', '--metadata', required=True, help='path to the metadata JSON file of the record')
    parser_meta.set_defaults(func=addMetadata)

    parser_pub = subparsers.add_parser('pub', help='publish the draft')
    parser_pub.add_argument('-pi', '--rec_id', required=True, help='the b2share id of the record')
    parser_pub.set_defaults(func=publish)

    args = parser.parse_args()
    args.func(args)
