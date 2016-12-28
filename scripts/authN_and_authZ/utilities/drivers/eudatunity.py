# !/usr/bin/env python

import sys
import json
import urllib2
import base64
from pprint import pformat
import requests
import simplejson
import fnmatch
import logging

class EudatRemoteSource:

    def _debugMsg(self, method, msg):
        """Internal: Print a debug message if debug is enabled.

        """
        logging.debug("[%s] %s" % (method, msg))

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

        self.role_map = role_map

        self.remote_users_list = self.getRemoteUsers()
#        print(pformat(remote_users_list))


    def queryUnity(self, sublink):
        """
        :param argument: url to unitydb with entity (entityID) or group (groupName)
        :return:
        """
#        auth = base64.encodestring('%s:%s' % (self.conf['username'], self.conf['password']))[:-1]
#        header = "Basic %s" % auth
        url = self.conf['host'] + sublink
#        request = urllib2.Request(url)
#        request.add_header("Authorization",header)
        try:
#            response = urllib2.urlopen(request)
            response = requests.get(url, verify=False, auth=(self.conf['username'], self.conf['password']))
        except IOError, e:
#            print "Wrong username or password"
            self.logger.error("Wrong username or password", exc_info=True)
            sys.exit(1)

#        assert response.code == 200
        assert response.status_code == 200
#        json_data = response.read()
        json_data = response.text
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
        attribs_map = {}
        for member_id in group_list['members']:
            user_record = self.queryUnity("entity/"+str(member_id))
            attr_list = {}
            self.logger.debug("Query: entity/" + str(member_id) +
                              ", user record: " + pformat(user_record))
            identity_types = {}
            for identity in user_record['identities']:
                self.logger.debug("identity['typeId'] = " + identity['typeId'])
                self.logger.debug("identity['value'] = " + identity['value'])
                identity_types[identity['typeId']] = identity['value']

            if "userName" in identity_types.keys():
                list_member.append(identity_types['userName'])
                users_map[member_id] = identity_types['userName']
            elif "identifier" in identity_types.keys():
                list_member.append(identity_types['identifier'])
                users_map[member_id] = identity_types['identifier']
            else:
                list_member.append(str(member_id))
                users_map[member_id] = str(member_id)

            if "persistent" in identity_types.keys():
                # Here we build the DN: the way to build it could change
                # in the future.
                userDN = self.conf['carootdn'] + '/CN=' + identity['value'] \
                       + '/CN=' + users_map[member_id]
                attr_list['DN'] = [userDN]

            attribs_map[users_map[member_id]] = attr_list

        final_list['members'] = list_member
        final_list['attributes'] = attribs_map

        # Query and get list of all user from Groups in Unity
        list_group = {}
        for group_name in group_list['subGroups']:
            member_list = self.queryUnity("group"+group_name)
            user_list = []
            for member_id in member_list['members']:
                user_list.append(users_map[member_id])
            list_group[group_name[1:]] = user_list

        final_list['groups'] = list_group

        return final_list


    def synchronize_user_db(self, data):
        """
        Synchronize the remote users' list with a local json file (user db)
        """

        if self.subgroups is not None:
            filtered_list = {org:members for (org,members)
                             in self.remote_users_list['groups'].iteritems()
                             if org in self.subgroups}
        else:
            filtered_list = self.remote_users_list['groups']

        #### erastova: open role map file

        try:
            filehandle = open(self.role_map, "r")
        except IOError as err:
            logging.error("error: failed to open %s: %s" % (self.role_map,
                                                            err.strerror))
            sys.exit(-1)

        with filehandle:
            map = simplejson.loads(filehandle.read())

        #### erastova: end of: open role map file

        for org,members in filtered_list.iteritems():

            self.logger.info('Adding users belonging to ' + org + ' ...')
            org = self.conf['ns_prefix'] + org

            #### erastova: get unity group and find it in role map for irods users
            #### if it exists, add its members to irods.remote.users under
            #### irods user name

            for userbs in map:
                subjectMatch = False
                for groupVal in map[userbs]['organization']:
                    subjectMatch = fnmatch.fnmatch(org, groupVal)
                    if subjectMatch:
                        data[self.main_project]["groups"][userbs] = []
                        for member in members:
                            member = self.conf['ns_prefix'] + member

                            for userb in map:
                                userMatch = False
                                for userVal in map[userb]['user']:
                                    userMatch = fnmatch.fnmatch(member, userVal)
                                    if userMatch:
                                        data[self.main_project]["groups"][userb] = []
                                        data[self.main_project]["groups"][userb].append(member)
                                    else:
									    data[self.main_project]["groups"][userbs].append(member)
                                    self.logger.debug('\tadded user %s' % (member,))

            #### erastova: end of: get unity group

        return data


    def synchronize_user_attributes(self, data):
        """
        Synchronize the remote users' attributes with a local json file
        for the time beeing just the DNs are considered
        """

        #### erastova: open role map file

        try:
            filehandle = open(self.role_map, "r")
        except IOError as err:
            logging.error("error: failed to open %s: %s" % (self.role_map,
                                                            err.strerror))
            sys.exit(-1)

        with filehandle:
            map = simplejson.loads(filehandle.read())

        #### erastova: end of: open role map file

        self.logger.info('Checking user attributes ...')

        if self.subgroups is not None:
            users = []
            for group in self.subgroups:
                self.logger.info('looking at group ' + group)

                if(subjectMatch):
                    for user in self.remote_users_list['groups'][group]:
                        self.logger.debug('looking at user ' + user)
                        users.append(user)
                        self.logger.debug('added user to the list ' + str(users))

            filtered_list = {user:attrs for (user,attrs)
                             in self.remote_users_list['attributes'].iteritems()
                             if user in users}
        else:
            filtered_list = self.remote_users_list['attributes']

        #### erastova: create mapping unity user - irods user

        userdict = {}

        for org,members in self.remote_users_list['groups'].iteritems():
            org = self.conf['ns_prefix'] + org

            subjectMatch = False

            for iuser in map:
                subjectMatch = False
                for groupVal in map[iuser]['organization']:
                    subjectMatch = fnmatch.fnmatch(org, groupVal)
                    if subjectMatch:
                        data[iuser] = [];
                        for member in members:
                            member = self.conf['ns_prefix'] + member
                            for userb in map:
                                userMatch = False
                                for userVal in map[userb]['user']:
                                    userMatch = fnmatch.fnmatch(member, userVal)
                                    if userMatch:
                                        userdict[member] = userb
                                        data[userb] = [];
                                    else:
                                        userdict[member] = iuser

        #### erastova: end of create mapping

        for user,attrs in filtered_list.iteritems():
            self.logger.info('Adding DNs belonging to the user ' + user + ' ...')
            user = self.conf['ns_prefix'] + user

            #### erastova: check if unity user belongs to b2safe and
            #### add its DN to the irods user

            if(user in userdict.keys()):
                user = userdict[user]
                data[user].append(attrs['DN'])
                self.logger.debug('\tadded user ' + user + '\' DNs: '
                              + pformat(attrs['DN']))

            #### erastova: end of check

        return data
