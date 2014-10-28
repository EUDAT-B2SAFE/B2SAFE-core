import unittest
import sys
import argparse

sys.path.append("../../cmd") 
import epicclient


class EpicClientTestCase(unittest.TestCase):

    def setUp(self):
        """Setup testB2SafeCmd environment before the tests have run"""
        pass

    def tearDown(self):
        """ Cleanup testB2SafeCmd environment after the tests have run
        """
        pass

    def test_case(self):
        """
        :return:
        """
        args = argparse.Namespace()
        args.credstore = 'os'
        args.credpath = '../../conf/credentials'
        epicclient.test(args)
