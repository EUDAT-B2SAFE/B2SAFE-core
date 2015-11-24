import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

sys.path.append("../../cmd") 
import epicclient

class EpicClientCredentialsTestCase(unittest.TestCase):
    """Test case for EPIC Client Credentials class"""

    def setUp(self):
        """Setup testB2SafeCmd environment before the tests have run."""


    def tearDown(self):
        """Cleanup testB2SafeCmd environment after the tests have run."""
        
        
    def test_credentials(self):
        """Test Credentials creation from local file."""
        credentials = epicclient.Credentials(
            'os', '../tests/resources/epic_credentials_example')
        credentials.parse()
        self.assertIsInstance(credentials, epicclient.Credentials,
                              'Credentials constructor returns unexpected object instance')
        self.assertEqual(credentials.baseuri, 'https://epic.service.eu/api/v2/handles/',
                         'Credentials object returns unexpected base URI')
        self.assertEqual(credentials.prefix, '90210',
                         'Credentials object returns unexpected prefix')
        self.assertEqual(credentials.username, 'foobaruser',
                         'Credentials object returns unexpected username')
        self.assertEqual(credentials.password, 'bigsecret',
                         'Credentials object returns unexpected password')
        self.assertEqual(credentials.accept_format, 'application/json',
                         'Credentials object returns unexpected accept_format')
        self.assertEqual(credentials.debug, False,
                         'Credentials object returns unexpected debug')
        
        
    def test_credentials_invalid_path(self):
        """Test error when creating Credentials from invalid path."""
        with self.assertRaises(SystemExit) as cm:
            epicclient.Credentials('os', 'FOO').parse()
            self.assertEqual(cm.exception.code, 1)
            
            
    def test_credentials_irods_store(self):
        """Test error when creating Credentials from iRODS storage."""
        with self.assertRaises(SystemExit) as cm:
            epicclient.Credentials('irods', 'FOO').parse()
            self.assertEqual(cm.exception.code, 1)
            
            
    def test_credentials_invalid_store(self):
        """Test error when creating Credentials from invalid storage."""
        with self.assertRaises(SystemExit) as cm:
            epicclient.Credentials('BAR', 'FOO').parse()
            self.assertEqual(cm.exception.code, 1)
            
            
    def test_credentials_missing_prefix(self):
        """Test that prefix is set to specified username when creating
        Credentials without explicitly setting the prefix key.
        """
        credentials = epicclient.Credentials(
            'os', '../tests/resources/epic_credentials_missing_prefix')
        credentials.parse()
        self.assertIsInstance(credentials, epicclient.Credentials,
                              'Credentials constructor returns unexpected object instance')
        self.assertEqual(credentials.prefix, credentials.username)
        
        
    def test_credentials_missing_key(self):
        """Test error when creating Credentials without supplying 
        required key.
        """
        with self.assertRaises(SystemExit) as cm:
            epicclient.Credentials(
              'os', '../tests/resources/epic_credentials_missing_key').parse()
            self.assertEqual(cm.exception.code, 1)
