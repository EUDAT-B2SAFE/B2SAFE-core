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

    def __init__(self, home_dir='/', logger_parent=None, debug=False):
        """initialize the object"""
        
        if logger_parent: 
            self.logger = logger_parent
        else: 
            logger_name = "IrodsUtils"
            self.logger = logging.getLogger(logger_name)
        self.irods_home_dir = home_dir
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def getFile(self, path):
        """get file content"""

        (rc, out) = self.execute_icommand(["iget", path, '-'])
        return out

    def getMetadata(self, path, key):
        """get file metadata"""
 
        option = '-C'
        query = "SELECT COLL_NAME WHERE COLL_NAME = '" + path + "'"
        (rc, out) = self.queryIrodsIcat(query)
        if out.startswith('CAT_NO_ROWS_FOUND'):
            option = '-d'

        (rc, out) = self.execute_icommand(["imeta", "ls", option, path, "PID"])
        if out:
            metadata = {}
            lines = out.splitlines()
            for line in lines:
                self.logger.debug('line: ' + line)
                if line.startswith('AVUs defined for'):
                    continue
                if line.startswith('None'):
                    break
                (name, value) = line.split(': ')
                if name.strip() == 'attribute':
                    last_key = value.strip()
                    if last_key == key:
                        metadata[key] = None
                if name.strip() == 'value' and last_key == key:
                    metadata[key] = value.strip()
                    
            return metadata

        return None

    def getChecksum(self, path):
        """get file checksum"""

        query = "SELECT COLL_NAME WHERE COLL_NAME = '" + path + "'"
        (rc, out) = self.queryIrodsIcat(query)
        if out.startswith('CAT_NO_ROWS_FOUND'):
            (rc, out) = self.execute_icommand(["ichksum", path])
            if out: 
                result = out.split()
                file_checksum = result[1]
                self.logger.debug('checksum: ' + file_checksum)
                return file_checksum.strip()

        return None

    def getOwners(self, path):
        """get file owners"""
     
        opt_clause = ""
        field_name = "COLL_OWNER_NAME"
        parent = path
        query = "SELECT COLL_NAME WHERE COLL_NAME = '" + path + "'"
        (rc, out) = self.queryIrodsIcat(query)
        if out.startswith('CAT_NO_ROWS_FOUND'):
            self.logger.debug('The path is a file')
            (parent, child) = path.rsplit('/',1)
            opt_clause = "AND DATA_NAME = '" + child + "'"
            field_name = "USER_NAME"
        query = ("SELECT " + field_name + " WHERE COLL_NAME = '" + parent  
              + "' AND DATA_ACCESS_NAME = 'own' " + opt_clause)
        (rc, out1) = self.queryIrodsIcat(query)
        if out1 and not out1.startswith('CAT_NO_ROWS_FOUND'):
            owners = []
            lines = out1.splitlines()
            for line in lines:
                if line.startswith('-----------------------------------------'):
                    continue
                else:
                    (attr, value) = line.split('=')
                    owners.append(value.strip())
            return owners

        return None

    def getResources(self, path):
        """get the resources of the file"""

        query = "SELECT COLL_NAME WHERE COLL_NAME = '" + path + "'"
        (rc, out) = self.queryIrodsIcat(query)
        if out.startswith('CAT_NO_ROWS_FOUND'):
            (parent, child) = path.rsplit('/',1)
            query = ("SELECT RESC_NAME WHERE COLL_NAME = '" + parent
                  + "' AND DATA_NAME = '" + child + "'")
            (rc1, out1) = self.queryIrodsIcat(query)
            if out1 and not out1.startswith('CAT_NO_ROWS_FOUND'):
                resources = []
                lines = out1.splitlines()
                for line in lines:
                    if line.startswith('-----------------------------------------'):
                        continue
                    else:
                        (attr, value) = line.split('=')
                        resources.append(value.strip())
                return resources
        return None

    def queryIrodsIcat(self, query):
        """query the iRODS DB"""

        (rc, out) = self.execute_icommand(["iquest", query])
        return (rc, out)

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
            return -1, [None, None]
