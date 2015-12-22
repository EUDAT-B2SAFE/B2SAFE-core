#!/usr/bin/env python

import subprocess
import re
import logging
import logging.handlers
import json
import pprint
import sys
import collections
import shutil

from pprint import pformat
from utilities.mailSender import MailSender
from utilities.filters import Filters
from utilities.irodsUtility import *

##############################################################################
# Synchronization Task Class #
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
                            + 'related to the project ' + proj_name
                        if not self.conf.irods_subgroup_home:
                            print ' and deleted its home'
                else:
                    self.logger.debug("group %s has already been created", sg)

                for user in project['groups'][sg]:

                    userinfo = self.irodsu.getIrodsUser(user)
                    if (userinfo is not None) and \
                       ("No rows found" in userinfo.splitlines()[0]):
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
                        else:
                            print "created user %s" % (user)
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
                self.irodsu.addIrodsUserToGroup(user, proj_name)
                self.logger.debug("added irods user %s to the group %s", 
                             user, proj_name)
            else:
                print "added user %s to the group %s" % (user, proj_name)


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
                    newGroupFlag = self.irodsu.createIrodsGroup(proj_name)
                    if not self.conf.irods_group_home:
                        self.irodsu.deleteGroupHome(proj_name)
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
            # users are in the UserDB and not in iRODS
            self.addUsersToProject(proj_name, self.projects[proj_name])
            # add users from irods externals
            user_list = self.projects[proj_name]['members']
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
            # projects are in iRODS and not in userDB
            if (not(proj_name in sg_list.keys())
                and (not(proj_name in self.projects.keys()) or quotaFlag)):
                self.logger.info("The project: " + proj_name + " should be deleted")
                if not(self.dryrun):
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
                    for sg in self.projects[proj_name]['groups'].keys():
                        user_list += self.projects[proj_name]['groups'][sg]
                    user_list = set(user_list)
##TODO here should be managed user attributes

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
                            if self.conf.notification_active:
                                message = "removed user " + user + "'s DN: " + dn
                                mailsnd = MailSender()
                                mailsnd.send(message, self.conf.notification_sender,
                                             self.conf.notification_receiver)
                            self.logger.info("the dn %s has been removed for "
                                        + "user %s", dn, user)
                        else:
                            print "the dn " + dn + " has been removed for " \
                                + "user " + user
