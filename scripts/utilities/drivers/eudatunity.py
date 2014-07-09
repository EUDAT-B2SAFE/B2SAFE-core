# !/usr/bin/env python

import sys
import json
import urllib2
import base64
from pprint import pformat

class EudatRemoteSource:
    def _debugMsg(self, method, msg):
        """Internal: Print a debug message if debug is enabled.

        """
        if self.debug:
            print "[", method, "]", msg

    def __init__(self, conf, parent_logger=None):
        """initialize the object"""
        
        if (parent_logger): self.logger = parent_logger
        else: self.logger = logging.getLogger('eudat')

        self.main_project = 'EUDAT'

        missingp = []    
        key = 'host'
        if key in conf: self.host = conf[key]
        else: missingp.append(key)
        key = 'username'
        if key in conf: self.username = conf[key]
        else: missingp.append(key)
        key = 'password'
        if key in conf: self.password = conf[key]
        else: missingp.append(key)
        if len(missingp) > 0:
            self.logger.error('missing parameters: ' + pformat(missingp))
            

    def queryUnity(self, sublink):
        """
        :param argument: url to unitydb with entity (entityID) or group (groupName)
        :return:
        """
        auth = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        header = "Basic %s" % auth
        url = self.host + sublink
        request = urllib2.Request(url)
        request.add_header("Authorization",header)
        try:
            response = urllib2.urlopen(request)
        except IOError, e:
            print "Wrong username or password"
            sys.exit(1)

        assert response.code == 200
        json_data = response.read()
        response_dict = json.loads(json_data)

        return response_dict
    
    
    def getRemoteUsers(self):
        """
        Get the remote users' list
        """

        self.logger.info("Getting list of users from eudat db...")
        # get list of all groups in Unity
        group_list = self.queryUnity("group/%2F")

        final_list = {}
        list_member = []
        users_map = {}
        for member_id in group_list['members']:
            user_record = self.queryUnity("entity/"+str(member_id))
            for identity in user_record['identities']:
                if identity['typeId'] == "userName":
                    list_member.append(identity['value'])
                    users_map[member_id] = identity['value']
## TODO: if typeId = "persistent" get value and combine 
##       with eudat CA root issuer DN to build dynamically the user DN

        # Append list_member to final_list
        final_list['members'] = list_member

        # Query and get list of all user from Groups in Unity
        list_group = {}
        for group_name in group_list['subGroups']:
            member_list = self.queryUnity("group"+group_name)
            user_list = []
            for member_id in member_list['members']:
                user_list.append(users_map[member_id])
            list_group[group_name[1:]] = user_list

        # Append list_group to final_list
        final_list['groups'] = list_group
        
        return final_list


    def synchronize_user_db(self, local_users_list, data, remove=False):
        """
        Synchronize the remote users' list with a local json file (user db)
        """

        remote_users_list = self.getRemoteUsers()
        
        for org,members in remote_users_list['groups'].iteritems():

            #if subgroup org doesn't exist, create it
            org = 'eudat_' + org
            if (org not in data[self.main_project]["groups"]):
                self.logger.info('Creating sub-group \''+ org + '\'')
                data[self.main_project]["groups"][org] = []

            # add new members
            self.logger.info('Adding users that have been added to ' + org + ' ...')
            for member in members:
                member = 'eudat_' + member
                if member not in data[self.main_project]["groups"][org]:
                    data[self.main_project]["groups"][org].append(member)
                    self.logger.debug('\tadded user %s' % (member,))

        # remove users that don't exist in remote groups
        if remove:
            for org,members in local_users_list.iteritems():
                self.logger.info('Removing users that have been removed from ' + org + '...') 
                for member in members:
                    remote_org = org[6:]
                    remote_member = member[6:]
                    if remote_member not in remote_users_list[remote_org]:
                        data[self.main_project]["groups"][org].remove(member)
                        self.logger.debug('\tremoved user %s' % (member,))

        return data