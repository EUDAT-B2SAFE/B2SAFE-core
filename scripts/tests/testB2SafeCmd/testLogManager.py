import unittest
import sys
import argparse

sys.path.append("../../cmd") 
import logmanager

__author__ = 'lphan'


class LogManagerTestCase(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case(self):
        
        args = argparse.Namespace()
        args.conffilepath = '../../conf/log.manager.conf'
        args.debug = False
        logmanager.test(args)