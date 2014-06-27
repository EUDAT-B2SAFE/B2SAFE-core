#!/usr/bin/env python
# -*- python -*-

import sys
import logging
import os
import subprocess
from pprint import pformat


class HBPRemoteSource:

    def __init__(self, conf, parent_logger=None):
        """initialize the object"""

        if (parent_logger): self.logger = parent_logger
        else: self.logger = logging.getLogger('hbpIncf')


    def getRemoteUsers(self):
        """ 
        Get the remote users' list
        """

        self.logger.info("Getting list of users from \'incf\' zone...")
        ids_groups = self.get_irods_group_membership('incf')
        self.logger.debug(pformat(ids_groups))
        if ids_groups == None:
            sys.exit(1)
        else:
            return ids_groups


    def get_irods_group_membership(self,zone):
        """
        Retrieves the IDS users and groups from iRODS. Only group names starting
        with 'ids-' are retrieved.
    
        Input: if 'zone' is provided, its the name of the remote zone for iquest.
    
        Returns: a dict where the key is the group name, and the value is a list
        of users who are members of the group.
        """
            
        query = "select USER_GROUP_NAME, USER_NAME where USER_GROUP_NAME like 'ids-%'"
            
        output = self.run_iquest(query, format='%s:%s', zone=zone)
        if output == None:
            # some error occurred
            return None
         
        group_list = {}
           
        for line in output.splitlines():
            if line.startswith('Zone is'):
                continue
            group, user = line.split(':')
            if not group == user:
                if group in group_list:
                    group_list[group].append(user)
                else:
                    group_list[group] = [ user, ]
            elif group not in group_list:
                group_list[group] = []  # empty group
             
        return group_list


    def run_iquest(self, query, format=None, zone=None, debug=False):
        """
        Runs iquest with the given string iquest_query
        
        input string iquest command
          
        return [string, string] output in separate lines
        """
    
        if not query:
            return None
   
        command = ['iquest', '--no-page']
    
        if zone:
            command.append('-z')
            command.append(zone)
    
        if format:
            command.append(format)
    
        command.append(query)
   
        (rc, output) = self.shell_command(command)
        if rc != 0 and not 'CAT_NO_ROWS_FOUND' in output[1]:
            self.logger.error('Error running %s, rc = %d' % (' '.join(command), rc))
            self.logger.error(output[1])
            return None
    
        # get rid of 'Zone is X' first line
        if zone:
            return output[0][(output[0].find('\n')+1):]
        else:
            return output[0]


    def synchronize_user_db(self, dest_groups, data, remove=False):
        """
        This function compares the source of users/groups to the destination
        and makes any changes to the destination iRODS instance to make them
        the same.
    
        Takes as input two dictionaries that are indexed by group name. Each
        dictionary entry is a list of users that are members of the group.
    
        The remove flag indicates that items that don't exist in the source zone
        should be removed from the destination. Make sure this is false if you
        want to make sure that local changes to the user DB are retained.
        """
    
        source_groups = self.getRemoteUsers()
    
        if not source_groups or dest_groups == None:
            return None
    
        #if group HBP_INCF doesn't exist, create it
        if (len(source_groups) != 0 and  "HBP_INCF" not in data["HBP_prjtome"]["groups"]):
             self.logger.info('Creating group \'HBP_INCF\'') 
             data["HBP_prjtome"]["groups"]["HBP_INCF"] = []
    
        # remove users that don't exist in IDS's ids-user group
        if remove:
            self.logger.info('Removing users that have been removed from \'ids-user\'...') 
            for user in dest_groups:
                zone_user = user.replace('#incf','')
                if zone_user not in source_groups['ids-user']:
                    data["HBP_prjtome"]["groups"]["HBP_INCF"].remove(user)
                    self.logger.debug('\tremoved user %s' % (user,)) 
    
        # Additions
        # add users from ids-user that don't exist locally
        self.logger.info('Adding new users from \'ids-user\'...') 
        source_groups['ids-user'].append('irods')
        for user in source_groups['ids-user']:
            if (user + '#incf') not in dest_groups:
                zone_user = user + '#incf'
                data["HBP_prjtome"]["groups"]["HBP_INCF"].append(zone_user)
                self.logger.debug('\tadded new user %s' % (zone_user,)) 
    
        return data
    

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
