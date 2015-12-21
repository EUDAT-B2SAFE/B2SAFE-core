#!/usr/bin/env python
# -*- python -*-

import argparse
import logging
import logging.handlers
import json
import pprint
import ConfigParser
import sys

from utilities.irodsUtility import *
from utilities.synchTask import SynchronizationTask

logger = logging.getLogger('UserSync')

################################################################################
# User Accounts Synchronization Class #
################################################################################
 
class UserSync():
    """Class implementing a user synchronization."""


    def __init__(self, conf):
        """Initialize object with configuration parameters."""
        self.conf = conf
        self.irodsu = IRODSUtils(conf.irods_home_dir, 'UserSync', 
                                 conf.irods_debug)


    def _parseDNMap(self):
        """Internal: Parse the distinguished name map file."""
        
        try:
            filehandle = open(self.conf.dn_map_file, "r")
            dns_map = json.load(filehandle)
            filehandle.close()
        except Exception, e:
            logger.warning("problem while reading dn map file %s", 
                           self.conf.dn_map_file)
            logger.warning("Error: %s", e)
            dns_map = None
            
        return dns_map


    def _parseExternal(self, file_path):
        """Internal: Parse the external users file."""

        try:
            filehandle = open(file_path, "r")
            projects_external = json.load(filehandle)
            filehandle.close()
        except Exception, e:
            logger.warning("problem while reading file %s", file_path)
            logger.warning("Error: %s", e)
            projects_external = None

        return projects_external


    def _parseIrodsProj(self):
        """Internal: Parse the projects irods info."""

        irods_zones = self.irodsu.getIrodsZones()
        out = self.irodsu.listIrodsGroups() 
        groups = {}
        for line in out.splitlines():
            group = {}
            out2 = self.irodsu.getIrodsGroup(line)
            group['members'] = []
            # add member list to each group, if the zone is remote, it is kept, otherwise it is dropped
            for row in out2.splitlines()[1:]:
                if row.find('#')>0:
                    [member,zone] = row.split('#')
                    if (irods_zones 
                        and irods_zones[zone]['zone_type'] == 'local'):
                        group['members'].append(member)
                    else:
                        group['members'].append(row)
            groups[line] = group

        return groups


    def _parseIrodsUser(self):
        """Internal: Parse the users irods info."""

        irods_zones = self.irodsu.getIrodsZones()
        out = self.irodsu.listIrodsUsers()
        users = {}
        if out:
            for line in out.splitlines():
                user = {}
                [member,zone] = line.split('#')
                if (irods_zones and irods_zones[zone]['zone_type'] == 'local'):
                    key = member
                else:
                    key = line
                users[key] = user
 
        return users

    
    def _merge_dicts(self, *dicts):
        """merges dictionaries"""

        if not reduce(lambda x, y: isinstance(y, dict) and x, dicts, True):
            raise TypeError, "Object in *dicts not of type dict"
        if len(dicts) < 2:
            raise ValueError, "Requires 2 or more dict objects"

        def merge(a, b):
            for d in set(a.keys()).union(b.keys()):
                if d in a and d in b:
                    if type(a[d]) == type(b[d]):
                        if not isinstance(a[d], dict):
                            if isinstance(a[d], list):
                                ret = sorted(set(a[d] + b[d]))
                            else:
                                # here it resolves a conflict creating a list
                                ret = list({a[d], b[d]})
                                if len(ret) == 1:
                                    ret = ret[0]
                            yield (d, ret)
                        else:
                            yield (d, dict(merge(a[d], b[d])))
                    else:
                        raise TypeError, "Conflicting key:value type assignment"
                elif d in a:
                    yield (d, a[d])
                elif d in b:
                    yield (d, b[d])
                else:
                    raise KeyError

        return reduce(lambda x, y: dict(merge(x, y)), dicts[1:], dicts[0])
 
    # Public methods
 
    def synchronize(self, dryrun):
        """Synchronize user/project accounts.
        
        Parameters:
        Returns True if successful.
        
        """
        irods_users = self._parseIrodsUser()
        irods_projects = self._parseIrodsProj()
        local_projects = self._parseExternal(self.conf.project_file)
        remote_projects = self._parseExternal(self.conf.external_file)
        dn_map = self._parseDNMap()

        # if log level is equal to DEBUG (level 10)
        if (logger.getEffectiveLevel() == 10):
            pp = pprint.PrettyPrinter(indent=4)
            print("###### irods users ######")
            pp.pprint(irods_users)
            print("###### irods groups ######")
            pp.pprint(irods_projects)
            print("### groups/projects imported from a local source ###")
            pp.pprint(local_projects)
            print("### groups/projects imported from a remote source ###")
            pp.pprint(remote_projects)
            print("### DNs imported from a remote source ###")
            pp.pprint(dn_map)
            
        if not self.conf.local_authoritative:
            logger.debug("local source is not authoritative")
            if local_projects is None:
                if remote_projects is None: projects = {}
                else: projects = remote_projects
            else:
                if remote_projects is None:
                    projects = local_projects
                else:
                    projects = self._merge_dicts(local_projects,remote_projects)
        else:
            logger.debug("local source is authoritative")
            if local_projects is None: projects = {}
            else: 
                merged_projects = self._merge_dicts(local_projects, 
                                                   remote_projects)
                projects = {key: merged_projects[key] 
                            for key in local_projects.keys()}

        sync_task = SynchronizationTask( irods_users, irods_projects, projects,
                                         dn_map, self.conf, dryrun, 'UserSync',
                                         self.conf.irods_debug)
        sync_task.addProjects()
        sync_task.updateProjects()
        sync_task.deleteProjects()
        sync_task.updateUsers()

#       TODO: manage properly return value
        return True


################################################################################
# Configuration Class #
################################################################################
 
class Configuration():
    """ 
    Get properties from filesystem
    """

    def __init__(self, file, logger):
   
        self.file = file
        self.logger = logger
        self.log_level = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, \
                          'ERROR': logging.ERROR, 'WARNING': logging.WARNING, \
                          'CRITICAL': logging.CRITICAL}

    def parseConf(self):
        """Parse the configuration file."""

        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(open(self.file))
        
        logfilepath = self._getConfOption('Logging', 'log_file')
        loglevel = self._getConfOption('Logging', 'log_level')
        logger.setLevel(self.log_level[loglevel])
        rfh = logging.handlers.RotatingFileHandler(logfilepath, \
                                                   maxBytes=8388608, \
                                                   backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: '
                                    + '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)
        
        self.notification_active = self._getConfOption('Notification', 
                                                       'notification_active',
                                                       True)
        self.notification_sender = self._getConfOption('Notification', 
                                                       'notification_sender')
        self.notification_receiver = self._getConfOption('Notification', 
                                                         'notification_receiver')

        self.project_file = self._getConfOption('Sources', 'project_file')
        self.external_file = self._getConfOption('Sources', 'external_file')
        self.dn_map_file = self._getConfOption('Sources', 'dn_map_file')
        self.local_authoritative = self._getConfOption('Sources', 
                                                       'local_authoritative',
                                                       True)
        self.condition = self._getConfOption('Sources', 'condition')

        self.quota_file = self._getConfOption('Quota', 'quota_file')
        self.quota_active = self._getConfOption('Quota', 'quota_active', True)
        self.quota_attribute = self._getConfOption('Quota', 'quota_attribute')
        self.quota_unity = self._getConfOption('Quota', 'quota_unity')

        self.gridftp_active = self._getConfOption('GridFTP', 'gridftp_active', True)
        self.gridmapfile = self._getConfOption('GridFTP', 'gridmapfile')
        self.gridftp_server_dn = self._getConfOption('GridFTP', 'gridftp_server_dn')

        self.internal_project_list = \
            self._getConfOption('iRODS', 'internal_project_list').split(',')
        self.irods_home_dir = self._getConfOption('iRODS', 'irods_home_dir')
        self.irods_subgroup_home = self._getConfOption('iRODS', 'irods_subgroup_home', True)
        self.irods_group_home = self._getConfOption('iRODS', 'irods_group_home', True)
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
# B2SAFE User Synchronization Tool Command Line Interface #
################################################################################

def sync(args):

    configuration = Configuration(args.confpath, logger)
    configuration.parseConf();
    us = UserSync(configuration)
     
    logger.info("Users/projects sync starting ...")
    us.synchronize(args.dryrun)
    logger.info("Users/projects sync completed")

    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='B2SAFE user sinchronization tool')
    parser.add_argument("confpath",default="NULL",help="path to the configuration file")
    parser.add_argument("-d", "--dryrun", action="store_true",\
        help="execute a command without performing any real change")

    subparsers = parser.add_subparsers(title='Actions',description='synchronization actions', \
        help='additional help')

    parser_sync = subparsers.add_parser('sync', help='synchronize file based user info with iRODS')
    parser_sync.set_defaults(func=sync) 

    args = parser.parse_args()
    args.func(args)
