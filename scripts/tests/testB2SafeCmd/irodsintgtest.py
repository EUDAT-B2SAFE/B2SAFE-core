"""test scripts to test iRODS integration"""
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import os
import os.path
import json
import subprocess
import string

sys.path.append("../../cmd")

TEST_RESOURCES_PATH = '../tests/resources/'    # Trailing '/' is required

HOME = os.path.expanduser("~")
IRODS_ENV_HOME = HOME+'/.irods/'
IRODS_ENV = 'irods_environment.json'
IRODS_ENV_PATH = IRODS_ENV_HOME+IRODS_ENV

@unittest.skipUnless(os.path.isfile(IRODS_ENV_PATH) and os.access(IRODS_ENV_PATH, os.R_OK),
                     'requires iRODS environment file at %s' % IRODS_ENV_PATH)

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


class IrodsIntegrationTests(unittest.TestCase):
    """These are iRODS integration tests"""

    def setUp(self):
        """Setup irods environment variables before the tests have run"""
        jsonfilecontent = json.loads(open(IRODS_ENV_PATH, 'r').read())
        self.irods_default_hash_scheme = jsonfilecontent.pop('irods_default_hash_scheme')
        self.irods_default_resource = jsonfilecontent.pop('irods_default_resource')
        self.irods_home = jsonfilecontent.pop('irods_home')
        self.irods_user_name = jsonfilecontent.pop('irods_user_name')
        self.irods_zone_name = jsonfilecontent.pop('irods_zone_name')


    def tearDown(self):
        """ Cleanup testB2SafeCmd environment after the tests have run
        """


    def test_irods_functions(self):
        """Test that iRODS functions."""
        irods_username_result = ''
        command = ["ienv"]
        ienv_result = subprocess_popen(command)
        for elem in ienv_result:
            if 'irods_user_name' in elem:
                irods_username_result = elem
        irods_username_result_expected = 'NOTICE: irods_user_name - '+self.irods_user_name
        self.assertEqual(
            irods_username_result, irods_username_result_expected,
            'The username we expect is different')


    def test_irods_put_file(self):
        """Test that it is possible to put a file in iRODS"""
        test_file = 'test_data.txt'
        test_path = '/tmp/'+test_file
        with open(test_path, "w") as write_file:
            write_file.write("Hello World!")
        command = ["iput", "-f", test_path]
        put_result = subprocess_popen(command)
        os.unlink(test_path)
        command = ["ils", test_file]
        ils_result = subprocess_popen(command)
        ils_result_expected = self.irods_home+'/'+test_file
        self.assertEqual(
            ils_result[0], ils_result_expected,
            'file should have been put in :'+ils_result_expected)

