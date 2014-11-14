#!/usr/bin/env python

import subprocess
import re
import logging
import logging.handlers
import json
import pprint
import sys
import collections

from pprint import pformat
from utilities.mailSender import MailSender
from utilities.filters import Filters
from utilities.jsonUtility import *
from utilities.irodsUtility import *

##############################################################################
# Synchronization Task Class #
# input:
#       irods_users: { 'user1': {user1_attr1, user1_attr2},
#                      'user2': {user2_attr1, user2_attr2}
#                    }
#       irods_projects: { 'irods_group1': {'members': ['user1, user2']},
#                         'irods_group2': {'members': ['user1, user2']}
#                       }
#       local_projects:{ 'main_group1': { 'PI': 'user1',
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
#       dn_map: { 'user1': [ '/C=XX/O=Consortium/OU=GC/OU=local/CN=userName1',
#                            '/C=YY/O=NNNN/OU=ZZ/L=PP/CN=userName2'],
#                 'user2': [ '/C=XX/O=Consortium/OU=GC/OU=local/CN=userName3',
#                            '/C=YY/O=NNNN/OU=ZZ/L=PP/CN=userName4']
#               }
##############################################################################

class SynchronizationTask():
    """
    perform synchronization operations
    """

    def __init__(self, irods_users, irods_projects, projects, dn_map,
                 conf, dryrun, logger_parent=None, debug=False):
        """Initialize object."""

        if logger_parent: logger_name = logger_parent + ".SynchTask"
        else: logger_name = "SynchTask"
        self.logger = logging.getLogger(logger_name)
    
        self.irods_users = irods_users
        self.irods_projects = irods_projects
        self.projects = projects
        self.dn_map = dn_map
        self.conf = conf
        self.dryrun = dryrun
        self.irodsu = IRODSUtils(conf.irods_home_dir, logger_name,
                                 conf.irods_debug)
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)


    def _parseQuotas(self):
        """Internal: Parse the quota info file."""

        self.logger.info("Reading the quota info from the file %s", 
                         self.conf.quota_file)

        try:
            with open(self.conf.quota_file, "r") as filehandle:
                try:
                    quotas = json.load(filehandle, object_hook=JSONUtils().decode_dict)
                    return quotas
                except (ValueError) as ve:
                    self.logger.error('the file ' + self.conf.quota_file
                                 + ' is not a valid json.')
                    sys.exit(1)
        except (IOError, OSError) as e:
            with open(self.conf.quota_file, "w+") as filehandle:
                json.dump({}, filehandle, indent=2, sort_keys=True)
                self.logger.debug('impossible to read the file %s, so a new one has'
                                  + ' been written', self.conf.quota_file)
            return {}
        
        return None


    def _writeQuota(self,quotas):
        """Internal: Write the quota info to the file."""

        self.logger.info("Writing the quota info to the file %s", 
                         self.conf.quota_file)
        try:
            filehandle = open(self.conf.quota_file,"w")
            json.dump(quotas, filehandle, indent=2, sort_keys=True)
            filehandle.close()
        except Exception, e:
            self.logger.error("problem while writing quota file %s", 
                              self.conf.quota_file)
            self.logger.error("Error: %s", e)
            return False

        return True


    def _updateQuota( self, proj_name ):
        """Internal: Update the quota info file."""

        self.logger.info("checking if an update of the quota info, related to the "
                    + " project " + proj_name + ", is required")
        quotas = self._parseQuotas() 
        if proj_name in quotas.keys():
            if (quotas[proj_name]['quota_limit'] != 
                self.projects[proj_name][self.conf.quota_attribute]):
                quotas[proj_name]['quota_limit'] = \
                        self.projects[proj_name][self.conf.quota_attribute]
                self._writeQuota(quotas)
                self.logger.debug("updated the quota info, project: " + proj_name 
                             + ", new quota limit value: " 
                             + str(quotas[proj_name]['quota_limit']))
            else:
                self.logger.debug("nothing to update for project: " + proj_name)
                return False
        else:
            quota = {'quota_limit':0, 'used_space':0, 
                     'unity':self.conf.quota_unity, 'used_space_perc':0}
            quota['quota_limit'] = \
                self.projects[proj_name][self.conf.quota_attribute]
            quotas[proj_name] = quota
            self._writeQuota(quotas)
            self.logger.debug("created a new quota info record for the project: "
                         + proj_name + ", with value: " + pformat(quota))

        return True

 
    def _deleteQuota(self,proj_name):
        """Internal: Delete the quota limit from the file."""

        self.logger.info("deleting the quota limit")
        quotas = self._parseQuotas()
        if proj_name in quotas.keys():
            del quotas[proj_name]
        else:
            self.logger.debug("no project quota to delete")

        return self._writeQuota(quotas)


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
        self.logger.info("adding sub-groups to the project %s", proj_name)
                        
#        if (self.logger.getEffectiveLevel() == 10):
#            pp = pprint.PrettyPrinter(indent=4)
#            pp.pprint(projects)
            
        if 'groups' in project.keys():
            for sg in project['groups'].keys():

                newGroupFlag = False
                if not(sg in self.irods_projects.keys()):
                    if not(self.dryrun):
                        newGroupFlag = self.irodsu.createIrodsGroup(sg)
                        if not newGroupFlag:
                            if self.conf.notification_active:
                                message = "creation of the irods group: " + sg \
                                        + " failed, related to the project: " \
                                        + proj_name
                                mailsnd = MailSender()
                                mailsnd.send(message, self.conf.notification_sender,
                                             self.conf.notification_receiver)
                            self.logger.debug("failed to create the irods group %s "
                                            + "related to the project %s", sg, proj_name)
                        else:
                            self.logger.debug("created group %s related to the project %s",
                                              sg, proj_name)
                            if not self.conf.irods_subgroup_home:
                                self.irodsu.deleteGroupHome(sg)
                                self.logger.debug("deleted group %s's home "
                                                + "related to the project %s",
                                                  sg, proj_name)
                    else:
                        newGroupFlag = True
                        print 'created group ' + sg + ' ' \
                            + 'related to the project ' + proj_name + ' and ' \
                            + 'deleted its home'
                else:
                    self.logger.debug("group %s has already been created", sg)

                for user in project['groups'][sg]:

                    userinfo = self.irodsu.getIrodsUser(user)
                    if (userinfo is not None) and \
                       ("No rows found" in userinfo.splitlines()[0]):
#                    if not(user in self.irods_users.keys()):
                        if not(self.dryrun):
                            response = self.irodsu.createIrodsUsers(user)
                            if response[0] != 0:
                                if self.conf.notification_active:
                                    message = "creation of the irods user " \
                                              + user + " failed"
                                    mailsnd = MailSender()
                                    mailsnd.send(message, 
                                                 self.conf.notification_sender,
                                                 self.conf.notification_receiver)
                                self.logger.error("failed to create the irods user %s", 
                                                  user)
                            else:
                                self.logger.debug("created user %s", user)
                                if self.conf.quota_active:
                                    # quota from userDB is set in GB, while iRODS uses bytes
                                    quota = self.toBytes( 
                                            int(project[self.conf.quota_attribute]),
                                            self.conf.quota_unity)
                                    self.irodsu.setIrodsUserQuota(user,str(quota))
                                    self.logger.debug("set the irods quota limit to " 
                                                      + str(quota))
                        else:
                            print "created user %s" % (user)
                            if self.conf.quota_active:
                                quotaGB = project[self.conf.quota_attribute]
                                print "and set the irods quota limit to " \
                                      + quotaGB + " GB"

                    # add a new user to the sub-group only if the sub-group is new
                    # or it is old, but the user is not included among its members yet
                    if (newGroupFlag) \
                        or (sg in self.irods_projects.keys() \
                        and not (user in self.irods_projects[sg]['members'])):
                        if not(self.dryrun):
                            self.irodsu.addIrodsUserToGroup(user,sg)
                            self.logger.debug("added user %s to the group %s",
                                         user, sg)
                        else:
                            print "added user %s to the group %s" % (user, sg)


    def addUsersToProject(self, proj_name, project, new_project_flag=False):
        """Add the users to iRODS groups (projects)."""

        self.logger.info("checking if there are users to be added to the group "
                    + proj_name)
        user_list = project['members']
        if 'PI' in project.keys():
            user_list.append(project['PI'])
            # eliminate duplicates when a PI is also a member of the project
            user_list = set(user_list)
        for user in [x for x in user_list
                     if (new_project_flag or 
                         not(x in self.irods_projects[proj_name]['members']))]:
            self.logger.info(user)
            if not(self.dryrun):
                if not(user in self.irods_users.keys()):
                    response = self.irodsu.createIrodsUsers(user)
                    if response[0] != 0:
                        if self.conf.notification_active:
                            message = "creation of the irods user " + user \
                                    + " failed"
                            mailsnd = MailSender()
                            mailsnd.send(message, self.conf.notification_sender,
                                         self.conf.notification_receiver)
                        self.logger.error("failed to create the irods user %s", user)
                    else:
                        self.logger.debug("created irods user %s", user)
                        if self.conf.quota_active:
                            # quota from userDB is set in GB, while iRODS uses bytes
                            quota = self.toBytes(
                                         int(project[self.conf.quota_attribute]),
                                         self.conf.quota_unity)
                else:
                    if self.conf.quota_active:
                        quota_limit = self.irodsu.listIrodsUserQuota(user)
                        # quota from userDB is set in GB, while iRODS uses bytes
                        quota = quota_limit + self.toBytes(
                                int(project[self.conf.quota_attribute] 
                                   ), self.conf.quota_unity)
                        self.irodsu.setIrodsUserQuota(user,str(quota))
                        self.logger.debug("defined quota limit to %s GB for the user %s",
                                     str(quota), user)                                     
                self.irodsu.addIrodsUserToGroup(user, proj_name)
                self.logger.debug("added irods user %s to the group %s", 
                             user, proj_name)
            else:
                print "added user %s to the group %s" % (user, proj_name)
                if self.conf.quota_active:
                    quotaGB = project[self.conf.quota_attribute]
                    print "and set the related user quota limit to %s GB" \
                          % (quotaGB,)


    def addProjects(self):
        """Add the users/projects file based info to iRODS."""

        self.logger.info("Checking if there are new projects to be added")

#        if (self.logger.getEffectiveLevel() == 10):
#            pp = pprint.PrettyPrinter(indent=4)
#            pp.pprint(self.projects)            

        # the project/group is in the list, but not in iRODS
        for proj_name in [x for x in self.projects.keys()
                          if not(x in self.irods_projects.keys())]:
            self.logger.info("Checking if the new project: " + proj_name
                           + " should be added")
            filterObj = Filters(self.logger)
            if filterObj.attr_filters(self.projects[proj_name], self.conf.condition):
                if not(self.dryrun):
                    if self.conf.quota_active:
                        self._updateQuota(proj_name)
                        self.logger.info("Added quota info for project: " 
                                         + proj_name)
                    newGroupFlag = self.irodsu.createIrodsGroup(proj_name)
                    if not newGroupFlag:
                        if self.conf.notification_active:
                            message = "creation of the irods group " + proj_name \
                                    + " failed"
                            mailsnd = MailSender()
                            mailsnd.send(message, self.conf.notification_sender,
                                         self.conf.notification_receiver)
                        self.logger.info("failed to create the irods group %s", 
                                         proj_name)
                    else:
                        self.logger.info("Created irods group %s", proj_name)
                else:
                    print "created irods group " + proj_name
                self.addUsersToProject(proj_name, self.projects[proj_name], True)
                self._addSubGroups(proj_name, self.projects[proj_name])


    def updateProjects(self):
        """Update the users/projects file based info to iRODS."""

        self.logger.info("Checking if an update for the projects is required")

        for proj_name in [x for x in self.projects.keys() 
                          if x in self.irods_projects.keys()]:
            self.logger.info("Updating the project: " + proj_name)
            if self.conf.quota_active:
                self._updateQuota(proj_name)
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
            for user in [x for x in self.irods_projects[proj_name]['members'] 
                         if not(x in user_list)]:
                self.logger.info("Deleting the user: " + user + ", from the group: "
                                 + proj_name)
                if not(self.dryrun):
                    if self.conf.notification_active:
                        message = "user " + user + " should be deleted from " \
                                + "project " + proj_name
                        mailsnd = MailSender()
                        mailsnd.send(message, self.conf.notification_sender, 
                                     self.conf.notification_receiver)
                        self.logger.info("Request for user deletion sent")
                else:
                    print "user " + user + " should be deleted from project " \
                         + proj_name
            self._addSubGroups(proj_name, self.projects[proj_name])


    def deleteProjects(self):
        """Delete the projects from iRODS according to the userDB file based info."""

        self.logger.info("Checking if there are projects to be deleted")
        # generate a list of all the sub-groups
        sg_list = self._getSubGroupsList()

#        if (self.logger.getEffectiveLevel() == 10):
#            print "Sub-groups:"
#            pp = pprint.PrettyPrinter(indent=4)
#            pp.pprint(sg_list)

        s = set(self.conf.internal_project_list)
        for proj_name in [x for x in self.irods_projects.keys() if x not in s]:
##TODO add filtering criteria as in addProjects
            quotaFlag = False
            if self.conf.quota_active and proj_name in self.projects.keys():
                quotaFlag = \
                    len((self.projects[proj_name][self.conf.quota_attribute]).strip()) == 0 \
                    or int(self.projects[proj_name][self.conf.quota_attribute]) == 0
            # projects are in iRODS and not in userDB
            if (not(proj_name in sg_list.keys())
                and (not(proj_name in self.projects.keys()) or quotaFlag)):
                self.logger.info("The project: " + proj_name + " should be deleted")
                if not(self.dryrun):
                    if self.conf.quota_active:
                        self._deleteQuota(proj_name)
                    if self.conf.notification_active:
                        # send message
                        message = "project " + proj_name + " should be " \
                                + "deleted from irods"
                        mailsnd = MailSender()
                        mailsnd.send(message, self.conf.notification_sender, 
                                     self.conf.notification_receiver)
                        self.logger.debug("project [%s]: request for deletion "
                                     + "sent", proj_name)
                else:
                    print "project " + proj_name + " should be deleted from " \
                        + "irods"


    def updateUsers(self):
        """Update the users according to the userDB file based info."""

        self.logger.info("Checking if there are updates related to the users")
        for user in self.irods_users.keys():

            self.logger.debug("Updating the info for user: " + user)
            s = set(self.conf.internal_project_list)
            total_quota_limit = 0
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
##TODO here should be managed user attributes
                if user in user_list:
                    if self.conf.quota_active:
                        # quota from userDB is set in GB, while iRODS uses bytes
                        if len((self.projects[proj_name][self.conf.quota_attribute]).strip()) > 0:
                            total_quota_limit += self.toBytes(
                                int(self.projects[proj_name][self.conf.quota_attribute]
                                   ), self.conf.quota_unity)
            if not(self.dryrun):
                if self.conf.quota_active:
                    self.irodsu.setIrodsUserQuota(user,str(total_quota_limit))
                    self.logger.debug("set the new quota limit for user %s to %s GB", 
                                      user, str(self.fromBytes(total_quota_limit,
                                                               self.conf.quota_unity)))
            else:
                if self.conf.quota_active:
                    print("set the new quota limit for user " + user + " to "
                          + str(self.fromBytes(total_quota_limit, 
                                self.conf.quota_unity)) + " GB")

            # managing the dn of a user
            self.logger.debug("Updating the dn mapping for user: " + user)
            out = self.irodsu.getUserDN(user)
            dn_list = []
            if (out is not None and out.strip() != 'No rows found'):
                for line in out.splitlines():
                    # remove the username from the beginning of the line (e.g. "rossim /O=IT/OU=...")
                    dn_list.append(line[len(user)+1:])
            # the user is in the map file, but not in irods
            if (self.dn_map is not None and user in self.dn_map.keys()):
                for dn in self.dn_map[user]:
                    if not(dn in dn_list):
                        self.logger.debug("the dn %s is not in irods for user "
                                          + "%s, so it will be added", dn, user)
                        if not(self.dryrun):
                            self.irodsu.addDNToUser(user,dn)
                            self.logger.info("the dn %s has been added for user "
                                             + "%s", dn, user)
                            if (self.conf.gridftp_active 
                                and dn != self.conf.gridftp_server_dn):
                                with open(self.conf.gridmapfile, 'a+') as mapf:
                                    mapf.write('"' + dn + '"' + " " + user + "\n")
                                    self.logger.info("the dn %s associated to the"
                                              + " user %s has been added to "
                                              + "the gridmapfile %s", dn, user, 
                                              self.conf.gridmapfile)
                        else:
                            print "the dn " + dn + " has been added for user " \
                                  + user

            # the user is in irods, but not in the map file
            if (self.dn_map is not None):
                for dn in dn_list:
                    if not(user in self.dn_map.keys()) \
                        or not(dn in self.dn_map[user]):
                        self.logger.debug("the dn %s is not in map file for "
                                     + "user %s, so it will be removed", 
                                     dn, user)
                        if not(self.dryrun):
                            self.irodsu.removeUserDN(user,dn)
                            self.logger.info("the dn %s has been removed for "
                                        + "user %s", dn, user)
                            if (self.conf.gridftp_active
                                and dn != self.conf.gridftp_server_dn):
                                with open(self.conf.gridmapfile, 'w+') as mapf:
                                    content = mapf.readlines()
                                    for line in content:
                                        if not (dn in line.split()):
                                            mapf.write(line)
                                    self.logger.info("the dn %s associated to the"
                                              + " user %s has been removed from"
                                              + " the gridmapfile %s", dn, user,
                                              self.conf.gridmapfile)
                        else:
                            print "the dn " + dn + " has been removed for " \
                                + "user " + user

    def toBytes(self, size, unity):
        """Convert file size to byte"""
        size_map = {'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3,
                    'TB': 1024 ** 4}
        return size * size_map[unity] 

    def fromBytes(self, size, unity):
        """Convert file size from byte"""
        size_map = {'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3,
                    'TB': 1024 ** 4}
        return size / size_map[unity]
