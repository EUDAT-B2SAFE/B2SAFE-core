"""test scripts to test iRODS B2SAFE integration"""
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import os
import os.path
import json
import re
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

# OS functions

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
    if arr and arr[-1] == '':
        arr.pop()
    return arr

def create_os_file(input_filename):
    '''procedure to create a file with "Hello World!"'''
    with open(input_filename, "w") as write_file:
        write_file.write("Hello World!")

def test_assert_array(self, testvaluesarray):
    '''procedure to test expected values, use input from an array of dicts'''
    for testvalues in testvaluesarray:
        action = testvalues['action']
        result = testvalues['result_value']
        expected = testvalues['expected_value']
        output_string = testvalues['string']
        if action.lower() == 'equal':
            self.assertEqual(result, expected, output_string)
        elif action.lower() == 'notequal':
            self.assertNotEqual(result, expected, output_string)
        else:
            print "The action defined is NOT valid"

# iRODS functions

def create_irods_directory(directory_to_create):
    '''procedure to create a directory in iRODS'''
    # execute rule to create directory
    command = ["imkdir", "-p", directory_to_create]
    imkdir_result = subprocess_popen(command)
    return imkdir_result

def delete_irods_directory(directory_to_delete):
    '''procedure to delete a directory in iRODS'''
    # execute rule to delete directory and all files in it
    command = ["irm", "-rf", directory_to_delete]
    irmdir_result = subprocess_popen(command)
    return irmdir_result

def delete_irods_file(file_to_delete):
    '''procedure to delete a file in iRODS'''
    # execute rule to delete file
    command = ["irm", "-f", file_to_delete]
    irm_result = subprocess_popen(command)
    return irm_result

def imeta_ls_specific(objtype, objname, avu_name):
    '''procedure to retrieve a specific value from an iRODS AVU'''
    # find AVU value in iCAT
    imeta_data_result = ''
    command = ["imeta", "ls", objtype, objname, avu_name]
    imeta_result = subprocess_popen(command)
    for elem in imeta_result:
        if 'value' in elem:
            imeta_data_result = elem.split()[1]
    return imeta_data_result

def log_to_rodsLog(log_string):
    '''procedure to log to iRODS logfile using b2safe logging'''
    # create test rule to log to iRODS logfile
    irule_rule = "{logInfo(*logging_line)}"
    irule_input = '*logging_line='+log_string
    irule_output = 'ruleExecOut'
    command = ["irule", irule_rule, irule_input, irule_output]
    # execute test rule
    irule_result = subprocess_popen(command)
    return irule_result

def put_irods_file(input_file, output_file):
    '''procedure to put a file on the OS in iRODS'''
    # put test file in iRODS
    command = ["iput", "-f", input_file, output_file]
    put_result = subprocess_popen(command)
    return put_result

def replicate_irods_file(source, destination, registered, recursive):
    '''procedure to replicate a file with EUDAT rules in iRODS'''
    # create test rule to replicate file
    irule_rule = "{*status = EUDATReplication(*source, *destination, *registered, *recursive, *response); if (*status) { writeLine('stdout', 'Success!'); } else { writeLine('stdout', 'Failed: *response'); }}"
    irule_input = '*source='+source+'%*destination='+destination+'%*registered='+registered+'+%*recursive='+recursive
    irule_output = 'ruleExecOut'
    command = ["irule", irule_rule, irule_input, irule_output]
    # execute test rule
    irule_result = subprocess_popen(command)
    replicate_result = irule_result[0]
    return replicate_result

# handle functions

def create_handle(irods_test_file_path, ror, fio, fixed_content):
    '''procedure to create a handle'''
    # create test rule
    irule_rule = '{EUDATCreatePID(*parent_pid, *path, *ror, *fio, *fixed, *newPID)}'
    irule_input = '*parent_pid=%*path='+irods_test_file_path+'%*ror='+ror+'%*fio='+fio+'%*fixed='+fixed_content
    irule_output = '*newPID'
    command = ["irule", irule_rule, irule_input, irule_output]
    # execute test rule
    irule_result = subprocess_popen(command)
    pid_found = re.search('[0-9A-Za-z\.]*/[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}', irule_result[0])
    if pid_found == None:
        create_result = pid_found
    else:
        create_result = irule_result[0].split('=')[1].lstrip(' ')
    return create_result

def create_handles_for_collection(irods_test_file_path, fixed_content):
    '''procedure to create all handles in a collection'''
    # create test rule
    irule_rule = '{EUDATPidsForColl(*path, *fixed)}'
    irule_input = '*path='+irods_test_file_path+'%*fixed='+fixed_content
    irule_output = '*out'
    command = ["irule", irule_rule, irule_input, irule_output]
    # execute test rule
    irule_result = subprocess_popen(command)
    return irule_result

def delete_handle(pid):
    '''procedure to delete a pid'''
    # create iRODS rule to delete created pid
    irule_rule = '{getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);' + \
                 ' msiExecCmd("epicclient2.py","*credStoreType *credStorePath delete *pid", "null", "null", "null", *out)}'
    irule_input = '*pid='+pid
    irule_output = '*out'
    command = ["irule", irule_rule, irule_input, irule_output]
    # execute rule to delete pid
    irule_result = subprocess_popen(command)
    return irule_result

def get_value_from_handle(pid, key):
    '''procedure to get the value from a key in a handle''' 
    # create test rule
    irule_rule = '*out={EUDATGeteValPid(*pid, *key)}'
    irule_input = '*pid='+pid+'%*key='+key
    irule_output = '*out'
    command = ["irule", irule_rule, irule_input, irule_output]
    # execute rule to retrieve value from pid
    irule_result = subprocess_popen(command)
    read_result = irule_result[0].split('*out = ')[1]
    return read_result

def get_all_values_from_handle(pid):
    '''procedure to get all possibles values from a handle and return a hash'''
    handle_values = {}

    # basic field (always needed)
    handle_values['url'] = get_value_from_handle(pid, "URL")
    # old/obsolete values
    handle_values['loc_10320'] = get_value_from_handle(pid, "10320/LOC")
    handle_values['checksum_old'] = get_value_from_handle(pid, "CHECKSUM")
    handle_values['ppid'] = get_value_from_handle(pid, "EUDAT/PPID")
    handle_values['ror_old'] = get_value_from_handle(pid, "ROR")
    # New PID profile v1 fields
    handle_values['checksum'] = get_value_from_handle(pid, "EUDAT/CHECKSUM")
    handle_values['checksum_timestamp'] = get_value_from_handle(pid, "EUDAT/CHECKSUM_TIMESTAMP")
    handle_values['fio'] = get_value_from_handle(pid, "EUDAT/FIO")
    handle_values['fixedcontent'] = get_value_from_handle(pid, "EUDAT/FIXED_CONTENT")
    handle_values['parent'] = get_value_from_handle(pid, "EUDAT/PARENT")
    handle_values['replica'] = get_value_from_handle(pid, "EUDAT/REPLICA")
    handle_values['ror'] = get_value_from_handle(pid, "EUDAT/ROR")
    handle_values['version'] = get_value_from_handle(pid, "EUDAT/PROFILE_VERSION")

    return handle_values

def search_handle(path):
    '''procedure to search for a handle'''
    # create iRODS rule to search for a pid
    irule_rule = '{EUDATSearchPID(*path, *existing_pid)}'
    irule_input = '*path='+path
    irule_output = '*existing_pid'
    command = ["irule", irule_rule, irule_input, irule_output]
    # execute rule to delete pid
    irule_result = subprocess_popen(command)
    # extract handle from search result
    search_result = irule_result[0].split('=')[1].lstrip(' ')
    return search_result


class IrodsB2safeIntegrationTests(unittest.TestCase):
    """These are iRODS B2SAFE integration tests"""

    def setUp(self):
        """Setup irods environment variables before the tests have run"""
        jsonfilecontent = json.loads(open(IRODS_ENV_PATH, 'r').read())
        self.irods_default_hash_scheme = jsonfilecontent.pop('irods_default_hash_scheme')
        self.irods_default_resource = jsonfilecontent.pop('irods_default_resource')
        self.irods_home = jsonfilecontent.pop('irods_home')
        self.irods_user_name = jsonfilecontent.pop('irods_user_name')
        self.irods_zone_name = jsonfilecontent.pop('irods_zone_name')
        deleted = {}
        res = search_handle(self.irods_home + '/*')
        while res != 'empty':
            deleted[res] = True
            dres = delete_handle(res)
            res = search_handle(self.irods_home + '/*')
            if res in deleted:
                raise RuntimeError('not deleted PID {0}'.format(res))

    def tearDown(self):
        """ Cleanup testB2SafeCmd environment after the tests have run
        """

    def test_10_irods_functions(self):
        """Test : basic iRODS functions."""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))
        irods_username_result = ''
        command = ["ienv"]
        ienv_result = subprocess_popen(command)
        for elem in ienv_result:
            if 'irods_user_name' in elem:
                irods_username_result = elem.strip("NOTICE: ")
        irods_username_result_expected = 'irods_user_name - '+self.irods_user_name

        # create array with values to test and execute
        test_values=[{ 'action': 'Equal', 'result_value': irods_username_result, 'expected_value': irods_username_result_expected, 'string': 'The username we expect is different'}]
        test_assert_array(self, test_values)


    def test_10_irods_put_file(self):
        """Test : put a file in iRODS"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create a test file
        test_file = 'test_data.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put the testfile in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)
        command = ["ils", test_file]
        ils_result = subprocess_popen(command)
        ils_result_expected = self.irods_home+'/'+test_file

        # create array with values to test and execute
        test_values=[{ 'action': 'Equal', 'result_value': ils_result[0], 'expected_value': ils_result_expected, 'string': 'file should have been put in :'+ils_result_expected}]
        test_assert_array(self, test_values)

    def test_30_b2safe_search_non_existing_PID(self):
        '''Test : search for non existing handles'''
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # search a non-existing handle
        search_result = search_handle('boekie_zoekie')

        # create array with values to test and execute
        test_values=[{ 'action': 'Equal', 'result_value': search_result, 'expected_value': 'empty', 'string': 'The result should have been "empty"'}]
        test_assert_array(self, test_values)

    def test_50_b2safe_create_pid_01(self):
        """Test : create a PID using b2safe (ror=None, fio=None, fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'None', 'None', 'false' )

        # cleanup before checks
        # retrieve values and delete if a handle has been created
        if handle_created != None:
            handle_dict = get_all_values_from_handle(handle_created)
            delete_handle(handle_created)
        # delete file from iRODS
        delete_irods_file(test_file)

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        # check basic handle field(s)
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
        # check for obsolete handle fields
        test_values.append({'action': 'Equal', 'result_value': handle_dict['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
        # check for PID V1 handle fields 
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fio'], 'expected_value': 'None', 'string': 'EUDAT/FIO has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror'], 'expected_value': 'None', 'string': 'EUDAT/ROR has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_assert_array(self, test_values)


    def test_50_b2safe_create_pid_02(self):
        """Test : create a PID using b2safe (ror=pid,  fio=None, fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)
        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'pid', 'None', 'false' )
        # cleanup before checks
        # retrieve values and delete if a handle has been created
        if handle_created != None:
            handle_dict = get_all_values_from_handle(handle_created)
            delete_handle(handle_created)
        # delete file from iRODS
        delete_irods_file(test_file)

       # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        # check basic handle field(s)
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
        # check for obsolete handle fields
        test_values.append({'action': 'Equal', 'result_value': handle_dict['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
        # check for PID V1 handle fields 
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fio'], 'expected_value': 'None', 'string': 'EUDAT/FIO has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror'], 'expected_value': handle_created, 'string': 'EUDAT/ROR has no value, we expect a value'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_assert_array(self, test_values)

    def test_50_b2safe_create_pid_03(self):
        """Test : create a PID using b2safe (ror=None, fio=pid,  fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'None', 'pid', 'false' )

        # cleanup before checks
        # retrieve values and delete if a handle has been created
        if handle_created != None:
            handle_dict = get_all_values_from_handle(handle_created)
            delete_handle(handle_created)
        # delete file from iRODS
        delete_irods_file(test_file)
        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        # check basic handle field(s)
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
        # check for obsolete handle fields
        test_values.append({'action': 'Equal', 'result_value': handle_dict['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
        # check for PID V1 handle fields 
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fio'], 'expected_value': handle_created, 'string': 'EUDAT/FIO has no value, we expect a vlaue'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror'], 'expected_value': 'None', 'string': 'EUDAT/ROR has a value, we expect a none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_assert_array(self, test_values)

    def test_50_b2safe_create_pid_04(self):
        """Test : create a PID using b2safe (ror=None, fio=None, fixed_content=true)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'None', 'None', 'true' )

        # cleanup before checks
        # retrieve values and delete if a handle has been created
        if handle_created != None:
            handle_dict = get_all_values_from_handle(handle_created)
            delete_handle(handle_created)
        # delete file from iRODS
        delete_irods_file(test_file)

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        # check basic handle field(s)
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
        # check for obsolete handle fields
        test_values.append({'action': 'Equal', 'result_value': handle_dict['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
        # check for PID V1 handle fields 
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fio'], 'expected_value': 'None', 'string': 'EUDAT/FIO has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fixedcontent'], 'expected_value': 'True', 'string': 'EUDAT/FIXED_CONTENT has not the value "True"'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror'], 'expected_value': 'None', 'string': 'EUDAT/ROR has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_assert_array(self, test_values)

    def test_50_b2safe_create_pid_05(self):
        """Test : create a PID using b2safe (ror=pid,  fio=pid,  fixed_content=true)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'pid', 'pid', 'true' )

        # cleanup before checks
        # retrieve values and delete if a handle has been created
        if handle_created != None:
            handle_dict = get_all_values_from_handle(handle_created)
            delete_handle(handle_created)
        # delete file from iRODS
        delete_irods_file(test_file)

         # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        # check basic handle field(s)
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
        # check for obsolete handle fields
        test_values.append({'action': 'Equal', 'result_value': handle_dict['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
        # check for PID V1 handle fields 
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fio'], 'expected_value': handle_created, 'string': 'EUDAT/FIO has no value, we expect a value'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fixedcontent'], 'expected_value': 'True', 'string': 'EUDAT/FIXED_CONTENT has not the value "True"'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror'], 'expected_value': handle_created, 'string': 'EUDAT/ROR has a value, we expect a value'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_assert_array(self, test_values)

    def test_50_b2safe_create_pid_06(self):
        """Test : create a PID using b2safe (ror=841/test,  fio=841/test,  fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, '841/test', '841/test', 'false' )

        # cleanup before checks
        # retrieve values and delete if a handle has been created
        if handle_created != None:
            handle_dict = get_all_values_from_handle(handle_created)
            delete_handle(handle_created)
        # delete file from iRODS
        delete_irods_file(test_file)

         # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        # check basic handle field(s)
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
        # check for obsolete handle fields
        test_values.append({'action': 'Equal', 'result_value': handle_dict['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
        # check for PID V1 handle fields 
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
        test_values.append({'action': 'NotEqual', 'result_value': handle_dict['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fio'], 'expected_value': '841/test', 'string': 'EUDAT/FIO has no value, we expect "841/test"'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['ror'], 'expected_value': '841/test', 'string': 'EUDAT/ROR has a value, we expect "841/test"'})
        test_values.append({'action': 'Equal', 'result_value': handle_dict['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_assert_array(self, test_values)

    def test_60_b2safe_create_pid_in_one_collection_01(self):
        """Test : create PIDs for a collection and files using b2safe (fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file1 = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_file3 = 'test_b2safe_data3.txt'
        test_file4 = 'test_b2safe_data4.txt'
        test_path = '/tmp/'+test_file1
        create_os_file(test_path)
        irods_input_test_path = self.irods_home+'/irods_input_dir'
        # create iRODS directory
        create_irods_directory(irods_input_test_path)

        # put test files in iRODS
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            put_irods_file(test_path, irods_input_test_path+'/'+irods_file)
        os.unlink(test_path)

        # create test handles
        handles_created = create_handles_for_collection(irods_input_test_path, 'false')

        # find PID for a collection
        handle_dir1_created = search_handle(irods_input_test_path)

        # find PID for a testfile
        handle1_created = search_handle(irods_input_test_path+'/'+test_file1)
        handle2_created = search_handle(irods_input_test_path+'/'+test_file2)
        handle3_created = search_handle(irods_input_test_path+'/'+test_file3)
        handle4_created = search_handle(irods_input_test_path+'/'+test_file4)

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        # delete directories from iRODS
        delete_irods_directory(irods_input_test_path)
        if handle_dir1_created != None:
            delete_handle(handle_dir1_created)

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle1_created, 'expected_value': 'empty', 'string': 'No PID has been created'}]
        test_values.append({'action': 'NotEqual', 'result_value': handle2_created, 'expected_value': 'empty', 'string': 'No PID has been created'})
        test_values.append({'action': 'NotEqual', 'result_value': handle3_created, 'expected_value': 'empty', 'string': 'No PID has been created'})
        test_values.append({'action': 'NotEqual', 'result_value': handle4_created, 'expected_value': 'empty', 'string': 'No PID has been created'})
        test_assert_array(self, test_values)

 
    def test_60_b2safe_create_pid_in_one_collection_02(self):
        """Test : create PIDs for a collection and files using b2safe (fixed_content=true)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file1 = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_file3 = 'test_b2safe_data3.txt'
        test_file4 = 'test_b2safe_data4.txt'
        test_path = '/tmp/'+test_file1
        create_os_file(test_path)
        irods_input_test_path = self.irods_home+'/irods_input_dir'
        # create iRODS directory
        create_irods_directory(irods_input_test_path)

        # put test files in iRODS
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            put_irods_file(test_path, irods_input_test_path+'/'+irods_file)
        os.unlink(test_path)

        # create test handles
        handles_created = create_handles_for_collection(irods_input_test_path, 'true')

        # find PID for a collection
        handle_dir1_created = search_handle(irods_input_test_path)

        # find PID for a testfile
        handle1_created = search_handle(irods_input_test_path+'/'+test_file1)
        handle2_created = search_handle(irods_input_test_path+'/'+test_file2)
        handle3_created = search_handle(irods_input_test_path+'/'+test_file3)
        handle4_created = search_handle(irods_input_test_path+'/'+test_file4)

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        # delete directories from iRODS
        delete_irods_directory(irods_input_test_path)
        if handle_dir1_created != None:
            delete_handle(handle_dir1_created)

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle1_created, 'expected_value': 'empty', 'string': 'No PID has been created'}]
        test_values.append({'action': 'NotEqual', 'result_value': handle2_created, 'expected_value': 'empty', 'string': 'No PID has been created'})
        test_values.append({'action': 'NotEqual', 'result_value': handle3_created, 'expected_value': 'empty', 'string': 'No PID has been created'})
        test_values.append({'action': 'NotEqual', 'result_value': handle4_created, 'expected_value': 'empty', 'string': 'No PID has been created'})
        test_assert_array(self, test_values)

    def test_60_b2safe_create_pid_in_one_collection_only_01(self):
        """Test : create PIDs for a collection and files using b2safe using similar directory names (fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file1 = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_file3 = 'test_b2safe_data3.txt'
        test_file4 = 'test_b2safe_data4.txt'
        test_path = '/tmp/'+test_file1
        create_os_file(test_path)
        irods_input_test_path  = self.irods_home+'/irods_input_dir'
        irods_input_test_path2 = self.irods_home+'/irods_input_dir2'
        # create iRODS directory
        create_irods_directory(irods_input_test_path)
        create_irods_directory(irods_input_test_path2)

        # put test files in iRODS
        for irods_file in [test_file1, test_file2]:
            put_irods_file(test_path, irods_input_test_path+'/'+irods_file)
        for irods_file in [test_file3, test_file4]:
            put_irods_file(test_path, irods_input_test_path2+'/'+irods_file)
        os.unlink(test_path)

        # create test handles
        handles_created = create_handles_for_collection(irods_input_test_path, 'false')

        # find PID for a collection
        handle_dir1_created = search_handle(irods_input_test_path)
        handle_dir2_created = search_handle(irods_input_test_path2)

        # find PIDs for testfiles
        handle1_created = search_handle(irods_input_test_path+'/'+test_file1)
        handle2_created = search_handle(irods_input_test_path+'/'+test_file2)
        handle3_created = search_handle(irods_input_test_path2+'/'+test_file3)
        handle4_created = search_handle(irods_input_test_path2+'/'+test_file4)

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file1, test_file2]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        for irods_file in [test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path2+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        # delete directories from iRODS
        for directory in [irods_input_test_path, irods_input_test_path2]:        
            delete_irods_directory(directory)
        if handle_dir1_created != None:
            delete_handle(handle_dir1_created)
        if handle_dir2_created != None:
            delete_handle(handle_dir2_created)

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle1_created, 'expected_value': 'empty', 'string': 'No PID has been created'}]
        test_values.append({'action': 'NotEqual', 'result_value': handle2_created, 'expected_value': 'empty', 'string': 'No PID has been created'})
        test_values.append({'action': 'Equal', 'result_value': handle3_created, 'expected_value': 'empty', 'string': 'A PID has been created, this should NOT happen'})
        test_values.append({'action': 'Equal', 'result_value': handle4_created, 'expected_value': 'empty', 'string': 'A PID has been created, this should NOT happen'})
        test_assert_array(self, test_values)


    def test_60_b2safe_create_pid_in_one_collection_only_02(self):
        """Test : create PIDs for a collection and files using b2safe using similar directory names (fixed_content=true)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file1 = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_file3 = 'test_b2safe_data3.txt'
        test_file4 = 'test_b2safe_data4.txt'
        test_path = '/tmp/'+test_file1
        create_os_file(test_path)
        irods_input_test_path  = self.irods_home+'/irods_input_dir'
        irods_input_test_path2 = self.irods_home+'/irods_input_dir2'
        # create iRODS directory
        create_irods_directory(irods_input_test_path)
        create_irods_directory(irods_input_test_path2)

        # put test files in iRODS
        for irods_file in [test_file1, test_file2]:
            put_irods_file(test_path, irods_input_test_path+'/'+irods_file)
        for irods_file in [test_file3, test_file4]:
            put_irods_file(test_path, irods_input_test_path2+'/'+irods_file)
        os.unlink(test_path)

        # create test handles
        handles_created = create_handles_for_collection(irods_input_test_path, 'true')

        # find PID for a collection
        handle_dir1_created = search_handle(irods_input_test_path)
        handle_dir2_created = search_handle(irods_input_test_path2)

        # find PIDs for testfiles
        handle1_created = search_handle(irods_input_test_path+'/'+test_file1)
        handle2_created = search_handle(irods_input_test_path+'/'+test_file2)
        handle3_created = search_handle(irods_input_test_path2+'/'+test_file3)
        handle4_created = search_handle(irods_input_test_path2+'/'+test_file4)

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file1, test_file2]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        for irods_file in [test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path2+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        # delete directories from iRODS
        for directory in [irods_input_test_path, irods_input_test_path2]:        
            delete_irods_directory(directory)
        for handle in [handle_dir1_created, handle_dir2_created]:
            if handle != None:
                delete_handle(handle)

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle1_created, 'expected_value': 'empty', 'string': 'No PID has been created'}]
        test_values.append({'action': 'NotEqual', 'result_value': handle2_created, 'expected_value': 'empty', 'string': 'No PID has been created'})
        test_values.append({'action': 'Equal', 'result_value': handle3_created, 'expected_value': 'empty', 'string': 'A PID has been created, this should NOT happen'})
        test_values.append({'action': 'Equal', 'result_value': handle4_created, 'expected_value': 'empty', 'string': 'A PID has been created, this should NOT happen'})
        test_assert_array(self, test_values)

    def test_70_b2safe_local_for_one_file_not_registered_non_recursive(self):
        """Test : replicate a single file locally using b2safe (not registered, non recursive)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # replicate the file
        replica_result = replicate_irods_file(self.irods_home+'/'+test_file, self.irods_home+'/'+test_file2, 'false', 'false')


        # find PID for testfile
        handle_created = search_handle(self.irods_home+'/'+test_file)

        # find 
        
        # find PID in iCAT for testfile2
        imeta_pid_result = imeta_ls_specific('-d', test_file2, 'PID')
        

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file, test_file2]:
            pid_result = search_handle(self.irods_home+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            # delete file from iRODS
            delete_irods_file(irods_file)

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        test_values.append({'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'})
        test_assert_array(self, test_values)

    def test_70_b2safe_local_for_one_file_not_registered_recursive(self):
        """Test : replicate a single file locally using b2safe (not registered,     recursive)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)

        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # replicate the file
        replica_result = replicate_irods_file(self.irods_home+'/'+test_file, self.irods_home+'/'+test_file2, 'false', 'true')

        # find PID for testfile
        handle_created = search_handle(self.irods_home+'/'+test_file)
         
        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file, test_file2]:
            pid_result = search_handle(self.irods_home+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            # delete file from iRODS
            delete_irods_file(irods_file)

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        test_values.append({'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'})
        test_assert_array(self, test_values)

    def test_70_b2safe_local_for_one_file_registered_non_recursive_01(self):
        """Test : replicate a single file locally using b2safe (    registered, non recursive, ror=pid, fio=pid, fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'pid', 'pid' , 'false' )

        # replicate the file
        replica_result = replicate_irods_file(self.irods_home+'/'+test_file, self.irods_home+'/'+test_file2, 'true', 'false')

        # find PID in iCAT for testfile2
        imeta_pid_result = imeta_ls_specific('-d', test_file2, 'PID')
        # find EUDAT/ROR in iCAT for testfile2
        imeta_ror_result = imeta_ls_specific('-d', test_file2, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        n = 0
        handle_array = []
        for irods_file in [test_file, test_file2]:
            pid_result = search_handle(self.irods_home+'/'+irods_file)
            if pid_result != None:
                handle_array.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                n += 1
            # delete file from iRODS
            delete_irods_file(irods_file)
            replica_handle = pid_result

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        test_values.append({'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'})
        if n >= 1:
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['fio'], 'expected_value': handle_created, 'string': 'EUDAT/FIO has no value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['replica'].upper(), 'expected_value': replica_handle.upper(), 'string': 'EUDAT/REPLICA has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ror'], 'expected_value': handle_created, 'string': 'EUDAT/ROR has a value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        if n >= 2:
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['fio'], 'expected_value': handle_created, 'string': 'EUDAT/FIO has no value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['parent'], 'expected_value': handle_created, 'string': 'EUDAT/PARENT has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ror'], 'expected_value': handle_created, 'string': 'EUDAT/ROR has a value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_values.append({'action': 'NotEqual', 'result_value': imeta_pid_result, 'expected_value': None, 'string': 'The PID is NOT filled in in the replica in iCAT'})
        test_values.append({'action': 'Equal', 'result_value': imeta_ror_result, 'expected_value': handle_created, 'string': 'The PID of the original file is NOT the EUDAT/ROR value in the iCAT'})
        test_assert_array(self, test_values)

    def test_70_b2safe_local_for_one_file_registered_non_recursive_02(self):
        """Test : replicate a single file locally using b2safe (    registered, non recursive, ror=841/test, fio=None, fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, '841/test', 'None', 'false' )

        # replicate the file
        replica_result = replicate_irods_file(self.irods_home+'/'+test_file, self.irods_home+'/'+test_file2, 'true', 'false')

        # find PID in iCAT for testfile2
        imeta_pid_result = imeta_ls_specific('-d', test_file2, 'PID')
        # find EUDAT/ROR in iCAT for testfile2
        imeta_ror_result = imeta_ls_specific('-d', test_file2, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        n = 0
        handle_array = []
        for irods_file in [test_file, test_file2]:
            pid_result = search_handle(self.irods_home+'/'+irods_file)
            if pid_result != None:
                handle_array.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                n += 1
            # delete file from iRODS
            delete_irods_file(irods_file)
            replica_handle = pid_result

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        test_values.append({'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'})
        if n >= 1:
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['fio'], 'expected_value': 'None', 'string': 'EUDAT/FIO has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['replica'].upper(), 'expected_value': replica_handle.upper(), 'string': 'EUDAT/REPLICA has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ror'], 'expected_value': '841/test', 'string': 'EUDAT/ROR has no value, we expect 841/test'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        if n >= 2:
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['fio'], 'expected_value': handle_created, 'string': 'EUDAT/FIO has no value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['parent'], 'expected_value': handle_created, 'string': 'EUDAT/PARENT has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ror'], 'expected_value': '841/test', 'string': 'EUDAT/ROR has no value, we expect 841/test'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_values.append({'action': 'NotEqual', 'result_value': imeta_pid_result, 'expected_value': None, 'string': 'The PID is NOT filled in in the replica in iCAT'})
        test_values.append({'action': 'Equal', 'result_value': imeta_ror_result, 'expected_value': '841/test', 'string': 'The ROR at the original file is NOT the EUDAT/ROR value in the iCAT'})
        test_assert_array(self, test_values)


    def test_70_b2safe_local_for_one_file_registered_non_recursive_03(self):
        """Test : replicate a single file locally using b2safe (    registered, non recursive, ror=None, fio=None, fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'None', 'None', 'false' )

        # replicate the file
        replica_result = replicate_irods_file(self.irods_home+'/'+test_file, self.irods_home+'/'+test_file2, 'true', 'false')

        # find PID in iCAT for testfile2
        imeta_pid_result = imeta_ls_specific('-d', test_file2, 'PID')
        # find EUDAT/ROR in iCAT for testfile2
        imeta_ror_result = imeta_ls_specific('-d', test_file2, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        n = 0
        handle_array = []
        for irods_file in [test_file, test_file2]:
            pid_result = search_handle(self.irods_home+'/'+irods_file)
            if pid_result != None:
                handle_array.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                n += 1
            # delete file from iRODS
            delete_irods_file(irods_file)
            replica_handle = pid_result

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        test_values.append({'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'})
        if n >= 1:
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['fio'], 'expected_value': 'None', 'string': 'EUDAT/FIO has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['replica'].upper(), 'expected_value': replica_handle.upper(), 'string': 'EUDAT/REPLICA has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ror'], 'expected_value': 'None', 'string': 'EUDAT/ROR has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        if n >= 2:
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['fio'], 'expected_value': handle_created, 'string': 'EUDAT/FIO has no value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['parent'], 'expected_value': handle_created, 'string': 'EUDAT/PARENT has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ror'], 'expected_value': handle_created, 'string': 'EUDAT/ROR has no value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_values.append({'action': 'NotEqual', 'result_value': imeta_pid_result, 'expected_value': None, 'string': 'The PID is NOT filled in in the replica in iCAT'})
        test_values.append({'action': 'Equal', 'result_value': imeta_ror_result, 'expected_value': handle_created, 'string': 'The PID of the original file is NOT the EUDAT/ROR value in the iCAT'})
        test_assert_array(self, test_values)

    def test_70_b2safe_local_for_one_file_registered_recursive(self):
        """Test : replicate a single file locally using b2safe (    registered,     recursive, ror=pid, fio=pid, fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)

        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'pid', 'pid', 'false' )

        # replicate the file
        replica_result = replicate_irods_file(self.irods_home+'/'+test_file, self.irods_home+'/'+test_file2, 'true', 'true')

        # find PID in iCAT for testfile2
        imeta_pid_result = imeta_ls_specific('-d', test_file2, 'PID')
        # find EUDAT/ROR in iCAT for testfile2
        imeta_ror_result = imeta_ls_specific('-d', test_file2, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        n = 0
        handle_array = []
        for irods_file in [test_file, test_file2]:
            pid_result = search_handle(self.irods_home+'/'+irods_file)
            if pid_result != None:
                handle_array.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                n += 1
            # delete file from iRODS
            delete_irods_file(irods_file)
            replica_handle = pid_result

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        test_values.append({'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'})
        if n >= 1:
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[0]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['fio'], 'expected_value': handle_created, 'string': 'EUDAT/FIO has no value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['replica'].upper(), 'expected_value': replica_handle.upper(), 'string': 'EUDAT/REPLICA has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['ror'], 'expected_value': handle_created, 'string': 'EUDAT/ROR has a value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[0]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        if n >= 2:
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array[1]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['fio'], 'expected_value': handle_created, 'string': 'EUDAT/FIO has no value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['parent'], 'expected_value': handle_created, 'string': 'EUDAT/PARENT has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['ror'], 'expected_value': handle_created, 'string': 'EUDAT/ROR has a value, we expect '+handle_created})
            test_values.append({'action': 'Equal', 'result_value': handle_array[1]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_values.append({'action': 'NotEqual', 'result_value': imeta_pid_result, 'expected_value': None, 'string': 'The PID is NOT filled in in the replica in iCAT'})
        test_values.append({'action': 'Equal', 'result_value': imeta_ror_result, 'expected_value': handle_created, 'string': 'The PID of the original file is NOT the EUDAT/ROR value in the iCAT'})
        test_assert_array(self, test_values)

    def test_75_b2safe_local_for_one_directory_not_registered_recursive(self):
        """Test : replicate a single directory locally using b2safe (not registered,    recursive)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file1 = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_file3 = 'test_b2safe_data3.txt'
        test_file4 = 'test_b2safe_data4.txt'
        test_path = '/tmp/'+test_file1
        create_os_file(test_path)
        irods_input_test_path = self.irods_home+'/irods_input_dir'
        irods_output_test_path = self.irods_home+'/irods_output_dir'
        # create iRODS directory
        create_irods_directory(irods_input_test_path)

        # put test files in iRODS
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            put_irods_file(test_path, irods_input_test_path+'/'+irods_file)
        os.unlink(test_path)

        # replicate the file
        replica_result = replicate_irods_file(irods_input_test_path, irods_output_test_path, 'false', 'true')

        # find PID for a collections
        handle_dir1_created = search_handle(irods_input_test_path)
        handle_dir2_created = search_handle(irods_output_test_path)

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            pid_result = search_handle(irods_output_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        # delete directories from iRODS
        for directory in [irods_input_test_path, irods_output_test_path]:        
            delete_irods_directory(directory)
        for handle in [handle_dir1_created, handle_dir2_created]:
            if handle != None:
                delete_handle(handle)

        # create array with values to test and execute
        test_values=[{'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'}]
        test_assert_array(self, test_values)


    def test_75_b2safe_local_for_one_directory_registered_recursive(self):
        """Test : replicate a single directory locally using b2safe (    registered,    recursive, ror=pid, fio=pid, fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file1 = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_file3 = 'test_b2safe_data3.txt'
        test_file4 = 'test_b2safe_data4.txt'
        test_path = '/tmp/'+test_file1
        create_os_file(test_path)
        irods_input_test_path = self.irods_home+'/irods_input_dir'
        irods_output_test_path = self.irods_home+'/irods_output_dir'
        # create iRODS directory
        create_irods_directory(irods_input_test_path)

        # put test files in iRODS
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            put_irods_file(test_path, irods_input_test_path+'/'+irods_file)
        os.unlink(test_path)

        # create test handle
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            handle_created = create_handle(irods_input_test_path+'/'+irods_file, 'pid', 'pid', 'false')

        # replicate the file
        replica_result = replicate_irods_file(irods_input_test_path, irods_output_test_path, 'true', 'true')

        # find PID in iCAT for testfile2 original
        imeta_pid_org_result = imeta_ls_specific('-d', irods_input_test_path+'/'+test_file2, 'PID')
        # find EUDAT/ROR in iCAT for testfile2 original
        imeta_ror_org_result = imeta_ls_specific('-d', irods_input_test_path+'/'+test_file2, 'EUDAT/ROR')

        # find PID in iCAT for testfile2 replica
        imeta_pid_repl_result = imeta_ls_specific('-d', irods_output_test_path+'/'+test_file2, 'PID')
        # find EUDAT/ROR in iCAT for testfile2 replica
        imeta_ror_repl_result = imeta_ls_specific('-d', irods_output_test_path+'/'+test_file2, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        ni = 0
        no = 0
        handles_created_arr = []
        handles_repl_arr = []
        handle_array_org = []
        handle_array_repl = []
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            handles_created_arr.append(pid_result)
            if pid_result != None:
                handle_array_org.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                ni += 1
            pid_result = search_handle(irods_output_test_path+'/'+irods_file)
            handles_repl_arr.append(pid_result)
            if pid_result != None:
                handle_array_repl.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                no += 1
        # delete directories from iRODS
        for directory in [irods_input_test_path, irods_output_test_path]:        
            delete_irods_directory(directory)

        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        test_values.append({'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'})
        test_values.append({'action': 'Equal', 'result_value': ni, 'expected_value': no, 'string': 'The number of handles and replicated handles is not the same'})
        for index in range(0, ni):
            # original handle
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['fio'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/FIO has no value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['replica'].upper(), 'expected_value': handles_repl_arr[index].upper(), 'string': 'EUDAT/REPLICA has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ror'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/ROR has a value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
            # replication handle
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['fio'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/FIO has no value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['parent'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/PARENT has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ror'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/ROR has a value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_values.append({'action': 'NotEqual', 'result_value': imeta_pid_repl_result, 'expected_value': None, 'string': 'The PID is NOT filled in in the replica in iCAT'})
        test_values.append({'action': 'Equal', 'result_value': imeta_ror_repl_result, 'expected_value': imeta_pid_org_result, 'string': 'The PID of the original file is NOT the EUDAT/ROR value in the iCAT'})
        test_assert_array(self, test_values)


    def test_80_b2safe_local_for_multiple_directories_not_registered_recursive(self):
        """Test : replicate multiple directories locally using b2safe (not registered,    recursive)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file1 = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_file3 = 'test_b2safe_data3.txt'
        test_file4 = 'test_b2safe_data4.txt'
        test_path = '/tmp/'+test_file1
        create_os_file(test_path)
        irods_input_test_path   = self.irods_home+'/irods_input_dir'
        irods_input_test_path2  = self.irods_home+'/irods_input_dir/irods_subdir'
        irods_output_test_path  = self.irods_home+'/irods_output_dir'
        irods_output_test_path2 = self.irods_home+'/irods_output_dir/irods_subdir'
        # create iRODS directory
        create_irods_directory(irods_input_test_path)
        create_irods_directory(irods_input_test_path2)

        # put test files in iRODS
        for irods_file in [test_file1, test_file2]:
            put_irods_file(test_path, irods_input_test_path+'/'+irods_file)
        for irods_file in [test_file3, test_file4]:
            put_irods_file(test_path, irods_input_test_path2+'/'+irods_file)
        os.unlink(test_path)

        # replicate the file
        replica_result = replicate_irods_file(irods_input_test_path, irods_output_test_path, 'false', 'true')

        # find PID for a collections
        handle_dir1_created = search_handle(irods_input_test_path)
        handle_dir2_created = search_handle(irods_output_test_path)
        handle_dir3_created = search_handle(irods_input_test_path2)
        handle_dir4_created = search_handle(irods_output_test_path2)

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file1, test_file2]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            pid_result = search_handle(irods_output_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        for irods_file in [test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path2+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            pid_result = search_handle(irods_output_test_path2+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        # delete directories from iRODS
        for directory in [irods_input_test_path, irods_output_test_path]:        
            delete_irods_directory(directory)
        for handle in [handle_dir1_created, handle_dir2_created, handle_dir3_created, handle_dir4_created]:
            if handle != None:
                delete_handle(handle)

        test_values=[{'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'}]
        test_assert_array(self, test_values)

    def test_80_b2safe_local_for_multiple_directories_registered_recursive_01(self):
        """Test : replicate multiple directories locally using b2safe (    registered,    recursive, ror=pid, fio=pid, fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file1 = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_file3 = 'test_b2safe_data3.txt'
        test_file4 = 'test_b2safe_data4.txt'
        test_path = '/tmp/'+test_file1
        create_os_file(test_path)
        irods_input_test_path   = self.irods_home+'/irods_input_dir'
        irods_input_test_path2  = self.irods_home+'/irods_input_dir/irods_subdir'
        irods_output_test_path  = self.irods_home+'/irods_output_dir'
        irods_output_test_path2 = self.irods_home+'/irods_output_dir/irods_subdir'
        # create iRODS directory
        create_irods_directory(irods_input_test_path)
        create_irods_directory(irods_input_test_path2)

        # put test files in iRODS
        for irods_file in [test_file1, test_file2]:
            put_irods_file(test_path, irods_input_test_path+'/'+irods_file)
        for irods_file in [test_file3, test_file4]:
            put_irods_file(test_path, irods_input_test_path2+'/'+irods_file)
        os.unlink(test_path)

        # create test handle
        for irods_file in [test_file1, test_file2]:
            handle_created = create_handle(irods_input_test_path+'/'+irods_file, 'pid', 'pid', 'false')
        for irods_file in [test_file3, test_file4]:
            handle_created = create_handle(irods_input_test_path2+'/'+irods_file, 'pid', 'pid', 'false')

        # replicate the file
        replica_result = replicate_irods_file(irods_input_test_path, irods_output_test_path, 'true', 'true')

        # find PID in iCAT for testfile4 original
        imeta_pid_org_result = imeta_ls_specific('-d', irods_input_test_path2+'/'+test_file4, 'PID')
        # find EUDAT/ROR in iCAT for testfile4 original
        imeta_ror_org_result = imeta_ls_specific('-d', irods_input_test_path2+'/'+test_file4, 'EUDAT/ROR')

        # find PID in iCAT for testfile4 replica
        imeta_pid_repl_result = imeta_ls_specific('-d', irods_output_test_path2+'/'+test_file4, 'PID')
        # find EUDAT/ROR in iCAT for testfile4 replica
        imeta_ror_repl_result = imeta_ls_specific('-d', irods_output_test_path2+'/'+test_file4, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        ni = 0
        no = 0
        handles_created_arr = []
        handles_repl_arr = []
        handle_array_org = []
        handle_array_repl = []
        for irods_file in [test_file1, test_file2]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            handles_created_arr.append(pid_result)
            if pid_result != None:
                handle_array_org.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                ni += 1
            pid_result = search_handle(irods_output_test_path+'/'+irods_file)
            handles_repl_arr.append(pid_result)
            if pid_result != None:
                handle_array_repl.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                no += 1
        for irods_file in [test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path2+'/'+irods_file)
            handles_created_arr.append(pid_result)
            if pid_result != None:
                handle_array_org.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                ni += 1
            pid_result = search_handle(irods_output_test_path2+'/'+irods_file)
            handles_repl_arr.append(pid_result)
            if pid_result != None:
                handle_array_repl.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                no += 1
        # delete directories from iRODS
        for directory in [irods_input_test_path, irods_output_test_path]:        
            delete_irods_directory(directory)


        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        test_values.append({'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'})
        test_values.append({'action': 'Equal', 'result_value': ni, 'expected_value': no, 'string': 'The number of handles and replicated handles is not the same'})
        for index in range(0, ni):
            # original handle
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['fio'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/FIO has no value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['replica'].upper(), 'expected_value': handles_repl_arr[index].upper(), 'string': 'EUDAT/REPLICA has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ror'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/ROR has a value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
            # replication handle
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['fio'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/FIO has no value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['parent'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/PARENT has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ror'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/ROR has a value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_values.append({'action': 'NotEqual', 'result_value': imeta_pid_repl_result, 'expected_value': None, 'string': 'The PID is NOT filled in in the replica in iCAT'})
        test_values.append({'action': 'Equal', 'result_value': imeta_ror_repl_result, 'expected_value': imeta_pid_org_result, 'string': 'The PID of the original file is NOT the EUDAT/ROR value in the iCAT'})
        test_assert_array(self, test_values)

    def test_80_b2safe_local_for_multiple_directories_registered_recursive_02(self):
        """Test : replicate multiple directories locally using b2safe (    registered,    recursive, ror=841/test, fio=None, fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file1 = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_file3 = 'test_b2safe_data3.txt'
        test_file4 = 'test_b2safe_data4.txt'
        test_path = '/tmp/'+test_file1
        create_os_file(test_path)
        irods_input_test_path   = self.irods_home+'/irods_input_dir'
        irods_input_test_path2  = self.irods_home+'/irods_input_dir/irods_subdir'
        irods_output_test_path  = self.irods_home+'/irods_output_dir'
        irods_output_test_path2 = self.irods_home+'/irods_output_dir/irods_subdir'
        # create iRODS directory
        create_irods_directory(irods_input_test_path)
        create_irods_directory(irods_input_test_path2)

        # put test files in iRODS
        for irods_file in [test_file1, test_file2]:
            put_irods_file(test_path, irods_input_test_path+'/'+irods_file)
        for irods_file in [test_file3, test_file4]:
            put_irods_file(test_path, irods_input_test_path2+'/'+irods_file)
        os.unlink(test_path)

        # create test handle
        for irods_file in [test_file1, test_file2]:
            handle_created = create_handle(irods_input_test_path+'/'+irods_file, '841/test', 'None', 'false')
        for irods_file in [test_file3, test_file4]:
            handle_created = create_handle(irods_input_test_path2+'/'+irods_file, '841/test', 'None', 'false')

        # replicate the file
        replica_result = replicate_irods_file(irods_input_test_path, irods_output_test_path, 'true', 'true')

        # find PID in iCAT for testfile4 original
        imeta_pid_org_result = imeta_ls_specific('-d', irods_input_test_path2+'/'+test_file4, 'PID')
        # find EUDAT/ROR in iCAT for testfile4 original
        imeta_ror_org_result = imeta_ls_specific('-d', irods_input_test_path2+'/'+test_file4, 'EUDAT/ROR')

        # find PID in iCAT for testfile4 replica
        imeta_pid_repl_result = imeta_ls_specific('-d', irods_output_test_path2+'/'+test_file4, 'PID')
        # find EUDAT/ROR in iCAT for testfile4 replica
        imeta_ror_repl_result = imeta_ls_specific('-d', irods_output_test_path2+'/'+test_file4, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        ni = 0
        no = 0
        handles_created_arr = []
        handles_repl_arr = []
        handle_array_org = []
        handle_array_repl = []
        for irods_file in [test_file1, test_file2]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            handles_created_arr.append(pid_result)
            if pid_result != None:
                handle_array_org.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                ni += 1
            pid_result = search_handle(irods_output_test_path+'/'+irods_file)
            handles_repl_arr.append(pid_result)
            if pid_result != None:
                handle_array_repl.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                no += 1
        for irods_file in [test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path2+'/'+irods_file)
            handles_created_arr.append(pid_result)
            if pid_result != None:
                handle_array_org.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                ni += 1
            pid_result = search_handle(irods_output_test_path2+'/'+irods_file)
            handles_repl_arr.append(pid_result)
            if pid_result != None:
                handle_array_repl.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                no += 1
        # delete directories from iRODS
        for directory in [irods_input_test_path, irods_output_test_path]:        
            delete_irods_directory(directory)


        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        test_values.append({'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'})
        test_values.append({'action': 'Equal', 'result_value': ni, 'expected_value': no, 'string': 'The number of handles and replicated handles is not the same'})
        for index in range(0, ni):
            # original handle
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['fio'], 'expected_value': 'None', 'string': 'EUDAT/FIO has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['replica'].upper(), 'expected_value': handles_repl_arr[index].upper(), 'string': 'EUDAT/REPLICA has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ror'], 'expected_value': '841/test', 'string': 'EUDAT/ROR has no value, we expect 841/test'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
            # replication handle
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['fio'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/FIO has no value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['parent'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/PARENT has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ror'], 'expected_value': '841/test', 'string': 'EUDAT/ROR has no value, we expect 841/test'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_values.append({'action': 'NotEqual', 'result_value': imeta_pid_repl_result, 'expected_value': None, 'string': 'The PID is NOT filled in in the replica in iCAT'})
        test_values.append({'action': 'Equal', 'result_value': imeta_ror_repl_result, 'expected_value': '841/test', 'string': 'The PID of the original file is NOT the EUDAT/ROR value in the iCAT'})
        test_assert_array(self, test_values)

    def test_80_b2safe_local_for_multiple_directories_registered_recursive_03(self):
        """Test : replicate multiple directories locally using b2safe (    registered,    recursive, ror=None, fio=None, fixed_content=false)"""
        log_to_rodsLog("Starting test: "+str(sys._getframe().f_code.co_name))

        # create test file
        test_file1 = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_file3 = 'test_b2safe_data3.txt'
        test_file4 = 'test_b2safe_data4.txt'
        test_path = '/tmp/'+test_file1
        create_os_file(test_path)
        irods_input_test_path   = self.irods_home+'/irods_input_dir'
        irods_input_test_path2  = self.irods_home+'/irods_input_dir/irods_subdir'
        irods_output_test_path  = self.irods_home+'/irods_output_dir'
        irods_output_test_path2 = self.irods_home+'/irods_output_dir/irods_subdir'
        # create iRODS directory
        create_irods_directory(irods_input_test_path)
        create_irods_directory(irods_input_test_path2)

        # put test files in iRODS
        for irods_file in [test_file1, test_file2]:
            put_irods_file(test_path, irods_input_test_path+'/'+irods_file)
        for irods_file in [test_file3, test_file4]:
            put_irods_file(test_path, irods_input_test_path2+'/'+irods_file)
        os.unlink(test_path)

        # create test handle
        for irods_file in [test_file1, test_file2]:
            handle_created = create_handle(irods_input_test_path+'/'+irods_file, 'None', 'None', 'false')
        for irods_file in [test_file3, test_file4]:
            handle_created = create_handle(irods_input_test_path2+'/'+irods_file, 'None', 'None', 'false')

        # replicate the file
        replica_result = replicate_irods_file(irods_input_test_path, irods_output_test_path, 'true', 'true')

        # find PID in iCAT for testfile4 original
        imeta_pid_org_result = imeta_ls_specific('-d', irods_input_test_path2+'/'+test_file4, 'PID')
        # find EUDAT/ROR in iCAT for testfile4 original
        imeta_ror_org_result = imeta_ls_specific('-d', irods_input_test_path2+'/'+test_file4, 'EUDAT/ROR')

        # find PID in iCAT for testfile4 replica
        imeta_pid_repl_result = imeta_ls_specific('-d', irods_output_test_path2+'/'+test_file4, 'PID')
        # find EUDAT/ROR in iCAT for testfile4 replica
        imeta_ror_repl_result = imeta_ls_specific('-d', irods_output_test_path2+'/'+test_file4, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        ni = 0
        no = 0
        handles_created_arr = []
        handles_repl_arr = []
        handle_array_org = []
        handle_array_repl = []
        for irods_file in [test_file1, test_file2]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            handles_created_arr.append(pid_result)
            if pid_result != None:
                handle_array_org.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                ni += 1
            pid_result = search_handle(irods_output_test_path+'/'+irods_file)
            handles_repl_arr.append(pid_result)
            if pid_result != None:
                handle_array_repl.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                no += 1
        for irods_file in [test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path2+'/'+irods_file)
            handles_created_arr.append(pid_result)
            if pid_result != None:
                handle_array_org.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                ni += 1
            pid_result = search_handle(irods_output_test_path2+'/'+irods_file)
            handles_repl_arr.append(pid_result)
            if pid_result != None:
                handle_array_repl.append(get_all_values_from_handle(pid_result))
                delete_handle(pid_result)
                no += 1
        # delete directories from iRODS
        for directory in [irods_input_test_path, irods_output_test_path]:        
            delete_irods_directory(directory)


        # create array with values to test and execute
        test_values=[{'action': 'NotEqual', 'result_value': handle_created, 'expected_value': None, 'string': 'No PID has been created'}]
        test_values.append({'action': 'Equal', 'result_value': replica_result, 'expected_value': 'Success!', 'string': 'The replication was NOT succesful'})
        test_values.append({'action': 'Equal', 'result_value': ni, 'expected_value': no, 'string': 'The number of handles and replicated handles is not the same'})
        for index in range(0, ni):
            # original handle
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_org[index]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['fio'], 'expected_value': 'None', 'string': 'EUDAT/FIO has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['parent'], 'expected_value': 'None', 'string': 'EUDAT/PARENT has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['replica'].upper(), 'expected_value': handles_repl_arr[index].upper(), 'string': 'EUDAT/REPLICA has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['ror'], 'expected_value': 'None', 'string': 'EUDAT/ROR has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_org[index]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
            # replication handle
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['url'], 'expected_value': 'None', 'string': 'URL does not have a value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['loc_10320'], 'expected_value': 'None', 'string': '10320/LOC has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['checksum_old'], 'expected_value': 'None', 'string': 'CHECKSUM has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ppid'], 'expected_value': 'None', 'string': 'PPID has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ror_old'], 'expected_value': 'None', 'string': 'ROR has a value, we expect none'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['checksum'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM has no value'})
            test_values.append({'action': 'NotEqual', 'result_value': handle_array_repl[index]['checksum_timestamp'], 'expected_value': 'None', 'string': 'EUDAT/CHECKSUM_TIMESTAMP has no value'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['fio'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/FIO has no value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['fixedcontent'], 'expected_value': 'False', 'string': 'EUDAT/FIXED_CONTENT has not the value "False"'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['parent'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/PARENT has no value, we expect one'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['replica'], 'expected_value': 'None', 'string': 'EUDAT/REPLICA has a value, we expect none'})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['ror'].upper(), 'expected_value': handles_created_arr[index].upper(), 'string': 'EUDAT/ROR has no value, we expect '+handles_created_arr[index]})
            test_values.append({'action': 'Equal', 'result_value': handle_array_repl[index]['version'], 'expected_value': '1', 'string': 'EUDAT/PROFILE_VERSION has no or a different version, we expect 1'})
        test_values.append({'action': 'NotEqual', 'result_value': imeta_pid_repl_result, 'expected_value': None, 'string': 'The PID is NOT filled in in the replica in iCAT'})
        test_values.append({'action': 'Equal', 'result_value': imeta_ror_repl_result, 'expected_value': imeta_pid_org_result, 'string': 'The PID of the original file is NOT the EUDAT/ROR value in the iCAT'})
        test_assert_array(self, test_values)



