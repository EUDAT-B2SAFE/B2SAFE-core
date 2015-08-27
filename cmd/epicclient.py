#!/usr/bin/env python
#
# epicclient.py
#
# * use 4 spaces!!! not tabs
# * set tabstop=4
# * set expandtab
# * See PEP-8 Python style guide http://www.python.org/dev/peps/pep-0008/
# * use pylint
#

"""EUDAT EPIC client API. Supports reading, querying, creating, modifying and
deleting handle records.

httplib2
download from http://code.google.com/p/httplib2
python setup.py install

simplejson
download from http://pypi.python.org/pypi/simplejson/
python setup.py install

lxml
pip install lxml

defusedxml
pip install defusedxml

ubuntu: apt-get install python-httplib2 python-simplejson
redhat: yum install python-argparse python-defusedxml
redhat: yum install python-httplib2 python-lxml python-simplejson

"""

import httplib2
import simplejson
from defusedxml import minidom
from lxml import etree
from lxml.etree import tostring
import base64
import uuid
import argparse
import sys


# ##############################################################################
# Epic Client Class #
# ##############################################################################


class EpicClient(object):
    """Class implementing an EPIC client."""

    def __init__(self, cred):
        """Initialize object with connection parameters."""

        self.cred = cred
        self.debug = cred.debug
        self.http = httplib2.Http(disable_ssl_certificate_validation=True)
        self.http.add_credentials(cred.username, cred.password)
        # do not throw exceptions for connection errors
        self.http.force_exception_to_status_code = True

    def _debugmsg(self, method, msg):
        """Internal: Print a debug message if debug is enabled."""

        if self.debug:
            print "[", method, "]", msg

    def _geturi(self, prefix, key, value, suffix=''):
        """
            build base-URI for HTTP-Request
        """
        if self.cred.baseuri.endswith('/'):
            uri = self.cred.baseuri + prefix
        else:
            uri = self.cred.baseuri + '/' + prefix
        if suffix != '':
            # uri += "/" + suffix.partition("/")[2]
            uri += "/" + suffix
        if key != '' and value != '':
            uri += '/?' + key + '=' + value
        return uri

    def _getheader(self, action):
        """
            build Header for HTTP-Request
        """
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
        else:
            self._debugmsg(str(action), "ACTION is unknown")

        return hdrs

    def _checkresponsecode(self, method, statuscode):
        """ using dict-style """
        codelist = [{"statuscode": "200", "info": "Request completed. No error,\
                     operation successful", "output": "True"},
                    {"statuscode": "201", "info": "Successful creation of a \
                     resource", "output": "True"},
                    {"statuscode": "202", "info": "The request was received",
                     "output": "True"},
                    {"statuscode": "204", "info": "The request was processed \
                     successfully, but no response body is needed", "output":
                     "True"},
                    {"statuscode": "304", "info": "Resource has not been \
                     modified", "output": "False"},
                    {"statuscode": "400", "info": "Bad Request", "output":
                     "False"},
                    {"statuscode": "401", "info": "Action requires user \
                     authentication", "output": "False"},
                    {"statuscode": "404", "info": "Resource not found",
                     "output": "False"},
                    {"statuscode": "405", "info": "Method Not Allowed",
                     "output": " False"},
                    {"statuscode": "409", "info": "Conflict",
                     "output": "False"},
                    {"statuscode": "500", "info": "Internal Server Error",
                     "output": "None"},
                    {"statuscode": "501", "info": "Requested HTTP operation \
                     not supported", "output": "None"},
                    {"statuscode": "503", "info": "Service Unavailable",
                     "output": "None"}]
        for item in codelist:
            if item["statuscode"] == str(statuscode):
                self._debugmsg("checkresponsecode", ".....")
                self._debugmsg(str(method), item["info"]+" "+str(statuscode))
                output = item["output"]
                if output is "None":
                    return None
                elif output is "False":
                    return False
                else:
                    return True
        print "Processing fails with statuscode = " + str(statuscode)
        return None


    # *************************** Public Methods *****************************

    def searchHandle(self, prefix, key, value):
        """Search for handles containing the specified key with
        the specified value.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        url: The URL to search for.
        Returns the searched data field, or None if error,
        or empty if not found.

        """

        uri = self._geturi(prefix, key, value, '')
        self._debugmsg('searchHandle', "URI " + uri)
        hdrs = self._getheader("SEARCH")
        response, content = self.http.request(uri, method='GET', headers=hdrs)
        output = True
        output = self._checkresponsecode("searchHandle", response.status)
        if not output or output is None or not content:
            # if not content:
            return None
        else:
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

        uri = self._geturi(prefix, '', '', suffix)
        self._debugmsg('retrieveHandle', "URI " + uri)
        hdrs = self._getheader("READ")
        response, content = self.http.request(uri, method='GET', headers=hdrs)
        output = self._checkresponsecode("retrieveHandle", response.status)
        if output is False or output is None or not content:
            return None
        else:
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
                self._debugmsg('getValueFromHandle',
                               "Found key " + key + " value=" +
                               str(item['parsed_data']))
                return str(item['parsed_data'])

        self._debugmsg('getValueFromHandle', "Value for key " + key +
                       " not found")
        return None

    def createHandle(self, prefix, location, checksum=None, extratype=None,
                     l10320=None, suffix=''):
        """Create a new handle for a file.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        location: The location (URL) of the file.
        checksum: Optional parameter, store the checksum of the file as well.
        suffix: The suffix of the handle. Default: ''.
        Returns the URI of the new handle, None if an error occurred.

        """
        self._debugmsg('createHandle', "PREFIX = " + prefix)
        self._debugmsg('createHandle', "SUFFIX = " + suffix)
        uri = self._geturi(prefix, '', '', suffix)
        self._debugmsg('createHandleWithLocation', "URI " + uri)
        hdrs = self._getheader("CREATE")

        idn = 0
        root = etree.Element('locations')

        if l10320 is None:
            # loc10320 = ('<locations><location id="0" href="' + str(location) +
            #            '" /></locations>')
            self._debugmsg('createHandle', "loc10320 = None")
            etree.SubElement(root, 'location', id=str(idn), href=str(location))
        else:
            etree.SubElement(root, 'location', id=str(idn), href=str(location))
            for item in l10320:
                idn += 1
                etree.SubElement(root, 'location', id=str(idn), href=str(item))

        loc10320 = tostring(root)

        handle_array = [{'type': 'URL', 'parsed_data': location}]
        handle_array.append({'type': '10320/LOC', 'parsed_data': loc10320})
        if ((checksum) and (checksum is not None)):
            handle_array.append({'type': 'CHECKSUM', 'parsed_data': checksum})
        if ((extratype) and (extratype is not None)):
            for key_value in extratype:
                key = key_value.split('=')[0]
                value = key_value.split('=')[1]
                if (next((item for item in handle_array if item['type'] == key),
                         None) is None):
                    handle_array.append({'type': key, 'parsed_data': value})

        new_handle_json = simplejson.dumps(handle_array)

        response, _ = self.http.request(uri, method='PUT', headers=hdrs,
                                        body=new_handle_json)
        output = True
        output = self._checkresponsecode("createHandle", response.status)
        if not output or output is None:
            self._debugmsg('createHandleWithLocation', 'body json:'
                           + new_handle_json)
            return None
        else:
            # make sure to only return the handle and strip off the baseuri
            # if it is included
            hdl = response['location']
            self._debugmsg('hdl', hdl)
            if hdl.startswith(self.cred.baseuri):
                hdl = hdl[len(self.cred.baseuri):len(hdl)]
            elif hdl.startswith(self.cred.baseuri + '/'):
                hdl = hdl[len(self.cred.baseuri + '/'):len(hdl)]
                self._debugmsg('final hdl', hdl)

        # update location. Use the previous created handle location
        # self.updateHandleWithLocation(hdl, location)

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

        uri = self._geturi(prefix, key, value, suffix)
        self._debugmsg('modifyHandle', "URI " + uri)

        hdrs = self._getheader("UPDATE")

        handle_json = self.retrieveHandle(prefix, suffix)
        if not handle_json:
            self._debugmsg('modifyHandle',
                           "Cannot modify an unexisting handle: " + uri)
            return False

        handle = simplejson.loads(handle_json)

        keyfound = False

        if (value is None) or (value is '') or (value is ""):
            for item in handle:
                if 'type' in item and item['type'] == key:
                    self._debugmsg('modifyHandle', 'Remove item ' + key)
                    del item['data']
                    del item['parsed_data']
                    break
        else:
            for item in handle:
                if 'type' in item and item['type'] == key:
                    keyfound = True
                    self._debugmsg('modifyHandle', "Found key " + key +
                                   " value=" + str(item['parsed_data']))
                    item['parsed_data'] = value
                    del item['data']
                    break

            if keyfound is False:
                self._debugmsg('modifyHandle', "Value of keyfound is false, "
                               "create new key")
                self._debugmsg('modifyHandle',
                               "Key " + key + " created. Generating new hash")
                handleitem = {'type': key, 'parsed_data': value}
                handle[len(handle):] = [handleitem]

        handle_json = simplejson.dumps(handle)
        self._debugmsg('modifyHandle', "JSON: " + str(handle_json))

        response, _ = self.http.request(uri, method='PUT', headers=hdrs,
                                        body=handle_json)
        output = self._checkresponsecode("modifyHandle", response.status)
        if output is None or False:
            return False
        else:
            return True

    def deleteHandle(self, prefix, key, suffix=''):
        """Delete a handle from the server.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        suffix: The suffix of the handle. Default: ''.
        Returns True if deleted, False otherwise.

        """

        uri = self._geturi(prefix, '', '', suffix)
        if not key or key is "":
            hdrs = self._getheader("DELETE")
            self._debugmsg('deleteHandle', "DELETE Handle " + prefix + "/"
                           + suffix + " of URI " + uri)
            response, _ = self.http.request(uri, method='DELETE',
                                            headers=hdrs)
        else:
            self._debugmsg('deleteHandle', "DELETE field " + key + " of URI"
                           + uri)
            handle_json = self.retrieveHandle(prefix, suffix)
            if not handle_json:
                self._debugmsg('deleteHandle',
                               "Cannot modify an unexisting handle: " + uri)
                return False
            keyfound = False
            handle = simplejson.loads(handle_json)

            for item in handle:
                if 'type' in item and item['type'] == key:
                    keyfound = True
                    self._debugmsg('deleteHandle', "Found key " + key +
                                   " value=" + str(item['parsed_data']))
                    self._debugmsg('deleteHandle', "Remove Key's Field")
                    del handle[handle.index(item)]
                    break

            if keyfound is False:
                self._debugmsg('deleteHandle', "No Value of key is found. "
                               "Quiting....")
                return False
            else:
                hdrs = self._getheader("UPDATE")
                handle_json = simplejson.dumps(handle)
                self._debugmsg('deleteHandle', "JSON: " + str(handle_json))
                response, _ = self.http.request(uri, method='PUT', headers=hdrs,
                                                body=handle_json)

        output = self._checkresponsecode("deleteHandle", response.status)
        self._debugmsg('deleteHandle', "OUTPUT = " + str(output))
        if (output is None) or (output is False):
            return False
        else:
            return True

    def updateHandleWithLocation(self, prefix, value, suffix=''):
        """Update the 10320/LOC handle type field of the handle record.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        value: New value to store in "10320/LOC"
        suffix: The suffix of the handle. Default: ''.
        Returns True if updated, False otherwise.

        """

        uri = self._geturi(prefix, '', value, suffix)

        loc10320 = self.getValueFromHandle(prefix, "10320/LOC", suffix)
        self._debugmsg('updateHandleWithLocation', "found 10320/LOC: " +
                       str(loc10320))
        if loc10320 is None:
            loc10320 = ('<locations><location id="0" href="' + value +
                        '" /></locations>')
            response = self.modifyHandle(prefix, "10320/LOC", loc10320, suffix)
            if not response:
                self._debugmsg('updateHandleWithLocation',
                               "Cannot update handle: " + uri +
                               " with location: " + value)
                return False
        else:
            lt = LocationType(loc10320, self.debug)
            response = lt.checkInclusion(value)
            if response:
                self._debugmsg('updateHandleWithLocation',
                               "the location " + value +
                               " is already included!")
            else:
                resp, content = lt.addLocation(value)
                if not resp:
                    self._debugmsg('updateHandleWithLocation',
                                   "the location " + value +
                                   " cannot be added")
                else:
                    if not self.modifyHandle(prefix, "10320/LOC",
                                             content, suffix):
                        self._debugmsg('updateHandleWithLocation',
                                       "Cannot update handle: " + uri +
                                       " with location: " + value)
                    else:
                        self._debugmsg('updateHandleWithLocation',
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

        uri = self._geturi(prefix, '', '', suffix)

        loc10320 = self.getValueFromHandle(prefix, "10320/LOC", suffix)
        if loc10320 is None:
            self._debugmsg('removeLocationFromHandle',
                           "Cannot remove location: " + value +
                           " from handle: " + uri +
                           ", the field 10320/LOC does not exists")
            return False
        else:
            lt = LocationType(loc10320, self.debug)
            if not lt.checkInclusion(value):
                self._debugmsg('removeLocationFromHandle', "the location " +
                               value + " is not included!")
                return False
            else:
                response, content = lt.removeLocation(value)
                if response:
                    if self.modifyHandle(prefix, "10320/LOC", content, suffix):
                        return True

                self._debugmsg('removeLocationFromHandle', "the location " +
                               value + " cannot be removed")
                return False

    def updateLocationInHandle(self, prefix, oldvalue, newvalue, suffix=''):
        """Update one of the 10320/LOC handle type values
        in the handle record.

        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
        oldvalue: Value to be updated/replaced in the "10320/LOC".
        newvalue: Value to be updated/put in the "10320/LOC".
        suffix: The suffix of the handle. Default: ''.
        Returns True if removed, False otherwise.

        """

        uri = self._geturi(prefix, '', '', suffix)

        loc10320 = self.getValueFromHandle(prefix, "10320/LOC", suffix)
        if loc10320 is None:
            self._debugmsg('updateLocationInHandle',
                           "Cannot update location: " + oldvalue +
                           " from handle: " + uri +
                           ", the field 10320/LOC does not exists")
            return False
        else:
            lt = LocationType(loc10320, self.debug)
            if not lt.checkInclusion(oldvalue):
                self._debugmsg('updateLocationInHandle', "the location " +
                               oldvalue + " is not included!")
                return False
            else:
                response, content = lt.updateLocation(oldvalue, newvalue)
                if response:
                    if self.modifyHandle(prefix, "10320/LOC", content, suffix):
                        return True

                self._debugmsg('removeLocationFromHandle', "the location " +
                               value + " cannot be updated")
                return False


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
        self.domfield = minidom.parseString(field)
        self.debug = debug

    def _debugmsg(self, method, msg):
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
            self._debugmsg('isEmpty', "the 10320/LOC field is empty")
            return True, 0
        self._debugmsg('isEmpty', "the 10320/LOC field contains " +
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
                self._debugmsg('checkInclusion',
                               "the location (" + loc + ") is included")
                return True

        self._debugmsg('checkInclusion',
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
                self._debugmsg('removeLocation', "removed location: " + loc)
                return True, main.toxml()

        self._debugmsg('removeLocation', "cannot remove location: " + loc)
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
            self._debugmsg('addLocation', "added new location: " + loc)
            return True, main.toxml()
        except TypeError:
            self._debugmsg('addLocation', "an XML TypeError occurred, "
                                          "adding the new location: " + loc)
            return False, None
        except AttributeError:
            self._debugmsg('addLocation', "an XML AttributeError occurred, "
                                          "adding the new location: " + loc)
            return False, None


    def updateLocation(self, oldloc, newloc):
        """Update a entry from the 10320/LOC handle type field.

        Parameters:
        oldloc: The value to replace in the 10320/LOC field.
        newloc: The new value for the 10320/LOC field.
        Returns True and the 10320/LOC handle type field itself
        if the value is updated, False and None otherwise.

        """

        main = self.domfield.childNodes[0]
        locations = self.domfield.getElementsByTagName("location")
        for url in locations:
            if url.getAttribute('href') == oldloc:
                newurl = self.domfield.createElement("location")
                _, content = self.isEmpty()
                newurl.setAttribute('id', url.getAttribute('id'))
                newurl.setAttribute('href', newloc)
                main.replaceChild(newurl, url)
                self._debugmsg('updateLocation', "updated location: " + oldloc
                                + "with: " + newloc)
                return True, main.toxml()

        self._debugmsg('updateLocation', "cannot update location: " + loc)
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
        """initialize member variables"""

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

        elif self.store == "irods":
            print "Function getting credential store in iRODS is in testing ..."
            # FIXME: is there better way to exit ?.
            sys.exit(-1)
        else:
            print "error: invalid store '%s', aborting" % self.store
            sys.exit(-1)

        if self.debug:
            print ("credentials from %s:%s %s %s %s" %
                   (self.store, self.baseuri, self.username, self.prefix,
                    self.accept_format))


###############################################################################
# EPIC Client Command Line Interface #
###############################################################################

def replaceHash(args):
    """perform Hash function """
    key = ' '.join(args.a)
    result = key.replace('#', '*').replace('%', '*').replace('&', '*')
    sys.stdout.write(str(result))


def search(args):
    """perform search action"""

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    epicclient = EpicClient(credentials)
    value = ' '.join(args.value)
    result = epicclient.searchHandle(credentials.prefix, args.key, value)

    sys.stdout.write(str(result))


def read(args):
    """perform read action"""

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()
    prefix = args.handle.partition("/")[0]
    suffix = args.handle.partition("/")[2]
    client = EpicClient(credentials)

    if args.key is None:
        result = client.retrieveHandle(prefix, suffix)
    else:
        result = client.getValueFromHandle(prefix, args.key, suffix)

    sys.stdout.write(str(result))


def create(args):
    """perform create action"""

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    uid = uuid.uuid1()
    suffix = str(uid)

    client = EpicClient(credentials)
    extype = None
    if args.extratype is not None:
        extype = args.extratype.split(';')
    if args.loc10320 is not None:
        l10320 = args.loc10320.split(';')
    else:
        l10320 = None
    result = client.createHandle(credentials.prefix, args.location,
                                 args.checksum, extype, l10320, suffix)

    if result is None:
        sys.stdout.write("error")
    else:
        sys.stdout.write(result)


def modify(args):
    """perform modify action"""

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    client = EpicClient(credentials)
    prefix = args.handle.partition("/")[0]
    suffix = args.handle.partition("/")[2]
    if args.key == "10320/LOC" and args.oldvalue:
        result = client.updateLocationInHandle(prefix, args.oldvalue,
                                               args.value, suffix)
    else:
        result = client.modifyHandle(prefix, args.key, args.value, suffix)

    sys.stdout.write(str(result))


def delete(args):
    """perform delete action"""

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    client = EpicClient(credentials)
    prefix = args.handle.partition("/")[0]
    suffix = args.handle.partition("/")[2]
    result = client.deleteHandle(prefix, args.key, suffix)

    sys.stdout.write(str(result))


def relation(args):
    """perform the relation action"""

    credentials = Credentials(args.credstore, args.credpath)
    credentials.parse()

    client = EpicClient(credentials)
    result = client.updateHandleWithLocation(args.ppid, args.cpid)
    sys.stdout.write(str(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='EUDAT EPIC client API. '
                                                 'Supports reading, querying,'
                                                 ' creating, modifying and '
                                                 'deleting handle records.')
    parser.add_argument("credstore", choices=['os', 'irods'], default="NULL",
                        help="the used credential storage "
                             "(os=filespace, irods=iRODS storage)")
    parser.add_argument("credpath", default="NULL",
                        help="path to the credentials")

    subparsers = parser.add_subparsers(title='Actions',
                                       description='Handle record management'
                                                   'actions',
                                       help='additional help')

    parser_replaceHash = subparsers.add_parser('replaceHash', help='')
    parser_replaceHash.add_argument("a", nargs='+', help="")
    parser_replaceHash.set_defaults(func=replaceHash)

    parser_create = subparsers.add_parser('create',
                                          help='creating handle records')
    parser_create.add_argument("location", help="location to store in "
                                                "the new handle record")
    parser_create.add_argument("--checksum", help="checksum to store in "
                                                  "the new handle record")
    parser_create.add_argument("--extratype", help="Extension create fields \
                               EUDAT/ROR and EUDAT/PPID \
                               in format: \"EUDAT/ROR=xyz;EUDAT/PPID=abc\"")
    parser_create.add_argument("--loc10320", help="Extension field 10320/LOC \
                               in format: \"location1;location2;location3\"")
    parser_create.set_defaults(func=create)

    parser_modify = subparsers.add_parser('modify',
                                          help='modifying handle records')
    parser_modify.add_argument("handle", help="the handle value")
    parser_modify.add_argument("key", help="the key of the field to change "
                                           "in the pid record")
    parser_modify.add_argument("oldvalue", nargs='?', help="OPTIONAL: the old \
                                value to replace in the pid record identified \
                                with the supplied key. Only needed with \
                                10320/LOC key")
    parser_modify.add_argument("value", help="the new value to store "
                                             "in the pid record identified "
                                             "with the supplied key")
    parser_modify.set_defaults(func=modify)

    parser_delete = subparsers.add_parser('delete',
                                          help='Deleting handle records or '
                                               'handle field')
    parser_delete.add_argument("handle",
                               help="the handle value of the digital object "
                                    "instance to delete")
    parser_delete.add_argument("--key",
                               help="the key-field of handle, field == '' in "
                                    "case delete complete handle ")
    parser_delete.set_defaults(func=delete)

    parser_read = subparsers.add_parser('read', help='Read handle record')
    parser_read.add_argument("handle", help="the handle value")
    parser_read.add_argument("--key", help="only read this key instead of "
                                           "the full handle record")
    parser_read.set_defaults(func=read)

    parser_search = subparsers.add_parser('search',
                                          help='Search for handle records')
    parser_search.add_argument("key", choices=['URL', 'CHECKSUM'],
                               help="the key to search")
    parser_search.add_argument("value", nargs='+', help="the value to search")
    parser_search.set_defaults(func=search)

    parser_relation = subparsers.add_parser('relation',
                                            help='Add a (parent,child) '
                                                 'relationship between '
                                                 'the specified handle '
                                                 'records')
    parser_relation.add_argument("ppid", help="parent handle value")
    parser_relation.add_argument("cpid", help="child handle value")
    parser_relation.set_defaults(func=relation)

    _args = parser.parse_args()
    _args.func(_args)
