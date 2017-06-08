import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import ast
import json
import os
import os.path
import string
import subprocess

sys.path.append("../../cmd") 

TEST_RESOURCES_PATH = '../tests/resources/'    # Trailing '/' is required
CRED_STORE = 'os'
CRED_FILENAME = 'epic2_credentials'
CRED_PATH = TEST_RESOURCES_PATH+CRED_FILENAME

EPIC_PATH = '../../cmd/epicclient2.py'

if 'EPIC_PATH' in os.environ:
    EPIC_PATH = os.environ['EPIC_PATH']

if 'CRED_PATH' in os.environ:
    CRED_PATH = os.environ['CRED_PATH']


@unittest.skipUnless(os.path.isfile(CRED_PATH) and os.access(CRED_PATH, os.R_OK),
                     'requires EPIC credentials file at %s' % CRED_PATH)

def subprocess_popen(cmd, input_string=None):
    '''run shell command, get output back in an array'''

    process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    (data_stdout, data_stderr) = process.communicate(input_string)
    process.wait()

    if data_stderr != None:
        # relay errors to stderr
        sys.stderr.write(data_stderr)

    arr = string.split(data_stdout, '\n')
    arr = map(string.strip, arr)
    return arr


class EpicClient2IntegrationTests(unittest.TestCase):

    def setUp(self):
        """Setup testB2SafeCmd environment before the tests have run"""
        jsonfilecontent = json.loads(open(CRED_PATH, 'r').read())
        self.prefix = jsonfilecontent.pop('prefix')

        command = [EPIC_PATH, CRED_STORE, CRED_PATH, "search", "URL", "http://www.testB2SafeCmd.com/1"]
        search_result = subprocess.Popen(command,
                                          shell=False,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        stdout_value, stderr_value = search_result.communicate()
        search_result.wait()

        out_arr = stdout_value.split('\n')
        out_arr = map(string.strip, out_arr)

        for line in out_arr:
            if line != 'empty':
                if line[:1] != '[':
                    delete_result = subprocess.call([EPIC_PATH, CRED_STORE, CRED_PATH, 'delete', line])
                else:
                    line_array = ast.literal_eval(line)
                    for handle in line_array:
                        delete_result = subprocess.call([EPIC_PATH, CRED_STORE, CRED_PATH, 'delete', handle])



    def tearDown(self):
        """ Cleanup testB2SafeCmd environment after the tests have run
        """
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, "search", "URL", "http://www.testB2SafeCmd.com/1"]
        search_result = subprocess.Popen(command,
                                          shell=False,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        stdout_value, stderr_value = search_result.communicate()
        search_result.wait()

        out_arr = stdout_value.split('\n')
        out_arr = map(string.strip, out_arr)

        for line in out_arr:
            if line != 'empty':
                if line[:1] != '[':
                    delete_result = subprocess.call([EPIC_PATH, CRED_STORE, CRED_PATH, 'delete', line])
                else:
                    line_array = ast.literal_eval(line)
                    for handle in line_array:
                        delete_result = subprocess.call([EPIC_PATH, CRED_STORE, CRED_PATH, 'delete', handle])


    def test_search_handle_by_key_value(self):
        """Test that search by key-value returns matching handle."""
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'search', 'URL', 'http://www.testB2SafeCmd.com/1']
        search_result = subprocess_popen(command)
        search_result_json = json.loads(search_result[0])
        self.assertEqual(
            create_result[0], search_result_json[0],
            'search existing handle by key returns unexpected response')

 
    def test_search_handle_by_non_existing_key_value(self):
        """Test that search handle by non existing key-value returns 'empty'."""
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'search', 'CHECKSUM', '123456789012345678901234567890']
        search_result = subprocess_popen(command)
        self.assertEqual(
            search_result[0], 'empty',
            'search handle by non existing key-value should return \"empty\"')
        
        
    def test_read_non_existing_handle(self):
        """Test that read non existing handle returns None."""
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', self.prefix+'/1234567890a']
        read_result = subprocess_popen(command)
        self.assertEqual(
          read_result[0], 'None',
          "read non existing handle should return None")


    def test_read_value_from_handle(self):
        """Test that read value by key returns stored handle value."""
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', 'URL']
        read_result = subprocess_popen(command)
        self.assertEqual(
            read_result[0], 'http://www.testB2SafeCmd.com/1',
            'read existing value from handle returns unexpected response')


    def test_read_value_from_non_existing_handle(self):
        """Test that read value by key from non existing handle returns None."""
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', self.prefix+'/1234567890a', '--key', 'URL']
        read_result = subprocess_popen(command)
        self.assertEqual(
            read_result[0], 'None',
            'read existing value from non existing handle returns unexpected response')


    def test_read_non_existing_value_from_handle(self):
        """Test that read value by non existing key returns None."""
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', 'FOO_KEY']
        read_result = subprocess_popen(command)
        self.assertEqual(
            read_result[0], 'None',
            'read value by non existing key should return None')


    def test_create_handle(self):
        """Test that create handle returns expected response and adds
        new handle.
        """
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'search', 'URL', 'http://www.testB2SafeCmd.com/1']
        search_result = subprocess_popen(command)
        search_result_json = json.loads(search_result[0])
        self.assertEqual(create_result[0], search_result_json[0],
                         'create handle should add new handle')
        
        
    def test_create_handle_with_checksum(self):
        """Test that create handle with checksum returns expected 
        response and adds new handle with supplied checksum.
        """
        checksum = '1cb285b'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', '--checksum', checksum, 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', 'CHECKSUM']
        read_result = subprocess_popen(command)
        self.assertEqual(checksum, read_result[0],
                         'create handle with checksum should add new handle')
        
        
    def test_create_handle_with_extra_key(self):
        """Test that create handle with extra key returns expected 
        response and adds new handle with supplied key value.
        """
        extra_key = 'EMAIL'
        extra_value = 'user@testB2SafeCmd.com'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', '--extratype', extra_key+'='+extra_value, 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', extra_key]
        read_result = subprocess_popen(command)
        self.assertEqual(extra_value, read_result[0],
                         'create handle with extra key should add new handle')
        
        
    def test_create_handle_with_extra_location(self):
        """Test that create handle with extra location returns expected 
        response and adds new handle with supplied locations.
        """
        location_key = '10320/LOC'
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', '--loc10320', extra_location, 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', location_key]
        read_result = subprocess_popen(command)
        self.assertIn(extra_location, read_result[0],
                         'create handle with extra location should add new handle')

    def test_create_handle_with_extra_key_FIO_real_pid(self):
        """Test that create handle with extra key EUDAT/FIO returns expected 
        response and adds new handle with supplied key value.
        """
        extra_key = 'EUDAT/FIO'
        extra_value = '841/totally_nonsen_suffix'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', '--extratype', extra_key+'='+extra_value, 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', extra_key]
        read_result = subprocess_popen(command)
        self.assertEqual(extra_value, read_result[0],
                         'create handle with extra key EUDAT/FIO should add new handle')

    def test_create_handle_with_extra_key_FIO_pid(self):
        """Test that create handle with extra key EUDAT/FIO and value 'pid' returns expected 
        response and adds new handle with supplied key value.
        """
        extra_key = 'EUDAT/FIO'
        extra_value = 'pid'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', '--extratype', extra_key+'='+extra_value, 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', extra_key]
        read_result = subprocess_popen(command)
        self.assertEqual(create_result[0], read_result[0],
                         'create handle with extra key EUDAT/FIO an value pid should add new handle')

    def test_create_handle_with_extra_key_FIO_PID(self):
        """Test that create handle with extra key EUDAT/FIO and value 'PID' returns expected 
        response and adds new handle with supplied key value.
        """
        extra_key = 'EUDAT/FIO'
        extra_value = 'PID'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', '--extratype', extra_key+'='+extra_value, 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', extra_key]
        read_result = subprocess_popen(command)
        self.assertEqual(create_result[0], read_result[0],
                         'create handle with extra key EUDAT/FIO an value pid should add new handle')

    def test_create_handle_with_extra_key_ROR_real_pid(self):
        """Test that create handle with extra key EUDAT/ROR returns expected 
        response and adds new handle with supplied key value.
        """
        extra_key = 'EUDAT/ROR'
        extra_value = '841/totally_nonsen_suffix'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', '--extratype', extra_key+'='+extra_value, 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', extra_key]
        read_result = subprocess_popen(command)
        self.assertEqual(extra_value, read_result[0],
                         'create handle with extra key EUDAT/ROR should add new handle')

    def test_create_handle_with_extra_key_ROR_pid(self):
        """Test that create handle with extra key EUDAT/ROR and value 'pid' returns expected 
        response and adds new handle with supplied key value.
        """
        extra_key = 'EUDAT/ROR'
        extra_value = 'pid'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', '--extratype', extra_key+'='+extra_value, 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', extra_key]
        read_result = subprocess_popen(command)
        self.assertEqual(create_result[0], read_result[0],
                         'create handle with extra key EUDAT/ROR an value pid should add new handle')

    def test_create_handle_with_extra_key_ROR_PID(self):
        """Test that create handle with extra key EUDAT/ROR and value 'PID' returns expected 
        response and adds new handle with supplied key value.
        """
        extra_key = 'EUDAT/ROR'
        extra_value = 'PID'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', '--extratype', extra_key+'='+extra_value, 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', extra_key]
        read_result = subprocess_popen(command)
        self.assertEqual(create_result[0], read_result[0],
                         'create handle with extra key EUDAT/ROR an value pid should add new handle')
  
    def test_modify_handle_key_value(self):
        """Test that modify handle value returns True and updates 
        stored value.
        """
        key = 'URL'
        value_before = 'http://www.testB2SafeCmd.com/3'
        value_after = 'http://www.testB2SafeCmd.com/1'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', value_before]
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'modify', create_result[0], 'URL', value_after]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], 'True',
                        'modify handle value should return True')
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', 'URL']
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[0], value_after,
                         'modify handle value failed to update value')
        
        
    def test_modify_handle_new_key_value(self):
        """Test that modify existing handle with new key-value pair
        returns True and updates stored handle.
        """
        key = "EMAIL"
        value = 'user@testB2SafeCmd.com'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'modify', create_result[0], key, value]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], 'True',
                        'modify handle value should return True')
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', key]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[0], value,
            'modify existing handle with new key-value should update value')
        
        
    def test_modify_handle_with_empty_value(self):
        """Test that modify existing handle key with empty value
        returns True and updates stored value accordingly.
        """
        key = "EMAIL"
        value_before = 'user@testB2SafeCmd.com'
        value_after = ''
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', 'http://www.testB2SafeCmd.com/1', '--extratype', key+"="+value_before]
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'modify', create_result[0], key, value_after]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], 'True',
                        'modify existing handle key with empty value should return True')
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', key]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[0], value_after,
                        "modify existing handle key with empty value should set stored value to ''")
        
        
    def test_modify_non_existing_handle(self):
        """Test that modify value of non existing handle returns False."""
        key = "FOO_KEY"
        value = "FOO_VALUE"
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'modify', self.prefix+"/1234567890a", key, value]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], 'False',
                         'modify non existing handle should return False')
        
        
    def test_delete_handle(self):
        """Test that delete existing handle returns True."""
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'delete', create_result[0]]
        delete_result = subprocess_popen(command)
        self.assertEqual(delete_result[0], 'True',
                        'delete existing handle should return True')
        
    
    def test_delete_non_existing_handle(self):
        """Test that delete non existing handle returns False."""
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'delete', self.prefix+"/1234567890ahabbiebabbie"]
        delete_result = subprocess_popen(command)
        self.assertEqual(delete_result[0], 'False',
                        'delete non existing handle should return False')
   
    
    def test_delete_key_from_handle(self):
        """Test that delete key from handle returns True."""
        key = 'EMAIL'
        value = 'user@testB2SafeCmd.com'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', 'http://www.testB2SafeCmd.com/1', '--extratype', key+"="+value]
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'delete', create_result[0], '--key', key ]
        delete_result = subprocess_popen(command)
        self.assertEqual(delete_result[0], 'True',
                        'delete existing handle value should return True')
        
        
    def test_delete_non_existing_key_from_handle(self):
        """Test that delete non existing key from handle returns False."""
        key = 'FOO_KEY'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'delete', self.prefix+"/1234567890a", '--key', key]
        delete_result = subprocess_popen(command)
        self.assertEqual(delete_result[0], 'False',
                         'delete key from non existing handle should return False')

   
    def test_update_handle_with_location(self):
        """Test that update handle with new location returns None and 
        persists new value.
        """
        location_key = '10320/LOC'
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', 'http://www.testB2SafeCmd.com/1']
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'relation', create_result[0], extra_location]
        relation_result = subprocess_popen(command)
        self.assertEqual(relation_result[0], 'None',
                        'modify existing handle with location should return None')
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'read', create_result[0], '--key', location_key]
        read_result = subprocess_popen(command)
        self.assertIn(extra_location, read_result[0],
                         'update handle with new location should persist new location value')


    def test_update_existing_handle_with_same_location(self):
        """Test that update handle with same location value returns None."""
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'create', 'http://www.testB2SafeCmd.com/1', '--loc10320', extra_location ]
        create_result = subprocess_popen(command)
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'relation', create_result[0], extra_location]
        relation_result = subprocess_popen(command)
        self.assertEqual(relation_result[0], 'None',
                         'update existing handle with same location value should return False')
        
        
    def test_update_non_existing_handle_with_location(self):
        """Test that update non existing handle with location returns False."""
        extra_location = '846/157c344a-0179-11e2-9511-00215ec779a8'
        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'relation', self.prefix+"/1234567890a", extra_location]
        relation_result = subprocess_popen(command)
        self.assertEqual(relation_result[0], 'False',
                         'update non existing handle with location should return False')

