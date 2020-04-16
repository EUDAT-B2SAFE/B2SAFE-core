#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
# B2SAFE B2SHARE client Command Line Interface                            #
###########################################################################
import argparse
import logging.handlers
import os
import pprint
import requests
import json

from b2shareclient import B2shareClient
from configuration import Configuration
# from irodsUtility import IRODSUtils

logger = logging.getLogger('B2shareClientCLI')

# the methods have return statement only because of unit tests


def draft(args):
    verboseprint = getVerbosePrintMethod(args)
    configuration = getConfigs(verboseprint)
    if not configuration:
        return None

    b2shcl = B2shareClient(configuration)
    filePIDsList = collectPIDsForCollection(configuration)
    if ']' == filePIDsList:
        if configuration.dryrun:
            filePIDsList = "[]"
        verboseprint("ERROR: no files collected for draft.")
        logger.error("ERROR: no files collected for draft.")
    commID = getCommunityIDByName(configuration, verboseprint)
    if not commID:
        verboseprint("NO community_id found for draft creation.")
        logger.error("NO community_id found for draft creation.")
    recordId = None
    if commID and (filePIDsList != ']'):
        recordId = b2shcl.createDraft(commID, filePIDsList)
    if recordId is not None:
        verboseprint("Drafting for record "+recordId+" END.")
        logger.info("Drafting for record "+recordId+" END.")
        if configuration.irodsu:
                configuration.irodsu.setMetadata(configuration.collection_path,
                                                 "EUDAT_B2SHARE_RECORD_ID",
                                                 recordId)
    else:
        verboseprint("Drafting FAILED.")
        logger.error("Drafting FAILED.")
    return recordId


def getCommunityIDByName(configuration, verboseprint):
    community_id = None
    if not configuration:
        return None
    community_name = configuration.community
    if not community_name:
        return None
    host = configuration.b2share_host_name
    endpoint = configuration.list_communities_endpoint
    acces_part = None
    list_communities_url = None
    if configuration.access_parameter and configuration.access_token:
        acces_part = configuration.access_parameter + "=" + \
                        configuration.access_token
    if acces_part and host and endpoint:
        list_communities_url = host + endpoint + acces_part
    if list_communities_url:
        try:
            response = requests.get(url=list_communities_url)
            verboseprint("getCommunityIDByName status code: " +
                         str(response.status_code))
            logger.debug("getCommunityIDByName status code: " +
                         str(response.status_code))
            if (str(response.status_code) == "200"):
                communities_list = response.json()["hits"]["hits"]
                for community_object in communities_list:
                    name = community_object["name"]
                    if community_name == name:
                        community_id = community_object["id"]
            else:
                verboseprint("NO community for name " + community_name +
                             " found: " + str(response.json()))
                logger.error("NO community for name " + community_name +
                             " found: " + str(response.json()))
        except requests.exceptions.RequestException as e:
            logger.error(e)
    return community_id


def getAllCommunities(args):
    verboseprint = getVerbosePrintMethod(args)
    configuration = getConfigs(verboseprint)
    if not configuration:
        verboseprint("configuration missing, abort")
        return None

    b2shcl = B2shareClient(configuration)
    communities = b2shcl.getAllCommunities()
    if communities:
        logger.info("All available communities: \n "+str(communities)+" END.")
        verboseprint("List of communities and their id's: \n" +
                     pprint.pformat(communities))
    else:
        verboseprint("get all communities FAILED")
        logger.error("get all communities FAILED")
    return communities


def collectPIDsForCollection(configuration):
    PIDobjectsString = '['
    res = configuration.irodsu.deepListDir(configuration.collection_path)
    if not res:
        return None
    filePathsMap = None
    if res:
        filePathsMap = collectFilePathsFromTree(res)
    if not filePathsMap:
        return None
    for filePath in filePathsMap.keys():
        filePID = configuration.irodsu.getMetadata(filePath, "PID")
        if filePID:
            # filePath[1:] deletes leading / in a path
            # as requested in issue #112 on GitHub
            PIDobject = '{"key":"'+filePath[1:] + \
                '",'+' "ePIC_PID":"'+filePID[0] + '"}'
            PIDobjectsString = PIDobjectsString + PIDobject + ','
    forLastElemIndex = len(PIDobjectsString) - 1  # delete last comma
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
    verboseprint = getVerbosePrintMethod(args)
    configuration = getConfigs(verboseprint)
    if not configuration:
        return None
    if args.metadata_file_name:
        metadata_file_path = configuration.collection_path + os.sep + \
                             args.metadata_file_name
    else:
         metadata_file_path = configuration.collection_path + os.sep + \
                              "b2share_metadata.json"
    # verboseprint(metadata_file_path)
    metadata_file = configuration.irodsu.getFile(metadata_file_path)
    b2shcl = B2shareClient(configuration)
    b2shcl.addB2shareMetadata(metadata_file)
    verboseprint("Added metadata to draft: " + configuration.record_id)
    logger.info("Added metadata" + configuration.record_id)


def compare(args):
    verboseprint = getVerbosePrintMethod(args)
    configuration = getConfigs(verboseprint)
    if not configuration:
        return None
    if args.coll_metadata_file_name:
        metadata_file_path = configuration.collection_path + os.sep + \
                             args.coll_metadata_file_name
    else:
        metadata_file_path = configuration.collection_path + os.sep + \
                              "b2share_metadata.json"
    metadata_file = configuration.irodsu.getFile(metadata_file_path)
    b2shcl = B2shareClient(configuration)
    b2shcl.compareMD(metadata_file)
    verboseprint("Success. Compare END.")
    logger.info("Compare END.")


def publish(args):
    verboseprint = getVerbosePrintMethod(args)
    configuration = getConfigs(verboseprint)
    if not configuration:
        return None
    b2shcl = B2shareClient(configuration)
    response = b2shcl.publishRecord()
    if response:
        if str(response.status_code) == "200":
            verboseprint("Publishing SUCCESSFUL.")
            logger.info("Publishing SUCCESSFUL. " +
                        str(response.text))
            if configuration.irodsu:
                configuration.irodsu.setMetadata(configuration.collection_path,
                                                 "EUDAT_B2SHARE_PUBLISHED_ID",
                                                 configuration.record_id)
    else:
        verboseprint("Publishing FAILED")
        logger.error("Publishing FAILED")
    logger.info("Publishing END.")


def getAccessTokenWithConfigs(configuration):
    # get access_token from users metadata in iRODS
    if configuration.irodsu:
        users_metadata = \
            configuration.irodsu.getUserMetadata(configuration.user,
                                                 "access_token")
        if users_metadata:
            return users_metadata[0]
        else:
            return None
    else:
        return None


def getCommunitySchema(args):
    verboseprint = getVerbosePrintMethod(args)
    configuration = getConfigs(verboseprint)
    if not configuration:
        return None

    commID = getCommunityIDByName(configuration, verboseprint)
    verboseprint("Get schema for community: " +
                 configuration.community + " with ID: " + commID)
    b2shcl = B2shareClient(configuration)
    schema = b2shcl.getCommunitySchema(commID)
    verboseprint(str(schema))
    verboseprint("Get Community Schema END.")
    logger.info("Get Community Schema END.")
    return schema


def getDraftByID(args):
    logger.info("Get draft by ID ...")
    verboseprint = getVerbosePrintMethod(args)
    configuration = getConfigs(verboseprint)
    if not configuration:
        return None

    b2shcl = B2shareClient(configuration)
    verboseprint("Get draft by ID ...")
    draft = b2shcl.getDraftByID(args.draft_id)
    if draft:
        verboseprint("Request for a draft with id " + draft + " SUCCESSFUL")
        logger.info("Request for a draft with id " + draft + " SUCCESSFUL.")
    logger.info("Get draft by ID END.")
    return draft


def deleteDraft(args):
    verboseprint = getVerbosePrintMethod(args)
    configuration = getConfigs(verboseprint)
    if not configuration:
        return None
    logger.info("DELETING DRAFT: " + args.draft_to_delete_id)
    b2shcl = B2shareClient(configuration)
    if not args.draft_to_delete_id:
        b2shcl.deleteDraft(configuration.record_id)
        verboseprint("DRAFT DELETED: " + configuration.record_id)
    else:
        b2shcl.deleteDraft(args.draft_to_delete_id)
        verboseprint("DRAFT DELETED: " + args.draft_to_delete_id)
    logger.info("DELETING DRAFT END.")


def getVerbosePrintMethod(args):
    if args.verbose:
        def verboseprint(*args):
            for arg in args:
                print(arg)
            return
    else:
        def verboseprint(*args):
            # do-nothing
            return
    return verboseprint


DEFAULT_CONFIG_FILENAME = "b2share_client.json"


def getConfigs(verboseprint):
    config_path = None
    if not args.confpath:
        default_config_path = os.path.dirname(os.getcwd()) + os.sep +\
                              "conf" + os.sep
        config_path = default_config_path + DEFAULT_CONFIG_FILENAME
    else:
        config_path = args.confpath
    if not os.path.exists(config_path):
        print('missing configuration file %s:' % (config_path))
        return None
    configuration = Configuration(logger)
    # verboseprint("config path: " + str(config_path))
    configuration.config_path = config_path
    read_config_error = configuration.loadConfigurarionsFrom(config_path)
    if read_config_error != "":
        print(read_config_error)
        return None
    
    if args.dryrun:
        configuration.dryrun = True
    configuration.user = args.user
    configuration.collection_path = args.collection_path

    if 'title' in args:
        configuration.title = args.title
    if 'community' in args:
        configuration.community = args.community
    if 'community_name' in args:
        configuration.community = args.community_name
    if 'draft_id' in args:
        configuration.record_id = args.draft_id
    if 'publish_id' in args:
        configuration.record_id = args.publish_id
    if 'draft_to_delete_id' in args:
        configuration.record_id = args.draft_to_delete_id
    if 'draft_to_add_md' in args:
        configuration.record_id = args.draft_to_add_md
    if 'draft_id_mdcompare' in args:
        configuration.record_id = args.draft_id_mdcompare

    accessToken = getAccessTokenWithConfigs(configuration)
    if accessToken is None:
        print("\
            No B2SHARE access token found in users meta data.")
        logger.error("\
            No B2SHARE access token found in users meta data.")
        return None
    configuration.access_token = accessToken
    return configuration



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='B2SAFE B2SHARE \
                                     command line client')
    parser.add_argument("--confpath",
                        help="path to the configuration file if not in default /path_to_b2safe/conf/b2share_client.json")
    # parser.add_argument("--irodsenv",
    #                     help="path to irods configuration")
    parser.add_argument("-u", "--user", required=True,
                        help="irods user to get B2SHARE access token")
    parser.add_argument("-p", "--collection_path", required=True,
                        help="irods path to the collection")
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="run without performing any real change")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="enable printouts for debug")

    # Options for the normal publication workflow:
    # create draft,
    # add metadata to it,
    # publish the draft.

    # draft
    subparsers = parser.add_subparsers(help='sub-command help', dest='subcmd')
    parser_draft = subparsers.add_parser('draft',
                                         help='create a draft in B2Share')
    parser_draft.add_argument('-t', '--title', required=True,
                              help='title to publish the draft unter')
    parser_draft.add_argument('-comm', '--community', required=True,
                              help='community to publish the draft unter')
    parser_draft.set_defaults(func=draft)

    # compare meta
    parser_compare_meta = subparsers.add_parser('compare_meta', help='compare \
                                                metadata of the draft \
                                                and collection')
    parser_compare_meta.add_argument('-mdn', '--coll_metadata_file_name',
                                     help='file name of the collection\
                                     describing metadata')
    parser_compare_meta.add_argument('-idc', '--draft_id_mdcompare',
                                     required=True,
                                     help='the b2share id of the record')
    parser_compare_meta.set_defaults(func=compare)

    # extend meta data
    parser_meta = subparsers.add_parser('meta',
                                        help='add metadata to the draft')
    parser_meta.add_argument('-md', '--metadata_file_name',
                             help='file name of the collection describing \
                             metadata')
    parser_meta.add_argument('-rid', '--draft_to_add_md', required=True,
                             help='the b2share id of the record')

    # publish
    parser_meta.set_defaults(func=addMetadata)

    parser_pub = subparsers.add_parser('publish', help='publish the draft')
    parser_pub.add_argument('-pubid', '--publish_id', required=True,
                            help='the b2share id of the record')
    parser_pub.set_defaults(func=publish)

    # extra options for the user to get more information
    # check or delete the draft in case there are errors in it

    # listCommunities
    parser_list_comm = subparsers.add_parser('listCommunities',
                                             help="list all communities " +
                                                  "with their names and id's")
    parser_list_comm.set_defaults(func=getAllCommunities)

    # communitySchema
    parser_commSchema = subparsers.add_parser('communitySchema',
                                              help='get community schema')
    parser_commSchema.add_argument('-comm_name', '--community_name',
                                   required=True, help='community name')
    parser_commSchema.set_defaults(func=getCommunitySchema)

    # getDraft
    parser_getDraft = subparsers.add_parser('getDraft',
                                            help='get draft and if there, ' +
                                            'write it to the log file')
    parser_getDraft.add_argument('-di', '--draft_id', required=True,
                                 help='the b2share id of the record')
    parser_getDraft.set_defaults(func=getDraftByID)

    # deleteDraft
    parser_deleteDraft = subparsers.add_parser('deleteDraft',
                                               help='delete the draft')
    parser_deleteDraft.add_argument('-ddi', '--draft_to_delete_id',
                                    required=True,
                                    help='the b2share id of the record')
    parser_deleteDraft.set_defaults(func=deleteDraft)

    args = parser.parse_args()
    args.func(args)
