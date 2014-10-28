import unittest
import sys
import argparse

sys.path.append("../../cmd")
import authZmanager

__author__ = 'lphan'


class AuthzManagerTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case(self):
        
        args = argparse.Namespace()
        args.mapfilepath = 'resources/authz.map.json'
        args.debug = False
        authZmanager.test(args)