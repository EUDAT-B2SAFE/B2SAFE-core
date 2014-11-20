#!/usr/bin/env python
# -*- python -*-

import subprocess
import logging


##############################################################################
# iRODS Admin Utility Class #
##############################################################################

class IRODSUtils():
    """ 
    utility for irods management
    """
    

    def __init__(self, home_dir, logger_parent=None, debug=False):
        """initialize the object"""
        
        if logger_parent: logger_name = logger_parent + ".IrodsUtils"
        else: logger_name = "IrodsUtils"
        self.logger = logging.getLogger(logger_name)
        self.irods_home_dir = home_dir
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        

    def getIrodsZones(self):
        """get the federated zones and their attributes"""

        (rc, out) = self.execute_icommand(["iadmin", "lz"])
        if out:
            zones = {}
            for line in out.splitlines():
                zone = {}
                (rc2, out2) = self.execute_icommand(["iadmin", "lz", line])
                if out2:
                # store only the zone type (remote or local)
                    for row in out2.splitlines():
                        tuple = row.split(':')
                        if (tuple[0] == 'zone_type_name'):
                            zone['zone_type'] = (tuple[1]).strip()
                            zones[line] = zone

            return zones
        
        return None


    def listIrodsGroups(self):
        """list the iRODS groups"""

        (rc, out) = self.execute_icommand(["iadmin", "lg"])
        return out


    def getIrodsGroup(self,group):
        """list info related to a single iRODS group"""
        
        (rc, out) = self.execute_icommand(["iadmin", "lg", group])
        return out


    def getIrodsUser(self,user):
        """list info related to a single iRODS user"""

        (rc, out) = self.execute_icommand(["iadmin", "lu", user])
        return out


    def listIrodsUsers(self):
        """list the iRODS users"""

        (rc, out) = self.execute_icommand(["iadmin", "lu"])
        return out


    def createIrodsUsers(self, user):
        """create iRODS users"""

        (rc, out) = self.execute_icommand(["iadmin", "mkuser", user, "rodsuser"])
        return (rc, out)


    def listIrodsUserQuota(self, user):
        """list iRODS user quota"""

        (rc, out) = self.execute_icommand(["iadmin", "lq", user])
        if out:
            for line in out.splitlines():
                if (line.startswith('quota_limit')):
                    tuple = line.split(':')
                    quota_limit = (tuple[1]).strip()
                    break
            else:
                quota_limit = 0
            return int(quota_limit)
        else:
            return None

    
    def setIrodsUserQuota(self, user, quota):
        """set iRODS user quota"""

        (rc, out) = self.execute_icommand(["iadmin", "suq", user, 'total', quota])
        return out


    def addIrodsUserToGroup(self, user, proj_name):
        """add iRODS user to a group"""

        (rc, out) = self.execute_icommand(["iadmin", "atg", proj_name, user])
        return out


    def addDNToUser(self, user, dn):
        """add DN to a user"""

        (rc, out) = self.execute_icommand(["iadmin", "aua", user, dn])
        return out


    def removeUserDN(self, user, dn):
        """remove DN from a user"""

        (rc, out) = self.execute_icommand(["iadmin", "rua", user, dn])
        return out


    def getUserDN(self, user):
        """get DN for a user"""

        (rc, out) = self.execute_icommand(["iadmin", "lua", user])
        return out


    def createIrodsGroup(self, proj_name):
        """create iRODS group"""

        (rc, out) = self.execute_icommand(["iadmin", "mkgroup", proj_name])
        if (rc != 0): return False
        else: return True


    def queryIrodsIcat(self, query):
        """query the iRODS DB"""

        (rc, out) = self.execute_icommand(["iquest", query])
        return (rc, out)


    def deleteGroupHome(self,group_name):
        """delete the home of the irods group without deleting the group"""

        (rc1, out1) = self.execute_icommand(["ienv"])
        if out1:
            for row in out1.splitlines():
                triplet = row.split(':')
                duplet = (triplet[1].strip()).split('=')
                if (duplet[0] == 'irodsUserName'):
                    irods_admin_user = duplet[1]

        (rc, out) = self.execute_icommand(["ichmod", "-Mr", "own", 
                                           irods_admin_user, 
                                           self.irods_home_dir + group_name])
        if (rc != 0):
            (rc2, out2) = self.execute_icommand(["irm", "-r", 
                                                 self.irods_home_dir + group_name])
            if (rc2 != 0): return False
            else: return True
        else:
            return False


    def execute_icommand(self, command):
        """Execute a shell command and manage error conditions"""
    
        (rc, output) = self._shell_command(command)
        if rc != 0:
            self.logger.error('Error running %s, rc = %d' % (' '.join(command),
                                                             rc))
            self.logger.error("output: %s", output[1])
            if output[0] is not None and len(output[0].strip()) > 0:
                self.logger.error("error message: %s", output[0])
            return (rc, None)
        
        self.logger.debug('executed %s, rc = %d' % (' '.join(command), rc))
        self.logger.debug('output: %s', output[1])
        return (rc, output[1])


    def _shell_command(self, command_list):
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
            (out, err) = process.communicate()
            return (process.returncode, [err, out])
        except:
            return (-1, [None, None])
