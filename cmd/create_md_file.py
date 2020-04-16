#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import logging.handlers
import argparse
import tempfile
import json

from configuration import Configuration
from irodsUtility import IRODSUtils

logger = logging.getLogger('create_md_schema')


def getAllCommunities(configuration):
    # get all community names and print/log them
    # warn the user that the script need community name

    host = configuration.b2share_host_name
    endpoint = configuration.list_communities_endpoint

    acces_part = configuration.access_parameter + "=" + \
        configuration.access_token
    list_communities_url = host + endpoint + acces_part

    response = requests.get(url=list_communities_url)
    communities_list = response.json()["hits"]["hits"]
    communities = {}
    for community_object in communities_list:
        name = community_object["name"]
        community_id = community_object["id"]
        communities[name] = community_id
    return communities


def getVerbosePrintMethod(args):
    if args.verbouse:
        def verboseprint(*args):
            # Print each argument separately so caller doesn't need to
            # stuff everything to be printed into a single string
            for arg in args:
                print(arg)
            return
    else:
        def verboseprint(*args):
            # do-nothing
            return
    return verboseprint


def getAccessTokenWithConfigs(configuration):
    # get access_token from users metadata in iRODS
    if configuration.irodsu:
        users_metadata = \
            configuration.irodsu.getUserMetadata(
                configuration.user, "access_token")
        if users_metadata:
            return users_metadata[0]
        else:
            return None
    else:
        return None


DEFAULT_CONFIG_FILENAME = "b2share_client.json"


def getConfigs(verboseprint):
    config_path = None
    if not args.confpath:
        config_path = os.path.dirname(os.getcwd()) + os.sep +\
            "conf" + os.sep + DEFAULT_CONFIG_FILENAME
    else:
        config_path = args.confpath
    if not os.path.exists(config_path):
        verboseprint('missing configuration file %s:' % (config_path))
        logger.error('missing configuration file %s:' % (config_path))
        return None
    configuration = Configuration(logger)
    configuration.config_path = config_path
    configuration.loadConfigurarionsFrom(config_path)
    configuration.user = args.user
    configuration.community = args.community
    configuration.collection_path = args.collection_path

    logger.info("Start creating draft ...")
    accessToken = getAccessTokenWithConfigs(configuration)
    if accessToken is None:
        verboseprint("Drafting FAILED. \
            No B2SHARE access token found in users meta data.")
        logger.error(
            "Drafting FAILED. \
            No B2SHARE access token found in users meta data.")
        return None
    configuration.access_token = accessToken
    if 'metadata_file_name' in args:
        configuration.metadata_file_name = args.metadata_file_name
    return configuration


def getCommunitySchema(configuration, verboseprint):
    # get metadata schema
    communities_list = getAllCommunities(configuration)
    if configuration.community not in communities_list.keys():
        logger.error("No communityName specified. " +
                     "Please select and specify " +
                     "one of the communities names: " +
                     str(communities_list.keys()))
        verboseprint("No communityName specified. " +
                     "Please select and specify " +
                     "one of the communities names: " +
                     str(communities_list.keys()))
        return None
    community_id = communities_list[configuration.community]
    host = configuration.b2share_host_name
    community_endpoint = configuration.list_communities_endpoint
    get_schema_endpoint = configuration.get_community_schema_endpoint
    acces_part = \
        configuration.access_parameter + \
        "=" + configuration.access_token
    get_community_schema_url = host + community_endpoint + \
        community_id + get_schema_endpoint + acces_part
    community_schema = None
    try:
        response = requests.get(url=get_community_schema_url)
        verboseprint("response status code: " + str(response.status_code))
        logger.debug("response status code: " + str(response.status_code))
        if ((str(response.status_code) == "200") |
                (str(response.status_code) == "201")):
            community_schema = response.json()["json_schema"]["allOf"][0]
            logger.info("Get schema for community: " + configuration.community)
        else:
            verboseprint("NO schema for community: " +
                         configuration.community +
                         "Response: " + str(response.json()))
            logger.error("NO schema for community: " +
                         configuration.community +
                         "Response: " + str(response.json()))
    except requests.exceptions.RequestException as e:
        logger.error(e)
    return community_schema


def create_md_schema(args):
    verboseprint = getVerbosePrintMethod(args)
    configuration = getConfigs(verboseprint)
    if not configuration:
        return None

    logger.info('Start creating metadata schema for the community' +
                str(configuration.community))
    community_schema = getCommunitySchema(configuration, verboseprint)
    if not community_schema:
        return
    requiredProperties_list = \
        community_schema["b2share"]["presentation"]["major"]
    optionalProperties_list = \
        community_schema["b2share"]["presentation"]["minor"]

    requiredProperties = {}
    for property_name in requiredProperties_list:
        property_type = \
            community_schema["properties"][property_name]["type"]
        requiredProperties[property_name] = property_type
    optionalProperties = {}
    for property_name in optionalProperties_list:
        property_type = \
            community_schema["properties"][property_name]["type"]
        optionalProperties[property_name] = property_type

    mdPatchSceleton = ""
    mdPatchSceleton = mdPatchSceleton + '{"metadata": {"required":['
    for requiredProperty in requiredProperties:
        mdPatchSceleton = mdPatchSceleton + \
            '{"option_name": "' + requiredProperty + '",' \
            '"value":"", ' + \
            '"type":"' + requiredProperties[requiredProperty] +\
            '"},'
    mdPatchSceleton = mdPatchSceleton[:-1]
    mdPatchSceleton = mdPatchSceleton + "],"
    mdPatchSceleton = mdPatchSceleton + '"optional":['
    for optionalPropertiy in optionalProperties.keys():
        mdPatchSceleton = mdPatchSceleton + \
            '{"option_name": "' + optionalPropertiy + '",' \
            '"value":"", ' + \
            '"type":"' + optionalProperties[optionalPropertiy] +\
            '"},'
    mdPatchSceleton = mdPatchSceleton[:-1]
    mdPatchSceleton = mdPatchSceleton + "]"
    mdPatchSceleton = mdPatchSceleton + '} }'

    json_formated = json.dumps(json.loads(mdPatchSceleton), indent=4)
    mdPatchSceleton = json_formated
    if args.dryrun:
        print(mdPatchSceleton)
    else:
        logger.info('Writing the metadata to a file')
        # file_path = configuration.collection_path + os.sep + \
        #     configuration.metadata_file_name
        metadata_file_path = ""
        if configuration.metadata_file_name:
            metadata_file_path = configuration.collection_path + os.sep + \
                                 configuration.metadata_file_name
        else:
            metadata_file_path = configuration.collection_path + os.sep + \
                              "b2share_metadata.json"
        temp = tempfile.NamedTemporaryFile()
        try:
            temp.write(bytes(mdPatchSceleton, 'UTF-8'))
            temp.flush()
            try:
                configuration.irodsu.putFile(temp.name, metadata_file_path)
            except Exception:
                # try again
                out = configuration.irodsu.putFile(temp.name,
                                                   metadata_file_path)
                print(str(out))
        finally:
            temp.close()

    logger.info('Finish creating metadata schema for the community' +
                configuration.community)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Metadata creator')
    parser.add_argument("-u", "--user", required=True,
                        help="irods user to get B2SHARE access token")
    parser.add_argument("-p", "--collection_path", required=True,
                        help="irods path to the collection")
    parser.add_argument('-comm', '--community', required=True,
                        help='community name toget the schema of')
    parser.add_argument("--confpath",
                        help="path to the configuration file")
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="run without performing any real change")
    parser.add_argument("-v", "--verbouse", action="store_true",
                        help="enable printouts for debug")
    parser.add_argument('-md', '--metadata_file_name',
                        help='file name of the collection describing \
                        metadata')
    parser.set_defaults(func=create_md_schema)
    args = parser.parse_args()
    args.func(args)
