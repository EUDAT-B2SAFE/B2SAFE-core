import unittest

from epicclient2beta import Credentials, EpicClient


class EpicClientTestCase(unittest.TestCase):

    def setUp(self):
        """Setup testB2SafeCmd environment before the tests have run"""
        self.cred = self._getcredinstance()

    def tearDown(self):
        """ Cleanup testB2SafeCmd environment after the tests have run
        """
        pass

    def _getcredinstance(self):
        fobj = open("testB2SafeCmd.conf", "r")
        lines = fobj.readlines()
        for line in lines:
            if line.find('CREDENTIAL_PATH') > -1:
                credpath = line.split()
        fobj.close()

        credentials = Credentials('os', credpath[1])
        credentials.parse()
        return credentials

    # # Test-Case 1 , getValuefromHandle, expected Value = None
    # def test_case1(self):
    #     """
    #     :return:
    #     """
    #     credentials = self._getcredinstance()
    #     client = EpicClient(credentials)
    #     self.assertIsNone(client.getValueFromHandle(credentials.prefix, "FOO",
    #                       "NON_EXISTING"))

    # Test-Case 2 , create Handle, retrieve Handle (with URL), modify Handle
    def test_case(self):
        """
        :return:
        """
        # credentials = self._getcredinstance()
        credentials = self.cred
        client = EpicClient(credentials)

        # Test retrieve unexisting Handle
        print
        print ("Retrieving Value of FOO from " + credentials.prefix +
               "/NONEXISTING (should be None)")
        self.assertIsNone(client.getValueFromHandle(credentials.prefix, "FOO",
                          "NON_EXISTING"))

        # Test create Handle
        print
        print ("Creating handle " + credentials.prefix +
               "/TEST_CR1 (should be prefix + '/TEST_CR1')")
        self.assertEqual(client.createHandle(credentials.prefix,
                                             "http://www.testB2SafeCmd.com/1",
                                             None, None, "TEST_CR1"),
                         credentials.prefix + "/TEST_CR1")

        # Test retrieve Handle
        print
        print "Retrieving handle info from " + credentials.prefix + "/TEST_CR1"
        self.assertIsNotNone(client.retrieveHandle(credentials.prefix +
                             "/TEST_CR1"))

        print
        print "Retrieving handle by url"
        self.assertEqual(client.searchHandle(credentials.prefix, "URL",
                         "http://www.testB2SafeCmd.com/1"),
                         credentials.prefix+"/TEST_CR1")

        # Test modify Handle
        print
        print ("Modifying handle info from " + credentials.prefix +
               "/TEST_CR1 (should be True)")
        self.assertTrue(client.modifyHandle(credentials.prefix, "uri",
                        "http://www.testB2SafeCmd.com/2", "TEST_CR1"))

        print
        print ("Retrieving Value of EMAIL from " + credentials.prefix +
               "/TEST_CR1 (should be None)")
        self.assertIsNone(client.getValueFromHandle(credentials.prefix, "EMAIL",
                                                    "TEST_CR1"))

        print
        print ("Adding new field EMAIL " + credentials.prefix + "/TEST_CR1 "
               "(should be True)")
        self.assertTrue(client.modifyHandle(credentials.prefix, "EMAIL",
                                            "testB2SafeCmd@te.st", "TEST_CR1"))

        print
        print ("Retrieving Value of EMAIL from " + credentials.prefix +
               "/TEST_CR1 (should be testB2SafeCmd@te.st)")
        self.assertEqual(client.getValueFromHandle(credentials.prefix,
                         "EMAIL", "TEST_CR1"), "testB2SafeCmd@te.st")

        print
        print ("Updating handle info with a new 10320/loc type location "
               "846/157c344a-0179-11e2-9511-00215ec779a8")
        print "(should be True)"
        self.assertTrue(client.updateHandleWithLocation(credentials.prefix,
                        "846/157c344a-0179-11e2-9511-00215ec779a8", "TEST_CR1")
                        )

        print
        print ("Updating handle info with a new 10320/loc type location "
               "846/157c344a-0179-11e2-9511-00215ec779a9")
        print "(should be True)"
        self.assertTrue(client.updateHandleWithLocation(credentials.prefix,
                        "846/157c344a-0179-11e2-9511-00215ec779a9", "TEST_CR1")
                        )

        print
        print "Retrieving handle info from " + credentials.prefix + "/TEST_CR1"
        print client.retrieveHandle(credentials.prefix + "/TEST_CR1")
        self.assertIsNotNone(client.retrieveHandle(credentials.prefix +
                                                   "/TEST_CR1"))

        print
        print ("Deleting field EMAIL parameter from " + credentials.prefix +
               "/TEST_CR1 (should be True)")
        self.assertTrue(client.deleteHandle(credentials.prefix, "EMAIL",
                                            "TEST_CR1"))

        print
        print ("Retrieving Value of EMAIL from " + credentials.prefix +
               "/TEST_CR1 (should be None)")
        self.assertIsNone(client.getValueFromHandle(credentials.prefix, "EMAIL",
                          "/TEST_CR1"))

        print
        print ("Updating handle info with a new 10320/loc type location "
               "846/157c344a-0179-11e2-9511-00215ec779a8")
        print "(should be False)"
        self.assertFalse(client.updateHandleWithLocation(credentials.prefix,
                         "846/157c344a-0179-11e2-9511-00215ec779a8", "TEST_CR1")
                         )

        print
        print ("Removing 10320/loc type location "
               "846/157c344a-0179-11e2-9511-00215ec779a8")
        print "(should be True)"
        self.assertTrue(client.removeLocationFromHandle(credentials.prefix,
                        "846/157c344a-0179-11e2-9511-00215ec779a8", "TEST_CR1")
                        )

        print
        print ("Removing 10320/loc type location "
               "846/157c344a-0179-11e2-9511-00215ec779a8")
        print "(should be False)"
        self.assertFalse(client.removeLocationFromHandle(credentials.prefix,
                         "846/157c344a-0179-11e2-9511-00215ec779a8", "TEST_CR1")
                         )

        print
        print "Retrieving handle info from " + credentials.prefix + "/TEST_CR1"
        print client.retrieveHandle(credentials.prefix, "TEST_CR1")
        self.assertIsNotNone(client.retrieveHandle(credentials.prefix,
                                                   "TEST_CR1"))

        print
        print "Deleting handle " + credentials.prefix + "/TEST_CR1 " \
                                                        "(should be True)"
        self.assertTrue(client.deleteHandle(credentials.prefix, "", "TEST_CR1")
                        )

        print
        print "Deleting (again) " + credentials.prefix + "/TEST_CR1 " \
              "(should be False)"
        self.assertFalse(client.deleteHandle(credentials.prefix, "", "TEST_CR1")
                         )

        print
        print ("Retrieving handle info from non existing " + credentials.prefix
               + "/TEST_CR1 (should be None)")
        self.assertIsNone(client.retrieveHandle(credentials.prefix, "TEST_CR1")
                          )
