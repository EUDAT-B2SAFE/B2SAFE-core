import unittest
import os
import sys
from os.path import dirname
from os.path import abspath
from os.path import join
from irods.models import DataObject
from irods.models import Collection
from irods.meta import iRODSMeta
sys.path.insert(0,
                join(dirname(dirname(dirname(dirname(abspath(__file__))))),
                     "cmd"))
from manifest.irodsUtility import IRODS  # noqa: E402
from manifest.irodsUtility import IRODSUtils as IRODSUtils  # noqa: E402

ENV = "/home/stefan/.irods/servers/b2safe/irods_environment.json"


class TestIRODSUtils(unittest.TestCase):
    # functional test
    # in order to execute the test we need a valid connection to
    # an iRODS instance
    # configured in ~/.irods/irods_enviornment.json
    # getMetadata(file, PID)
    # getMetadata(user, access_token, -u)
    # getFile
    # deepListDir

    def setUp(self):
        irodsu = IRODSUtils(irods_env=ENV)
        with IRODS(irods_config_file=irodsu.irods_env,
                   irods_auth_file=irodsu.irods_auth) as session:
            self.coll_path = '/{}/home/{}/test_dir'.format(session.zone,
                                                           session.username)
            self.irods_username = session.username
            session.collections.create(self.coll_path)
            session.cleanup()

    def tearDown(self):
        '''Remove test data and close connections
        '''
        irodsu = IRODSUtils(irods_env=ENV)
        with IRODS(irods_config_file=irodsu.irods_env,
                   irods_auth_file=irodsu.irods_auth) as session:
            coll = session.collections.get(self.coll_path)
            coll.remove(recurse=True, force=True)
            session.cleanup()

    def test_put_get(self):
        testfile = os.path.join(dirname(abspath(__file__)),
                                "testfile.txt")
        with open(testfile, 'r') as fp:
            testfile_content = fp.read()
        remote_file = self.coll_path + "/TESTFILE"
        irodsu = IRODSUtils(irods_env=ENV)
        irodsu.putFile(testfile, remote_file)
        content = irodsu.getFile(remote_file)
        self.assertEqual(content,
                         testfile_content)

    def test_get_metadata(self):
        testfile = os.path.join(dirname(abspath(__file__)),
                                "testfile.txt")
        remote_file = self.coll_path + "/TESTFILE"
        irodsu = IRODSUtils(irods_env=ENV)
        irodsu.putFile(testfile, remote_file)
        with IRODS(irods_config_file=irodsu.irods_env,
                   irods_auth_file=irodsu.irods_auth) as session:
            session.metadata.add(DataObject,
                                 remote_file,
                                 iRODSMeta("attr1", "value1"))
            session.metadata.add(Collection,
                                 self.coll_path,
                                 iRODSMeta("attr2", "value2"))
        self.assertEqual(irodsu.getMetadata(remote_file, "attr1"),
                         ["value1"])
        self.assertEqual(irodsu.getMetadata(self.coll_path, "attr2"),
                         ["value2"])
        self.assertEqual(irodsu.getAllMetadata(remote_file).get('attr1'),
                         'value1')
        self.assertEqual(irodsu.getAllMetadata(self.coll_path).get('attr2'),
                         'value2')

    def test_deep_list_dir(self):
        testfile = os.path.join(dirname(abspath(__file__)),
                                "testfile.txt")
        a = '{}/a'.format(self.coll_path)
        ab = '{}/a/b'.format(self.coll_path)
        abc = '{}/a/b/c'.format(self.coll_path)
        abd = '{}/a/b/d'.format(self.coll_path)
        irodsu = IRODSUtils(irods_env=ENV)
        with IRODS(irods_config_file=irodsu.irods_env,
                   irods_auth_file=irodsu.irods_auth) as session:
            session.collections.create(a)
            session.collections.create(ab)
            session.collections.create(abc)
            session.collections.create(abd)
            session.cleanup()
        irodsu = IRODSUtils(irods_env=ENV)
        irodsu.putFile(testfile, a + "/TESTFILE")
        irodsu.putFile(testfile, ab + "/TESTFILE")
        irodsu.putFile(testfile, abc + "/TESTFILE")
        irodsu.putFile(testfile, abd + "/TESTFILE")
        result = irodsu.deepListDir(a, False)
        self.assertEqual(result, {'a': {'__files__': ['TESTFILE'],
                                        'b': {'__files__': ['TESTFILE'],
                                              'c': {'__files__':
                                                    ['TESTFILE']},
                                              'd': {'__files__':
                                                    ['TESTFILE']}}}})
        result = irodsu.listDir(a, False)
        self.assertEqual(result, {'a': {'__files__': ['TESTFILE'],
                                        'b': {}}})

    def test_get_owner(self):
        testfile = os.path.join(dirname(abspath(__file__)),
                                "testfile.txt")
        remote_file = self.coll_path + "/TESTFILE"
        irodsu = IRODSUtils(irods_env=ENV)
        irodsu.putFile(testfile, remote_file)
        owner = self.irods_username
        self.assertEqual(irodsu.getOwners(remote_file), [owner])
        self.assertEqual(irodsu.getOwners(self.coll_path), [owner])
