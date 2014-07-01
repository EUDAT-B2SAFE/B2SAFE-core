#!/usr/bin/env python
#
# unitydb.py

"""
  Script is used to query UnityDB to get list of user and its attributes to local
"""
import sys
import argparse
import ConfigParser
import json
from eudatunity import EudatRemoteSource

class UnityClient:
    """Class to implement functions used to query UnityDB
    """

    def __init__(self):
        """
        :return:
        """

    def _getConfOption(self, section, option):
        """
        get Information configuration from conf-file
        :param section: host/ username/ password
        :param option:
        :return:
        """
        if (self.config.has_option(section, option)):
            return self.config.get(section,option)
        else:
            sys.exit(0)


    def main(self):

        parser = argparse.ArgumentParser(description='Synchronize remote user '
                                                     'accounts to a local json '
                                                     'file.')
        parser.add_argument('conf', default='unitydbsync.conf', help='path to the configuration file')
        subparsers = parser.add_subparsers(title='Target group', help='additional help')
        parser_group = subparsers.add_parser('syncto', help='the synchronization target')
        parser_group.add_argument('group', help='the target group (or project)')

        _args = parser.parse_args()
        project = _args.group

        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(open(_args.conf))

        if project == 'EUDAT':
            """call EudatRemoteSource
            """
            outputfile = self._getConfOption('COMMON','export')
            host = self._getConfOption('EUDAT','host')
            username = self._getConfOption('EUDAT','username')
            password = self._getConfOption('EUDAT','password')

            # userparam = {k:v for k,v in self.config.items(project)}
            # send request to EUDATRemoteSource and parse it
            query = EudatRemoteSource(host,username,password)

            # get list of all groups in Unity
            group_list = query.queryUnity("group/%2F")

            final_list = []
            list_member = []
            for group in group_list['members']:
                list_member.append(group)

            # Append list_member to final_list
            final_list.append({'members': list_member})

            # Query and get list of all user from Groups in Unity
            list_group = []
            for group_name in group_list['subGroups']:
                member_list = query.queryUnity("group"+group_name)
                list_group.append({group_name[1:]: member_list['members']})

            # Append list_group to final_list
            final_list.append({'groups': list_group})
            print json.dumps(final_list, indent=4, separators=(',',':'))

        else:
            sys.exit(0)

        with open(outputfile, 'w') as outfile:
            json.dump(final_list,outfile, indent=4)

if __name__ == '__main__':
    UnityClient().main()


