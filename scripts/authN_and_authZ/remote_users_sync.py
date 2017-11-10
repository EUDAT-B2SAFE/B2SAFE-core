#!/usr/bin/env python
# -*- python -*-
# -*- coding: utf-8 -*-

import sys
import argparse
import json
import subprocess
import logging
import logging.handlers
import urllib2
import urllib
from pprint import pformat
import os
import ConfigParser
import ast
import io

from utilities.drivers.eudatunity import *

logger = logging.getLogger('remote.users.sync')

class SyncRemoteUsers:

    def __init__(self):
        """initialize the object"""

        self.logger = logger


    def main(self):
        """
        It synchronizes the remote users accounts with a local json file
        """

        parser = argparse.ArgumentParser(description='Synchronize remote user '
                                                     'accounts to a local json '
                                                     'file.')
        parser.add_argument('-d', '--debug', action='store_true',
                            dest='debug', default=False,
                            help='print debug messages')
        parser.add_argument('conf', default='remote.users.sync.conf',
                            help='path to the configuration file')

        parser.add_argument('role_map', default='role_map.json',
                            help='path to the role map file')

        subparsers = parser.add_subparsers(title='Target group',
                                           help='additional help')
        parser_group = subparsers.add_parser('syncto',
                                             help='the syncronization target')
        parser_group.add_argument('group', help='the target group (or project)')
        parser_group.add_argument('-s', '--subgroups', dest='subgroups',
                                  required=True, help='the target sub-groups')

        _args = parser.parse_args()

        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(open(_args.conf))
        logfilepath = self._getConfOption('Common', 'logfile')
        loglevel = self._getConfOption('Common', 'loglevel')
        self.filepath = self._getConfOption('Common', 'usersfile')
        self.dnsfilepath = self._getConfOption('Common', 'dnsfile')

        main_project = _args.group
        role_map = _args.role_map
        if (_args.subgroups is not None) and (len(_args.subgroups)) > 0:
            subgroups = [n.strip() for n in _args.subgroups.split(",")]
        else:
            subgroups = None

        ll = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, \
              'ERROR': logging.ERROR, 'WARNING': logging.WARNING}
        self.logger.setLevel(ll[loglevel])
        if (_args.debug):
            self.logger.setLevel(logging.DEBUG)

        rfh = logging.handlers.RotatingFileHandler(logfilepath,
                                                   maxBytes=4194304,
                                                   backupCount=1)
        formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
        rfh.setFormatter(formatter)
        self.logger.addHandler(rfh)

        userparam = {k:v for k,v in self.config.items(main_project)}
        data = None
        # Write the json file containing the list of projects, sub-groups and
        # related members
        with open(self.filepath, "w+") as jsonFile:
            if 'type' not in userparam or userparam['type'] != 'attributes':
                data = {main_project: {"groups": {}, "members": []}}
                jsonFile.write(json.dumps(data, indent=2))
        if subgroups:
            for subgroup in (x for x in subgroups \
                             if x not in data[main_project]['groups']):
                if 'ns_prefix' in userparam and userparam['ns_prefix']:
                    data[main_project]['groups'][userparam['ns_prefix']+subgroup] = []
                else:
                    data[main_project]['groups'][subgroup] = []

        userdata = None
        # Write the json file containing the list of distinguished names and users
        with open(self.dnsfilepath, "w+") as jsonFile:
            userdata = {}
            jsonFile.write(json.dumps(userdata,indent=2))

        if (main_project == 'EUDAT'):
            self.logger.info('Syncronizing local json file with eudat user DB...')
            eudatRemoteSource = EudatRemoteSource(main_project, subgroups,
                                                  userparam, role_map, self.logger)
            data = eudatRemoteSource.synchronize_user_db(data)
            userdata = eudatRemoteSource.synchronize_user_attributes(userdata)
        else:
            self.logger.info('Nothing to sync')
            sys.exit(0)

        if data:
            with io.open(self.filepath, 'w', encoding='utf-8') as jsonFile:
                jsonFile.write(json.dumps(data, indent=2, ensure_ascii=False))
            self.logger.info('{0} correctly written!'.format(self.filepath))
        else:
            self.logger.info('No data to write to {0}'.format(self.filepath))

        if userdata:
            with io.open(self.dnsfilepath, 'w', encoding='utf-8') as jsonFile:
                jsonFile.write(json.dumps(userdata, indent=2, ensure_ascii=False))
            self.logger.info('{0} correctly written!'.format(self.dnsfilepath))
        else:
            self.logger.info('No data to write to {0}'.format(self.dnsfilepath))

        sys.exit(0)


    def _getConfOption(self, section, option):
        """
        get the options from the configuration file
        """

        if (self.config.has_option(section, option)):
            return self.config.get(section, option)
        else:
            self.logger.error('missing parameter %s:%s' % (section, option))
            sys.exit(1)


if __name__ == '__main__':
    SyncRemoteUsers().main()
