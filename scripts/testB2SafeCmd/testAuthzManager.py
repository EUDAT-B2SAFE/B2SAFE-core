import unittest
from authZmanager import AuthZClient

__author__ = 'lphan'


class AuthzManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.authzmap = self._getauthzmap()

    def tearDown(self):
        pass

    def _getauthzmap(self):
        fobj = open("testB2SafeCmd.conf", "r")
        lines = fobj.readlines()
        for line in lines:
            if line.find('AUTHZ_MAP') > -1:
                authzmap = line.split()
        fobj.close()
        return authzmap[1]

    def test_case(self):
        print "Path of Authzmap =", self.authzmap
        authzclient = AuthZClient(self.authzmap, "-d")
        authzclient.parse()

        print
        print "Test Case:"
        self.assertTrue(authzclient.checkauth('testuser#testzone',
                        'epicclient2beta.py', '* delete *',
                        'path/to/creds'))