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

simplejson is needed only if your python stdlib does not include json
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
from defusedxml import minidom
from lxml import etree
from lxml.etree import tostring
import base64
import uuid
import argparse
import sys
import logging
try:
    import simplejson as json
except ImportError:
    import json


# ##############################################################################
# Epic Client Class #
# ##############################################################################


class EpicClient(object):
    """Class implementing an EPIC client."""

    def __init__(self, cred):
        """Initialize object with connection parameters."""

        self.cred = cred
        self.debug = cred.debug
        self.http = httplib2.Http(disable_ssl_certificate_validation=False)
        self.http.add_credentials(cred.username, cred.password)
        # do not throw exceptions for connection errors
        self.http.force_exception_to_status_code = True

    # def _debugmsg(self, method, msg):
    #    """Internal: Print a debug message if debug is enabled."""

    #    if self.debug:
    #        print "[", method, "]", msg

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
            logging.debug('[_getheader] %s ACTION is unknown' % str(action))

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
                logging.debug('[checkresponsecode] .....')
                logging.debug('[%s] %s %s' % (str(method), item["info"],
                                              str(statuscode)))
                output = item["output"]
                if output is "None":
                    return None
                elif output is "False":
                    return False
                else:
                    return True
        logging.error('Processing fails with statuscode = %s' % str(statuscode))
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
        logging.debug('[searchHandle] URI %s' % uri)
        hdrs = self._getheader("SEARCH")
        response, content = self.http.request(uri, method='GET', headers=hdrs)
        output = True
        output = self._checkresponsecode("searchHandle", response.status)
        if not output or output is None or not content:
            # if not content:
            return None
        else:
            handle = json.loads(content)
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
        logging.debug('[retrieveHandle] URI %s' % uri)
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
        handle = json.loads(jsonhandle)
        for item in handle:
            if 'type' in item and item['type'] == key:
                logging.debug('[getValueFromHandle] Found key %s value=%s'
                              % (key, str(item['parsed_data'])))
                return str(item['parsed_data'])

        logging.debug('[getValueFromHandle] Value for key %s not found' % key)
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
        logging.debug('[createHandle] PREFIX = %s' % prefix)
        logging.debug('[createHandle] SUFFIX = %s' % suffix)
        uri = self._geturi(prefix, '', '', suffix)
        logging.debug('[createHandleWithLocation] URI %s' % uri)
        hdrs = self._getheader("CREATE")

        idn = 0
        root = etree.Element('locations')

        handle_array = [{'type': 'URL', 'parsed_data': location}]
        if l10320 is not None:
            # loc10320 = ('<locations><location id="0" href="' + str(location) +
            #            '" /></locations>')
            for item in l10320:
                etree.SubElement(root, 'location', id=str(idn), href=str(item))
                idn += 1
            loc10320 = tostring(root)
            handle_array.append({'type': '10320/LOC', 'parsed_data': loc10320})
        if ((checksum) and (checksum is not None)):
            handle_array.append({'type': 'CHECKSUM', 'parsed_data': checksum})
        if ((extratype) and (extratype is not None)):
            for key_value in extratype:
                key = key_value.split('=')[0]
                value = key_value.split('=')[1]
                # replace "EUDAT/ROR=pid" with "EUDAT/ROR=handle"
                if key == 'EUDAT/ROR' and value.lower() == 'pid':
                    if uri.startswith(self.cred.baseuri):
                       handle = uri[len(self.cred.baseuri):len(uri)]
                    elif uri.startswith(self.cred.baseuri + '/'):
                       handle = uri[len(self.cred.baseuri + '/'):len(uri)]
                    value = handle
                if (next((item for item in handle_array if item['type'] == key),
                         None) is None):
                    handle_array.append({'type': key, 'parsed_data': value})

        new_handle_json = json.dumps(handle_array)

        response, _ = self.http.request(uri, method='PUT', headers=hdrs,
                                        body=new_handle_json)
        output = True
        output = self._checkresponsecode("createHandle", response.status)
        if not output or output is None:
            logging.debug('[createHandleWithLocation] Body json: %s'
                          % new_handle_json)
            return None
        else:
            # make sure to only return the handle and strip off the baseuri
            # if it is included
            hdl = response['location']
            logging.debug('[hdl] %s' % hdl)
            if hdl.startswith(self.cred.baseuri):
                hdl = hdl[len(self.cred.baseuri):len(hdl)]
            elif hdl.startswith(self.cred.baseuri + '/'):
                hdl = hdl[len(self.cred.baseuri + '/'):len(hdl)]
                logging.debug('[final hdl] %s' % hdl)

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
        logging.debug('[modifyHandle] URI %s' % uri)

        hdrs = self._getheader("UPDATE")

        handle_json = self.retrieveHandle(prefix, suffix)
        if not handle_json:
            logging.debug('[modifyHandle] Cannot modify an unexisting handle: %s'
                          % uri)
            return False

        handle = json.loads(handle_json)

        keyfound = False

        if (value is None) or (value is '') or (value is ""):
            for item in handle:
                if 'type' in item and item['type'] == key:
                    logging.debug('[modifyHandle] Remove item %s' % key)
                    del item['data']
                    del item['parsed_data']
                    break
        else:
            for item in handle:
                if 'type' in item and item['type'] == key:
                    keyfound = True
                    logging.debug('[modifyHandle] Found key %s value=%s'
                                  % (key, str(item['parsed_data'])))
                    item['parsed_data'] = value
                    del item['data']
                    break

            if keyfound is False:
                logging.debug('[modifyHandle] Value of keyfound is false, '
                              'create new key')
                logging.debug('[modifyHandle] Key %s created. Generating new hash'
                              % key)
                handleitem = {'type': key, 'parsed_data': value}
                handle[len(handle):] = [handleitem]

        handle_json = json.dumps(handle)
        logging.debug('[modifyHandle] JSON: %s' % str(handle_json))

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
            logging.debug('[deleteHandle] "DELETE Handle %s/%s of URI %s'
                          % (prefix, suffix, uri))
            response, _ = self.http.request(uri, method='DELETE',
                                            headers=hdrs)
        else:
            logging.debug('[deleteHandle] "DELETE field %s of URI %s'
                          % (key, uri))
            handle_json = self.retrieveHandle(prefix, suffix)
            if not handle_json:
                logging.debug('[deleteHandle] Cannot modify an unexisting '
                              'handle: %s' % uri)
                return False
            keyfound = False
            handle = json.loads(handle_json)

            for item in handle:
                if 'type' in item and item['type'] == key:
                    keyfound = True
                    logging.debug('[deleteHandle] Found key %s value=%s'
                                  % (key, str(item['parsed_data'])))
                    logging.debug("[deleteHandle] Remove Key's Field")
                    del handle[handle.index(item)]
                    break

            if keyfound is False:
                logging.debug('[deleteHandle] No Value of key is found. '
                              'Quiting....')
                return False
            else:
                hdrs = self._getheader("UPDATE")
                handle_json = json.dumps(handle)
                logging.debug('[deleteHandle] JSON: %s' % str(handle_json))
                response, _ = self.http.request(uri, method='PUT', headers=hdrs,
                                                body=handle_json)

        output = self._checkresponsecode("deleteHandle", response.status)
        logging.debug('[deleteHandle] OUTPUT = %s' % str(output))
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
        logging.debug('[updateHandleWithLocation] Found 10320/LOC: %s'
                      % str(loc10320))
        if loc10320 is None:
            loc10320 = ('<locations><location id="0" href="' + value +
                        '" /></locations>')
            response = self.modifyHandle(prefix, "10320/LOC", loc10320, suffix)
            if not response:
                logging.debug('[updateHandleWithLocation] Cannot update handle:'
                              ' %s with location: %s' % (uri, value))
                return False
        else:
            lt = LocationType(loc10320)
            response = lt.checkInclusion(value)
            if response:
                logging.debug('[updateHandleWithLocation] The location %s is '
                              'already included!' % value)
            else:
                resp, content = lt.addLocation(value)
                if not resp:
                    logging.debug('[updateHandleWithLocation] The location %s '
                                  ' cannot be added' % value)
                else:
                    if not self.modifyHandle(prefix, "10320/LOC",
                                             content, suffix):
                        logging.debug('[updateHandleWithLocation] Cannot update'
                                      ' handle: %s with location: %s'
                                      % (uri, value))
                    else:
                        logging.debug('[updateHandleWithLocation] Location added')
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
            logging.debug('[removeLocationFromHandle] Cannot remove location: '
                          '%s from handle: %s, the field 10320/LOC does not '
                          'exists' % (value, uri))
            return False
        else:
            lt = LocationType(loc10320)
            if not lt.checkInclusion(value):
                logging.debug('[removeLocationFromHandle] The location %s '
                              'is not included!' % value)
                return False
            else:
                response, content = lt.removeLocation(value)
                if response:
                    if self.modifyHandle(prefix, "10320/LOC", content, suffix):
                        return True

                logging.debug('[removeLocationFromHandle] The location %s '
                              'cannot be removed' % value)
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
            logging.debug('[updateLocationInHandle] Cannot update location: '
                          '%s from handle: %s, the field 10320/LOC does not exists'
                          % (oldvalue, uri))
            return False
        else:
            lt = LocationType(loc10320)
            if not lt.checkInclusion(oldvalue):
                logging.debug('[updateLocationInHandle] The location '
                              '%s is not included!' % oldvalue)
                return False
            else:
                response, content = lt.updateLocation(oldvalue, newvalue)
                if response:
                    if self.modifyHandle(prefix, "10320/LOC", content, suffix):
                        return True

                logging.debug('[removeLocationFromHandle] The location '
                              '%s cannot be updated' % oldvalue)
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

    def __init__(self, field):
        self.domfield = minidom.parseString(field)
        # self.debug = debug

    #  def _debugmsg(self, method, msg):
    #    """Internal: Print a debug message if debug is enabled."""

    #    logging.debug("[%s] %s" % (method, msg))

    def isEmpty(self):
        """Check if the 10320/LOC handle type field is empty.

        Parameters:
        Returns True and 0 if empty,
        False and the number of locations otherwise.

        """

        locations = self.domfield.getElementsByTagName("location")
        if locations.length == 0:
            logging.debug('[isEmpty] The 10320/LOC field is empty')
            return True, 0
        logging.debug('[isEmpty] The 10320/LOC field contains %s locations'
                      % str(locations.length))
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
                logging.debug('[checkInclusion] The location (%s) is included'
                              % loc)
                return True

        logging.debug('[checkInclusion] The location (%s) is not included'
                      % loc)
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
                logging.debug('[removeLocation] Removed location: %s' % loc)
                return True, main.toxml()

        logging.debug('[removeLocation] Cannot remove location: %s' % loc)
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
            logging.debug('[addLocation] Added new location: %s' % loc)
            return True, main.toxml()
        except TypeError:
            logging.debug('[addLocation] An XML TypeError occurred '
                          'adding the new location: %s' % loc)
            return False, None
        except AttributeError:
            logging.debug('[addLocation] An XML AttributeError occurred '
                          'adding the new location: %s' % loc)
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
                logging.debug('[updateLocation] Updated location: %s with %s'
                              % (oldloc, newloc))
                return True, main.toxml()

        logging.debug('[updateLocation] Cannot update location: %s' % oldloc)
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
                logging.error("Failed to open %s: %s" % (self.filename,
                                                         err.strerror))
                sys.exit(-1)

            with filehandle:
                tmp = json.loads(filehandle.read())

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
                    logging.basicConfig(level=logging.DEBUG)
                else:
                    logging.basicConfig(level=logging.INFO)
            except KeyError:
                logging.error("Missing key-value-pair in credentials file")
                sys.exit(-1)

        elif self.store == "irods":
            logging.info("Function getting credential store in iRODS is in "
                         "testing ...")
            # FIXME: is there better way to exit ?.
            sys.exit(-1)
        else:
            logging.error("Invalid store '%s', aborting" % self.store)
            sys.exit(-1)

        logging.debug("credentials from %s:%s %s %s %s" %
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
    parser.add_argument("-d", "--debug", default=False, action="store_true",
                        help="Display debug messages")

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

    if _args.debug:
        logging.basicConfig(level=logging.DEBUG)

    _args.func(_args)
