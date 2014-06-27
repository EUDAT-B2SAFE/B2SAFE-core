#!/usr/bin/env python
# -*- python -*-

import sys
import logging
import os
import subprocess
import urllib2
import urllib
import json
from pprint import pformat

class EuhitRemoteSource:

    def __init__(self, conf, parent_logger=None):
        """initialize the object"""

        if (parent_logger): self.logger = parent_logger
        else: self.logger = logging.getLogger('euhit')

        self.main_project = 'EUHIT_Repo'

        missingp = []    
        key = 'ckan_api_root'
        if key in conf: self.ckan_api_root = conf[key]
        else: missingp.append(key)
        key = 'admin_api_key'
        if key in conf: self.admin_api_key = conf[key]
        else: missingp.append(key)
        key = 'default_groups'
        if key in conf: self.default_groups = conf[key]
        else: missingp.append(key)
        if len(missingp) > 0:
            self.logger.error('missing parameters: ' + pformat(missingp))


    def getRemoteUsers(self):
        """
        Get the remote users' list
        """

        self.logger.info("Getting list of users from euhit db...")
        data_dict = { 'all_fields' : False }  # set to True to get additional info
        data_string = urllib.quote(json.dumps(data_dict))
        request = urllib2.Request(self.ckan_api_root+'organization_list')
        request.add_header('Authorization', self.admin_api_key)
        response = urllib2.urlopen(request, data_string)
        assert response.code == 200
        response_dict = json.loads(response.read())
        assert response_dict['success'] is True
        org_list = response_dict['result']
        self.logger.debug(pformat(org_list))

        # Get the list of all users in at least one organization (user_all_org_editor_list)
        # and the dictionaries of members for each organization (user_org_editor_dict)
        user_all_org_editor_list = []
        user_org_editor_dict = {}
        for org in org_list:
            user_org_editor_dict[org] = []
            data_dict = {
                         'id': org  ,
                         'object_type' : 'user',
                         'capacity' : 'editor'
                        }
            data_string = urllib.quote(json.dumps(data_dict))
            request = urllib2.Request(self.ckan_api_root+'member_list')
            request.add_header('Authorization', self.admin_api_key)
            response = urllib2.urlopen(request, data_string)
            assert response.code == 200
            response_dict = json.loads(response.read())
            assert response_dict['success'] is True
            member_list = response_dict['result']
            for member in member_list:
                data_dict = {
                             'id': member[0],
                            }
                data_string = urllib.quote(json.dumps(data_dict))
                request = urllib2.Request(self.ckan_api_root+'user_show')
                request.add_header('Authorization', self.admin_api_key)
                response = urllib2.urlopen(request, data_string)
                assert response.code == 200
                response_dict = json.loads(response.read())
                assert response_dict['success'] is True
                user_name = response_dict['result']['name']
                user_org_editor_dict[org].append(user_name)
#                user_all_org_editor_list.append(user_name)
        # avoid repetitions using sets!
#        user_all_org_editor_list = list(set(user_all_org_editor_list))

        return user_org_editor_dict


    def synchronize_user_db(self, local_users_list, data, remove=False):
        """
        Synchronize the remote users' list with a local json file (user db)
        """

        remote_users_list = self.getRemoteUsers()

        # default groups management
        default_gl = self.default_groups.split(',')
        for dgroup in default_gl:
            if (dgroup not in data[self.main_project]["groups"]):
                data[self.main_project]["groups"][dgroup] = []
                self.logger.info('Creating default group \''+ dgroup + '\'')

        for org,members in remote_users_list.iteritems():

            #if subgroup org doesn't exist, create it
            org = 'euhit_' + org
            if (org not in data[self.main_project]["groups"]):
                self.logger.info('Creating sub-group \''+ org + '\'')
                data[self.main_project]["groups"][org] = []

            # add new members
            self.logger.info('Adding users that have been added to ' + org + ' ...')
            for member in members:
                member = 'euhit_' + member
                if member not in data[self.main_project]["groups"][org]:
                    data[self.main_project]["groups"][org].append(member)
                    self.logger.debug('\tadded user %s' % (member,))
                for dgroup in default_gl:
                    if member not in data[self.main_project]["groups"][dgroup]:
                        data[self.main_project]["groups"][dgroup].append(member)
                        self.logger.debug('\tadded user %s to the default group %s' % (member,dgroup,))

        # remove users that don't exist in remote groups
        if remove:
            for org,members in local_users_list.iteritems():
                if org in default_gl: continue
                self.logger.info('Removing users that have been removed from ' + org + '...') 
                for member in members:
                    remote_org = org[6:]
                    remote_member = member[6:]
                    if remote_member not in remote_users_list[remote_org]:
                        data[self.main_project]["groups"][org].remove(member)
                        for dgroup in default_gl: 
                            data[self.main_project]["groups"][dgroup].remove(member)
                        self.logger.debug('\tremoved user %s' % (member,))

        return data
