import sys
if sys.version_info < (2, 7):
    sys.path.append('/usr/lib/python2.7/site-packages')
    import unittest2 as unittest
else:
    import unittest
import mock
import httplib2
from lxml import etree 
from lxml.etree import tostring
import simplejson
import base64
import os.path

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
        body = self.build_create_body(location)
        mock_http.request.assert_called_once_with(
            uri, method='PUT', headers=hdrs, body=body)
        self.assertEqual(result, str(self.cred.prefix + '/' + suffix),
                         'create handle returns unexpected response')
    
    
    def test_create_handle_with_checksum(self):
        """Test that create handle with checksum returns expected response.
        
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
        checksum = '1cb285b'
        suffix = 'TEST_CR1'
        result = self.client.createHandle(self.cred.prefix, location,
                                          checksum, None, None, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('CREATE')
        body = self.build_create_body(location, checksum=checksum)
        mock_http.request.assert_called_once_with(
            uri, method='PUT', headers=hdrs, body=body)
        self.assertEqual(result, str(self.cred.prefix + '/' + suffix),
                         'create handle returns unexpected response')    
        
    
    def test_create_handle_with_extra_key(self):
        """Test that create handle with extra key returns expected
        response.
        
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
        extra_key = 'EMAIL'
        extra_value = 'user@testB2SafeCmd.com'
        suffix = 'TEST_CR1'
        result = self.client.createHandle(
            self.cred.prefix, location, None,
            [str(extra_key+'='+extra_value)], None, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('CREATE')
        body = self.build_create_body(location,
                               extratype=[str(extra_key+'='+extra_value)])
        mock_http.request.assert_called_once_with(
            uri, method='PUT', headers=hdrs, body=body)
        self.assertEqual(result, str(self.cred.prefix + '/' + suffix),
                         'create handle with extra key returns unexpected response')
        
    def test_create_handle_with_extra_location(self):
        """Test that create handle with extra location returns expected
        response.
        
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
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        suffix = 'TEST_CR1'
        result = self.client.createHandle(
            self.cred.prefix, location, None, None, [extra_location], suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('CREATE')
        body = self.build_create_body(location, l10320=extra_location)
        mock_http.request.assert_called_once_with(
            uri, method='PUT', headers=hdrs, body=body)
        self.assertEqual(result, str(self.cred.prefix + '/' + suffix),
                         'create handle with extra location returns unexpected response')
    
    
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
        body = self.build_create_body(location)
        mock_http.request.assert_called_once_with(
            uri, method='PUT', headers=hdrs, body=body)
        self.assertIsNone(result,
                          'create existing handle should return None')
        
    
    def test_modify_handle_key_value(self):
        """Test that modify value of existing handle key returns True.
        
        Example result from non-mocked HTTP request (1/2):
        -- response={'status': '200', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 'transfer-encoding': 'chunked', 
                     'last-modified': 'Sat, 01 Aug 2015 23:14:53 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Sat, 01 Aug 2015 23:14:54 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle)
        
        Example result from non-mocked HTTP request (2/2):
        -- response={'status': '204', 
                     'content-length': '0', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1',
                     'last-modified': 'Sat, 01 Aug 2015 23:14:54 GMT', 
                     'etag': '"+Led8XZM52GWYA8GMy/Neg"', 
                     'date': 'Sat, 01 Aug 2015 23:14:54 GMT'}
        -- content=''
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(200)
        mock_content = self.build_content('retrieve_handle')
        mock_http.request.return_value = mock_response, mock_content
        key = 'URL'
        value = 'http://www.testB2SafeCmd.com/2'
        suffix = 'TEST_CR1'
        result = self.client.modifyHandle(
            self.cred.prefix, key, value, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        # 1st call to retrieve existing handle
        uri1 = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs1 = self.build_headers('READ')
        call1 = mock.call(uri1, method='GET', headers=hdrs1)
        # 2nd call to update specified key value
        uri2 = self.build_uri(self.cred.prefix, key, value, suffix)
        hdrs2 = self.build_headers('UPDATE')
        handle_json = self.build_content('retrieve_handle')
        body2 = self.build_modify_body(handle_json, key, value)
        call2 = mock.call(uri2, method='PUT', headers=hdrs2, body=body2)
        calls = [call1, call2]
        self.assertEqual(mock_http.request.call_count, len(calls),
                    'modify handle key value should make 2 HTTP requests')
        mock_http.request.assert_has_calls(calls)
        self.assertTrue(result,
                        'modify value of existing handle key should return True')
        
        
    def test_modify_handle_new_key_value(self):
        """Test that modify existing handle with new key-value pair
        returns True.
        
        Example result from non-mocked HTTP request (1/2):
        -- response={'status': '200', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 'transfer-encoding': 'chunked', 
                     'last-modified': 'Sat, 01 Aug 2015 23:14:53 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Sat, 01 Aug 2015 23:14:54 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle)
        
        Example result from non-mocked HTTP request (2/2):
        -- response={'status': '204', 
                     'content-length': '0', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1',
                     'last-modified': 'Sat, 01 Aug 2015 23:14:54 GMT', 
                     'etag': '"+Led8XZM52GWYA8GMy/Neg"', 
                     'date': 'Sat, 01 Aug 2015 23:14:54 GMT'}
        -- content=''
        """
        mock_http = self.MockHttp.return_value
        mock_response_200 = self.build_response(200)
        mock_content_200 = self.build_content('retrieve_handle')
        mock_response_204 = self.build_response(204)
        mock_content_204 = ''
        mock_http.request.side_effect = [
            # 1st HTTP response: modifyHandle, i.e. GET -> 200
            (mock_response_200, mock_content_200),
            # 2nd HTTP response: modifyHandle, i.e. PUT -> 204
            (mock_response_204, mock_content_204)]
        key = "EMAIL"
        value = 'user@testB2SafeCmd.com'
        suffix = 'TEST_CR1'
        result = self.client.modifyHandle(
            self.cred.prefix, key, value, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        # 1st HTTP request: modifyHandle, i.e. GET -> 200
        uri1 = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs1 = self.build_headers('READ')
        call1 = mock.call(uri1, method='GET', headers=hdrs1)
        # 2nd HTTP request: modifyHandle, i.e. PUT -> 204
        uri2 = self.build_uri(self.cred.prefix, key, value, suffix)
        hdrs2 = self.build_headers('UPDATE')
        handle_json = self.build_content('retrieve_handle')
        body2 = self.build_modify_body(handle_json, key, value)
        call2 = mock.call(uri2, method='PUT', headers=hdrs2, body=body2)
        calls = [call1, call2]
        self.assertEqual(
            mock_http.request.call_count, len(calls),
            'modify handle with new key-value pair should make 2 HTTP requests')
        mock_http.request.assert_has_calls(calls)
        self.assertTrue(
          result,
          'modify handle with new key-value pair should return True')
        
        
    def test_modify_handle_with_empty_value(self):
        """Test that modify existing handle key with empty value
        returns True.
        
        Example result from non-mocked HTTP request (1/2):
        -- response={'status': '200', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 'transfer-encoding': 'chunked', 
                     'last-modified': 'Sat, 01 Aug 2015 23:14:53 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Sat, 01 Aug 2015 23:14:54 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle_with_extra_key)
        
        Example result from non-mocked HTTP request (2/2):
        -- response={'status': '204', 
                     'content-length': '0', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1',
                     'last-modified': 'Sat, 01 Aug 2015 23:14:54 GMT', 
                     'etag': '"+Led8XZM52GWYA8GMy/Neg"', 
                     'date': 'Sat, 01 Aug 2015 23:14:54 GMT'}
        -- content=''
        """
        mock_http = self.MockHttp.return_value
        mock_response_200 = self.build_response(200)
        mock_content_200 = self.build_content('retrieve_handle_with_extra_key')
        mock_response_204 = self.build_response(204)
        mock_content_204 = ''
        mock_http.request.side_effect = [
            # 1st HTTP response: modifyHandle, i.e. GET -> 200
            (mock_response_200, mock_content_200),
            # 2nd HTTP response: modifyHandle, i.e. PUT -> 204
            (mock_response_204, mock_content_204)]
        key = "EMAIL"
        value = ''
        suffix = 'TEST_CR1'
        result = self.client.modifyHandle(
            self.cred.prefix, key, value, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        # 1st HTTP request: modifyHandle, i.e. GET -> 200
        uri1 = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs1 = self.build_headers('READ')
        call1 = mock.call(uri1, method='GET', headers=hdrs1)
        # 2nd HTTP request: modifyHandle, i.e. PUT -> 204
        uri2 = self.build_uri(self.cred.prefix, key, value, suffix)
        hdrs2 = self.build_headers('UPDATE')
        body2 = self.build_modify_body(mock_content_200, key, value)
        call2 = mock.call(uri2, method='PUT', headers=hdrs2, body=body2)
        calls = [call1, call2]
        self.assertEqual(
            mock_http.request.call_count, len(calls),
            'modify handle key with empty value should make 2 HTTP requests')
        mock_http.request.assert_has_calls(calls)
        self.assertTrue(
          result,
          'modify handle key with empty value should return True')
        
        
    def test_modify_non_existing_handle(self):
        """Test that modify key of non existing handle returns False.
        
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
        key = 'URL'
        value = 'http://www.testB2SafeCmd.com/1'
        suffix = 'TEST_CR1'
        result = self.client.modifyHandle(
            self.cred.prefix, key, value, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('READ')
        mock_http.request.assert_called_once_with(
            uri, method='GET', headers=hdrs)
        self.assertFalse(result,
                         'modify key of non existing handle should return False')
    
    
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
          
        
    def test_delete_key_from_handle(self):
        """Test that delete key from handle returns True.
        
        Example result from non-mocked HTTP request (1/2):
        -- response={'status': '200', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 'transfer-encoding': 'chunked', 
                     'last-modified': 'Sat, 01 Aug 2015 23:14:53 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Sat, 01 Aug 2015 23:14:54 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle_with_extra_key)
        
        Example result from non-mocked HTTP request (2/2):
        -- response={'date': 'Mon, 03 Aug 2015 00:38:53 GMT', 
                     'status': '204', 
                     'content-length': '0'}
        -- content=''
        """
        mock_http = self.MockHttp.return_value
        mock_response_200 = self.build_response(200)
        mock_content_200 = self.build_content('retrieve_handle_with_extra_key')
        mock_response_204 = self.build_response(204)
        mock_content_204 = ''
        mock_http.request.side_effect = [
            # 1st HTTP response: retrieveHandle, i.e. GET -> 200
            (mock_response_200, mock_content_200),
            # 2nd HTTP response: deleteHandle, i.e. PUT -> 204
            (mock_response_204, mock_content_204)]
        key = "EMAIL"
        suffix = 'TEST_CR1'
        result = self.client.deleteHandle(
            self.cred.prefix, key, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        # 1st HTTP request: retrieveHandle, i.e. GET -> 200
        uri1 = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs1 = self.build_headers('READ')
        call1 = mock.call(uri1, method='GET', headers=hdrs1)
        # 2nd HTTP request: deleteHandle, i.e. PUT -> 204
        uri2 = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs2 = self.build_headers('UPDATE')
        body2 = self.build_delete_body(mock_content_200, key)
        call2 = mock.call(uri2, method='PUT', headers=hdrs2, body=body2)
        calls = [call1, call2]
        self.assertEqual(
            mock_http.request.call_count, len(calls),
            'delete key from handle should make 2 HTTP requests')
        mock_http.request.assert_has_calls(calls)
        self.assertTrue(result, 'delete key from handle should return True')
        
    
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
        self.assertFalse(
            result,
            'delete key from non existing handle should return False')
        
    
    def test_delete_non_existing_key_from_handle(self):
        """Test that delete non existing key from handle returns False.
        
        Example result from non-mocked HTTP request:
        -- response={'status': '200',
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 'transfer-encoding': 'chunked', 
                     'last-modified': 'Mon, 03 Aug 2015 08:02:03 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Mon, 03 Aug 2015 08:02:03 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(200)
        mock_content = self.build_content('retrieve_handle')
        mock_http.request.return_value = mock_response, mock_content
        key = 'FOO_KEY'
        suffix = 'TEST_CR1'
        result = self.client.deleteHandle(self.cred.prefix, key, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('READ')
        mock_http.request.assert_called_once_with(
          uri, method='GET', headers=hdrs)
        self.assertFalse(
          result,
          'delete non existing key from handle should return False')
        
        
    def test_update_handle_with_location(self):
        """Test that update handle with new location returns True.
        
        Example result from non-mocked HTTP request (1/3):
        -- response={'status': '200', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 
                     'transfer-encoding': 'chunked', 
                     'last-modified': 'Sun, 02 Aug 2015 09:04:21 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Sun, 02 Aug 2015 09:04:22 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle)
        
        Example result from non-mocked HTTP request (2/3):
        -- response={'status': '200', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 
                     'transfer-encoding': 'chunked', 
                     'last-modified': 'Sun, 02 Aug 2015 09:04:21 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Sun, 02 Aug 2015 09:04:22 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle)
        
        Example result from non-mocked HTTP request (3/3):
        -- response={'status': '204', 
                     'content-length': '0', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1',
                     'last-modified': 'Sun, 02 Aug 2015 09:04:22 GMT',
                     'connection': 'close', 
                     'etag': '"aJFgz1QQzwiletfK/6o5cg"', 
                     'date': 'Sun, 02 Aug 2015 09:04:22 GMT'}
        -- content=''
        """
        mock_http = self.MockHttp.return_value
        mock_response_200 = self.build_response(200)
        mock_content_200 = self.build_content('retrieve_handle')
        mock_response_204 = self.build_response(204)
        mock_content_204 = ''
        mock_http.request.side_effect = [
            # 1st HTTP response: getValueFromHandle, i.e. GET -> 200
            (mock_response_200, mock_content_200),
            # 2nd HTTP response: modifyHandle, i.e. GET -> 200
            (mock_response_200, mock_content_200),
            # 3nd HTTP response: modifyHandle, i.e. PUT -> 204
            (mock_response_204, mock_content_204)]
        key = '10320/LOC'
        value = '846/157c344a-0179-11e2-9511-00215ec779a8'
        suffix = 'TEST_CR1'
        result = self.client.updateHandleWithLocation(
            self.cred.prefix, value, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        # 1st HTTP request: getValueFromHandle, i.e. GET -> 200
        uri1 = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs1 = self.build_headers('READ')
        call1 = mock.call(uri1, method='GET', headers=hdrs1)
        # 2nd HTTP request: modifyHandle, i.e. GET -> 200
        call2 = mock.call(uri1, method='GET', headers=hdrs1)
        # 3rd HTTP request: modifyHandle, i.e. PUT -> 204
        loc10320 = self.build_loc10320('http://www.testB2SafeCmd.com/1')
        lt = epicclient.LocationType(loc10320)
        _, loc10320_value = lt.addLocation(value)
        uri3 = self.build_uri(self.cred.prefix, key, loc10320_value, suffix)
        hdrs3 = self.build_headers('UPDATE')
        body3 = self.build_modify_body(mock_content_200, key, loc10320_value)
        call3 = mock.call(uri3, method='PUT', headers=hdrs3, body=body3)
        calls = [call1, call2, call3]
        self.assertEqual(
            mock_http.request.call_count, len(calls),
            'update handle with new location should make 3 HTTP requests')
        mock_http.request.assert_has_calls(calls)
        self.assertTrue(result,
                         'update handle with new location should return True')
    
    
    def test_update_handle_with_same_location(self):
        """Test that update handle with same location value returns False.
        
        Example result from non-mocked HTTP request:
        -- response={'status': '200', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 
                     'transfer-encoding': 'chunked', 
                     'last-modified': 'Sun, 02 Aug 2015 09:04:21 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Sun, 02 Aug 2015 09:04:22 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle_with_extra_location)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(200)
        mock_content = self.build_content('retrieve_handle_with_extra_location')
        mock_http.request.return_value = mock_response, mock_content
        value = '846/157c344a-0179-11e2-9511-00215ec779a8'
        suffix = 'TEST_CR1'
        result = self.client.updateHandleWithLocation(
            self.cred.prefix, value, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('READ')
        mock_http.request.assert_called_once_with(uri, method='GET', headers=hdrs)
        self.assertFalse(
            result,
            'update handle with same location value should return False')
    
            
    def test_update_non_existing_handle_with_location(self):
        """Test that update non existing handle with location returns
        False.
        
        Example result from non-mocked HTTP request (1/2):
        -- response={'date': 'Thu, 30 Jul 2015 10:37:25 GMT', 
                     'status': '404', 
                     'content-length': '2127'}
        -- content=(see resources/epic_srv_content-retrieve_non_existing_handle)
        
        Example result from non-mocked HTTP request (2/2):
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
        result = self.client.updateHandleWithLocation(
          self.cred.prefix, value, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        # 1st call to getValueFromHandle, i.e. retrieveHandle -> 404
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('READ')
        call1 = mock.call(uri, method='GET', headers=hdrs)
        # 2nd call to modifyHandle, i.e. retrieveHandle -> 404
        call2 = mock.call(uri, method='GET', headers=hdrs)
        calls = [call1, call2]
        self.assertEqual(
            mock_http.request.call_count, len(calls),
            'update non existing handle with location should make 2 HTTP GET requests')
        mock_http.request.assert_has_calls(calls)
        self.assertFalse(result,
                         'update non existing handle with location should return False')
        
    
    def test_remove_location_from_handle(self):
        """Test that remove location from handle returns True.
        
        Example result from non-mocked HTTP request (1/3):
        -- response={'status': '200', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 
                     'transfer-encoding': 'chunked', 
                     'last-modified': 'Sun, 02 Aug 2015 09:04:21 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Sun, 02 Aug 2015 09:04:22 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle_with_extra_location)
        
        Example result from non-mocked HTTP request (2/3):
        -- response={'status': '200', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 
                     'transfer-encoding': 'chunked', 
                     'last-modified': 'Sun, 02 Aug 2015 09:04:21 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Sun, 02 Aug 2015 09:04:22 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle_with_extra_location)
        
        Example result from non-mocked HTTP request (3/3):
        -- response={'status': '204', 
                     'content-length': '0', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1',
                     'last-modified': 'Sun, 02 Aug 2015 09:04:22 GMT',
                     'connection': 'close', 
                     'etag': '"aJFgz1QQzwiletfK/6o5cg"', 
                     'date': 'Sun, 02 Aug 2015 09:04:22 GMT'}
        -- content=''
        """
        mock_http = self.MockHttp.return_value
        mock_response_200 = self.build_response(200)
        mock_content_200 = self.build_content('retrieve_handle_with_extra_location')
        mock_response_204 = self.build_response(204)
        mock_content_204 = ''
        mock_http.request.side_effect = [
            # 1st HTTP response: getValueFromHandle, i.e. GET -> 200
            (mock_response_200, mock_content_200),
            # 2nd HTTP response: modifyHandle, i.e. GET -> 200
            (mock_response_200, mock_content_200),
            # 3nd HTTP response: modifyHandle, i.e. PUT -> 204
            (mock_response_204, mock_content_204)]
        key = '10320/LOC'
        value = '846/157c344a-0179-11e2-9511-00215ec779a8'
        suffix = 'TEST_CR1'
        result = self.client.removeLocationFromHandle(
            self.cred.prefix, value, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        # 1st HTTP request: getValueFromHandle, i.e. GET -> 200
        uri1 = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs1 = self.build_headers('READ')
        call1 = mock.call(uri1, method='GET', headers=hdrs1)
        # 2nd HTTP request: modifyHandle, i.e. GET -> 200
        call2 = mock.call(uri1, method='GET', headers=hdrs1)
        # 3rd HTTP request: modifyHandle, i.e. PUT -> 204
        loc10320 = self.build_loc10320(
            'http://www.testB2SafeCmd.com/1', [value])
        lt = epicclient.LocationType(loc10320)
        _, loc10320_value = lt.removeLocation(value)
        uri3 = self.build_uri(self.cred.prefix, key, loc10320_value, suffix)
        hdrs3 = self.build_headers('UPDATE')
        body3 = self.build_modify_body(mock_content_200, key, loc10320_value)
        call3 = mock.call(uri3, method='PUT', headers=hdrs3, body=body3)
        calls = [call1, call2, call3]
        self.assertEqual(
            mock_http.request.call_count, len(calls),
            'remove location from handle should make 3 HTTP requests')
        mock_http.request.assert_has_calls(calls)
        self.assertTrue(result,
                        'remove location from handle should return True')
        
        
    def test_remove_non_existing_location_from_handle(self):
        """Test that remove non existing location from handle returns False.
        
        Example result from non-mocked HTTP request:
        -- response={'status': '200', 
                     'content-location': 'https://epic.service.eu/api/v2/handles/90210/TEST_CR1', 
                     'transfer-encoding': 'chunked', 
                     'last-modified': 'Sun, 02 Aug 2015 09:04:21 GMT', 
                     'etag': '"gkCVbVUVJvf/EILjgSZ0HQ"', 
                     'date': 'Sun, 02 Aug 2015 09:04:22 GMT', 
                     'content-type': 'application/json'}
        -- content=(see resources/epic_srv_content-retrieve_handle)
        """
        mock_http = self.MockHttp.return_value
        mock_response = self.build_response(200)
        mock_content = self.build_content('retrieve_handle')
        mock_http.request.return_value = mock_response, mock_content
        value = '846/157c344a-0179-11e2-9511-00215ec779a8'
        suffix = 'TEST_CR1'
        result = self.client.removeLocationFromHandle(
            self.cred.prefix, value, suffix)
        self.MockHttp.assert_called_once
        mock_http.request.assert_called_once
        uri = self.build_uri(self.cred.prefix, '', '', suffix)
        hdrs = self.build_headers('READ')
        mock_http.request.assert_called_once_with(uri, method='GET', headers=hdrs)
        self.assertFalse(
            result,
            'remove non existing location from handle should return False')
    
        
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
      
    
    def build_create_body(self, location, checksum=None, extratype=None, l10320=None):
        """Build mock create request body for given params."""
        #loc10320 = self.build_loc10320(location, l10320)
 
        handle_array = [{'type': 'URL', 'parsed_data': location}] 
        if l10320:
            loc10320 = self.build_loc10320(l10320)
            handle_array.append({'type': '10320/LOC', 'parsed_data': loc10320}) 
        if checksum: 
            handle_array.append({'type': 'CHECKSUM', 'parsed_data': checksum}) 
        if extratype: 
            for key_value in extratype: 
                key   = key_value.split('=')[0] 
                value = key_value.split('=')[1] 
                if (next((item for item in handle_array if item['type'] == key), 
                    None) is None): 
                    handle_array.append({'type': key, 'parsed_data': value}) 
 
        return simplejson.dumps(handle_array)
        
      
    def build_modify_body(self, handle_json, key, value):
      """Build mock modify request body for given JSON-formatted
      handle.
      """
      handle_json_obj = simplejson.loads(handle_json)
      
      keyfound = False 
      if not value: 
          for item in handle_json_obj: 
              if 'type' in item and item['type'] == key: 
                  del item['data'] 
                  del item['parsed_data'] 
                  break 
      else: 
          for item in handle_json_obj: 
              if 'type' in item and item['type'] == key: 
                  keyfound = True 
                  item['parsed_data'] = value 
                  del item['data'] 
                  break 

          if keyfound is False: 
              handle_item = {'type': key, 'parsed_data': value} 
              handle_json_obj[len(handle_json_obj):] = [handle_item]
      
      return simplejson.dumps(handle_json_obj)
    
    
    def build_delete_body(self, handle_json, key):
      """Build mock delete request body for given JSON-formatted
      handle.
      """
      handle_json_obj = simplejson.loads(handle_json)
      
      for item in handle_json_obj:
          if 'type' in item and item['type'] == key:
              del handle_json_obj[handle_json_obj.index(item)]
              break
      
      return simplejson.dumps(handle_json_obj)
    
    
    def build_loc10320(self, location, l10320=None):
        """Build 10320/LOC handle property from specified values."""
        idn = 0 
        root = etree.Element('locations') 
 
        if not l10320: 
            etree.SubElement(root, 'location', id=str(idn), href=str(location)) 
        else: 
            etree.SubElement(root, 'location', id=str(idn), href=str(location)) 
            for item in l10320: 
                idn += 1 
                etree.SubElement(root, 'location', id=str(idn), href=str(item)) 
 
        return tostring(root)
    
