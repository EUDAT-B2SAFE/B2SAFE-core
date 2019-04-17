#!/usr/bin/env python 
# -*- coding: utf-8 -*-

################################################################################
# B2SAFE B2SHARE client Command Line Interface                                 #
################################################################################
import argparse
import logging.handlers
import os
import pprint
import requests

from b2shareclient import B2shareClient
from configuration import Configuration
from manifest import IRODSUtils


logger = logging.getLogger('B2shareClientCLI')

def draft(args):
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    logger.info("Start creating draft ...")
    accessToken = getAccessTokenWithConfigs(configuration, args)
    if accessToken is None:
        logger.error("Drafting FAILED. No B2SHARE access token found in users meta data.")
        return None
    configuration.access_token = accessToken
    
    b2shcl = B2shareClient(configuration)
    filePIDsList = collectPIDsForCollection(args.collectionPath, configuration)
    commID = args.communityID
    if args.communityID is None:
        commID = getCommunityIDByName(configuration, args.communityName)
    recordId = None
    if commID and filePIDsList:
        recordId = b2shcl.createDraft(commID, args.title, filePIDsList)
    if recordId is not None:
        logger.info("Drafting for record "+recordId+" END.")
    else:
        logger.error("Drafting FAILED.")
    return recordId

def getCommunityIDByName(configuration, community_name):
    community_id = None
    if not configuration:
        return community_id
    if not community_name:
        return community_id
    host = configuration.b2share_host_name
    endpoint = configuration.list_communities_endpoint
    acces_part = None
    list_communities_url = None
    if configuration.access_parameter and configuration.access_token:
        acces_part = configuration.access_parameter + "=" + configuration.access_token
    if acces_part and host and endpoint:
        list_communities_url = host + endpoint + acces_part
    if list_communities_url:
        try:
            #TODO: delete 'verify=False', if B2SHARE server has proper certificate
            response = requests.get(url=list_communities_url, verify=False)
            print(list_communities_url)
            logger.debug("status code: " + str(response.status_code))
            if (str(response.status_code) == "200"): 
                communities_list = response.json()["hits"]["hits"]
                for community_object in communities_list:
                    name = community_object["name"]
                    if community_name == name:
                        community_id = community_object["id"]
            else:
                logger.error("NO community found: " + str(response.json()))
        except requests.exceptions.RequestException as e:
            logger.error(e)
    return community_id

def getAllCommunities(args):
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    logger.info("Start get all communities ...")
    accessToken = getAccessTokenWithConfigs(configuration, args)
    if accessToken is None:
        logger.error("Drafting FAILED. No B2SHARE access token found in users meta data.")
        return None
    configuration.access_token = accessToken
    
    b2shcl = B2shareClient(configuration)
    communities = b2shcl.getAllCommunities()
    if communities:
        logger.info("All available communities: \n "+str(communities)+" END.")
        print("List of communities and their id's: \n"+ pprint.pformat(communities))
    else:
        logger.error("get all communities FAILED.")
    return communities

def collectPIDsForCollection(collectionPath, configuration):
    PIDobjectsString = '['
    irodsu = IRODSUtils(configuration.irods_home_dir, logger,
                        configuration.irods_debug,
                        irods_env=configuration.irodsenv)
    rc, res = irodsu.deepListDir(collectionPath)
    if not res:
        return None
    filePathsMap = None
    if res:
        filePathsMap = collectFilePathsFromTree(res)
    if not filePathsMap:
        return None
    for filePath in filePathsMap.keys():
        filePID = irodsu.getMetadata(filePath, "PID")
        if filePID : 
            # filePath[1:] deletes leading / in a path as requested in issue #112 on GitHub
            PIDobject = '{"key":"'+filePath[1:]+'",'+' "ePIC_PID":"'+filePID[0] +'"}'
            PIDobjectsString = PIDobjectsString + PIDobject +','
    forLastElemIndex = len(PIDobjectsString) - 1 #delete last comma
    PIDobjectsString = PIDobjectsString[:forLastElemIndex] + ']'
    return PIDobjectsString

def collectFilePathsFromTree(filesTree):
    filePaths = {}
    for coll in filesTree:
        for fp in filesTree[coll]['__files__']:
            # loop over the files of the collection
            filePaths[coll + os.sep + fp] = fp
        if len(filesTree[coll]) > 1:
                # there are also subdirs
                del filesTree[coll]['__files__']
                filemap = collectFilePathsFromTree(filesTree[coll])
                # merge the map dictionaries
                temp = filemap.copy()
                temp.update(filePaths)
                filePaths = temp  
    return filePaths

def addMetadata(args):
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    logger.info("Adding metadata ...")
    accessToken = getAccessTokenWithConfigs(configuration, args)
    if accessToken is None:
        logger.error("Adding metadata FAILED. No B2SHARE access token found in users meta data.")
        return None
    
    configuration.access_token = accessToken
    
    irodsu = IRODSUtils(configuration.irods_home_dir, logger,
                        configuration.irods_debug,
                        irods_env=configuration.irodsenv)
    metadata_file = irodsu.getFile(args.metadata)
    b2shcl = B2shareClient(configuration)
    b2shcl.addB2shareMetadata(args.record_id, metadata_file)
    logger.info("Added metadata")

def publish(args):
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    logger.info("Publishing ...")
    accessToken = getAccessTokenWithConfigs(configuration, args)
    if not accessToken:
        logger.error("Publishing FAILED. No B2SHARE access token found in users meta data.")
        return None
    configuration.access_token = accessToken
    
    b2shcl = B2shareClient(configuration)
    b2shcl.publishRecord(args.rec_id)
    logger.info("Publishing END.")

#get access_token from users metadata in iRODS
def getAccessTokenWithConfigs(configuration, args):
    irodsu = IRODSUtils(configuration.irods_home_dir, logger,
                        configuration.irods_debug,
                        irods_env=configuration.irodsenv)
    if irodsu:
        users_metadata = irodsu.getMetadata(args.userName, "access_token", '-u')
        if users_metadata:
            return users_metadata[0]
        else:
            return None
    else:
        return None

def getCommunitySchema(args):
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    logger.info("Get Community Schema ...")
    accessToken = getAccessTokenWithConfigs(configuration, args)
    if not accessToken:
        logger.error("Get Community Schema FAILED. No B2SHARE access token found in users meta data.")
        return None
    configuration.access_token = accessToken
    
    commID = args.commID
    if commID is None:
        commID = getCommunityIDByName(configuration, args.commName)
    
    b2shcl = B2shareClient(configuration)
    schema = b2shcl.getCommunitySchema(commID)
    logger.info(str(schema))
    logger.info("Get Community Schema END.")
    return schema
        
def getDraftByID(args):
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    logger.info("Get draft by ID ...")
    accessToken = getAccessTokenWithConfigs(configuration, args)
    if not accessToken:
        logger.error("Get draft by ID FAILED. No B2SHARE access token found in users meta data.")
        return None
    configuration.access_token = accessToken
    
    b2shcl = B2shareClient(configuration)
    draft = b2shcl.getDraftByID(args.draft_id)
    if draft:
        logger.info("Request for a draft with id " + draft + " SUCCESSFUL.")  
    logger.info("Get draft by ID END.")
    return draft

def deleteDraft(args):
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf()
    logger.info("DELETING DRAFT: " + args.draft_to_delete_id)
    accessToken = getAccessTokenWithConfigs(configuration, args)
    if not accessToken:
        logger.error("DELETING DRAFT FAILED. No B2SHARE access token found in users meta data.")
        return None
    configuration.access_token = accessToken
    
    b2shcl = B2shareClient(configuration)
    b2shcl.deleteDraft(args.draft_to_delete_id)     
    logger.info("DELETING DRAFT END.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='B2SAFE B2SHARE client')
    parser.add_argument("--confpath", help="path to the configuration file")
    parser.add_argument("-dbg", "--debug", action="store_true",
                        help="enable debug")
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="run without performing any real change")
    parser.add_argument("-u", "--userName", help="iRODS user name")
    parser.add_argument("--irodenv", help="Path to irods configuration")
    subparsers = parser.add_subparsers(help='sub-command help', dest='subcmd')
    
    parser_draft = subparsers.add_parser('draft', help='create a draft record in B2Share')
    comm_group = parser_draft.add_mutually_exclusive_group(required=True)
    comm_group.add_argument("-c", "--communityName", help="B2Share community name")
    comm_group.add_argument("-i", "--communityID", help="B2Share community id")
    parser_draft.add_argument('-ti', '--title', help='title of the record')
    parser_draft.add_argument('-cp', '--collectionPath', required=True, help='path to the collection in iRODS with files')
    parser_draft.set_defaults(func=draft)

    parser_meta = subparsers.add_parser('meta', help='add metadata to the draft')
    parser_meta.add_argument('-id', '--record_id', required=True, help='the b2share id of the record')
    parser_meta.add_argument('-md', '--metadata', required=True, help='path to the metadata JSON file of the record')
    parser_meta.set_defaults(func=addMetadata)

    parser_pub = subparsers.add_parser('pub', help='publish the draft')
    parser_pub.add_argument('-pi', '--rec_id', required=True, help='the b2share id of the record')
    parser_pub.set_defaults(func=publish)
    
    parser_list_comm = subparsers.add_parser('listCommunities', help="list all communities with their names and id's")
    parser_list_comm.set_defaults(func=getAllCommunities)
    
    parser_commSchema = subparsers.add_parser('communitySchema', help='get community schema')
    input_group = parser_commSchema.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-cn", "--commName", help="B2Share community name")
    input_group.add_argument("-ci", "--commID", help="B2Share community id")
    parser_commSchema.set_defaults(func=getCommunitySchema)
    
    parser_getDraft = subparsers.add_parser('getDraft', help='get draft and if there write it to the log file')
    parser_getDraft.add_argument('-di', '--draft_id', required=True, help='the b2share id of the record')
    parser_getDraft.set_defaults(func=getDraftByID)
    
    parser_deleteDraft = subparsers.add_parser('deleteDraft', help='delete the draft')
    parser_deleteDraft.add_argument('-ddi', '--draft_to_delete_id', required=True, help='the b2share id of the record')
    parser_deleteDraft.set_defaults(func=deleteDraft)

    args = parser.parse_args()
    args.func(args)
