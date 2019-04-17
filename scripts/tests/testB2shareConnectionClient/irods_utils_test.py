import unittest
import os
from os.path import dirname
from os.path import abspath
from os.path import join
import sys
sys.path.insert(0,
                join(dirname(dirname(dirname(dirname(abspath(__file__))))),
                     "cmd"))
from manifest.irodsUtility import IRODS  # noqa: E402
from manifest.irodsUtility import IRODSUtils as IRODSUtils  # noqa: E402

ENV = None


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
            session.collections.create(self.coll_path)
            print(self.coll_path)
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
        print(remote_file)
        irodsu = IRODSUtils(irods_env=ENV)
        irodsu.putFile(testfile, remote_file)
        content = irodsu.getFile(remote_file)
        self.assertEqual(content,
                         testfile_content)
