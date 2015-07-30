import unittest
import mock
import httplib2
import base64
import os.path
import sys

sys.path.append("../../cmd") 
import epicclient

TEST_RESOURCES_PATH = '../tests/resources/'    # Trailing '/' is required
CRED_STORE = 'os'
CRED_FILENAME = 'epic_credentials_example'
MOCK_CONTENT_BASENAME = 'epic_srv_content-'

class EpicClientAPITestCase(unittest.TestCase):

    def setUp(self):
        """Setup testB2SafeCmd environment before the tests have run."""
        self.cred = epicclient.Credentials(
          CRED_STORE, TEST_RESOURCES_PATH+CRED_FILENAME)
        self.cred.parse()
        patcher = mock.patch('epicclient.httplib2.Http')
        self.MockHttp = patcher.start()
        self.addCleanup(patcher.stop)
        self.client = epicclient.EpicClient(self.cred)


    def tearDown(self):
        """Cleanup testB2SafeCmd environment after the tests have run."""
        
        
    def test_search_handle_by_key(self):
        """Test that search by existing key returns matching handle.
        
        Example result from non-mocked HTTP request:
        -- response={'date': 'Thu, 30 Jul 2015 02:11:12 GMT', 
                     'transfer-encoding': 'chunked',
                     'status': '200', 
                     'content-type': 'application/json', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/?URL=http://www.testB2SafeCmd.com/1'}
        -- content=(see resources/epic_srv_content-search_handle_by_key)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(200)
        mock_content = self.build_content('search_handle_by_key')
        mock_http.request.return_value = mock_response, mock_content
        key = 'URL'
        value = 'http://www.testB2SafeCmd.com/1'
        suffix = '/TEST_CR1'
        result = self.client.searchHandle(self.cred.prefix, key, value)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, key, value, '')
        hdrs = self.build_headers('SEARCH')
        mock_http.request.assert_called_once_with(
            uri, method='GET', headers=hdrs)
        self.assertEqual(result, self.cred.prefix + suffix,
                         "search existing handle by key returns unexpected response")
        
        
    def test_search_handle_by_non_existing_key(self):
        """Test that search handle by non existing key returns 'empty'.
        
        Example result from non-mocked HTTP request:
        -- response={'date': 'Thu, 30 Jul 2015 12:53:02 GMT', 
                     'transfer-encoding': 'chunked', 
                     'status': '200', 
                     'content-type': 'application/json', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/?FOO=BAR'}
        -- content=[]
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(200)
        mock_content = '[]'
        mock_http.request.return_value = mock_response, mock_content
        key = 'FOO'
        value = 'BAR'
        result = self.client.searchHandle(self.cred.prefix, key, value)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, key, value, '')
        hdrs = self.build_headers('SEARCH')
        mock_http.request.assert_called_once_with(
            uri, method='GET', headers=hdrs)
        self.assertEqual(result, 'empty',
                         'search existing handle by non existing key should return \"empty\"')
    
    
    def test_search_non_existing_handle_by_key(self):
        """Test that search non existing handle by key returns 'empty'.
        
        Example result from non-mocked HTTP request:
        -- response={'date': 'Thu, 30 Jul 2015 12:53:02 GMT', 
                     'transfer-encoding': 'chunked', 
                     'status': '200', 
                     'content-type': 'application/json', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/?FOO=BAR'}
        -- content=[]
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(200)
        mock_content = '[]'
        mock_http.request.return_value = mock_response, mock_content
        key = 'FOO'
        value = 'BAR'
        result = self.client.searchHandle(self.cred.prefix, key, value)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, key, value, '')
        hdrs = self.build_headers('SEARCH')
        mock_http.request.assert_called_once_with(
            uri, method='GET', headers=hdrs)
        self.assertEqual(result, 'empty',
                         'search non existing handle by key should return \"empty\"')
      
        
    def test_retrieve_non_existing_handle(self):
        """Test that retrieve non existing handle returns None.
        
        Example result from non-mocked HTTP request:
        -- response={'date': 'Wed, 29 Jul 2015 09:48:26 GMT', 
                  'status': '404', 'content-length': '2127'}
        -- content=(see resources/epic_srv_content-retrieve_non_existing_handle)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(404)
        mock_content = self.build_content('retrieve_non_existing_handle')
        mock_http.request.return_value = mock_response, mock_content
        result = self.client.retrieveHandle(self.cred.prefix + '/TEST_CR1')
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', 'TEST_CR1')
        hdrs = self.build_headers('READ')
        mock_http.request.assert_called_once_with(
            uri, method='GET', headers=hdrs)
        self.assertIsNone(result,
                          'retrieve non existing handle should return None')
        
    
    def test_get_value_from_handle(self):
        """Test that get existing key from handle returns mapped value.
        
        Example result from non-mocked HTTP request:
        -- response={'status': '200', 
                  'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 
                  'transfer-encoding': 'chunked', 
                  'last-modified': 'Wed, 29 Jul 2015 11:29:28 GMT', 
                  'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                  'date': 'Wed, 29 Jul 2015 11:29:29 GMT', 
                  'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(200)
        mock_content = self.build_content('retrieve_handle')
        mock_http.request.return_value = mock_response, mock_content
        key = 'URL'
        suffix = 'TEST_CR1'
        result = self.client.getValueFromHandle(
            self.cred.prefix, key, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('READ')
        mock_http.request.assert_called_once_with(
            uri, method='GET', headers=hdrs)
        self.assertEqual(result, 'http://www.testB2SafeCmd.com/1',
                         'get existing value from handle returns unexpected response')
    
        
    def test_get_non_existing_value_from_handle(self):
        """Test that get non existing value from handle returns None.
        
        Example result from non-mocked HTTP request:
        -- response={'status': '200', 
                  'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 
                  'transfer-encoding': 'chunked', 
                  'last-modified': 'Wed, 29 Jul 2015 11:29:28 GMT', 
                  'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                  'date': 'Wed, 29 Jul 2015 11:29:29 GMT', 
                  'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(200)
        mock_content = self.build_content('retrieve_handle')
        mock_http.request.return_value = mock_response, mock_content
        key = 'FOO_KEY'
        suffix = 'TEST_CR1'
        result = self.client.getValueFromHandle(
            self.cred.prefix, key, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('READ')
        mock_http.request.assert_called_once_with(
            uri, method='GET', headers=hdrs)
        self.assertIsNone(result,
                          'get non existing value handle should return None')
        
        
    def test_create_handle(self):
        """Test that create handle returns expected response.
        
        Example result from non-mocked HTTP request:
        -- response={'status': '201', 
                     'content-length': '2207', 
                     'last-modified': 'Thu, 01 Jan 1970 00:00:00 GMT', 
                     'etag': '"1B2M2Y8AsgTpgAmY7PhCfg"', 
                     'location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 'date': 'Thu, 30 Jul 2015 02:43:56 GMT'}
        -- content=(see resources/epic_srv_content-create_handle)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(
          201,
          location='https://epic.service.eu/api/v2/handles/90210/TEST_CR1')
        mock_content = self.build_content('create_handle')
        mock_http.request.return_value = mock_response, mock_content
        location = 'http://www.testB2SafeCmd.com/1'
        suffix = 'TEST_CR1'
        result = self.client.createHandle(self.cred.prefix, location,
                                          None, None, None, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('CREATE')
        body = self.build_body(location)
        mock_http.request.assert_called_once_with(
            uri, method='PUT', headers=hdrs, body=body)
        print result
        print str(self.cred.prefix + '/' + suffix)
        self.assertEqual(result, str(self.cred.prefix + '/' + suffix),
                         'create handle returns unexpected response')
    
    
    def test_create_existing_handle(self):
        """Test that create existing handle returns None.
        
        Example result from non-mocked HTTP request:
        -- response={'date': 'Thu, 30 Jul 2015 10:56:52 GMT', 
                     'status': '412', 
                     'content-length': '2219'}
        -- content=(see resources/epic_srv_content-create_existing_handle)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(412)
        mock_content = self.build_content('create_existing_handle')
        mock_http.request.return_value = mock_response, mock_content
        location = 'http://www.testB2SafeCmd.com/1'
        suffix = 'TEST_CR1'
        result = self.client.createHandle(self.cred.prefix, location,
                                          None, None, None, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('CREATE')
        body = self.build_body(location)
        mock_http.request.assert_called_once_with(
            uri, method='PUT', headers=hdrs, body=body)
        self.assertIsNone(result,
                          'create existing handle should return None')
        
    
    def test_delete_handle(self):
        """Test that delete existing handle returns True.
        
        Example result from non-mocked HTTP request:
        -- response={'date': 'Thu, 30 Jul 2015 09:47:49 GMT', 
                     'status': '204', 
                     'content-length': '0'}
        -- content=''
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(204)
        mock_content = ''
        mock_http.request.return_value = mock_response, mock_content
        key = ''
        suffix = 'TEST_CR1'
        result = self.client.deleteHandle(self.cred.prefix, key, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('DELETE')
        mock_http.request.assert_called_once_with(
            uri, method='DELETE', headers=hdrs)
        self.assertTrue(result,
                        'delete existing handle should return True')
    
        
    def test_delete_non_existing_handle(self):
        """Test that delete non existing handle returns False.
        
        Example result from non-mocked HTTP request:
        -- response={'date': 'Thu, 30 Jul 2015 09:12:15 GMT',
                     'status': '404', 
                     'content-length': '2127'}
        -- content=(see resources/epic_srv_content-delete_non_existing_handle)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(404)
        mock_content = self.build_content('delete_non_existing_handle')
        mock_http.request.return_value = mock_response, mock_content
        key = ''
        suffix = 'TEST_CR2'
        result = self.client.deleteHandle(self.cred.prefix, key, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('DELETE')
        mock_http.request.assert_called_once_with(
          uri, method='DELETE', headers=hdrs)
        self.assertFalse(result,
                         'delete non existing handle should return False')
        
    
    def test_delete_key_from_non_existing_handle(self):
        """Test that delete key from non existing handle returns False.
        
        Example result from non-mocked HTTP request:
        -- response={'date': 'Thu, 30 Jul 2015 10:37:25 GMT', 
                     'status': '404', 
                     'content-length': '2127'}
        -- content=(see resources/epic_srv_content-retrieve_non_existing_handle)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(404)
        mock_content = self.build_content('retrieve_non_existing_handle')
        mock_http.request.return_value = mock_response, mock_content
        key = 'FOO_KEY'
        suffix = 'TEST_CR2'
        result = self.client.deleteHandle(self.cred.prefix, key, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('READ')
        mock_http.request.assert_called_once_with(
          uri, method='GET', headers=hdrs)
        self.assertFalse(result,
                         'delete key from non existing handle should return False')
        
        
    def test_remove_location_from_non_existing_handle(self):
        """Test that remove location from non existing handle returns False.
        
        Example result from non-mocked HTTP request:
        -- response={'date': 'Thu, 30 Jul 2015 10:37:25 GMT', 
                     'status': '404', 
                     'content-length': '2127'}
        -- content=(see resources/epic_srv_content-retrieve_non_existing_handle)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(404)
        mock_content = self.build_content('retrieve_non_existing_handle')
        mock_http.request.return_value = mock_response, mock_content
        value = '846/157c344a-0179-11e2-9511-00215ec779a8'
        suffix = 'TEST_CR2'
        result = self.client.removeLocationFromHandle(
          self.cred.prefix, value, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('READ')
        mock_http.request.assert_called_once_with(
          uri, method='GET', headers=hdrs)
        self.assertFalse(result,
                         'remove location from non existing handle should return False')
        
        
    def build_uri(self, prefix, key, value, suffix=''):
        """Build HTTP URI for REST EPIC API call."""
        if self.cred.baseuri.endswith('/'):
            uri = self.cred.baseuri + prefix
        else:
            uri = self.cred.baseuri + '/' + prefix
        if suffix != '':
            uri += "/" + suffix
        if key != '' and value != '':
            uri += '/?' + key + '=' + value
        return uri
      
      
    def build_headers(self, action):
        """Build HTTP headers for REST EPIC API call."""
        hdrs = None
        auth = base64.encodestring(self.cred.username + ":" +
                                   self.cred.password)
        if action is "SEARCH":
            if self.cred.accept_format:
                hdrs = {'Accept': self.cred.accept_format,
                        'Authorization': 'Basic ' + auth}
        elif action is "READ":
            if self.cred.accept_format:
                hdrs = {'Accept': self.cred.accept_format,
                        'Authorization': 'Basic ' + auth}
        elif action is "CREATE":
            hdrs = {'If-None-Match': '*', 'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + auth}
        elif action is "UPDATE":
            hdrs = {'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + auth}
        elif action is "DELETE":
            hdrs = {'Authorization': 'Basic ' + auth}

        return hdrs

      
    def build_response(self, status_code, **kwargs):
        """Build response to REST EPIC API call using the supplied 
        status code.
        
        Example 404 response:
        {'date': 'Wed, 29 Jul 2015 09:24:15 GMT', 'status': '404', 'content-length': '2127'}
        """
        response = dict(kwargs)
        response['status'] = str(status_code)
        return httplib2.Response(response)
      
      
    def build_content(self, handle_request):
        """Build mock content for given handle request."""
        resource_file = os.path.normpath(
            TEST_RESOURCES_PATH + MOCK_CONTENT_BASENAME + handle_request)
        file_handle = open(resource_file, mode='rb')
        return file_handle.read().decode('utf-8')
      
    
    def build_body(self, location):
        """Build mock request body for given location."""
        body = '[{"type": "URL", "parsed_data": "%s"}, {"type": "10320/LOC", "parsed_data": "<locations><location href=\\"%s\\" id=\\"0\\"/></locations>"}]';
        return body % (location, location)
      
