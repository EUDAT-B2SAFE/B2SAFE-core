#!/usr/bin/env python

import argparse
import subprocess
import re
import logging
import logging.handlers
import json
import pprint
import ConfigParser
import sys
import collections

from utilities.mailSender import MailSender
from utilities.filters import Filters
from utilities.jsonUtility import *
from utilities.irodsUtility import *

logger = logging.getLogger('UserSync')

################################################################################
# User Accounts Synchronization Class #
################################################################################
 
class UserSync():
    """Class implementing a user synchronization."""


    def __init__(self, conf):
        """Initialize object with configuration parameters."""
        self.conf = conf
        self.irodsu = IRODSUtils(conf.irods_admin_user, conf.irods_home_dir,
                                 'UserSync', conf.irods_debug)


    def _parseExternal(self, file_path):
        """Internal: Parse the external users file."""

        try:
            filehandle = open(file_path, "r")
            projects_external = json.load(filehandle, 
                                          object_hook=JSONUtils().decode_dict)
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
            # add member list to each group, if the zone is remote, it is kept,
            # otherwise it is dropped
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
            
        if not self.conf.local_authoritative:
            logger.debug("[synchronize] local source is not authoritative")
            if local_projects is None:
                if remote_projects is None: projects = {}
                else: projects = remote_projects
            else:
                if remote_projects is None:
                    projects = local_projects
                else:
                    projects = self._merge_dicts(local_projects,remote_projects)
        else:
            logger.debug("[synchronize] local source is authoritative")
            if local_projects is None: projects = {}
            else: 
                merged_projects = self._merge_dicts(local_projects, 
                                                   remote_projects)
                projects = {key: merged_projects[key] 
                            for key in local_projects.keys()}

        sync_task = SyncronizationTask( irods_users, irods_projects, projects,
                                        self.conf, dryrun)
        sync_task.addProjects()
        sync_task.updateProjects()
        sync_task.deleteProjects()
        sync_task.updateUsers()

#       TODO: manage properly return value
        return True

##############################################################################
# Synchronization Task Class #
# input:
#       irods_users: { 'user1': {user1_attr1, user1_attr2},
#                      'user2': {user2_attr1, user2_attr2}
#                    }
#       irods_projects: { 'irods_group1': {'members': ['user1, user2']},
#                         'irods_group2': {'members': ['user1, user2']}
#                       }
#       file_projects: { 'main_group1': { 'PI': 'user1',
#                                         'groups': { 'group1': ['user8',
#                                                                'user6'],
#                                                     'group2': ['user1']
#                                                   },
#                                         'members': ['user1, user2']
#                      }
#       externals: { 'main_group1': { 'PI': 'user1',
#                                     'groups': { 'group1': ['user8',
#                                                            'user6'],
#                                                 'group2': ['user1']
#                                               },
#                                     'members': ['user1, user2']
#                  }
##############################################################################

class SyncronizationTask():
    """
    perform syncronization operations
    """

    def __init__(self, irods_users, irods_projects, projects,
                 conf, dryrun):
        """Initialize object."""
    
        self.irods_users = irods_users
        self.irods_projects = irods_projects
        self.projects = projects
        self.conf = conf
        self.dryrun = dryrun
        self.irodsu = IRODSUtils(conf.irods_admin_user, conf.irods_home_dir, 
                                 'UserSync', conf.irods_debug)


    def _getSubGroupsList(self):
        """Internal: get the list of projects per subgroup"""

        sg_list = {}
        for proj_name in self.projects.keys():
            for sg in self.projects[proj_name]['groups'].keys():
                sg_list[sg] = proj_name

        return sg_list


    def _addSubGroups(self, proj_name, project):
        """Internal: create sub-groups and add users to them"""

        newGroupFlag = False
        logger.info("adding sub-groups to the project %s", proj_name)
                        
#        if (logger.getEffectiveLevel() == 10):
#            pp = pprint.PrettyPrinter(indent=4)
#            pp.pprint(projects)
            
        if 'groups' in project.keys():
            for sg in project['groups'].keys():
                newGroupFlag = False
                if not(sg in self.irods_projects.keys()):
                    if not(self.dryrun):
                        newGroupFlag = self.irodsu.createIrodsGroup(sg)
                        logger.info("created group %s related to the project %s",
                                    sg, proj_name)
                        self.irodsu.deleteGroupHome(sg)
                        logger.info("deleted group %s's home "
                                  + "related to the project %s", sg, proj_name)
                    else:
                        newGroupFlag = True
                        print 'created group ' + sg + ' ' \
                            + 'related to the project ' + proj_name + ' and ' \
                            + 'deleted its home'
                else:
                    logger.debug("group %s has already been created", sg)
                for user in project['groups'][sg]:
                    if not(user in self.irods_users.keys()):
                        if not(self.dryrun):
                            self.irodsu.createIrodsUsers(user)
                            logger.info("created user %s", user)
                        else:
                            print "created user %s" % (user)
                    # add a new user to the sub-group only if the sub-group is new
                    # or it is old, but the user is not included among its members yet
                    if (newGroupFlag) \
                        or (sg in self.irods_projects.keys() \
                        and not (user in self.irods_projects[sg]['members'])):
                        if not(self.dryrun):
                            self.irodsu.addIrodsUserToGroup(user,sg)
                            logger.info("added user %s to the group %s", 
                                        user, sg)
                        else:
                            print "added user %s to the group %s" % (user, sg)


    def addUsersToProject(self, proj_name, project, new_project_flag=False):
        """Add the users to iRODS groups (projects)."""

        logger.info("adding the following users to the group:")
        user_list = project['members']
        if 'PI' in project.keys():
            user_list.append(project['PI'])
            # eliminate duplicates when a PI is also a member of the project
            user_list = set(user_list)
        for user in [x for x in user_list
                     if (new_project_flag or 
                         not(x in self.irods_projects[proj_name]['members']))]:
            logger.info(user)
            if not(self.dryrun):
                if not(user in self.irods_users.keys()):
                    self.irodsu.createIrodsUsers(user)
                    logger.info("created irods user %s", user)
                self.irodsu.addIrodsUserToGroup(user, proj_name)
                logger.info("added irods user %s to the group %s", 
                            user, proj_name)
            else:
                print "added user %s to the group %s" % (user, proj_name)


    def addProjects(self):
        """Add the users/projects file based info to iRODS."""

        logger.info("creating the following projects:")

        if (logger.getEffectiveLevel() == 10):
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(self.projects)            

        # the project/group is in the list, but not in iRODS
        for proj_name in [x for x in self.projects.keys()
                          if not(x in self.irods_projects.keys())]:
            logger.info("#### "+proj_name+" ####")
            filterObj = Filters(logger)
            if filterObj.attr_filters(self.projects[proj_name], self.conf.condition):
                if not(self.dryrun):
                    # add users to the new project
                    self.irodsu.createIrodsGroup(proj_name)
                    logger.info("created irods group %s", proj_name)
                else:
                    print "create irods group " + proj_name
                self.addUsersToProject(proj_name, self.projects[proj_name], True)
                # create sub-groups and add users to them
                self._addSubGroups(proj_name, self.projects[proj_name])


    def updateProjects(self):
        """Update the users/projects file based info to iRODS."""

        logger.info("updating the following projects:")

        for proj_name in [x for x in self.projects.keys() 
                          if x in self.irods_projects.keys()]:
            logger.info("#### "+proj_name+" ####")
            # users are in the UserDB and not in iRODS
            self.addUsersToProject(proj_name, self.projects[proj_name])
            # add users from irods externals
            user_list = self.projects[proj_name]['members']
            if 'PI' in self.projects[proj_name].keys():
                user_list.append(self.projects[proj_name]['PI'])
            for sg in self.projects[proj_name]['groups'].keys():
                user_list += self.projects[proj_name]['groups'][sg]
            user_list = set(user_list)
            # users are in iRODS and not in the userDB
            logger.info("deleting the following users from the group:")
            for user in [x for x in self.irods_projects[proj_name]['members'] 
                         if not(x in user_list)]:
                logger.info(user)
                if not(self.dryrun):
                    if self.conf.notification_active:
                        message = "user " + user + " should be deleted from " \
                                + "project " + proj_name
                        mailsnd = MailSender()
                        mailsnd.send(message, self.conf.notification_sender, 
                                     self.conf.notification_receiver)
                        logger.info("user request for deletion sent")
                else:
                    print "user " + user + " should be deleted from project " \
                         + proj_name
            # update sub-groups
            self._addSubGroups(proj_name, self.projects[proj_name])


    def deleteProjects(self):
        """Delete the projects from iRODS according to the userDB file based info."""

        logger.info("deleting the following projects:")
        # generate a list of all the sub-groups
        sg_list = self._getSubGroupsList()
        s = set(self.conf.internal_project_list)
        for proj_name in [x for x in self.irods_projects.keys() if x not in s]:
            # projects are in iRODS and not in userDB
            if (not(proj_name in sg_list.keys())
                and (not(proj_name in self.projects.keys())
                )):
                logger.info("#### "+proj_name+" ####")
                if not(self.dryrun):
                    if self.conf.notification_active:
                        # send message
                        message = "project " + proj_name + " should be " \
                                + "deleted from irods"
                        mailsnd = MailSender()
                        mailsnd.send(message, self.conf.notification_sender, 
                                     self.conf.notification_receiver)
                        logger.info("project [%s]: request for deletion "
                                  + "sent", proj_name)
                else:
                    print "project " + proj_name + " should be deleted from " \
                        + "irods"


    def updateUsers(self):
        """Update the users according to the userDB file based info."""

        logger.info("updating the users")
        for user in self.irods_users.keys():
            logger.debug("#### " + user + " ####")
            s = set(self.conf.internal_project_list)
            for proj_name in [x for x in self.irods_projects.keys() 
                              if x not in s]:
                user_list = []
                if (proj_name in self.projects.keys()):
                    user_list = self.projects[proj_name]['members']
                    if 'PI' in self.projects[proj_name].keys():
                        user_list.append(self.projects[proj_name]['PI'])
                    for sg in self.projects[proj_name]['groups'].keys():
                        user_list += self.projects[proj_name]['groups'][sg]
                    user_list = set(user_list)


################################################################################
# CINECA Client Configuration Class #
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
                                                   maxBytes=4194304, \
                                                   backupCount=1)
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
        self.local_authoritative = self._getConfOption('Sources', 
                                                       'local_authoritative',
                                                       True)
        self.condition = self._getConfOption('Sources', 'condition')
        self.internal_project_list = \
            self._getConfOption('iRODS', 'internal_project_list').split(',')
        self.irods_admin_user = self._getConfOption('iRODS', 
                                                    'irods_admin_user')
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
# CINECA User Synchronization Tool Command Line Interface #
################################################################################

def sync(args):

    configuration = Configuration(args.confpath, logger)
    configuration.parseConf();
    us = UserSync(configuration)
     
    logger.info("Users/projects sync starting ...")
    us.synchronize(args.dryrun)
    logger.info("Users/projects sync completed")

    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='CINECA iRODS user sinchronization tool')
    parser.add_argument("confpath", default="NULL",
                        help="path to the configuration file")
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="execute a command without performing any real change")

    subparsers = parser.add_subparsers(title='Actions', 
                                       description='synchronization actions',
                                       help='additional help')

    parser_sync = subparsers.add_parser('sync', 
                                        help='synchronize file based user info with iRODS')
    parser_sync.set_defaults(func=sync) 

    args = parser.parse_args()
    args.func(args)
