import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import os
import os.path

sys.path.append("../../cmd") 
import epicclient

TEST_RESOURCES_PATH = '../tests/resources/'    # Trailing '/' is required
CRED_STORE = 'os'
CRED_FILENAME = 'epic_credentials'
CRED_PATH = TEST_RESOURCES_PATH+CRED_FILENAME

@unittest.skipUnless(os.path.isfile(CRED_PATH) and os.access(CRED_PATH, os.R_OK), 
                     'requires EPIC credentials file at %s' % CRED_FILENAME)
class EpicClientIntegrationTests(unittest.TestCase):

    def setUp(self):
        """Setup testB2SafeCmd environment before the tests have run"""
        self.cred = epicclient.Credentials(
            CRED_STORE, TEST_RESOURCES_PATH+CRED_FILENAME)
        self.cred.parse()
        self.client = epicclient.EpicClient(self.cred)


    def tearDown(self):
        """ Cleanup testB2SafeCmd environment after the tests have run
        """
        self.client.deleteHandle(self.cred.prefix, '', 'TEST_CR1')

    
    def test_search_handle_by_key_value(self):
        """Test that search by key-value returns matching handle."""
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, None, None, 'TEST_CR1')
        result = self.client.searchHandle(
            self.cred.prefix, 'URL', 'http://www.testB2SafeCmd.com/1')
        self.assertEqual(
            result, self.cred.prefix + '/TEST_CR1',
            'search existing handle by key returns unexpected response')
        
        
    def test_search_handle_by_non_existing_key_value(self):
        """Test that search handle by non existing key-value returns
        'empty'.
        """
        result = self.client.searchHandle(
            self.cred.prefix, 'FOO_KEY', 'FOO_BAR')
        self.assertEqual(
            result, 'empty',
            'search handle by non existing key-value should return \"empty\"')
        
        
    def test_retrieve_non_existing_handle(self):
        """Test that retrieve non existing handle returns None."""
        result = self.client.retrieveHandle(
            self.cred.prefix + "/TEST_CR1")
        self.assertIsNone(
          result,
          "retrieve non existing handle should return None")
        
    
    def test_get_value_from_handle(self):
        """Test that get value by key returns stored handle value."""
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, None, None, 'TEST_CR1')
        result = self.client.getValueFromHandle(self.cred.prefix, 'URL', 
                                                'TEST_CR1')
        self.assertEqual(
            result, 'http://www.testB2SafeCmd.com/1',
            'get existing value from handle returns unexpected response')
    
    
    def test_get_non_existing_value_from_handle(self):
        """Test that get value by non existing key returns None."""
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, None, None, 'TEST_CR1')
        result = self.client.getValueFromHandle(self.cred.prefix, 'FOO_KEY', 
                                                'TEST_CR1')
        self.assertIsNone(
            result,
            'get value by non existing key should return None')
        
    
    def test_create_handle(self):
        """Test that create handle returns expected response and adds
        new handle.
        """
        create_result = self.client.createHandle(
            self.cred.prefix, 'http://www.testB2SafeCmd.com/1', None, None,
            None, 'TEST_CR1')
        self.assertEqual(
            create_result, str(self.cred.prefix + '/TEST_CR1'),
            'create handle returns unexpected response')
        search_result = self.client.searchHandle(
            self.cred.prefix, 'URL', 'http://www.testB2SafeCmd.com/1')
        self.assertEqual(search_result, create_result,
                         'create handle should add new handle')
        
        
        
    def test_create_handle_with_checksum(self):
        """Test that create handle with checksum returns expected 
        response and adds new handle with supplied checksum.
        """
        checksum = '1cb285b'
        create_result = self.client.createHandle(
            self.cred.prefix, 'http://www.testB2SafeCmd.com/1', checksum, 
            None, None, 'TEST_CR1')
        self.assertEqual(
            create_result, str(self.cred.prefix + "/TEST_CR1"),
            "create handle with checksum returns unexpected response")
        search_result = self.client.searchHandle(
            self.cred.prefix, 'CHECKSUM', checksum)
        self.assertEqual(search_result, create_result,
                         'create handle with checksum should add new handle')
        
        
    def test_create_handle_with_extra_key(self):
        """Test that create handle with extra key returns expected 
        response and adds new handle with supplied key value.
        """
        extra_key = 'EMAIL'
        extra_value = 'user@testB2SafeCmd.com'
        create_result = self.client.createHandle(
            self.cred.prefix, 'http://www.testB2SafeCmd.com/1', None, 
            [str(extra_key+'='+extra_value)], None, 'TEST_CR1')
        self.assertEqual(
            create_result, str(self.cred.prefix + "/TEST_CR1"),
            "create handle with extra key returns unexpected response")
        search_result = self.client.searchHandle(
            self.cred.prefix, extra_key, extra_value)
        self.assertEqual(search_result, create_result,
                         'create handle with extra key should add new handle')
        
        
    def test_create_handle_with_extra_location(self):
        """Test that create handle with extra location returns expected 
        response and adds new handle with supplied locations.
        """
        location_key = '10320/LOC'
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        create_result = self.client.createHandle(
            self.cred.prefix, 'http://www.testB2SafeCmd.com/1', None, 
            None, [extra_location], 'TEST_CR1')
        self.assertEqual(
            create_result, str(self.cred.prefix + "/TEST_CR1"),
            "create handle with extra location returns unexpected response")
        retrieve_result = self.client.getValueFromHandle(
            self.cred.prefix, location_key, 'TEST_CR1')
        self.assertIn(extra_location, retrieve_result,
                         'create handle with extra location should add new handle')
   
   
    def test_create_existing_handle(self):
        """Test that create existing handle returns None."""
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, None, None, 'TEST_CR1')
        result = self.client.createHandle(self.cred.prefix, 
                                          'http://www.testB2SafeCmd.com/1',
                                          None, None, None, 'TEST_CR1')
        self.assertIsNone(result,
                          'create handle returns unexpected response')
        
    
    def test_modify_handle_key_value(self):
        """Test that modify handle value returns True and updates 
        stored value.
        """
        key = 'URL'
        value_before = 'http://www.testB2SafeCmd.com/1'
        value_after = 'http://www.testB2SafeCmd.com/2'
        self.client.createHandle(self.cred.prefix, value_before, None, None,
                                 None, 'TEST_CR1')
        modify_result = self.client.modifyHandle(
            self.cred.prefix, key, value_after, 'TEST_CR1')
        self.assertTrue(modify_result, 
                        'modify handle value should return True')
        get_value_result = self.client.getValueFromHandle(
            self.cred.prefix, key, 'TEST_CR1')
        self.assertEqual(get_value_result, value_after,
                         'modify handle value failed to update value')
        
        
    def test_modify_handle_new_key_value(self):
        """Test that modify existing handle with new key-value pair
        returns True and updates stored handle.
        """
        key = "EMAIL"
        value = 'user@testB2SafeCmd.com'
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, None, None, 'TEST_CR1')
        modify_result = self.client.modifyHandle(
            self.cred.prefix, key, value, 'TEST_CR1')
        self.assertTrue(
            modify_result,
            'modify existing handle with new key-value should return True')
        get_value_result = self.client.getValueFromHandle(
            self.cred.prefix, key, 'TEST_CR1')
        self.assertEqual(
            get_value_result, value,
            'modify existing handle with new key-value should update value')
        
        
    def test_modify_handle_with_empty_value(self):
        """Test that modify existing handle key with empty value
        returns True and updates stored value accordingly.
        """
        key = "EMAIL"
        value_before = 'user@testB2SafeCmd.com'
        value_after = ''
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, [str(key+'='+value_before)], 
                                 None, "TEST_CR1")
        modify_result = self.client.modifyHandle(
            self.cred.prefix, key, value_after, 'TEST_CR1')
        self.assertTrue(
            modify_result,
            'modify existing handle key with empty value should return True')
        get_value_result = self.client.getValueFromHandle(
            self.cred.prefix, key, 'TEST_CR1') 
        self.assertEqual(
            get_value_result, value_after,
            "modify existing handle key with empty value should set stored value to ''")
        
        
    def test_modify_non_existing_handle(self):
        """Test that modify value of non existing handle returns False."""
        key = "FOO_KEY"
        value = "FOO_VALUE"
        modify_result = self.client.modifyHandle(
            self.cred.prefix, key, value, 'TEST_CR1')
        self.assertFalse(modify_result,
                         'modify non existing handle should return false')
        
        
    def test_delete_handle(self):
        """Test that delete existing handle returns True."""
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, None, None, 'TEST_CR1')
        result = self.client.deleteHandle(self.cred.prefix, '', 'TEST_CR1')
        self.assertTrue(result, 'delete existing handle should return True')
        
    
    def test_delete_non_existing_handle(self):
        """Test that delete non existing handle returns False."""
        result = self.client.deleteHandle(self.cred.prefix, '', 'TEST_CR2')
        self.assertFalse(result, 'delete non existing handle should return False')
   
    
    def test_delete_key_from_handle(self):
        """Test that delete key from handle returns True."""
        key = 'EMAIL'
        value = 'user@testB2SafeCmd.com'
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1', None,
                                 [str(key+'='+value)], None, 'TEST_CR1')
        result = self.client.deleteHandle(self.cred.prefix, key, 'TEST_CR1')
        self.assertTrue(result, 
                        'delete existing handle value should return True')
        
        
    def test_delete_non_existing_key_from_handle(self):
        """Test that delete non existing key from handle returns False."""
        key = 'FOO_KEY'
        result = self.client.deleteHandle(self.cred.prefix, key, 'TEST_CR1')
        self.assertFalse(result,
                         'delete key from non existing handle should return False')
        
   
    def test_update_handle_with_location(self):
        """Test that update handle with new location returns True and 
        persists new value.
        """
        location_key = '10320/LOC'
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, None, None, 'TEST_CR1')
        update_location_result = self.client.updateHandleWithLocation(
            self.cred.prefix, extra_location, 'TEST_CR1')
        self.assertTrue(update_location_result,
                        'modify existing handle with location should return True')
        retrieve_result = self.client.getValueFromHandle(
            self.cred.prefix, location_key, 'TEST_CR1')
        self.assertIn(extra_location, retrieve_result,
                         'update handle with new location should persist new location value')
        
        
    def test_modify_existing_handle_with_same_location(self):
        """Test that update handle with same location value returns 
        False.
        """
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, None, [extra_location], 'TEST_CR1')
        result = self.client.updateHandleWithLocation(
            self.cred.prefix, extra_location, 'TEST_CR1')
        self.assertFalse(result,
                         'modify existing handle with same location value should return False')
        
        
    def test_update_non_existing_handle_with_location(self):
        """Test that update non existing handle with location returns
        False.
        """
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        result = self.client.updateHandleWithLocation(
            self.cred.prefix, extra_location, 'TEST_CR1')
        self.assertFalse(result,
                         'modify non existing handle with location should return False')
        
    def test_remove_location_from_handle(self):
        """Test that remove location from handle returns True and 
        deletes the value from the repository.
        """
        location_key = '10320/LOC'
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, None, [extra_location], 'TEST_CR1')
        remove_location_result = self.client.removeLocationFromHandle(
            self.cred.prefix, extra_location, 'TEST_CR1')
        self.assertTrue(remove_location_result,
                        'remove location from handle should return True')
        retrieve_result = self.client.getValueFromHandle(
            self.cred.prefix, location_key, 'TEST_CR1')
        self.assertNotIn(extra_location, retrieve_result,
                         'remove location from handle should delete the value from the repository')
        
        
    def test_remove_non_existing_location_from_handle(self):
        """Test that remove non existing location from handle returns 
        False.
        """
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        self.client.createHandle(self.cred.prefix, 
                                 'http://www.testB2SafeCmd.com/1',
                                 None, None, None, 'TEST_CR1')
        result = self.client.removeLocationFromHandle(
            self.cred.prefix, extra_location, 'TEST_CR1')
        self.assertFalse(result,
                         'remove non existing location from handle should return False')
        
    
    def test_remove_location_from_non_existing_handle(self):
        """Test that remove location from non existing handle returns 
        False.
        """
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        result = self.client.removeLocationFromHandle(
            self.cred.prefix, extra_location, 'TEST_CR2')
        self.assertFalse(result,
                         'remove location from non existing handle should return False')
