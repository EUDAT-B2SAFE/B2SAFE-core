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
    return arr

def create_os_file(input_filename):
    '''procedure to create a file with "Hello World!"'''
    with open(input_filename, "w") as write_file:
        write_file.write("Hello World!")

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
    '''procedure to retrive a specific value from an iRODS AVU'''
    # find AVU value in iCAT
    imeta_data_result = ''
    command = ["imeta", "ls", objtype, objname, avu_name]
    imeta_result = subprocess_popen(command)
    for elem in imeta_result:
        if 'value' in elem:
            imeta_data_result = elem.split()[1]
    return imeta_data_result

def put_irods_file(input_file, output_file):
    '''procedure to put a file on the OS in iRODS'''
    # put test file in iRODS
    command = ["iput", "-f", input_file, output_file]
    put_result = subprocess_popen(command)
    return put_result

def replicate_irods_file(source, destination, registered, recursive):
    '''procedure to replicate a file with EUDAT rulesin iRODS'''
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

def create_handle(irods_test_file_path, icat_cache):
    '''procedure to create a handle'''
    # create test rule
    irule_rule = '{EUDATCreatePID(*parent_pid, *path, *ror, *iCATCache, *newPID)}'
    irule_input = '*parent_pid=%*path='+irods_test_file_path+'%*ror=%*iCATCache='+icat_cache
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

def delete_handle(pid):
    '''procedure to delete a pid'''
    # create iRODS rule to delete created pid
    irule_rule = '{getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);msiExecCmd("epicclient.py","*credStoreType *credStorePath delete *pid", "null", "null", "null", *out)}'
    irule_input = '*pid='+pid
    irule_output = '*out'
    command = ["irule", irule_rule, irule_input, irule_output]
    # execute rule to delete pid
    irule_result = subprocess_popen(command)
    return irule_result

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

    def tearDown(self):
        """ Cleanup testB2SafeCmd environment after the tests have run
        """

    def test_10_irods_functions(self):
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

    def test_10_irods_put_file(self):
        """Test that it is possible to put a file in iRODS"""
        test_file = 'test_data.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)
        command = ["ils", test_file]
        ils_result = subprocess_popen(command)
        ils_result_expected = self.irods_home+'/'+test_file
        self.assertEqual(
            ils_result[0], ils_result_expected,
            'file should have been put in :'+ils_result_expected)

    def test_30_b2safe_search_non_existing_PID(self):
        '''Test that it is possible to search for non existing handles'''
        search_result = search_handle('boekie_zoekie')
        self.assertEqual(
            search_result, 'empty',
            'The result should have been "empty"')

    def test_50_b2safe_create_pid(self):
        """Test that it is possible to create a PID using b2safe"""
        # create test file
        test_file = 'test_b2safe_data.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'false')

        # cleanup before checks
        # delete created pid
        if handle_created != None:
            delete_handle(handle_created)
        # delete file from iRODS
        delete_irods_file(test_file)

        # check if PID is created
        self.assertNotEqual(
            handle_created, None,
            'No PID has been created')


    def test_50_b2safe_create_pid_with_pid_in_icat(self):
        """Test that it is possible to create a PID using b2safe and put pid in icat database"""
        # create test file
        test_file = 'test_b2safe_data.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'true')

        # find PID in iCAT
        imeta_pid_result = imeta_ls_specific('-d', test_file, 'PID')

        # cleanup before checks
        # delete created pid
        if handle_created != None:
            delete_handle(handle_created)
        # delete file from iRODS
        delete_irods_file(test_file)

        # compare to expected output
        # check if PID is created
        self.assertNotEqual(
            handle_created, None,
            'No PID has been created')
        # check if PID is part AVU of iRODS file
        self.assertEqual(
            handle_created, imeta_pid_result,
            'The PID is NOT the same')

    def test_70_b2safe_local_for_one_file_registered_non_recursive(self):
        """Test that it is possible to replicate a single file locally using b2safe (registered, non recursive)"""
        # create test file
        test_file = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)
        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'false')

        # replicate the file
        replica_result = replicate_irods_file(self.irods_home+'/'+test_file, self.irods_home+'/'+test_file2, 'true', 'false')

        # find PID in iCAT for testfile2
        imeta_pid_result = imeta_ls_specific('-d', test_file2, 'PID')
        # find EUDAT/ROR in iCAT for testfile2
        imeta_ror_result = imeta_ls_specific('-d', test_file2, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file, test_file2]:
            pid_result = search_handle(self.irods_home+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            # delete file from iRODS
            delete_irods_file(irods_file)

        # check if PID is created for original
        self.assertNotEqual(
            handle_created, None,
            'No PID has been created')
        # check if replication was succesfull
        self.assertEqual(
            replica_result, 'Success!',
            'The replication was NOT succesful')
        # check if replica has PID filled in
        self.assertNotEqual(
            imeta_pid_result, None,
            'The PID is NOT filled in in the replica in iCAT')
        # check if EUDAT/ROR of replica is original PID
        self.assertEqual(
            handle_created, imeta_ror_result,
            'The PID of the original file is NOT the EUDAT/ROR value in the iCAT')

    def test_70_b2safe_local_for_one_file_not_registered_non_recursive(self):
        """Test that it is possible to replicate a single file locally using b2safe (not registered, non recursive)"""
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

        # find PID in iCAT for testfile2
        imeta_pid_result = imeta_ls_specific('-d', test_file2, 'PID')
        # find EUDAT/ROR in iCAT for testfile2
        imeta_ror_result = imeta_ls_specific('-d', test_file2, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file, test_file2]:
            pid_result = search_handle(self.irods_home+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            # delete file from iRODS
            delete_irods_file(irods_file)

        # check if PID is created for original
        self.assertNotEqual(
            handle_created, None,
            'No PID has been created')
        # check if replication was succesfull
        self.assertEqual(
            replica_result, 'Success!',
            'The replication was NOT succesful')
        # check if replica has PID filled in
        self.assertNotEqual(
            imeta_pid_result, None,
            'The PID is NOT filled in in the replica in iCAT')
        # check if EUDAT/ROR of replica is original PID
        self.assertEqual(
            handle_created, imeta_ror_result,
            'The PID of the original file is NOT the EUDAT/ROR value in the iCAT')

    def test_70_b2safe_local_for_one_file_registered_recursive(self):
        """Test that it is possible to replicate a single file locally using b2safe (registered, recursive)"""
        # create test file
        test_file = 'test_b2safe_data1.txt'
        test_file2 = 'test_b2safe_data2.txt'
        test_path = '/tmp/'+test_file
        create_os_file(test_path)

        # put test file in iRODS
        put_irods_file(test_path, self.irods_home+'/'+test_file)
        os.unlink(test_path)

        # create test handle
        handle_created = create_handle(self.irods_home+'/'+test_file, 'false')

        # replicate the file
        replica_result = replicate_irods_file(self.irods_home+'/'+test_file, self.irods_home+'/'+test_file2, 'true', 'true')

        # find PID in iCAT for testfile2
        imeta_pid_result = imeta_ls_specific('-d', test_file2, 'PID')
        # find EUDAT/ROR in iCAT for testfile2
        imeta_ror_result = imeta_ls_specific('-d', test_file2, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file, test_file2]:
            pid_result = search_handle(self.irods_home+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            # delete file from iRODS
            delete_irods_file(irods_file)

        # check if PID is created for original
        self.assertNotEqual(
            handle_created, None,
            'No PID has been created')
        # check if replication was succesfull
        self.assertEqual(
            replica_result, 'Success!',
            'The replication was NOT succesful')
        # check if replica has PID filled in
        self.assertNotEqual(
            imeta_pid_result, None,
            'The PID is NOT filled in in the replica in iCAT')
        # check if EUDAT/ROR of replica is original PID
        self.assertEqual(
            handle_created, imeta_ror_result,
            'The PID of the original file is NOT the EUDAT/ROR value in the iCAT')

    def test_70_b2safe_local_for_one_file_not_registered_recursive(self):
        """Test that it is possible to replicate a single file locally using b2safe (not registered, recursive)"""
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
         
        # find PID in iCAT for testfile2
        imeta_pid_result = imeta_ls_specific('-d', test_file2, 'PID')
        # find EUDAT/ROR in iCAT for testfile2
        imeta_ror_result = imeta_ls_specific('-d', test_file2, 'EUDAT/ROR')

        # cleanup before checks
        # find and delete handle entries, iRODS files
        for irods_file in [test_file, test_file2]:
            pid_result = search_handle(self.irods_home+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            # delete file from iRODS
            delete_irods_file(irods_file)

        # check if replication was succesfull
        self.assertEqual(
            replica_result, 'Success!',
            'The replication was NOT succesful')
        # check if replica has PID filled in
        self.assertNotEqual(
            imeta_pid_result, None,
            'The PID is NOT filled in in the replica in iCAT')
        # check if EUDAT/ROR of replica is original PID
        self.assertEqual(
            handle_created, imeta_ror_result,
            'The PID of the original file is NOT the EUDAT/ROR value in the iCAT')

    def test_75_b2safe_local_for_one_directory_registered_recursive(self):
        """Test that it is possible to replicate a single directory locally using b2safe (registered, recursive)"""
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
            handle_created = create_handle(irods_input_test_path+'/'+irods_file, 'false')

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
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            pid_result = search_handle(irods_output_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        # delete directories from iRODS
        delete_irods_directory(irods_input_test_path)
        delete_irods_directory(irods_output_test_path)

        # check if PID is created for original
        self.assertNotEqual(
            handle_created, None,
            'No PID has been created')
        # check if replication was succesfull
        self.assertEqual(
            replica_result, 'Success!',
            'The replication was NOT succesful')
        # check if replica has PID filled in
        self.assertNotEqual(
            imeta_pid_repl_result, None,
            'The PID is NOT filled in in the replica in iCAT')
        # check if EUDAT/ROR of replica is original PID
        self.assertEqual(
            imeta_pid_org_result, imeta_ror_repl_result,
            'The PID of the original file is NOT the EUDAT/ROR value in the iCAT')

    def test_75_b2safe_local_for_one_directory_not_registered_recursive(self):
        """Test that it is possible to replicate a single directory locally using b2safe (not registered, recursive)"""
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
        for irods_file in [test_file1, test_file2, test_file3, test_file4]:
            pid_result = search_handle(irods_input_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
            pid_result = search_handle(irods_output_test_path+'/'+irods_file)
            if pid_result != None:
                delete_handle(pid_result)
        # delete directories from iRODS
        delete_irods_directory(irods_input_test_path)
        delete_irods_directory(irods_output_test_path)

        # check if replication was succesfull
        self.assertEqual(
            replica_result, 'Success!',
            'The replication was NOT succesful')
        # check if replica has PID filled in
        self.assertNotEqual(
            imeta_pid_repl_result, None,
            'The PID is NOT filled in in the replica in iCAT')
        # check if EUDAT/ROR of replica is original PID
        self.assertEqual(
            imeta_pid_org_result, imeta_ror_repl_result,
            'The PID of the original file is NOT the EUDAT/ROR value in the iCAT')

