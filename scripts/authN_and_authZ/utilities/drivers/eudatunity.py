# !/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import json
import base64
from pprint import pformat
import requests
import fnmatch
import logging

class EudatRemoteSource:

    def __init__(self, main_project, subgroups, conf, role_map, parent_logger=None):
        """initialize the object"""

        if (parent_logger): self.logger = parent_logger
        else: self.logger = logging.getLogger('eudat')

        self.main_project = main_project
        self.subgroups = subgroups

        confkeys = ['host', 'username', 'password', 'carootdn', 'ns_prefix']
        missingp = []
        for key in confkeys:
            if not key in conf: missingp.append(key)
        if len(missingp) > 0:
            self.logger.warning('missing parameters: ' + pformat(missingp))
        self.conf = conf
        self.roles = self.readRoleMapFile(role_map)
        self.remote_users_list = self.getRemoteUsers()


    def readRoleMapFile(self, path):

        try:
            filehandle = open(path, "r")
        except IOError as err:
            print "error: failed to open %s: %s" % (path, err.strerror)
            sys.exit(-1)

        with filehandle:
            return json.loads(filehandle.read())        
    
        
    def queryUnity(self, sublink):
        """
        :param argument: url to unitydb with entity (entityID) or group (groupName)
        :return:
        """
        url = self.conf['host'] + sublink
        try:
            self.logger.debug("Querying the URL: {}".format(url))
            response = requests.get(url, verify=False, auth=(self.conf['username'], self.conf['password']))
            self.logger.debug("Encoding:{}".format(response.encoding))
            response.encoding = 'utf-8'
            self.logger.debug("New Encoding:{}".format(response.encoding))
        except IOError, e:
            self.logger.error("Wrong username or password", exc_info=True)
            sys.exit(1)
        assert (response.status_code == 200 or response.status_code == 400)
        
        json_data = response.content
        self.logger.debug("Response:{}".format(json_data))
        response_dict = json.loads(json_data)

        return response_dict


    def getRemoteUsers(self):
        """
        Get the remote users' list
        """
        self.logger.info("Getting list of users from eudat db...")
        # get list of all groups in Unity
        final_list = {'members':[], 'attributes':{}, 'groups':{}}
        for subg in self.subgroups:

            subjectMatch = False
            for iuser in self.roles:
                if subjectMatch: break
                for groupVal in self.roles[iuser]['organization']:
                    subjectMatch = fnmatch.fnmatch(subg, groupVal)
                    if subjectMatch: break
            if not subjectMatch:
                self.logger.error("The group '{}' is not mapped".format(subg))
                continue

            subg_attrs = self.queryUnity("group/%2F" + subg)
            if (subg_attrs is None) or (len(subg_attrs) == 0):
                self.logger.error("The group '{}' does not exist on B2ACCESS".format(subg))
                continue

            list_member = []
            users_map = {}
            attribs_map = {}
            for member_id in subg_attrs['members']:
                attr_list = {}

# only for B2ACCESS devel

                # 16/08/2017 bug fix @Paolo
                member_id = str(member_id.get('entityId',''))
                user_record = self.queryUnity("entity/"+member_id+"?group=%2F" + subg)
                # 16/08/2017 bug fix @Paolo

                identity_types = {}
                for identity in user_record['identities']:
                    self.logger.debug("identity['typeId'] = " + identity['typeId'])
                    self.logger.debug("identity['value'] = " + identity['value'])
                    identity_types[identity['typeId']] = identity['value']
                user_persistent_id = identity_types['persistent']
# end B2ACCESS devel

                user_attrs = self.queryUnity("entity/"+str(member_id)+"/attributes?group=%2F" + subg)
                if isinstance(user_attrs, dict) and ("error" in user_attrs.keys()):
                    self.logger.error("Error: " + user_attrs['error'])
                    continue
                user_cn = None
# for production
#               user_persistent_id = None
#
                for user_attr in user_attrs:
                    if user_attr['name'] == 'cn':
                        user_cn = user_attr['values'][0]
                        self.logger.debug("user_cn = " + user_cn)
                    elif user_attr['name'] == 'unity:persistent':
                        user_persistent_id = user_attr['values'][0]
                        self.logger.debug("user_persistent_id = " + user_persistent_id)
        
# only for B2ACCESS devel                    
                if "userName" in identity_types.keys():
                    list_member.append(identity_types['userName'])
                    users_map[member_id] = identity_types['userName']
                elif user_persistent_id is not None:
# end B2ACCESS devel
#                if user_persistent_id is not None:
                    list_member.append(user_persistent_id)
                    users_map[member_id] = user_persistent_id
                else:
                    list_member.append(str(member_id))
                    users_map[member_id] = str(member_id)
 
                if user_cn is None:
                    user_cn = users_map[member_id]
                  
                userDN = None
                if user_persistent_id is not None:
                    
                    # Here we build the DN: the way to build it could change
                    # in the future.
#TODO catch unicode error and filter out strange CN, logging the errors
                    userDN = self.conf['carootdn'] + '/CN=' + user_persistent_id \
                           + '/CN=' + user_cn
                    # Here the DN attribute is considered a list because, 
                    # in principle, multiple DNs could be associated to a user
                    self.logger.debug("userDN = " + userDN)
                attr_list['DN'] = [userDN]
   
                attribs_map[users_map[member_id]] = attr_list

            final_list['members'] = final_list['members'] + list_member
            final_list['attributes'].update(attribs_map)
            final_list['groups'][subg] = list_member

        return final_list


    def synchronize_user_db(self, data):
        """
        Synchronize the remote users' list with a local json file (user db)
        """
        filtered_list = self.remote_users_list['groups']
        data = self._userMapper(filtered_list, data, False)
            
        return data


    def synchronize_user_attributes(self, data):
        """
        Synchronize the remote users' attributes with a local json file
        for the time beeing just the DNs are considered
        """
        self.logger.info('Checking user attributes ...')
        filtered_list = self.remote_users_list['attributes']
        filtered_group_list = self.remote_users_list['groups']

        userdict = self._userMapper(filtered_group_list)
            
        for user,attrs in filtered_list.iteritems():
            self.logger.info('Adding DNs belonging to the user ' + user + ' ...')
            #### add its DN to the irods user
            if (user in userdict.keys()):
                u = userdict[user]
                if u not in data.keys():
                    data[u] = []
                if attrs['DN'] is not None:
                    data[u] = list(set(data[u] + attrs['DN']))
                    self.logger.debug('\tadded user ' + u + '\' DNs: '
                                     + pformat(attrs['DN']))            
 
        return data


    def _userMapper(self, mainDict, data=None, directMap=True):
        """
        Check which of the remote users should be associated to a local user
        according to the local user map
        """
        userdict = None
        if directMap:
            userdict = {}
        else:
            userdict = data[self.main_project]["groups"]
            self.logger.debug('The user dictionary for the project {}: {}'.format(self.main_project, userdict))
        for org,members in mainDict.iteritems():
            subjectMatch = False
            for iuser in self.roles:
                if not directMap:
                    if iuser not in userdict:
                        userdict[iuser] = []
                subjectMatch = False
                for groupVal in self.roles[iuser]['organization']:
                    subjectMatch = fnmatch.fnmatch(org, groupVal)
                    if subjectMatch:
                        if 'exclude' in self.roles[iuser].keys():
                            remoteUsers = set(members) - set(self.roles[iuser]['exclude'])
                        for member in remoteUsers:
                            if directMap:
                                userdict[member] = iuser
                            else:
                                userdict[iuser].append(member)
                                userdict[iuser] = list(set(userdict[iuser]))
                userMatch = False
                for userVal in self.roles[iuser]['user']:
                    for member in members:
                        userMatch = fnmatch.fnmatch(member, userVal)
                        if userMatch:
                            if directMap:
                                userdict[member] = iuser
                            else:
                                userdict[iuser].append(member)
                                userdict[iuser] = list(set(userdict[iuser]))
        #remove empty groups
        final_dict = {}
        for group in userdict.keys():
            if len(userdict[group]) > 0:
                final_dict[group] = userdict[group]

        return final_dict

