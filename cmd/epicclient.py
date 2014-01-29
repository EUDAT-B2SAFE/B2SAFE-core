#!/home/proirod1/.pythonbrew/pythons/Python-2.7/bin/python 
#!/usr/bin/env python
#
#   epicclient.py
#
#   * use 4 spaces!!! not tabs
#   * See PEP-8 Python style guide http://www.python.org/dev/peps/pep-0008/
#   * use pylint
#

"""EUDAT EPIC client API. Supports reading, querying, creating, modifying and
deleting handle records.

httplib2
download from http://code.google.com/p/httplib2
python setup.py install

simplejson
download from http://pypi.python.org/pypi/simplejson/
python setup.py install

ubuntu: apt-get install python-httplib2 python-simplejson

apt-get install pylint

"""

import httplib2
import simplejson
# FIXME xml.dom.minidom is not secure against maliciously crafted XML
from xml.dom import minidom

import base64
import uuid
import argparse
import sys

###############################################################################
# Epic Client Class #
###############################################################################

class EpicClient(object):
    """Class implementing an EPIC client."""

    def __init__(self, cred):
        """Initialize object with connection parameters."""

        self.cred  = cred
        self.debug = cred.debug
        self.http = httplib2.Http(disable_ssl_certificate_validation=True)
        self.http.add_credentials(cred.username, cred.password)
        # do not throw exceptions for connection errors
        self.http.force_exception_to_status_code = True

    def _debugMsg(self, method, msg):
        """Internal: Print a debug message if debug is enabled."""

        if self.debug:
            print "[", method, "]", msg

    # Public methods

    def searchHandle(self, prefix, key, value):
        """Search for handles containing the specified key with
        the specified value.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        url: The URL to search for.
        Returns the searched data field, or None if error,
        or empty if not found.

        """

        if self.cred.baseuri.endswith('/'):
            uri = self.cred.baseuri + prefix + '/?' + key + '=' + value
        else:
            uri = self.cred.baseuri + '/' + prefix + '/?' + key + '=' + value

        self._debugMsg('searchHandle', "URI " + uri)

        hdrs = None
        auth = base64.encodestring(self.cred.username + ':' +
                                   self.cred.password)
        if self.cred.accept_format:
            hdrs = {'Accept': self.cred.accept_format,
                    'Authorization': 'Basic ' + auth}

        response, content = self.http.request(uri, method='GET', headers=hdrs)
        if response.status == 200:
            self._debugMsg('searchHandle', "Request completed")
        else:
            self._debugMsg('searchHandle', "Response status: " +
                                           str(response.status))
            return None

        if not content:
            return None

        handle = simplejson.loads(content)
        if not handle:
            return 'empty'

        # make sure to only return the handle and strip off the baseuri
        # if it is included
        hdl = handle[0]
        if hdl.startswith(self.cred.baseuri):
            return hdl[len(self.cred.baseuri):len(hdl)]
        elif hdl.startswith(self.cred.baseuri + '/'):
            return hdl[len(self.cred.baseuri + '/'):len(hdl)]
        return prefix + '/' + hdl

    def retrieveHandle(self, prefix, suffix=''):
        """Retrieve a handle from the PID service.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        suffix: The suffix of the handle. Default: ''.
        Returns the content of the handle in JSON, None on error.

        """

        if self.cred.baseuri.endswith('/'):
            uri = self.cred.baseuri + prefix
        else:
            uri = self.cred.baseuri + '/' + prefix
        if suffix != '':
            uri += "/" + suffix.partition("/")[2]

        self._debugMsg('retrieveHandle', "URI " + uri)
        hdrs = None
        auth = base64.encodestring(self.cred.username + ':' +
                                   self.cred.password)
        if self.cred.accept_format:
            hdrs = {'Accept': self.cred.accept_format,
                    'Authorization': 'Basic ' + auth}

        response, content = self.http.request(uri, method='GET', headers=hdrs)
        if response.status == 200:
            self._debugMsg('retrieveHandle', "Request completed")
        else:
            self._debugMsg('retrieveHandle', "Response status: " +
                                             str(response.status))
            return None

        return content

    def getValueFromHandle(self, prefix, key, suffix=''):
        """Retrieve a value from a handle.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        key: The key to search (in type parameter).
        suffix: The suffix of the handle. Default: ''.
        Returns the searched data field, or None if not found.

        """

        jsonhandle = self.retrieveHandle(prefix, suffix)
        if not jsonhandle:
            return None
        handle = simplejson.loads(jsonhandle)
        for item in handle:
            if 'type' in item and item['type'] == key:
                self._debugMsg('getValueFromHandle',
                               "Found key " + key + " value=" +
                               str(item['parsed_data']))
                return str(item['parsed_data'])

        self._debugMsg('getValueFromHandle', "Value for key " + key +
                                             " not found")
        return None

    def createHandle(self, prefix, location, checksum=None, suffix=''):
        """Create a new handle for a file.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        location: The location (URL) of the file.
        checksum: Optional parameter, store the checksum of the file as well.
        suffix: The suffix of the handle. Default: ''.
        Returns the URI of the new handle, None if an error occurred.

        """

        if self.cred.baseuri.endswith('/'):
            uri = self.cred.baseuri + prefix
        else:
            uri = self.cred.baseuri + '/' + prefix

        if suffix != '':
            uri += "/" + suffix.partition("/")[2]
        self._debugMsg('createHandleWithLocation',"URI " + uri)
        auth = base64.encodestring(self.cred.username + ':' +
                                   self.cred.password)
        hdrs = {'If-None-Match': '*', 'Content-Type': 'application/json',
                'Authorization': 'Basic ' + auth }

        if checksum:
            new_handle_json = simplejson.dumps([{'type': 'URL',
                                                 'parsed_data': location},
                                                {'type': 'CHECKSUM',
                                                 'parsed_data': checksum}])
        else:
            new_handle_json = simplejson.dumps([{'type': 'URL',
                                                 'parsed_data': location}])

        response, _ = self.http.request(uri, method='PUT', headers=hdrs,
                                        body=new_handle_json)
        if response.status == 201:
            self._debugMsg('createHandleWithLocation', "Request completed")
        elif response.status == 400:
            self._debugMsg('createHandleWithLocation',
                           'body json:' + new_handle_json)
            return None
        else:
            self._debugMsg('createHandleWithLocation',
                           "Not Created: Response status: " +
                           str(response.status))
            return None

        # make sure to only return the handle and strip off the baseuri
        # if it is included
        hdl = response['location']
        self._debugMsg('hdl', hdl)
        if hdl.startswith(self.cred.baseuri):
            hdl = hdl[len(self.cred.baseuri):len(hdl)]
        elif hdl.startswith(self.cred.baseuri + '/'):
            hdl = hdl[len(self.cred.baseuri + '/'):len(hdl)]
            self._debugMsg('final hdl', hdl)

        # update location. Use the previous created handle location
        self.updateHandleWithLocation(hdl, location)
        return hdl

    def modifyHandle(self, prefix, key, value, suffix=''):
        """Modify a parameter of a handle

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        key: The parameter "type" wanted to change
        value: New value to store in "data"
        suffix: The suffix of the handle. Default: ''.
        Returns True if modified or parameter not found, False otherwise.

        """

        if prefix.startswith(self.cred.baseuri):
            prefix = prefix[len(self.cred.baseuri):]

        if self.cred.baseuri.endswith('/'):
            uri = self.cred.baseuri + prefix
        else:
            uri = self.cred.baseuri + '/' + prefix

        if suffix != '':
            uri += "/" + suffix.partition("/")[2]

        self._debugMsg('modifyHandle',"URI " + uri)
        auth = base64.encodestring(self.cred.username + ':' +
                                   self.cred.password)
        hdrs = {'Content-Type': 'application/json',
                'Authorization': 'Basic ' + auth}

        # FIXME move this if-statement up, to beginning of method?
        if not key:
            return False

        handle_json = self.retrieveHandle(prefix, suffix)
        if not handle_json:
            self._debugMsg('modifyHandle',
                           "Cannot modify an unexisting handle: " + uri)
            return False

        handle = simplejson.loads(handle_json)
        KeyFound = False

        if value is "" or None or '':
            for item in handle:
                if item.has_key('type') and item['type'] == key:
                    self._debugMsg('modifyHandle','Remove item ' + key)
                    handle.remove(item)
                    break
        else:
            for item in handle:
                if item.has_key('type') and item['type'] == key:
                    KeyFound = True
                    self._debugMsg('modifyHandle',
                                   "Found key " + key + " value=" +
                                   str(item['parsed_data']))
                    item['parsed_data'] = value
                    del item['data']
                    break

            if KeyFound is False:
                if value is None:
                    self._debugMsg('modifyHandle', "No value for Key " + key +
                                                   " . Quitting")
                    # FIXME what is the reason for returning True here?
                    return True

                self._debugMsg('modifyHandle', "Key " + key +
                                               " not found. Generating new hash")
                handleItem = {'type': key, 'parsed_data': value}
                handle.append(handleItem)

        handle_json = simplejson.dumps(handle)
        self._debugMsg('modifyHandle', "JSON: " + str(handle_json))

        response, _ = self.http.request(uri, method='PUT', headers=hdrs,
                                        body=handle_json)
        # FIXME this can't be true; there are many status codes
        # FIXME in the 200 range that do not indicate a "OK" status
        # FIXME So this test is probably not good enough
        if response.status < 200 or response.status >= 300:
            self._debugMsg('modifyHandle', "Not Modified: Response status: " +
                                           str(response.status))
            return False
        else:
            self._debugMsg('modifyHandle', "Request completed")

        return True

    def deleteHandle(self, prefix, suffix=''):
        """Delete a handle from the server.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        suffix: The suffix of the handle. Default: ''.
        Returns True if deleted, False otherwise.

        """

        if self.cred.baseuri.endswith('/'):
            uri = self.cred.baseuri + prefix
        else:
            uri = self.cred.baseuri + '/' + prefix

        if suffix != '':
            uri += "/" + suffix.partition("/")[2]
        self._debugMsg('deleteHandle', "DELETE URI " + uri)
        auth = base64.encodestring(self.cred.username + ':' +
                                   self.cred.password)
        hdrs = {'Authorization': 'Basic ' + auth}

        response, _ = self.http.request(uri, method='DELETE', headers=hdrs)
        # FIXME this can't be true; there are many status codes
        # FIXME in the 200 range that do not indicate a "OK" status
        # FIXME So this test is probably not good enough
        if response.status < 200 or response.status >= 300:
            self._debugMsg('deleteHandle', "Not Deleted: Response status: " +
                                           str(response.status))
            return False
        else:
            self._debugMsg('deleteHandle', "Request completed")

        return True

    def updateHandleWithLocation(self, prefix, value, suffix=''):
        """Update the 10320/LOC handle type field of the handle record.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        value: New value to store in "10320/LOC"
        suffix: The suffix of the handle. Default: ''.
        Returns True if updated, False otherwise.

        """

        if self.cred.baseuri.endswith('/'):
            uri = self.cred.baseuri + prefix
        else:
            uri = self.cred.baseuri + '/' + prefix

        if suffix != '':
            uri += "/" + suffix.partition("/")[2]

        loc10320 = self.getValueFromHandle(prefix, "10320/LOC", suffix)
        self._debugMsg('updateHandleWithLocation', "found 10320/LOC: " +
                                                   str(loc10320))
        if loc10320 is None:
            loc10320 = ('<locations><location id="0" href="' + value +
                        '" /></locations>')
            response = self.modifyHandle(prefix, "10320/LOC", loc10320,
                                         suffix)
            if not response:
                self._debugMsg('updateHandleWithLocation',
                               "Cannot update handle: " + uri +
                               " with location: " + value)
                return False
        else:
            lt = LocationType(loc10320, self.debug)
            response = lt.checkInclusion(value)
            if response:
                self._debugMsg('updateHandleWithLocation',
                               "the location " + value +
                               " is already included!")
            else:
                resp, content = lt.addLocation(value)
                if not resp:
                    self._debugMsg('updateHandleWithLocation',
                                   "the location "+ value +
                                   " cannot be added")
                else:
                    if not self.modifyHandle(prefix, "10320/LOC",
                                             content,suffix):
                        self._debugMsg('updateHandleWithLocation',
                                       "Cannot update handle: " + uri +
                                       " with location: " + value)
                    else:
                        self._debugMsg('updateHandleWithLocation',
                                       "location added")
                        return True

            return False

        return True

    def removeLocationFromHandle(self, prefix, value, suffix=''):
        """Remove one of the 10320/LOC handle type values
        from the handle record.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        value: Value to be deleted from the "10320/LOC".
        suffix: The suffix of the handle. Default: ''.
        Returns True if removed, False otherwise.

        """

        if self.cred.baseuri.endswith('/'):
            uri = self.cred.baseuri + prefix
        else:
            uri = self.cred.baseuri + '/' + prefix

        if suffix != '':
            uri += "/" + suffix.partition("/")[2]

        loc10320 = self.getValueFromHandle(prefix, "10320/LOC", suffix)
        if loc10320 is None:
            self._debugMsg('removeLocationFromHandle',
                           "Cannot remove location: " + value +
                           " from handle: " + uri +
                           ", the field 10320/LOC does not exists")
            return False
        else:
            lt = LocationType(loc10320, self.debug)
            if not lt.checkInclusion(value):
                self._debugMsg('removeLocationFromHandle',
                               "the location " + value + " is not included!")
            else:
                response, content = lt.removeLocation(value)
                if response:
                    if self.modifyHandle(prefix, "10320/LOC", content,
                                         suffix):
                        return True

                # FIXME is this at the correct indent level??
                self._debugMsg('removeLocationFromHandle',
                               "the location " + value + " cannot be removed")
            return False

        return True


################################################################################
# EPIC Client Location Type Class #
################################################################################

class LocationType(object):
    """Class implementing a 10320/LOC handle type.
    Expected format for 10320/LOC handle type:
    <locations>
      <location id="0" href="location" country="xx" weight="0" />
    </locations>

    """

    def __init__(self, field, debug=False):
        # FIXME xml.dom.minidom is not secure against maliciously crafted XML
        self.domfield = minidom.parseString(field)
        self.debug = debug

    def _debugMsg(self, method, msg):
        """Internal: Print a debug message if debug is enabled."""

        if self.debug:
            print "[", method, "]", msg

    def isEmpty(self):
        """Check if the 10320/LOC handle type field is empty.

        Parameters:
        Returns True and 0 if empty,
        False and the number of locations otherwise.

        """

        locations = self.domfield.getElementsByTagName("location")
        if locations.length == 0:
            self._debugMsg('isEmpty', "the 10320/LOC field is empty")
            return True, 0
        self._debugMsg('isEmpty', "the 10320/LOC field contains " +
                                  str(locations.length) + " locations")
        return False, str(locations.length)

    def checkInclusion(self, loc):
        """Check if a 10320/LOC handle type value is included.

        Parameters:
        loc: The replica location PID value.
        Returns True if it is included, False otherwise.

        """

        locations = self.domfield.getElementsByTagName("location")
        for url in locations:
            if url.getAttribute('href') == loc:
                self._debugMsg('checkInclusion',
                               "the location (" + loc + ") is included")
                return True

        self._debugMsg('checkInclusion',
                       "the location (" + loc + ") is not included")
        return False

    def removeLocation(self, loc):
        """Remove a replica PID from the 10320/LOC handle type field.

        Parameters:
        loc: The replica location PID value.
        Returns True and the 10320/LOC handle type field itself
        if the value is removed, False and None otherwise.

        """

        main = self.domfield.childNodes[0]
        locations = self.domfield.getElementsByTagName("location")
        for url in locations:
            if url.getAttribute('href') == loc:
                main.removeChild(url)
                self._debugMsg('removeLocation', "removed location: " + loc)
                return True, main.toxml()

        self._debugMsg('removeLocation', "cannot remove location: " + loc)
        return False, None

    def addLocation(self, loc):
        """Add a replica PID to the 10320/LOC handle type field.

        Parameters:
        loc: The replica location PID value.
        Returns True and the 10320/LOC handle type field itself
        if the value is added, False and None otherwise.

        """

        try:
            newurl = self.domfield.createElement("location")
            _, content = self.isEmpty()
            newurl.setAttribute('id', content)
            newurl.setAttribute('href', loc)
            self.domfield.childNodes[0].appendChild(newurl)
            main = self.domfield.childNodes[0]
            self._debugMsg('addLocation', "added new location: " + loc)
            return True, main.toxml()
        except TypeError:
            self._debugMsg('addLocation', "an XML TypeError occurred, "
                                          "adding the new location: " + loc)
            return False, None
        except AttributeError:
            self._debugMsg('addLocation', "an XML AttributeError occurred, "
                                          "adding the new location: " + loc)
            return False, None


###############################################################################
# EPIC Client Credentials Class #
###############################################################################

class Credentials(object):
    """
    get credentials from different storages, right now
    irods or filesystem. please store credentials in the
    following format, otherwise there are problems...
    {
        "baseuri": "https://epic_api_endpoint here",
        "username": "USER",
        "prefix": "YYY",
        "password": "ZZZZZZZ",
        "accept_format": "application/json",
        "debug": "False"
    }

    """

    def __init__(self, store, filename):
        '''initialize member variables'''

        self.store = store
        self.filename = filename
        self.debug = False
        self.baseuri = None
        self.username = None
        self.prefix = None
        self.password = None
        self.accept_format = 'application/json'

    def parse(self):
        """parse credentials from json file on filespace/irods.
        if you want to use irods you need embedded python!

        This method terminates the program on error

        """

        if self.store == "os":
            try:
                filehandle = open(self.filename, "r")
            except IOError as err:
                print "error: failed to open %s: %s" % (self.filename,
                                                        err.strerror)
                sys.exit(-1)

            with filehandle:
                tmp = simplejson.loads(filehandle.read())

        elif self.store == "irods":
            try:
                irods = __import__("irods")
            except ImportError as err:
                print "error: failed to import module 'irods':", err
                sys.exit(-1)

            # FIXME add try/except block for specific exceptions
            myEnv, _ = irods.getRodsEnv()
            conn, _ = irods.rcConnect(myEnv.getRodsHost(), myEnv.getRodsPort(),
                                      myEnv.getRodsUserName(),
                                      myEnv.getRodsZone())
            if self.debug:
                print (myEnv.getRodsHost(), myEnv.getRodsPort(),
                       myEnv.getRodsUserName(), myEnv.getRodsZone())
            irods.clientLogin(conn)
            testconn = irods.iRodsOpen(conn, self.filename, 'r')
            tmp = simplejson.loads(testconn.read())
            testconn.close()
            conn.disconnect()
        else:
            print "error: invalid store '%s', aborting" % self.store
            sys.exit(-1)

        try:
            self.baseuri = tmp['baseuri']
            self.username = tmp['username']
            try:
                self.prefix = tmp['prefix']
            except KeyError:
                self.prefix = self.username
            self.password = tmp['password']
            self.accept_format = tmp['accept_format']
            if tmp['debug'] == 'True':
                self.debug = True
        except KeyError:
            print "error: missing key-value-pair in credentials file"
            sys.exit(-1)

        if self.debug:
            print ("credentials from %s:%s %s %s %s" %
                   (self.store, self.baseuri, self.username, self.prefix,
                    self.accept_format))


###############################################################################
# EPIC Client Command Line Interface #
###############################################################################

def search(args):
    '''perform search action'''

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    ec = EpicClient(credentials)
    result = ec.searchHandle(credentials.prefix, args.key, args.value)

    sys.stdout.write(str(result))


def read(args):
    '''perform read action'''

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    ec = EpicClient(credentials)
    if args.key == None:
        result = ec.retrieveHandle(credentials.prefix, args.handle)
    else:
        result = ec.getValueFromHandle(args.handle, args.key)

    sys.stdout.write(str(result))


def create(args):
    '''perform create action'''

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    uid = uuid.uuid1()
    pid = credentials.prefix + "/" + str(uid)

    ec = EpicClient(credentials)
    result = ec.createHandle(pid, args.location, args.checksum)

    if result == None:
        sys.stdout.write("error")
    else:
        sys.stdout.write(result)


def modify(args):
    '''perform modify action'''

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    ec = EpicClient(credentials)
    result = ec.modifyHandle(args.handle, args.key, args.value)

    sys.stdout.write(str(result))


def delete(args):
    '''perform delete action'''

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    ec = EpicClient(credentials)
    result = ec.deleteHandle(args.handle)

    sys.stdout.write(str(result))


def relation(args):
    '''perform the relation action'''

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    ec = EpicClient(credentials)
    result = ec.updateHandleWithLocation(args.ppid, args.cpid)
    sys.stdout.write(str(result))


def test(args):
    '''do a series of tests'''

    def test_result(result, testval):
        '''local helper func: print OK/FAIL for test result
        Returns 0 on OK, 1 on failure'''

        if type(result) != type(testval):
            print "FAIL (wrong type; test is bad)"
            return 1

        if result == testval:
            print "OK"
            return 0
        else:
            print "FAIL"
            return 1

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    ec = EpicClient(credentials)

    fail = 0

    print
    print ("Retrieving Value of FOO from " + credentials.prefix +
           "/NONEXISTING (should be None)")
    fail += test_result(ec.getValueFromHandle(credentials.prefix, "FOO",
                                              "NONEXISTING"), None)

    print
    print ("Creating handle " + credentials.prefix +
           "/TEST_CR1 (should be prefix + '/TEST_CR1')")
    fail += test_result(ec.createHandle(credentials.prefix + "/TEST_CR1",
                                        "http://www.test.com/1"),
                        credentials.prefix + "/TEST_CR1")

    print
    print "Retrieving handle info from " + credentials.prefix + "/TEST_CR1"
    print ec.retrieveHandle(credentials.prefix + "/TEST_CR1")

    print
    print "Retrieving handle by url"
    fail += test_result(ec.searchHandle(credentials.prefix, "URL",
                                        "http://www.test.com/1"),
                        credentials.prefix + "/TEST_CR1")

    print
    print ("Modifying handle info from " + credentials.prefix +
           "/TEST_CR1 (should be True)")
    fail += test_result(ec.modifyHandle(credentials.prefix + "/TEST_CR1",
                                        "uri", "http://www.test.com/2"), True)

    print
    print ("Retrieving Value of EMAIL from " + credentials.prefix +
           "/TEST_CR1 (should be None)")
    fail += test_result(ec.getValueFromHandle(credentials.prefix +
                                              "/TEST_CR1", "EMAIL"), None)

    print
    print ("Adding new info to " + credentials.prefix +
           "/TEST_CR1 (should be True)")
    fail += test_result(ec.modifyHandle(credentials.prefix + "/TEST_CR1",
                                        "EMAIL", "test@te.st"), True)

    print
    print ("Retrieving Value of EMAIL from " + credentials.prefix +
           "/TEST_CR1 (should be test@te.st)")
    fail += test_result(ec.getValueFromHandle(credentials.prefix +
                                              "/TEST_CR1", "EMAIL"),
                                              "test@te.st")

    print
    print ("Updating handle info with a new 10320/loc type location "
           "846/157c344a-0179-11e2-9511-00215ec779a8")
    print "(should be True)"
    fail += test_result(ec.updateHandleWithLocation(credentials.prefix +
                        "/TEST_CR1",
                        "846/157c344a-0179-11e2-9511-00215ec779a8"), True)

    print
    print ("Updating handle info with a new 10320/loc type location "
           "846/157c344a-0179-11e2-9511-00215ec779a9")
    print "(should be True)"
    fail += test_result(ec.updateHandleWithLocation(credentials.prefix +
                        "/TEST_CR1",
                        "846/157c344a-0179-11e2-9511-00215ec779a9"), True)

    print
    print "Retrieving handle info from " + credentials.prefix + "/TEST_CR1"
    print ec.retrieveHandle(credentials.prefix + "/TEST_CR1")

    print
    print ("Deleting EMAIL parameter from " + credentials.prefix +
           "/TEST_CR1 (should be True)")
    fail += test_result(ec.modifyHandle(credentials.prefix + "/TEST_CR1",
                                        "EMAIL", None), True)

    print
    print ("Retrieving Value of EMAIL from " + credentials.prefix +
           "/TEST_CR1 (should be None)")
    # FIXME this actually gives an empty string: ""
    # FIXME the problem seems to be that modifyHandle() does not actually
    # FIXME delete the field when value is None
    # FIXME So either modifyHandle() is bugged when "value is None" or
    # FIXME this test is wrong; it doesn't result in "None"
    fail += test_result(ec.getValueFromHandle(credentials.prefix +
                                              "/TEST_CR1", "EMAIL"), None)

    print
    print ("Updating handle info with a new 10320/loc type location "
           "846/157c344a-0179-11e2-9511-00215ec779a8")
    print "(should be False)"
    fail += test_result(ec.updateHandleWithLocation(credentials.prefix +
                        "/TEST_CR1",
                        "846/157c344a-0179-11e2-9511-00215ec779a8"), False)

    print
    print ("Removing 10320/loc type location "
           "846/157c344a-0179-11e2-9511-00215ec779a8")
    print "(should be True)"
    fail += test_result(ec.removeLocationFromHandle(credentials.prefix +
                        "/TEST_CR1",
                        "846/157c344a-0179-11e2-9511-00215ec779a8"), True)

    print
    print ("Removing 10320/loc type location "
           "846/157c344a-0179-11e2-9511-00215ec779a8")
    print "(should be False)"
    fail += test_result(ec.removeLocationFromHandle(credentials.prefix +
                        "/TEST_CR1",
                        "846/157c344a-0179-11e2-9511-00215ec779a8"), False)

    print
    print "Retrieving handle info from " + credentials.prefix + "/TEST_CR1"
    print ec.retrieveHandle(credentials.prefix + "/TEST_CR1")

    print
    print "Deleting " + credentials.prefix + "/TEST_CR1 (should be True)"
    fail += test_result(ec.deleteHandle(credentials.prefix + "/TEST_CR1"),
                        True)

    print
    print ("Deleting (again) " + credentials.prefix +
           "/TEST_CR1 (should be False)")
    fail += test_result(ec.deleteHandle(credentials.prefix + "/TEST_CR1"),
                        False)

    print
    print ("Retrieving handle info from non existing " + credentials.prefix +
           "/TEST_CR1 (should be None)")
    fail += test_result(ec.retrieveHandle(credentials.prefix + "/TEST_CR1"),
                        None)

    print
    if fail == 0:
        print "All tests passed OK"
    else:
        print "%d tests failed" % fail


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='EUDAT EPIC client API. '
                                                 'Supports reading, querying,'
                                                 ' creating, modifying and '
                                                 'deleting handle records.')
    parser.add_argument("credstore", choices=['os','irods'], default="NULL",
                        help="the used credential storage "
                             "(os=filespace,irods=iRODS storage)")
    parser.add_argument("credpath", default="NULL",
                        help="path to the credentials")
    #parser.add_argument("-d", "--debug", help="Show debug output")

    subparsers = parser.add_subparsers(title='Actions',
                                       description='Handle record management '
                                                   'actions',
                                       help='additional help')
    parser_create = subparsers.add_parser('create',
                                          help='creating handle records')
    parser_create.add_argument("location", help="location to store in "
                                                "the new handle record")
    parser_create.add_argument("--checksum", help="checksum to store in "
                                                  "the new handle record")
    parser_create.set_defaults(func=create)

    parser_modify = subparsers.add_parser('modify',
                                          help='modifying handle records')
    parser_modify.add_argument("handle", help="the handle value")
    parser_modify.add_argument("key", help="the key of the field to change "
                                           "in the pid record")
    parser_modify.add_argument("value", help="the new value to store "
                                             "in the pid record identified "
                                             "with the supplied key")
    parser_modify.set_defaults(func=modify)

    parser_delete = subparsers.add_parser('delete',
                                          help='Deleting handle records')
    parser_delete.add_argument("handle",
                               help="the handle value of the digital object "
                                    "instance to delete")
    parser_delete.set_defaults(func=delete)

    parser_read = subparsers.add_parser('read', help='Read handle record')
    parser_read.add_argument("handle", help="the handle value")
    parser_read.add_argument("--key", help="only read this key instead of "
                                           "the full handle record")
    parser_read.set_defaults(func=read)

    parser_search = subparsers.add_parser('search',
                                          help='Search for handle records')
    parser_search.add_argument("key", choices=['URL','CHECKSUM'],
                               help="the key to search")
    parser_search.add_argument("value", help="the value to search")
    parser_search.set_defaults(func=search)

    parser_relation = subparsers.add_parser('relation',
                                            help='Add a (parent,child) '
                                                 'relationship between '
                                                 'the specified handle '
                                                 'records')
    parser_relation.add_argument("ppid", help="parent handle value")
    parser_relation.add_argument("cpid", help="child handle value")
    parser_relation.set_defaults(func=relation)

    parser_test = subparsers.add_parser('test', help='Run test suite')
    parser_test.set_defaults(func=test)

    _args = parser.parse_args()
    _args.func(_args)

