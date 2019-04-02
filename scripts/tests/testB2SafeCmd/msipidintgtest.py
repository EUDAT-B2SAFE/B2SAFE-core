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

IRODS_ENV = '/.irods/irods_environment.json'

if 'prefix' in os.environ:
    PREFIX = os.environ['prefix']
else:
    print "please define prefix as a variable "
    print "example: export prefix=21.T12996 "
    exit(1)

if 'url_prefix_in_profile' in os.environ:
    URL_PREFIX_IN_PROFILE = os.environ['url_prefix_in_profile']
else:
    print "please define url_prefix_in_profile as a variable "
    print "example: export url_prefix_in_profile='true' "
    print "example: export url_prefix_in_profile='false' "
    print "This is dependant on the configuration of the profile in \"/etc/irods/irods_pid.json\" "
    exit(1)

if 'HOME' in os.environ:
    IRODS_ENV = os.environ['HOME']+IRODS_ENV

RULE_FILE_MSIPID_CREATE='/tmp/msiPidCreate.r'
RULE_FILE_MSIPID_DELETE_HANDLE='/tmp/msiPidDeleteHandle.r'
RULE_FILE_MSIPID_GET_HANDLE='/tmp/msiPidGetHandle.r'
RULE_FILE_MSIPID_LOOKUP='/tmp/msiPidLookup.r'
RULE_FILE_MSIPID_LOOKUP_KEY='/tmp/msiPidLookupKey.r'
RULE_FILE_MSIPID_SET_HANDLE='/tmp/msiPidSetHandle.r'
RULE_FILE_MSIPID_UNSET_HANDLE='/tmp/msiPidUnsetHandle.r'

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


def create_file(filename, list):
    '''create a file using the list as input'''

    f = open(filename,"w+")
    for line in list:
        f.write(line+'\n' )
    f.close()


def create_msiPidCreate_rule():
    '''create msiPidCreate rule in tmp directory'''

    rule_file_lines = []
    rule_file_lines.append('myRule {')
    rule_file_lines.append('   if(strlen(*key_values_inp) > 0)')
    rule_file_lines.append('   {')
    rule_file_lines.append('      *key_values = split(*key_values_inp, ",");')
    rule_file_lines.append('   }')
    rule_file_lines.append('   else')
    rule_file_lines.append('   {')
    rule_file_lines.append('       *key_values = "";')
    rule_file_lines.append('   }')
    rule_file_lines.append('')
    rule_file_lines.append('   *err = errorcode(msiPidCreate(*path,*key_values,*handle));')
    rule_file_lines.append('   writeLine("stdout", *err);')
    rule_file_lines.append('   writeLine("stdout", *handle);')
    rule_file_lines.append('}')
    rule_file_lines.append('')
    rule_file_lines.append('INPUT *path="", *key_values_inp=""')
    rule_file_lines.append('OUTPUT ruleExecOut')

    create_file(RULE_FILE_MSIPID_CREATE, rule_file_lines)


def create_msiPidDeleteHandle_rule():
    '''create msiPidDeletHandle rule in tmp directory'''
 
    rule_file_lines = []
    rule_file_lines.append('myRule {')
    rule_file_lines.append('   *err = errorcode(msiPidDeleteHandle(*handle));')
    rule_file_lines.append('   writeLine("stdout", *err);')
    rule_file_lines.append('}')
    rule_file_lines.append('')
    rule_file_lines.append('INPUT *handle=""')
    rule_file_lines.append('OUTPUT ruleExecOut')

    create_file(RULE_FILE_MSIPID_DELETE_HANDLE, rule_file_lines)


def create_msiPidGetHandle_rule():
    '''create msiPidDeletHandle rule in tmp directory'''
 
    rule_file_lines = []
    rule_file_lines.append('myRule {')
    rule_file_lines.append('   *err = errorcode(msiPidGetHandle(*handle, *key, *result));')
    rule_file_lines.append('   writeLine("stdout", *err);')
    rule_file_lines.append('   if (*err >= 0) {')
    rule_file_lines.append('      writeLine("stdout", *result);')
    rule_file_lines.append('   }')
    rule_file_lines.append('}')
    rule_file_lines.append('')
    rule_file_lines.append('INPUT *handle="",*key=""')
    rule_file_lines.append('OUTPUT ruleExecOut')

    create_file(RULE_FILE_MSIPID_GET_HANDLE, rule_file_lines)


def create_msiPidLookup_rule():
    '''create msiPidLookup rule in tmp directory'''

    rule_file_lines = []
    rule_file_lines.append('myRule {')
    rule_file_lines.append('   *err = errorcode(msiPidLookup(*path, *handles));')
    rule_file_lines.append('   writeLine("stdout", *err);')
    rule_file_lines.append('   foreach(*handles) {')
    rule_file_lines.append('      writeLine("stdout", *handles);')
    rule_file_lines.append('    }')
    rule_file_lines.append('}')
    rule_file_lines.append('')
    rule_file_lines.append('INPUT *path=""')
    rule_file_lines.append('OUTPUT ruleExecOut')

    create_file(RULE_FILE_MSIPID_LOOKUP, rule_file_lines)


def create_msiPidLookupKey_rule():
    '''create msiPidLookupKey rule in tmp directory'''

    rule_file_lines = []
    rule_file_lines.append('myRule {')
    rule_file_lines.append('   *err = errorcode(msiPidLookupKey(*key, "*value", *handles));')
    rule_file_lines.append('   writeLine("stdout", *err);')
    rule_file_lines.append('   foreach(*handles) {')
    rule_file_lines.append('      writeLine("stdout", *handles);')
    rule_file_lines.append('   }')
    rule_file_lines.append('}')
    rule_file_lines.append('')
    rule_file_lines.append('INPUT *key="", *value=""')
    rule_file_lines.append('OUTPUT ruleExecOut')

    create_file(RULE_FILE_MSIPID_LOOKUP_KEY, rule_file_lines)


def create_msiPidSetHandle():
    '''create msiPidSetHandle rule in tmp directory'''

    rule_file_lines = []
    rule_file_lines.append('myRule {')
    rule_file_lines.append('       if(strlen(*mvalue) > 0)')
    rule_file_lines.append('       {')
    rule_file_lines.append('          *value = ""')
    rule_file_lines.append('          *key = split(*mvalue, ",");')
    rule_file_lines.append('       }')
    rule_file_lines.append('       *err = errorcode(msiPidSetHandle(*handle, *key, *value));')
    rule_file_lines.append('       writeLine("stdout", "*err");')
    rule_file_lines.append('}')
    rule_file_lines.append('')
    rule_file_lines.append('INPUT *handle="", *key="", *value="", *mvalue=""')
    rule_file_lines.append('OUTPUT ruleExecOut')

    create_file(RULE_FILE_MSIPID_SET_HANDLE, rule_file_lines)


def create_msiPidUnsetHandle():
    '''create msiPidUnsetHandle rule in tmp directory'''

    rule_file_lines = []
    rule_file_lines.append('myRule {')
    rule_file_lines.append('       if(strlen(*mvalue) > 0)')
    rule_file_lines.append('       {')
    rule_file_lines.append('          *value = ""')
    rule_file_lines.append('          *key = split(*mvalue, ",");')
    rule_file_lines.append('       }')
    rule_file_lines.append('       *err = errorcode(msiPidUnsetHandle(*handle, *key));')
    rule_file_lines.append('       writeLine("stdout", "*err");')
    rule_file_lines.append('}')
    rule_file_lines.append('')
    rule_file_lines.append('INPUT *handle="", *key="", *mvalue=""')
    rule_file_lines.append('OUTPUT ruleExecOut')

    create_file(RULE_FILE_MSIPID_UNSET_HANDLE, rule_file_lines)


class MsiPidIntegrationTests(unittest.TestCase):

    def setUp(self):
        """Setup testB2SafeCmd environment before the tests have run"""
        create_msiPidCreate_rule()
        create_msiPidDeleteHandle_rule()
        create_msiPidGetHandle_rule()
        create_msiPidLookup_rule()
        create_msiPidLookupKey_rule()
        create_msiPidSetHandle()
        create_msiPidUnsetHandle()

        jsonfilecontent = json.loads(open(IRODS_ENV, 'r').read())
        self.irods_zone_name = jsonfilecontent.pop('irods_zone_name')

        if URL_PREFIX_IN_PROFILE.lower() == 'true':
            command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'"]
        else:
            command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP_KEY, "*key='URL'", "*value='/"+self.irods_zone_name+"/testB2SafeCmd/1'"]
        lookup_result = subprocess_popen(command)
        for line in lookup_result:
            if line != '':
                   command = [ 'irule', '-F', RULE_FILE_MSIPID_DELETE_HANDLE, "*handle='"+line+"'"]
                   delete_result = subprocess_popen(command)


    def tearDown(self):
        """ Cleanup testB2SafeCmd environment after the tests have run"""
        if URL_PREFIX_IN_PROFILE.lower() == 'true':
            command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'"]
        else:
            command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP_KEY, "*key='URL'", "*value='/"+self.irods_zone_name+"/testB2SafeCmd/1'"]
        lookup_result = subprocess_popen(command)

        #print lookup_result

        for line in lookup_result:
            if line != '' or line != '0':
                   command = [ 'irule', '-F', RULE_FILE_MSIPID_DELETE_HANDLE, "*handle='"+line+"'"]
                   delete_result = subprocess_popen(command)


    def test_search_handle_by_key_value(self):
        """Test that search by key-value returns matching handle."""

        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'", "*key_values_inp='BOEKIE,zoekie,AAP,noot'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP_KEY, "*key='BOEKIE'", "*value='zoekie'"]
        lookup_result = subprocess_popen(command)
        self.assertEqual(
            unicode(create_result[1]).lower(), lookup_result[1].lower(),
            'search existing handle by key returns unexpected response')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP_KEY, "*key='AAP'", "*value='noot'"]
        lookup_result = subprocess_popen(command)
        self.assertEqual(
            unicode(create_result[1]).lower(), lookup_result[1].lower(),
            'search existing handle by key returns unexpected response')
 

    def test_search_handle_by_non_existing_key_value(self):
        """Test that search handle by non existing key-value returns ''."""
        command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP_KEY, "*key='checksum'", "*value='123456789012345678901234567890'"]
        lookup_result = subprocess_popen(command)
        self.assertEqual(
            lookup_result[0], '0',
            'search handle by non existing key-value should return \"\"')
        

    def test_read_non_existing_handle(self):
        """Test that read non existing handle returns -1090000."""
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+PREFIX+"/1234567890a'"]
        read_result = subprocess_popen(command)
        self.assertEqual(
          read_result[0], '-1090000',
          "read non existing handle should return -1090000")


    def test_read_value_from_handle(self):
        """Test that read value by key returns stored handle value."""
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'", "*key_values_inp='CHECKSUM,1234567890,AAP,noot'"]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='CHECKSUM'"]
        read_result = subprocess_popen(command)
        self.assertEqual(
            read_result[1], '1234567890',
           'read existing value from handle returns unexpected response')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='AAP'"]
        read_result = subprocess_popen(command)
        self.assertEqual(
            read_result[1], 'noot',
           'read existing value from handle returns unexpected response')


    def test_read_value_from_non_existing_handle(self):
        """Test that read value by key from non existing handle returns -1090000."""
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+PREFIX+"/1234567890a'", "*key='boekiezoekie'"]
        read_result = subprocess_popen(command)
        self.assertEqual(
            read_result[0], '-1090000',
            'read existing value from non existing handle returns unexpected response')


    def test_read_non_existing_value_from_handle(self):
        """Test that read value by non existing key returns -1090000."""
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'", "*key_values_inp='CHECKSUM,1234567890,AAP,noot'"]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+PREFIX+"/1234567890a'", "*key='boekiezoekie'"]
        read_result = subprocess_popen(command)
        self.assertEqual(
            read_result[0], '-1090000',
            'read value by non existing key should return -1090000')


    def test_create_handle(self):
        """Test that create handle returns expected response and adds new handle."""
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'"]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        if URL_PREFIX_IN_PROFILE.lower() == 'true':
            command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'"]
        else:
            command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP_KEY, "*key='URL'", "*value='/"+self.irods_zone_name+"/testB2SafeCmd/1'"]
        lookup_result = subprocess_popen(command)
        self.assertEqual(unicode(create_result[1]).lower(), lookup_result[1].lower(),
                         'create handle should add new handle')


    def test_create_handle_with_checksum(self):
        """Test that create handle with checksum returns expected response and adds new handle with supplied checksum."""
        checksum = '1cb285b'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" , "*key_values_inp='CHECKSUM,"+checksum+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='CHECKSUM'"]
        read_result = subprocess_popen(command)
        self.assertEqual(checksum, read_result[1],
                         'create handle with checksum should add new handle')


    def test_create_handle_with_extra_key(self):
        """Test that create handle with extra key returns expected response and adds new handle with supplied key value."""
        checksum = '1cb285b'
        extra_key = 'EMAIL'
        extra_value = 'user@testB2SafeCmd.com'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" , "*key_values_inp='CHECKSUM,"+checksum+","+extra_key+","+extra_value+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='CHECKSUM'"]
        read_result = subprocess_popen(command)
        self.assertEqual(checksum, read_result[1],
                         'create handle with checksum should add new handle')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+extra_key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(extra_value, read_result[1],
                         'create handle with extra key should add new handle')


    def test_create_handle_with_extra_key_FIO_real_pid(self):
        """Test that create handle with extra key EUDAT/FIO returns expected response and adds new handle with supplied key value."""
        extra_key = 'EUDAT/FIO'
        extra_value = '841/totally_nonsen_suffix'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" , "*key_values_inp='"+extra_key+","+extra_value+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+extra_key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(extra_value, read_result[1],
                         'create handle with extra key EUDAT/FIO should add new handle')


    def test_create_handle_with_extra_key_FIO_PID(self):
        """Test that create handle with extra key EUDAT/FIO and value 'PID' returns expected response and adds new handle with supplied key value."""
        extra_key = 'EUDAT/FIO'
        extra_value = 'PID'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" , "*key_values_inp='"+extra_key+","+extra_value+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP_KEY, "*key='"+extra_key+"'", "*value='"+extra_value+"'"]
        lookup_result = subprocess_popen(command)
        self.assertEqual(create_result[1].lower(), lookup_result[1].lower(),
                         'create handle with extra key EUDAT/FIO an value pid should add new handle')


    def test_create_handle_with_extra_key_ROR_real_pid(self):
        """Test that create handle with extra key EUDAT/ROR returns expected response and adds new handle with supplied key value."""
        extra_key = 'EUDAT/ROR'
        extra_value = '841/totally_nonsen_suffix'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" , "*key_values_inp='"+extra_key+","+extra_value+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+extra_key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(extra_value, read_result[1],
                         'create handle with extra key EUDAT/ROR should add new handle')


    def test_create_handle_with_extra_key_ROR_pid(self):
        """Test that create handle with extra key EUDAT/ROR and value 'pid' returns expected response and adds new handle with supplied key value."""
        extra_key = 'EUDAT/ROR'
        extra_value = 'pid'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" , "*key_values_inp='"+extra_key+","+extra_value+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_LOOKUP_KEY, "*key='"+extra_key+"'", "*value='"+extra_value+"'"]
        lookup_result = subprocess_popen(command)
        self.assertEqual(create_result[1].lower(), lookup_result[1].lower(),
                         'create handle with extra key EUDAT/ROR an value pid should add new handle')


    def test_modify_handle_key_value_1(self):
        """Test that modify handle value returns handle and updates stored value."""
        key = 'URL2'
        value_before = 'http://www.testB2SafeCmd.com/3'
        value_after = 'http://www.testB2SafeCmd.com/1'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" , "*key_values_inp='"+key+","+value_before+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value_before,
                         'modify handle value failed to create value')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_SET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'", "*value='"+value_after+"'" ]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], '0' ,
                         'modify handle value should return 0')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value_after,
                         'modify handle value failed to update value')


    def test_modify_handle_key_value_2(self):
        """Test that modify handle value returns handle and updates stored value."""
        key = 'URL2'
        value_before = 'http://www.testB2SafeCmd.com/3'
        value_after = 'http://www.testB2SafeCmd.com/1'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" , "*key_values_inp='"+key+","+value_before+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value_before,
                         'modify handle value failed to create value')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_SET_HANDLE, "*handle='"+create_result[1]+"'", "*mvalue='"+key+","+value_after+"'" ]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], '0' ,
                         'modify handle value should return 0')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value_after,
                         'modify handle value failed to update value')


    def test_modify_handle_key_value_3(self):
        """Test that modify handle value returns handle and updates stored value."""
        key = 'URL2'
        value_before = 'http://www.testB2SafeCmd.com/3'
        value_after = 'http://www.testB2SafeCmd.com/1'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" , "*key_values_inp='"+key+","+value_before+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value_before,
                         'modify handle value failed to create value')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_SET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'", "*mvalue='"+key+","+value_after+"'" ]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], '0' ,
                         'modify handle value should return 0')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value_after,
                         'modify handle value failed to update value')


    def test_modify_handle_new_key_value_1(self):
        """Test that modify existing handle with new key-value pair returns 0 and updates stored handle."""
        key = "EMAIL"
        value = 'user@testB2SafeCmd.com'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_SET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'", "*value='"+value+"'" ]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], '0' ,
                         'modify handle value should return 0')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value,
            'modify existing handle with new key-value should update value')


    def test_modify_handle_new_key_value_2(self):
        """Test that modify existing handle with new key-value pair returns 0 and updates stored handle."""
        key = "EMAIL"
        value = 'user@testB2SafeCmd.com'
        key2 = "BOOKIE"
        value2 = "zookie"
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_SET_HANDLE, "*handle='"+create_result[1]+"'", "*mvalue='"+key+","+value+"'" ]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], '0' ,
                         'modify handle value should return 0')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value,
            'modify existing handle with new key-value should update value')


    def test_modify_handle_new_key_value_3(self):
        """Test that modify existing handle with new key-value pair returns 0 and updates stored handle."""
        key = "EMAIL"
        value = 'user@testB2SafeCmd.com'
        key2 = "BOOKIE"
        value2 = "zookie"
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_SET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'", "*mvalue='"+key+","+value+"'" ]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], '0' ,
                         'modify handle value should return 0')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value,
            'modify existing handle with new key-value should update value')


    def test_modify_handle_new_key_value_4(self):
        """Test that modify existing handle with new key-value pair returns 0 and updates stored handle."""
        key = "EMAIL"
        value = 'user@testB2SafeCmd.com'
        key2 = "BOOKIE"
        value2 = "zookie"
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_SET_HANDLE, "*handle='"+create_result[1]+"'", "*mvalue='"+key+","+value+","+key2+","+value2+"'" ]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], '0' ,
                         'modify handle value should return 0')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value,
            'modify existing handle with new key-value should update value')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key2+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value2,
            'modify existing handle with new key-value should update value')


    def test_modify_handle_new_key_value_5(self):
        """Test that modify existing handle with new key-value pair returns 0 and updates stored handle."""
        key = "EMAIL"
        value = 'user@testB2SafeCmd.com'
        key2 = "BOOKIE"
        value2 = "zookie"
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_SET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'", "*mvalue='"+key+","+value+","+key2+","+value2+"'" ]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], '0' ,
                         'modify handle value should return 0')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value,
            'modify existing handle with new key-value should update value')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key2+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value2,
            'modify existing handle with new key-value should update value')


    def test_modify_handle_with_empty_value(self):
        """Test that modify existing handle key with empty value returns 0 and updates stored value accordingly."""
        key = "EMAIL"
        value_before = 'user@testB2SafeCmd.com'
        value_after = ''
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'" , "*key_values_inp='"+key+","+value_before+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value_before,
                         'modify handle value failed to create value')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_SET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'", "*value='"+value_after+"'" ]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], '0' ,
                         'modify handle value should return 0')
        command = [ 'irule', '-F', RULE_FILE_MSIPID_GET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'"]
        read_result = subprocess_popen(command)
        self.assertEqual(read_result[1], value_after,
                        "modify existing handle key with empty value should set stored value to ''")


    def test_modify_non_existing_handle(self):
        """Test that modify value of non existing handle returns -1090000."""
        key = "FOO_KEY"
        value = "FOO_VALUE"
        command = [ 'irule', '-F', RULE_FILE_MSIPID_SET_HANDLE, "*handle='"+PREFIX+"/1234567890a'", "*key='"+key+"'", "*value='"+value+"'" ]
        modify_result = subprocess_popen(command)
        self.assertEqual(modify_result[0], '-1090000',
                         'modify non existing handle should return -1090000')


    def test_delete_handle(self):
        """Test that delete existing handle returns 0."""
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'"]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_DELETE_HANDLE, "*handle='"+create_result[1]+"'"]
        delete_result = subprocess_popen(command)
        self.assertEqual(delete_result[0], '0',
                        'delete existing handle should return 0')


    def test_delete_non_existing_handle(self):
        """Test that delete non existing handle returns -1090000."""
        command = [ 'irule', '-F', RULE_FILE_MSIPID_DELETE_HANDLE, "*handle='"+PREFIX+"/1234567890a'"]
        delete_result = subprocess_popen(command)
        self.assertEqual(delete_result[0], '-1090000',
                        'delete non existing handle should return -1090000')

 
    def test_delete_key_from_handle(self):
        """Test that delete key from handle returns 0."""
        key = 'EMAIL'
        value = 'user@testB2SafeCmd.com'
        command = [ 'irule', '-F', RULE_FILE_MSIPID_CREATE, "*path='/"+self.irods_zone_name+"/testB2SafeCmd/1'", "*key_values_inp='"+key+","+value+"'" ]
        create_result = subprocess_popen(command)
        self.assertEqual(
          create_result[0], '0',
          "create handle should return 0")
        command = [ 'irule', '-F', RULE_FILE_MSIPID_UNSET_HANDLE, "*handle='"+create_result[1]+"'", "*key='"+key+"'" ]
        delete_result = subprocess_popen(command)
        self.assertEqual(delete_result[0].lower(), '0',
                        'delete existing handle value should return handle')


###    def test_delete_non_existing_key_from_handle(self):
###        """Test that delete non existing key from handle returns False."""
###        key = 'FOO_KEY'
###        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'delete', self.prefix+"/1234567890a", '--key', key]
###        delete_result = subprocess_popen(command)
###        self.assertEqual(delete_result[0], 'False',
###                         'delete key from non existing handle should return False')
###
###   
##
###    def test_bulk_actions(self):
###        """Test that bulk actions can be executed and gives proper responses."""
###        bulk_input = '/tmp/bulk_input'
###        bulk_output = '/tmp/bulk_result'
###        prefix = self.prefix
###
###        # open input file
###        try:
###            bulk_input_file = open(bulk_input, "w") 
###        except:
###            sys.stdout.write('error opening: '+bulk_input)
###
###        bulk_input_file.write('SEARCH URL http://www.test'+prefix+'.com\n')
###        bulk_input_file.write('CREATE '+prefix+'/TEST_'+prefix+'_01 http://www.test'+prefix+'.com\n')
###        bulk_input_file.write('SEARCH URL http://www.test'+prefix+'.com\n')
###        bulk_input_file.write('CREATE '+prefix+'/TEST_'+prefix+'_02 http://www.test'+prefix+'.com 123456789\n')
###        bulk_input_file.write('CREATE '+prefix+'/TEST_'+prefix+'_03 http://www.test'+prefix+'.com 123456789 http://www.test.com\n')
###        bulk_input_file.write('CREATE '+prefix+'/TEST_'+prefix+'_04 http://www.test'+prefix+'.com 123456789 http://www.test.com AAP=noot;JUT=jul\n')
###        bulk_input_file.write('CREATE '+prefix+'/TEST_'+prefix+'_05 http://www.test'+prefix+'.com 123456789 none AAP=noot;JUT=jul\n')
###        bulk_input_file.write('CREATE '+prefix+'/TEST_'+prefix+'_06 http://www.test'+prefix+'.com none http://www.test.com AAP=noot;JUT=jul\n')
###        bulk_input_file.write('CREATE '+prefix+'/TEST_'+prefix+'_07 http://www.test'+prefix+'.com none none AAP=noot;JUT=jul\n')
###        bulk_input_file.write('SEARCH URL http://www.test'+prefix+'*\n')
###
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_01 URL\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_02 URL\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_02 CHECKSUM\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_03 URL\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_03 CHECKSUM\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_03 10320/LOC\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_04 URL\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_04 CHECKSUM\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_04 10320/LOC\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_04 AAP\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_04 JUT\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_05 URL\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_05 CHECKSUM\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_05 10320/LOC\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_05 AAP\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_05 JUT\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_06 URL\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_06 CHECKSUM\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_06 10320/LOC\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_06 AAP\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_06 JUT\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_07 URL\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_07 CHECKSUM\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_07 10320/LOC\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_07 AAP\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_07 JUT\n')
###
###        bulk_input_file.write('MODIFY '+prefix+'/TEST_'+prefix+'_07 JUT joep\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_07 JUT\n')
###
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_02 CHECKSUM\n')
###        bulk_input_file.write('REPLACE '+prefix+'/TEST_'+prefix+'_02 CHECKSUM 345 543\n')
###        bulk_input_file.write('READ '+prefix+'/TEST_'+prefix+'_02 CHECKSUM\n')
###        bulk_input_file.write('REPLACE '+prefix+'/TEST_'+prefix+'_02 CHECKSUM 345 543\n')
###        bulk_input_file.write('REPLACE '+prefix+'/TEST_'+prefix+'_02 CHECKSUMM 345 543\n')
###        bulk_input_file.write('REPLACE '+prefix+'/TEST_'+prefix+'_021 CHECKSUM 345 543\n')
###
###        bulk_input_file.write('DELETE '+prefix+'/TEST_'+prefix+'_01\n')
###        bulk_input_file.write('DELETE '+prefix+'/TEST_'+prefix+'_02\n')
###        bulk_input_file.write('DELETE '+prefix+'/TEST_'+prefix+'_03\n')
###        bulk_input_file.write('DELETE '+prefix+'/TEST_'+prefix+'_04\n')
###        bulk_input_file.write('DELETE '+prefix+'/TEST_'+prefix+'_05\n')
###        bulk_input_file.write('DELETE '+prefix+'/TEST_'+prefix+'_06\n')
###        bulk_input_file.write('DELETE '+prefix+'/TEST_'+prefix+'_07 AAP\n')
###        bulk_input_file.write('DELETE '+prefix+'/TEST_'+prefix+'_07\n')
###
###        bulk_input_file.close()
###
###        expected_lines = []
###        expected_lines.append('search handle key: URL value: http://www.test'+prefix+'.com result: empty\n')
###        expected_lines.append('create handle: '+prefix+'/TEST_'+prefix+'_01 result: '+prefix+'/TEST_'+prefix+'_01\n')
###        expected_lines.append('search handle key: URL value: http://www.test'+prefix+'.com result: ["'+prefix+'/TEST_'+prefix+'_01"]\n')
###        expected_lines.append('create handle: '+prefix+'/TEST_'+prefix+'_02 result: '+prefix+'/TEST_'+prefix+'_02\n')
###        expected_lines.append('create handle: '+prefix+'/TEST_'+prefix+'_03 result: '+prefix+'/TEST_'+prefix+'_03\n')
###        expected_lines.append('create handle: '+prefix+'/TEST_'+prefix+'_04 result: '+prefix+'/TEST_'+prefix+'_04\n')
###        expected_lines.append('create handle: '+prefix+'/TEST_'+prefix+'_05 result: '+prefix+'/TEST_'+prefix+'_05\n')
###        expected_lines.append('create handle: '+prefix+'/TEST_'+prefix+'_06 result: '+prefix+'/TEST_'+prefix+'_06\n')
###        expected_lines.append('create handle: '+prefix+'/TEST_'+prefix+'_07 result: '+prefix+'/TEST_'+prefix+'_07\n')
###        expected_lines.append('search handle key: URL value: http://www.test'+prefix+'* result: ["'+prefix+'/TEST_'+prefix+'_01", "'+prefix+'/TEST_'+prefix+'_02", "'+prefix+'/TEST_'+prefix+'_03", "'+prefix+'/TEST_'+prefix+'_04", "'+prefix+'/TEST_'+prefix+'_05", "'+prefix+'/TEST_'+prefix+'_06", "'+prefix+'/TEST_'+prefix+'_07"]\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_01 key: URL result: http://www.test'+prefix+'.com\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_02 key: URL result: http://www.test'+prefix+'.com\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_02 key: CHECKSUM result: 123456789\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_03 key: URL result: http://www.test'+prefix+'.com\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_03 key: CHECKSUM result: 123456789\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_03 key: 10320/LOC result: <locations><location href=\\"http://www.test.com\\" id=\\"0\\" /></locations>\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_04 key: URL result: http://www.test'+prefix+'.com\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_04 key: CHECKSUM result: 123456789\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_04 key: 10320/LOC result: <locations><location href=\\"http://www.test.com\\" id=\\"0\\" /></locations>\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_04 key: AAP result: noot\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_04 key: JUT result: jul\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_05 key: URL result: http://www.test'+prefix+'.com\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_05 key: CHECKSUM result: 123456789\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_05 key: 10320/LOC result: None\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_05 key: AAP result: noot\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_05 key: JUT result: jul\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_06 key: URL result: http://www.test'+prefix+'.com\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_06 key: CHECKSUM result: None\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_06 key: 10320/LOC result: <locations><location href=\\"http://www.test.com\\" id=\\"0\\" /></locations>\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_06 key: AAP result: noot\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_06 key: JUT result: jul\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_07 key: URL result: http://www.test'+prefix+'.com\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_07 key: CHECKSUM result: None\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_07 key: 10320/LOC result: None\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_07 key: AAP result: noot\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_07 key: JUT result: jul\n')
###        expected_lines.append('modify handle: '+prefix+'/TEST_'+prefix+'_07 key: JUT value: joep result: True\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_07 key: JUT result: joep\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_02 key: CHECKSUM result: 123456789\n')
###        expected_lines.append('replace handle: '+prefix+'/TEST_'+prefix+'_02 key: CHECKSUM data1: 345 data2: 543 result: True\n')
###        expected_lines.append('read handle: '+prefix+'/TEST_'+prefix+'_02 key: CHECKSUM result: 125436789\n')
###        expected_lines.append('replace handle: '+prefix+'/TEST_'+prefix+'_02 key: CHECKSUM data1: 345 data2: 543 result: None\n')
###        expected_lines.append('replace handle: '+prefix+'/TEST_'+prefix+'_02 key: CHECKSUMM data1: 345 data2: 543 result: None\n')
###        expected_lines.append('replace handle: '+prefix+'/TEST_'+prefix+'_021 key: CHECKSUM data1: 345 data2: 543 result: None\n')
###        expected_lines.append('delete handle: '+prefix+'/TEST_'+prefix+'_01 result: True\n')
###        expected_lines.append('delete handle: '+prefix+'/TEST_'+prefix+'_02 result: True\n')
###        expected_lines.append('delete handle: '+prefix+'/TEST_'+prefix+'_03 result: True\n')
###        expected_lines.append('delete handle: '+prefix+'/TEST_'+prefix+'_04 result: True\n')
###        expected_lines.append('delete handle: '+prefix+'/TEST_'+prefix+'_05 result: True\n')
###        expected_lines.append('delete handle: '+prefix+'/TEST_'+prefix+'_06 result: True\n')
###        expected_lines.append('delete handle: '+prefix+'/TEST_'+prefix+'_07 key: AAP result: True\n')
###        expected_lines.append('delete handle: '+prefix+'/TEST_'+prefix+'_07 result: True\n')
###
###        # execute bulk command
###        command = [EPIC_PATH, CRED_STORE, CRED_PATH, 'bulk', '--input', bulk_input, '--result', bulk_output ]
###        bulk_result = subprocess_popen(command)
###
###        # open result file
###        try:
###            bulk_result_file = open(bulk_output, "r") 
###        except:
###            sys.stdout.write('error opening: '+bulk_output)
###
###        # read all lines in a list/array
###        lines = bulk_result_file.readlines()
###
###        self.assertEqual(expected_lines, lines,
###                         'bulk update should give expected return values')
###
