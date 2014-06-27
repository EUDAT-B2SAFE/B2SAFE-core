#!/usr/bin/env python
# -*- python -*-

import sys
import logging
import os
import subprocess
import json
from pprint import pformat

class MyProxyRemoteSource:

    def __init__(self, conf, parent_logger=None):
        """initialize the object"""

        if (parent_logger): self.logger = parent_logger
        else: self.logger = logging.getLogger('myproxy')

        missingp = []
        key = 'irods_path_to_dns'
        if key in conf: self.irods_path = conf[key]
        else: missingp.append(key)
        key = 'gridftp_cert_dn'
        if key in conf: self.gridftp_cert_dn = conf[key]
        else: missingp.append(key)
        if len(missingp) > 0:
             self.logger.error('missing parameters: ' + pformat(missingp))
             sys.exit(1)


    def synchronize_user_db(self, data):
        """
        Synchronize the remote users' list with a local json file (user db)
        """

        dn_user_dict = self.getRemoteUsers()
        self.logger.info("Synchronizing list of user DNs to the json file")
        if dn_user_dict:
            for dn,user in dn_user_dict.iteritems():
                if user in data:
                    if not dn in data[user]: 
                        data[user].append(dn)
                        self.logger.debug('Added dn '+ dn +' to user ' + user)
                else:
                    data[user] = [dn, self.gridftp_cert_dn]
                    self.logger.debug('Added dn '+ self.gridftp_cert_dn +
                                      ' to user ' + user)
                if self.gridftp_cert_dn not in data[user]: 
                    data[user].append(self.gridftp_cert_dn)
                    self.logger.debug('Added dn '+ self.gridftp_cert_dn +
                                      ' to user ' + user)
        else:
            self.logger.info("No distinguished names to sync")
            return None

        return data


    def getRemoteUsers(self):
        """
        Get the remote users' list
        """

        self.logger.info("Getting list of user DNs from file " + self.irods_path)
        dn_user_dict = {}

        command = ['iget', '-f', self.irods_path]
        (rc, output) = self.shell_command(command)
        if rc != 0 and not 'CAT_NO_ROWS_FOUND' in output[1]:
            self.logger.error('Error running %s, rc = %d' % (' '.join(command), rc))
            self.logger.error(output[1])
            return None

        fileName = self.irods_path[self.irods_path.rfind("/")+1:]
        with open (fileName, "r") as dnfile:
            data = dnfile.readlines()

        self.logger.debug('Got the content of the dn file: ' + pformat(data))
        for line in data:
            dn = line[line.find('"')+1:line.rfind('"')]
            user = line[line.rfind('"')+1:].strip()
            dn_user_dict[dn] = user
        self.logger.debug('Got list of user DNs: ' + pformat(dn_user_dict))

        os.remove(fileName)

        return dn_user_dict


    def shell_command(self, command_list):
        """
        Performs a shell command using the subprocess object
        
        input list of strings that represent the argv of the process to create
        return tuple (return code, the output object from subprocess.communicate)
        """
    
        if not command_list:
            return None
            
        try:
            process = subprocess.Popen(command_list, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            output = process.communicate()
            return (process.returncode, output)
        except:
            return (-1, [None, None])
