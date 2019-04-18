#!/usr/bin/env python
# -*- python -*-
import logging
import os
import io
from os.path import expanduser
from irods.session import iRODSSession
from irods.models import DataObject
from irods.models import Collection
from irods.exception import DataObjectDoesNotExist
from irods.meta import iRODSMeta
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

    def setMetadata(self, path, name, value):
        """
        Set metadata to iRODSobject with metadataAttributeName and
        metadataAttributeValue
        """
        with IRODS(irods_config_file=self.irods_env,
                   irods_auth_file=self.irods_auth) as session:
            try:
                session.data_objects.get(path)
                model = DataObject
            except DataObjectDoesNotExist:
                model = Collection
        session.metadata.set(model, path, iRODSMeta(name,
                                                    value))

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
        """
        get file owners
        :param path: path to data object or collection
        :return: list of owners
        """
        with IRODS(irods_config_file=self.irods_env,
                   irods_auth_file=self.irods_auth) as session:
            try:
                ooc = session.data_objects.get(path)
            except DataObjectDoesNotExist:
                ooc = session.collections.get(path)
            return [acl.user_name
                    for acl in session.permissions.get(ooc)
                    if acl.access_name == 'own']

    def getResources(self, path):
        """get the resources of the file"""
        with IRODS(irods_config_file=self.irods_env,
                   irods_auth_file=self.irods_auth) as session:
            obj = session.data_objects.get(path)
            return [replica.resource_name for replica in obj.replicas]

    def deepListDir(self, path, abs_path=True):
        """List recursively the content of a directory"""
        # TODO in case of memory issue for large collections, consider to use
        # a shelve object instead of a dictionary.
        # or use generators to walk throw the collection
        def process_collection(coll, tree, abs_path):
            pathname = coll.path if abs_path else os.path.basename(coll.path)
            tree[pathname] = {'__files__':
                              [o.name for o in coll.data_objects]}
            for sc in coll.subcollections:
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
        # TODO in case of memory issue for large collections, consider to use
        # a shelve object instead of a dictionary.
        # or use generators to walk throw the collection
        pathString = str(path)
        self.logger.debug('Listing the path: ' + pathString)
        tree = {}
        with IRODS(irods_config_file=self.irods_env,
                   irods_auth_file=self.irods_auth) as session:
            coll = session.collections.get(pathString)
            pathname = coll.path if abs_path else os.path.basename(coll.path)
            tree[pathname] = {'__files__':
                              [o.name for o in coll.data_objects]}
            for sc in coll.subcollections:
                subpath = sc.path if abs_path else os.path.basename(sc.path)
                tree[pathname][subpath] = {}
        return tree
