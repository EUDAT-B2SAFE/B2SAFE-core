#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import json
import requests
import logging.handlers
import argparse
import ConfigParser

logger = logging.getLogger('B2shareClient')

################################################################################
# B2SHARE client #
################################################################################

class B2shareClient():


    def __init__(self, conf, token):

        self.conf = conf
        self.token = token
        self.b2share_url = ( conf.b2share_scheme + "://" + conf.b2share_addr 
                           + conf.b2share_path)


    def createDraft(self, community_id, title):
        """
        Create a new record, in the draft state.
        """
        logger.debug("title: " + str(title) + ", token: " + str(self.token) + ", community: " + str(community_id))
        create_draft_url = self.b2share_url + "records/?access_token=" + self.token
        data = '{"titles":[{"title":"' + title + '"}], "community":"' \
               + community_id + '", "open_access":true, "community_specific": {}}'
        headers = {"Content-Type":"application/json"}

        draft = requests.post(url=create_draft_url, headers=headers, data=data)

        logger.debug("status code: " + str(draft.status_code))

        record_id = draft.json()['id']
        logger.info("Record created with id: " + record_id) 
        return record_id         

# Get iRODS metadata
    def getB2safeMetadata(self):
        """Get system metadata"""
        return None

# Patch the draft with extra metadata
    def addB2shareMetadata(self, record_id, metadata):
        """
        This action updates the draft record with new information.
        """
        patch_url = self.b2share_url + "records/" + record_id \
                  + "/draft?access_token=" + self.token
#TODO translate into jsonpatch: http://jsonpatch.com/
        # metadataJson = toJsonPatch(metadata)
        # patch = '[{"op":"add","path":"/descriptions","value":['
        #       + '{"description":"metadata: '+ str(metadataJson) +'"}]}]'
        #headers = {"Content-Type":"application/json-patch+json"}
        #response = requests.patch(url=patch_url, headers=headers, data=patch)

# Publish the record
    def publishRecord(self, record_id):
        """Publish a record in B2SHARE"""
        patch_url = self.b2share_url + "records/" + record_id \
                  + "/draft?access_token=" + self.token
        patch = '[{"op":"add", "path":"/publication_state", "value":"submitted"}]'
        response = requests.patch(url=patch_url, headers=headers, data=patch)


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

#        self.msg_token = self._getConfOption('MessageSystem', 'token')
#        self.msg_endpoint = self._getConfOption('MessageSystem', 'endpoint')
#        self.msg_buffer = self._getConfOption('MessageSystem', 'buffer')
#        self.msg_subscription = self._getConfOption('MessageSystem', 'subscription')

#        self.irods_zone_name = self._getConfOption('iRODS', 'zone_name')
#        self.irods_zone_ep = self._getConfOption('iRODS', 'zone_ep')
#        self.irods_res = self._getConfOption('iRODS', 'resources')
#        self.irods_home_dir = self._getConfOption('iRODS', 'irods_home_dir')
#        self.irods_debug = self._getConfOption('iRODS', 'irods_debug', True)

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
    configuration.parseConf();

    if (not args.token) or len(args.token) == 0:
#TODO: implement the token management via local DB (iCAT?)
#        token = getTokenFromDB()
        token = ""
    else:
        token = args.token[0]

#TODO: add possibility to get community id from community name
#      using the list of all community.

    b2shcl = B2shareClient(configuration, token)
    record_id = b2shcl.createDraft(args.community_id[0], args.title[0])
    logger.info("Drafting END")


def addMetadata(args):

    logger.info("Adding metadata ...")
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf();

    b2shcl = B2shareClient(configuration, args.token)
    #system_metadata = b2shcl.getB2safeMetadata()
    b2shcl.addB2shareMetadata(self, args.record_id[0], args.metadata[0])
    logger.info("Added metadata")


def publish(args):

    logger.info("Publishing ...")
    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf();

    b2shcl = B2shareClient(configuration, args.token)
    b2shcl.publishRecord(args.rec_id[0])        
    logger.info("Published")

#TODO add the function "Search drafts"

#TODO add the function "Get community schema"

#TODO add the function "List all communities"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='B2SAFE B2SHARE client')
    parser.add_argument("confpath", help="path to the configuration file")
    parser.add_argument("-dbg", "--debug", action="store_true",
                        help="enable debug")
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="run without performing any real change")
    parser.add_argument("-t", "--token", nargs=1, help="user's token")

    subparsers = parser.add_subparsers(help='sub-command help', dest='subcmd')
    parser_draft = subparsers.add_parser('draft', help='Create a draft record')
    parser_draft.add_argument('-i', '--community_id', nargs=1, required=True,
                              help='the b2share id of the community')
    parser_draft.add_argument('-ti', '--title', nargs=1, 
                              help='title of the record')
    parser_draft.set_defaults(func=draft)

    parser_meta = subparsers.add_parser('meta', help='Add metadata to the draft')
    parser_meta.add_argument('-id', '--record_id', nargs=1, required=True,
                              help='the b2share id of the record')
    parser_meta.add_argument('-md', '--metadata', nargs=1,
                              help='metadata of the record')
    parser_meta.set_defaults(func=addMetadata)    

    parser_pub = subparsers.add_parser('pub', help='publish the draft')
    parser_pub.add_argument('-pi', '--rec_id', nargs=1, required=True,
                              help='the b2share id of the record')
    parser_pub.set_defaults(func=publish)

    args = parser.parse_args()
    args.func(args)

