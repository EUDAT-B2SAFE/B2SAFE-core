import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import mock
import argparse

sys.path.append("../../cmd") 
import epicclient

class EpicClientCLITestCase(unittest.TestCase):

    credpath = "/foo/credentials"
    
    creds = { 
        "store": "os",
        "baseuri": "https://epic.server.eu/api/v2/handles/",
        "username": "user1", 
        "prefix": "90210",
        "accept_format": "application/json",
        "debug": True
    }

    def setUp(self):
        """Setup testB2SafeCmd environment before the tests have run."""
        self.args = argparse.Namespace()
        self.args.credstore = self.creds["store"]
        self.args.credpath = self.credpath

    def tearDown(self):
        """Cleanup testB2SafeCmd environment after the tests have run."""
        
    @mock.patch('epicclient.EpicClient')
    @mock.patch('epicclient.Credentials', **creds)
    def test_read(self, mock_creds, mock_epic_api):
        """Test that read CLI command invokes retrieveHandle API method
        when no key param is supplied.
        """
        self.args.handle = '90210//TEST_CR1'
        self.args.key = None
        epicclient.read(self.args)
        mock_creds.assert_called_once
        mock_creds.assert_called_once_with(self.creds['store'], self.credpath)
        mock_creds.parse.assert_called_once
        mock_creds_instance = mock_creds.return_value
        mock_epic_api.assert_called_once
        mock_epic_api.assert_called_once_with(mock_creds_instance)
        mock_epic_api_instance = mock_epic_api.return_value
        mock_epic_api_instance.retrieveHandle.assert_called_once
        mock_epic_api_instance.retrieveHandle.assert_called_once_with(
            self.args.handle.partition("/")[0], self.args.handle.partition("/")[2])


    @mock.patch('epicclient.EpicClient')
    @mock.patch('epicclient.Credentials', **creds)
    def test_read_with_key(self, mock_creds, mock_epic_api):
        """Test that read CLI command invokes getValueFromHandle API
        method when a key is supplied.
        """
        self.args.handle = '90210//TEST_CR1'
        self.args.key = 'FOO_KEY'
        epicclient.read(self.args)
        mock_creds.assert_called_once
        mock_creds.assert_called_once_with(self.creds['store'], self.credpath)
        mock_creds.parse.assert_called_once
        mock_creds_instance = mock_creds.return_value
        mock_epic_api.assert_called_once
        mock_epic_api.assert_called_once_with(mock_creds_instance)
        mock_epic_api_instance = mock_epic_api.return_value
        mock_epic_api_instance.getValueFromHandle.assert_called_once
        mock_epic_api_instance.getValueFromHandle.assert_called_once_with(
            '90210//TEST_CR1'.partition("/")[0], 'FOO_KEY',
            '90210//TEST_CR1'.partition("/")[2])
        
        
    @mock.patch('epicclient.EpicClient')
    @mock.patch('epicclient.Credentials', **creds)
    def test_search(self, mock_creds, mock_epic_api):
        """Test that search CLI command invokes searchHandle API
        method with the supplied prefix and key-value pair.
        """
        self.args.key = 'FOO_KEY'
        self.args.value = 'FOO_VALUE'
        epicclient.search(self.args)
        mock_creds.assert_called_once
        mock_creds.assert_called_once_with(self.creds['store'], self.credpath)
        mock_creds.parse.assert_called_once
        mock_creds_instance = mock_creds.return_value
        mock_epic_api.assert_called_once
        mock_epic_api.assert_called_once_with(mock_creds_instance)
        mock_epic_api_instance = mock_epic_api.return_value
        mock_epic_api_instance.searchHandle.assert_called_once
        mock_epic_api_instance.searchHandle.assert_called_once_with(
            mock_creds_instance.prefix, 'FOO_KEY', ' '.join('FOO_VALUE'))
        
        
    @mock.patch('epicclient.sys.stdout')
    @mock.patch('epicclient.uuid')
    @mock.patch('epicclient.EpicClient')
    @mock.patch('epicclient.Credentials', **creds)
    def test_create(self, mock_creds, mock_epic_api, mock_uuid, mock_stdout):
        """Test that create CLI command invokes createHandle API
        method with the supplied mandatory params.
        """
        mock_epic_api.return_value.createHandle.return_value = 'GREAT SUCCESS'
        mock_uuid.uuid1.return_value = 'UUID'
        self.args.location = 'http://www.testB2SafeCmd.com/1'
        self.args.checksum = '1cb285b'
        self.args.extratype = None
        self.args.loc10320 = None
        epicclient.create(self.args)
        mock_creds.assert_called_once
        mock_creds.assert_called_once_with(self.creds['store'], self.credpath)
        mock_creds.parse.assert_called_once
        mock_creds_instance = mock_creds.return_value
        mock_epic_api.assert_called_once
        mock_epic_api.assert_called_once_with(mock_creds_instance)
        mock_epic_api_instance = mock_epic_api.return_value
        mock_epic_api_instance.createHandle.assert_called_once
        mock_epic_api_instance.createHandle.assert_called_once_with(
            mock_creds_instance.prefix, 'http://www.testB2SafeCmd.com/1', 
            '1cb285b', None, None, 'UUID')
        mock_stdout.write.assert_called_once
        mock_stdout.write.assert_called_once_with('GREAT SUCCESS')
        # Test None result
        mock_epic_api.return_value.createHandle.return_value = None
        mock_stdout.reset_mock()
        epicclient.create(self.args)
        mock_stdout.write.assert_called_once
        mock_stdout.write.assert_called_once_with('error')
        
        
    @mock.patch('epicclient.uuid')
    @mock.patch('epicclient.EpicClient')
    @mock.patch('epicclient.Credentials', **creds)
    def test_create_with_extra_type(self, mock_creds, mock_epic_api, mock_uuid):
        """Test that create CLI command invokes createHandle API
        method with the supplied mandatory params and the given extra
        type.
        """
        mock_epic_api.return_value.createHandle.return_value = 'GREAT SUCCESS'
        mock_uuid.uuid1.return_value = 'UUID'
        self.args.location = 'http://www.testB2SafeCmd.com/1'
        self.args.checksum = '1cb285b'
        self.args.extratype = 'FOO_KEY=FOO_BAR'
        self.args.loc10320 = None
        epicclient.create(self.args)
        mock_creds.assert_called_once
        mock_creds.assert_called_once_with(self.creds['store'], self.credpath)
        mock_creds.parse.assert_called_once
        mock_creds_instance = mock_creds.return_value
        mock_epic_api.assert_called_once
        mock_epic_api.assert_called_once_with(mock_creds_instance)
        mock_epic_api_instance = mock_epic_api.return_value
        mock_epic_api_instance.createHandle.assert_called_once
        mock_epic_api_instance.createHandle.assert_called_once_with(
            mock_creds_instance.prefix, 'http://www.testB2SafeCmd.com/1', 
            '1cb285b', 'FOO_KEY=FOO_BAR'.split(';'), None, 'UUID')

        
    @mock.patch('epicclient.uuid')
    @mock.patch('epicclient.EpicClient')
    @mock.patch('epicclient.Credentials', **creds)
    def test_create_with_loc10320(self, mock_creds, mock_epic_api, mock_uuid):
        """Test that create CLI command invokes createHandle API
        method with the supplied mandatory params and the given 
        10320/LOC property.
        """
        mock_epic_api.return_value.createHandle.return_value = 'GREAT SUCCESS'
        mock_uuid.uuid1.return_value = 'UUID'
        self.args.location = 'http://www.testB2SafeCmd.com/1'
        self.args.checksum = '1cb285b'
        self.args.extratype = None
        self.args.loc10320 = 'FOO_LOC'
        epicclient.create(self.args)
        mock_creds.assert_called_once
        mock_creds.assert_called_once_with(self.creds['store'], self.credpath)
        mock_creds.parse.assert_called_once
        mock_creds_instance = mock_creds.return_value
        mock_epic_api.assert_called_once
        mock_epic_api.assert_called_once_with(mock_creds_instance)
        mock_epic_api_instance = mock_epic_api.return_value
        mock_epic_api_instance.createHandle.assert_called_once
        mock_epic_api_instance.createHandle.assert_called_once_with(
            mock_creds_instance.prefix, 'http://www.testB2SafeCmd.com/1', 
            '1cb285b', None, 'FOO_LOC'.split(';'), 'UUID')


    @mock.patch('epicclient.EpicClient')
    @mock.patch('epicclient.Credentials', **creds)
    def test_modify(self, mock_creds, mock_epic_api):
        """Test that modify CLI command invokes modifyHandle API
        method based on the supplied PID handle.
        """
        self.args.handle = '90210//TEST_CR1'
        self.args.key = 'FOO_KEY'
        self.args.value = 'FOO_VALUE'
        epicclient.modify(self.args)
        mock_creds.assert_called_once
        mock_creds.assert_called_once_with(self.creds['store'], self.credpath)
        mock_creds.parse.assert_called_once
        mock_creds_instance = mock_creds.return_value
        mock_epic_api.assert_called_once
        mock_epic_api.assert_called_once_with(mock_creds_instance)
        mock_epic_api_instance = mock_epic_api.return_value
        mock_epic_api_instance.modifyHandle.assert_called_once
        mock_epic_api_instance.modifyHandle.assert_called_once_with(
            '90210//TEST_CR1'.partition("/")[0], 'FOO_KEY', 'FOO_VALUE',
            '90210//TEST_CR1'.partition("/")[2])


    @mock.patch('epicclient.EpicClient')
    @mock.patch('epicclient.Credentials', **creds)
    def test_delete(self, mock_creds, mock_epic_api):
        """Test that delete CLI command invokes deleteHandle API
        method based on the supplied PID handle.
        """
        self.args.handle = '90210//TEST_CR1'
        self.args.key = 'FOO_KEY'
        epicclient.delete(self.args)
        mock_creds.assert_called_once
        mock_creds.assert_called_once_with(self.creds['store'], self.credpath)
        mock_creds.parse.assert_called_once
        mock_creds_instance = mock_creds.return_value
        mock_epic_api.assert_called_once
        mock_epic_api.assert_called_once_with(mock_creds_instance)
        mock_epic_api_instance = mock_epic_api.return_value
        mock_epic_api_instance.deleteHandle.assert_called_once
        mock_epic_api_instance.deleteHandle.assert_called_once_with(
            '90210//TEST_CR1'.partition("/")[0], 'FOO_KEY',
            '90210//TEST_CR1'.partition("/")[2])
    
    
    @mock.patch('epicclient.EpicClient')
    @mock.patch('epicclient.Credentials', **creds)
    def test_relation(self, mock_creds, mock_epic_api):
        """Test that relation CLI command invokes 
        updateHandleWithLocation API method with the supplied parent &
        child PIDs.
        """
        self.args.ppid = 'FOO_PARENT_PID'
        self.args.cpid = 'FOO_CHILD_PID'
        epicclient.relation(self.args)
        mock_creds.assert_called_once
        mock_creds.assert_called_once_with(self.creds['store'], self.credpath)
        mock_creds.parse.assert_called_once
        mock_creds_instance = mock_creds.return_value
        mock_epic_api.assert_called_once
        mock_epic_api.assert_called_once_with(mock_creds_instance)
        mock_epic_api_instance = mock_epic_api.return_value
        mock_epic_api_instance.updateHandleWithLocation.assert_called_once
        mock_epic_api_instance.updateHandleWithLocation.assert_called_once_with(
            'FOO_PARENT_PID', 'FOO_CHILD_PID')
        
        
    @mock.patch('epicclient.sys.stdout')
    def test_replaceHash(self, mock_stdout):
        """Test that replaceHash CLI command transforms the supplied 
        string as follows:
        
        - string elements joined by space separator  
        - '#' instances replaced with '*'
        - '%' instances replaced with '*'
        - '&' instances replaced with '*'
        """
        self.args.a = '#foo s%bar foo&bar'
        key = ' '.join(self.args.a)
        expected_result = key.replace('#', '*').replace('%', '*').replace('&', '*')
        epicclient.replaceHash(self.args)
        mock_stdout.write.assert_called_once
        mock_stdout.write.assert_called_once_with(expected_result)
