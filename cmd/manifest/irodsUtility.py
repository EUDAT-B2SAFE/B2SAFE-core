#!/usr/bin/env python
# -*- python -*-
import logging
import os
import io
import subprocess
from os.path import expanduser
from irods.session import iRODSSession
from irods.models import DataObject
from irods.models import Collection
from irods.exception import DataObjectDoesNotExist
import irods.keywords as kw


class IRODS(object):
    """
    Wrapper class for iRODS session with cleanup on context exit
    """
    def __init__(self,
                 irods_config_file,
                 irods_auth_file):
        self.irods_config_file = irods_config_file
        self.irods_auth_file = irods_auth_file

    def __enter__(self):
        auth_file = self.irods_auth_file
        env_file = self.irods_config_file
        self.session = iRODSSession(irods_env_file=env_file,
                                    irods_authentication_file=auth_file)
        # self.session.connection_timeout = self.connection_timeout
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.cleanup()


##############################################################################
# iRODS Admin Utility Class #
##############################################################################
class IRODSUtils(object):
    """
    utility for irods management
    """

    def __init__(self, home_dir='/', logger_parent=None, debug=False,
                 irods_env=None):
        """initialize the object"""
        if irods_env is None:
            self.irods_env = expanduser("~/.irods/irods_environment.json")
        else:
            self.irods_env = irods_env
        self.irods_auth = os.path.join(os.path.dirname(self.irods_env),
                                       ".irodsA")
        self.user = None
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

    def getFile(self, path, resource=None):
        """get file content"""

        BLOCK_SIZE = 1024 * io.DEFAULT_BUFFER_SIZE
        if resource is None:
            options = {}
        else:
            options = {kw.DEST_RESC_NAME_KW: resource}

        with IRODS(irods_config_file=self.irods_env,
                   irods_auth_file=self.irods_auth) as session:
            obj = session.data_objects.get(path)
            result = ''
            with obj.open('r', **options) as f:
                while True:
                    chunk = f.read(BLOCK_SIZE)
                    if chunk:
                        result += chunk
                    else:
                        break
            return result

    def putFile(self, source, destination, resource=None):
        """put the file into the destination collection"""
        if resource is None:
            options = {}
        else:
            options = {kw.DEST_RESC_NAME_KW: resource}
        with IRODS(irods_config_file=self.irods_env,
                   irods_auth_file=self.irods_auth) as session:
            session.data_objects.put(source, destination, **options)

    def getMetadata(self, path, key):
        """get file metadata for object or collection"""

        with IRODS(irods_config_file=self.irods_env,
                   irods_auth_file=self.irods_auth) as session:
            try:
                session.data_objects.get(path)
                meta = session.metadata.get(DataObject, path)
            except DataObjectDoesNotExist:
                meta = session.metadata.get(Collection, path)
            if meta:
                return [m.value.strip()
                        for m in meta
                        if m.name == key]
            else:
                return None

    def getAllMetadata(self, path):
        """get all metadata for the file or collection under the path"""
        with IRODS(irods_config_file=self.irods_env,
                   irods_auth_file=self.irods_auth) as session:
            try:
                session.data_objects.get(path)
                meta = session.metadata.get(DataObject, path)
            except DataObjectDoesNotExist:
                meta = session.metadata.get(Collection, path)

            if meta:
                return {m.name.strip(): m.value.strip()
                        for m in meta}
            else:
                return None

    def getChecksum(self, path):
        """get file checksum"""
        with IRODS(irods_config_file=self.irods_env,
                   irods_auth_file=self.irods_auth) as session:
            try:
                obj = session.data_objects.get(path)
                return obj.checksum
            except Exception as e:
                self.logger.error('failed: ' + str(e))
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
 
    def deepListDir(self, path, abs_path=True):
        """List recursively the content of a directory"""
        #TODO in case of memory issue for large collections, consider to use
        # a shelve object instead of a dictionary.
        # or use generators to walk throw the collection
        def process_collection(coll, tree, abs_path):
            for collection, subcollections, objects in \
                coll.walk(topdown=True):
                if abs_path:
                    pathname = collection.path
                else:
                    pathname = os.path.basename(collection.path)
                tree[pathname] = {'__files__':
                                  [o.name for o in objects]}
                for sc in subcollections:
                    process_collection(sc,
                                       tree[pathname],
                                       abs_path)

        pathString = str(path)
        tree = {}
        with IRODS(irods_config_file=self.irods_env,
                   irods_auth_file=self.irods_auth) as session:
            coll = session.collections.get(pathString)
            process_collection(coll, tree, abs_path)
        return tree

    def listDir(self, path, abs_path=True):
        """List only the content of a directory"""
        pathString = str(path)
        self.logger.debug('Listing the path: ' + pathString)
        #TODO in case of memory issue for large collections, consider to use
        # a shelve object instead of a dictionary.
        # or use generators to walk throw the collection
        (rc, out) = self.execute_icommand(["ils", pathString])
        if out is not None:
            tree = {}
            fpath = ''
            i = 0
            lines = out.splitlines()
            if lines and len(lines) > 0:
                # split the root path in parent and child(relative or absolute)
                parent, fpath = self._pathSplit(lines[0].strip()[:-1], abs_path)
                # recursive loop over collections
                tree[fpath], ind = self._parseColl(fpath, {'__files__': []}, 
                                                   lines[1:], abs_path)

            return (rc, tree)

        return (rc, None)
    
    def _parseColl(self, parent_path, tree, lines, abs_path=True):

        i = 0
        tc = 0
        for line in lines:
            self.logger.debug('Skip function: ' + str(i) + ' < ' + str(tc))
            if i < tc:
                i += 1
                continue
            self.logger.debug('Walking through the path: ' + parent_path)
            self.logger.debug('line: ' + line)
            i += 1
            # parse the content of a single dir
            if line.startswith('  '):
                self.logger.debug('We are in the single dir')
                # the path is a collection
                if line.lstrip().startswith('C-'):
                    self.logger.debug('It is a collection')
                    coll = line.split('C- ')[1].strip()
                    parent, norm_coll = self._pathSplit(coll, abs_path)
                    # save it only if it is a subdir of the current parent 
                    # collection
                    self.logger.debug('the parent: ' + parent)
                    if parent == parent_path:
                        tree[norm_coll] = {'__files__': []}
                # the path is a file
                else:
                    self.logger.debug('It is a file')
                    # save it only if it is part of the current parent dir
                    if len(tree) == 1:
                        tree['__files__'].append(line.strip())
            # enter inside a new dir
            else:
                self.logger.debug('We are in a different dir')
                parent, fpath = self._pathSplit(line.strip()[:-1], abs_path)
                # parse the subdir
                self.logger.debug('the parent: ' + parent + ', the fpath: ' +fpath)
                if fpath in tree:
                    self.logger.debug('fpath is in the tree')
                    tree[fpath], counter = self._parseColl(fpath, tree[fpath], 
                                                           lines[i:], abs_path)
                    self.logger.debug('counter is :' + str(counter))
                    tc = counter + i
                    self.logger.debug('total counter is :' + str(tc))
                # return if it is not a subdir
                else:
                    self.logger.debug('fpath is not in the tree')
                    return tree, i-2

        return tree, i-2    


    def _pathSplit(self, path, absolute=True):

        parent, child = (path.rsplit('/',1))
        if absolute:
            fpath = parent+'/'+child
        else:
            fpath = child
            grand, parent = parent.rsplit('/',1)
        return (parent, fpath)
 

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

        d = dict(os.environ)
        if self.user is not None:
            d['clientUserName'] = self.user
        try:
            process = subprocess.Popen(command_list, env=d, 
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            (out, err) = process.communicate()
            return (process.returncode, [err, out])
        except:
            return -1, [None, None]
    
    def adding_metadata(self, iRODSobject, metadataAttributeName, metadataAttributeValue):
        """Add metadata to iRODSobject with metadataAttributeName and metadataAttributeValue"""
        command = [ "imeta", "set", "-d", iRODSobject, metadataAttributeName, metadataAttributeValue ] 
        (rc, out) = self.execute_icommand(command)
        return (rc, out)

    def setUser(self, user):
        """Set the environment variable 'clientUserName' for the icommands"""

        self.user = user


    def unsetUser(self):
        """Unset the environment variable 'clientUserName'"""

        self.user = None
