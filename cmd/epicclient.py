#!/usr/bin/env python

import httplib2
import simplejson
from xml.dom import minidom, Node
"""
httpib2
download from http://code.google.com/p/httplib2
python setup.py install

simplejson
download from http://pypi.python.org/pypi/simplejson/
python setup.py install

ubuntu: apt-get install python-httplib2 python-simplejson

"""

"""
    get credentials from different storages, right now irods or filesystem
    
    Please store credentials in the following format, otherwise there are problems...
    {
    "baseuri": "https://epic.sara.nl/epic1/", 
    "username": "XXX",
    "password": "YYYYYYYY",
    "accept_format": "application/json"
    }

"""
def credential_parser(store, file, debug):

    baseuri = 'https://epic.sara.nl/epic1/'
    username = 'XXX'
    password = 'YYYYYY'
    accept_format = 'application/json'

    if ((store!="os" and store!="irods") or file =="NULL"):
        if debug: print "credential store or path not given/valid, using:%s %s %s" % (baseuri,username,accept_format)
        return [baseuri,username,password,accept_format]
    
    if store=="os":
        try:
            filehandle=open(file,"r")
            tmp=eval(filehandle.read())
            filehandle.close()
            baseuri=tmp['baseuri']
            username=tmp['username']
            password=tmp['password']
            accept_format=tmp['accept_format']
            if debug: print "credentials from filespace:%s %s %s" % (baseuri,username,accept_format)
        except Exception, e:
            print "problem while getting credentials from filespace"
            print "Error:", e
    elif store=="irods":
        try:
            from irods import getRodsEnv,rcConnect,clientLogin,iRodsOpen
            myEnv, status = getRodsEnv()
            conn, errMsg = rcConnect(myEnv.getRodsHost(), myEnv.getRodsPort(), myEnv.getRodsUserName(), myEnv.getRodsZone())
            if debug: print myEnv.getRodsHost(), myEnv.getRodsPort(), myEnv.getRodsUserName(), myEnv.getRodsZone()
            status = clientLogin(conn)
            test = iRodsOpen(conn, file, 'r')
            
            tmp = eval(test.read())    
            test.close()
            conn.disconnect()
            
            baseuri=tmp['baseuri']
            username=tmp['username']
            password=tmp['password']
            accept_format=tmp['accept_format']
            if debug: print "credentials from irods:%s %s %s" % (baseuri,username,accept_format)
        except Exception, e:
            print "problem while getting credentials from irods"
    else:
        print "this should not happen..."
        
    return [baseuri,username,password,accept_format]



class EpicClient():
    """Class implementing an EPIC client."""
    
    
    def __init__(self, baseuri, username, password, accept_format=None,debug=False):
	"""Initialize object with connection parameters."""
	
	self.baseuri = baseuri
	self.username = username
	self.password = password
	self.accept_format = accept_format
	self.debug = debug
	self.http = httplib2.Http(disable_ssl_certificate_validation=True)
	self.http.add_credentials(username, password)
	
	
    def _debugMsg(self,method,msg):
	"""Internal: Print a debug message if debug is enabled."""
	
	if self.debug: print "[",method,"]",msg

    
    # Public methods
	    
    def searchHandle(self,prefix,url):
        """Search for handles containing the specified URL.
	
	Parameters:
	prefix: URI to the resource, or the prefix if suffix is not ''.
	url: The URL to search for.
	Returns the searched data field, or None if not found.
	
	"""
        if self.baseuri.endswith('/'):
            uri = self.baseuri + prefix + '/?URL='+url
        else:
            uri = self.baseuri + '/' + prefix + '/?URL='+url
		
	self._debugMsg('searchHandle',"URI " + uri)
	
	hdrs = None
	if self.accept_format: hdrs = {'Accept': self.accept_format}
	try:
	    response, content = self.http.request(uri,method='GET',headers=hdrs)
	except:
	    self._debugMsg('searchHandle', "An Exception occurred during request")
	    return None
	else:
	    self._debugMsg('searchHandle', "Request completed")
	    
	if response.status != 200:
	    self._debugMsg('searchHandle', "Response status: "+str(response.status))
	    return None

        if not content: return None
	handle = simplejson.loads(content)
        if not handle:
            return 'empty'
        
        """
        make sure to only return the handle and strip off the baseuri if it is included
        """
        hdl = handle[0]
        if hdl.startswith(self.baseuri):
            return hdl[len(self.baseuri):len(hdl)]
        elif hdl.startswith(self.baseuri + '/'):
            return hdl[len(self.baseuri + '/'):len(hdl)]
	return prefix + '/' + hdl

    def retrieveHandle(self,prefix,suffix=''):
	"""Retrieve a handle from the PID service. 
	
	Parameters:
	prefix: URI to the resource, or the prefix if suffix is not ''.
	suffix: The suffix of the handle. Default: ''.
	Returns the content of the handle in JSON, None on error.
	
	"""
	if self.baseuri.endswith('/'):
            uri = self.baseuri + prefix
        else:
            uri = self.baseuri + '/' + prefix
	if suffix != '': uri += "/" + suffix
	
	self._debugMsg('retrieveHandle',"URI " + uri)
	hdrs = None
	if self.accept_format: hdrs = {'Accept': self.accept_format}
	try:
	    response, content = self.http.request(uri,method='GET',headers=hdrs)
	except:
	    self._debugMsg('retrieveHandle', "An Exception occurred during request")
	    return None
	else:
	    self._debugMsg('retrieveHandle', "Request completed")
	    
	if response.status != 200:
	    self._debugMsg('retrieveHandle', "Response status: "+str(response.status))
	    return None
	return content

	
    def getValueFromHandle(self,prefix,key,suffix=''):
	"""Retrieve a value from a handle.
	
	Parameters:
	prefix: URI to the resource, or the prefix if suffix is not ''.
	key: The key to search (in type parameter).
	suffix: The suffix of the handle. Default: ''.
	Returns the searched data field, or None if not found.
	
	"""
	
	jsonhandle = self.retrieveHandle(prefix,suffix)
	if not jsonhandle: return None
	handle = simplejson.loads(jsonhandle)
	KeyFound = False
	Value =''
	for item in handle:
	   if 'type' in item and item['type']==key:
		KeyFound = True
		self._debugMsg('getValueFromHandle', "Found key " + key + " value=" + str(item['parsed_data']) )
		Value=str(item['parsed_data'])
		break;

	if KeyFound is False:
	    self._debugMsg('getValueFromHandle', "Value for key " + key + " not found")
	    return None
	else:
	    
	    self._debugMsg('getValueFromHandle', "Found value for key " + key )
	    return Value
	
	
    def createHandle(self,prefix,location,checksum=None,suffix=''):
	"""Create a new handle for a file.
	
	Parameters:
	prefix: URI to the resource, or the prefix if suffix is not ''.
	location: The location (URL) of the file.
	checksum: Optional parameter, store the checksum of the file as well.
	suffix: The suffix of the handle. Default: ''.
	Returns the URI of the new handle, None if an error occurred.
	
	"""
	
        if self.baseuri.endswith('/'):
            uri = self.baseuri + prefix
        else:
            uri = self.baseuri + '/' + prefix

	if suffix != '': uri += "/" + suffix
	self._debugMsg('createHandleWithLocation',"URI " + uri)
	hdrs = {'If-None-Match': '*','Content-Type':'application/json'}

	if checksum:
	    new_handle_json = simplejson.dumps([{'type':'URL','parsed_data':location}, {'type':'CHECKSUM','parsed_data': checksum}])
	else:
	    new_handle_json = simplejson.dumps([{'type':'URL','parsed_data':location}])

	    
	try:
	    response, content = self.http.request(uri,method='PUT',headers=hdrs,body=new_handle_json)
	except:
	    self._debugMsg('createHandleWithLocation', "An Exception occurred during Creation of " + uri)
	    return None
	else:
	    self._debugMsg('createHandleWithLocation', "Request completed")
	    
	if response.status != 201:
	    self._debugMsg('createHandleWithLocation', "Not Created: Response status: "+str(response.status))
	    return None
	
        """
        make sure to only return the handle and strip off the baseuri if it is included
        """
        hdl = response['location']
	self._debugMsg('hdl', hdl)
        if hdl.startswith(self.baseuri):
            return hdl[len(self.baseuri):len(hdl)]
        elif hdl.startswith(self.baseuri + '/'):
            return hdl[len(self.baseuri + '/'):len(hdl)]
   	
    	self._debugMsg('final hdl', hdl)
	return hdl
	
	
    def modifyHandle(self,prefix,key,value,suffix=''):
	"""Modify a parameter of a handle
	
	Parameters:
	prefix: URI to the resource, or the prefix if suffix is not ''.
	key: The parameter "type" wanted to change
	value: New value to store in "data"
	suffix: The suffix of the handle. Default: ''.
	Returns True if modified or parameter not found, False otherwise.
	
	"""

        if prefix.startswith(self.baseuri): 
	    prefix = prefix[len(self.baseuri):] 
	
        if self.baseuri.endswith('/'):
            uri = self.baseuri + prefix
        else:
            uri = self.baseuri + '/' + prefix

	if suffix != '': uri += "/" + suffix
	
	self._debugMsg('modifyHandle',"URI " + uri)
	hdrs = {'Content-Type' : 'application/json'}
	
	if not key: return False
	

	handle_json = self.retrieveHandle(prefix,suffix)
	if not handle_json: 
	    self._debugMsg('modifyHandle', "Cannot modify an unexisting handle: " + uri)
	    return False
	    
	handle = simplejson.loads(handle_json)
	KeyFound = False
	for item in handle:
	   if 'type' in item and item['type']==key:
		KeyFound = True
		self._debugMsg('modifyHandle', "Found key " + key + " value=" + str(item['parsed_data']) )
		if value is None:
		    del(item)
		else:
		   item['parsed_data']=value
		   del item['data']
		break;

	if KeyFound is False:
	    if value is None:
		self._debugMsg('modifyHandle', "No value for Key " + key + " . Quiting")
		return True
	 		    
	    self._debugMsg('modifyHandle', "Key " + key + " not found. Generating new hash")
	    handleItem={'type': key, 'parsed_data' : value}
	    handle.append(handleItem)
			
	handle_json = simplejson.dumps(handle)
	self._debugMsg('modifyHandle', "JSON: " + str(handle_json))    
	
	try:
	    response, content = self.http.request(uri,method='PUT',headers=hdrs,body=handle_json)
	except:
	    self._debugMsg('modifyHandle', "An Exception occurred during Creation of " + uri)
	    return False
	else:
	    self._debugMsg('modifyHandle', "Request completed")
		    
	if response.status < 200 and response.status >= 300:
	    self._debugMsg('modifyHandle', "Not Modified: Response status: "+str(response.status))
	    return False
	    
	return True
	
	
    def deleteHandle(self,prefix,suffix=''):
	"""Delete a handle from the server.
	
	Parameters:
	prefix: URI to the resource, or the prefix if suffix is not ''.
	suffix: The suffix of the handle. Default: ''.
	Returns True if deleted, False otherwise.
	
	"""
	
	if self.baseuri.endswith('/'):
            uri = self.baseuri + prefix
        else:
            uri = self.baseuri + '/' + prefix

	if suffix != '': uri += "/" + suffix
	self._debugMsg('deleteHandle',"DELETE URI " + uri)
	
	try:
	    response, content = self.http.request(uri,method='DELETE')
	except:
	    self._debugMsg('deleteHandle', "An Exception iccurred during deletion of " + uri)
	    return False
	else:
	    self._debugMsg('deleteHandle', "Request completed")
	    
	if response.status < 200 and response.status >= 300:
	    self._debugMsg('deleteHandle', "Not Deleted: Response status: "+str(response.status))
	    return False
	    
	return True    


    def updateHandleWithLocation(self,prefix,value,suffix=''):
	"""Update the 10320/LOC handle type field of the handle record.
         
        Parameters:
        prefix: URI to the resource, or the prefix if suffix is not ''.
	value: New value to store in "10320/LOC"
        suffix: The suffix of the handle. Default: ''.
        Returns True if updated, False otherwise.
         
        """

	if self.baseuri.endswith('/'):
		uri = self.baseuri + prefix
	else:
	        uri = self.baseuri + '/' + prefix

	if suffix != '': uri += "/" + suffix

	loc10320 = self.getValueFromHandle(prefix,"10320/LOC",suffix)
	self._debugMsg('updateHandleWithLocation', "found 10320/LOC: " +str(loc10320))
	if loc10320 is None:
		loc10320 = '<locations><location id="0" href="'+value+'" /></locations>'
		response = self.modifyHandle(prefix,"10320/LOC",loc10320,suffix)
		if not response:
			self._debugMsg('updateHandleWithLocation', "Cannot update handle: " + uri \
					+ " with location: " + value)
             		return False
	else:
		lt = LocationType(loc10320,self.debug)
		response = lt.checkInclusion(value)
		if response:
			self._debugMsg('updateHandleWithLocation', "the location "+value+" is already included!")
		else:
			resp, content = lt.addLocation(value)
			if not resp: 
				self._debugMsg('updateHandleWithLocation', "the location "+value \
						+" cannot be added")
			else:
				if not self.modifyHandle(prefix,"10320/LOC",content,suffix):
				        self._debugMsg('updateHandleWithLocation', "Cannot update handle: " \
							+uri+ " with location: " + value)
				else:
					self._debugMsg('updateHandleWithLocation', "location added")
					return True
		return False 

	return True


    def removeLocationFromHandle(self,prefix,value,suffix=''):
        """Remove one of the 10320/LOC handle type values from the handle record.
	
	Parameters:
	prefix: URI to the resource, or the prefix if suffix is not ''.
	value: Value to be deleted from the "10320/LOC".
	suffix: The suffix of the handle. Default: ''.
	Returns True if removed, False otherwise.
	"""
	
	if self.baseuri.endswith('/'):
		uri = self.baseuri + prefix
	else:
	        uri = self.baseuri + '/' + prefix
	
	if suffix != '': uri += "/" + suffix

        loc10320 = self.getValueFromHandle(prefix,"10320/LOC",suffix)
        if loc10320 is None:
		self._debugMsg('removeLocationFromHandle', "Cannot remove location: " +value \
		                + " from handle: " +uri+ ", the field 10320/LOC does not exists")
		return False
	else:
	        lt = LocationType(loc10320,self.debug)
		if not lt.checkInclusion(value):
			self._debugMsg('removeLocationFromHandle', "the location "+value+" is not included!")
		else:
			response, content = lt.removeLocation(value)
		        if response:
				if self.modifyHandle(prefix,"10320/LOC",content,suffix):
					return True
			self._debugMsg('removeLocationFromHandle', "the location " +value \
			                + " cannot be removed")
		return False
			
	return True


class LocationType():
	"""Class implementing a 10320/LOC handle type."""
	# Expected format for 10320/LOC handle type:
	# <locations><location id="0" href="location" country="xx" weight="0" /></locations>


	def __init__(self,field,debug=False):
		self.domfield = minidom.parseString(field)
		self.debug = debug


	def _debugMsg(self,method,msg):
		"""Internal: Print a debug message if debug is enabled."""
		 
		if self.debug: print "[",method,"]",msg


	def isEmpty(self):
		"""Check if the 10320/LOC handle type field is empty.
			     
		Parameters:
	        Returns True and 0 if empty, False and the number of locations otherwise.
	        """

		locations = self.domfield.getElementsByTagName("location")
		if locations.length == 0: 
			self._debugMsg('isEmpty', "the 10320/LOC field is empty")
			return True, 0
		self._debugMsg('isEmpty', "the 10320/LOC field contains " +str(locations.length)+ " locations")
		return False, str(locations.length)


	def checkInclusion(self,loc):
		"""Check if a 10320/LOC handle type value is included.
                              
                Parameters:
		loc: The replica location PID value.
                Returns True if it is included, False otherwise.
                """

		locations = self.domfield.getElementsByTagName("location")
		for url in locations:
			if ( url.getAttribute('href') == loc ):
				self._debugMsg('checkInclusion', "the location (" +loc+ ") is included")
				return True
		self._debugMsg('checkInclusion', "the location (" +loc+ ") is not included")
		return False


	def removeLocation(self,loc):
		"""Remove a replica PID from the 10320/LOC handle type field.
		                              
		Parameters:
		loc: The replica location PID value.
		Returns True and the 10320/LOC handle type field itself if the value is removed, False and None otherwise.
                """

		main = self.domfield.childNodes[0]
		locations = self.domfield.getElementsByTagName("location")
		for url in locations:
			if ( url.getAttribute('href') == loc ):
				main.removeChild(url)
				self._debugMsg('removeLocation', "removed location: " +loc)
				return True, main.toxml()
		self._debugMsg('removeLocation', "cannot remove location: " +loc)
		return False, None
	

	def addLocation(self,loc):
		"""Add a replica PID to the 10320/LOC handle type field.
                              
                Parameters:
                loc: The replica location PID value.
                Returns True and the 10320/LOC handle type field itself if the value is added, False and None otherwise.
                """

		try:
			newurl = self.domfield.createElement("location")
			response, content = self.isEmpty()
			newurl.setAttribute('id', content)
			newurl.setAttribute('href', loc)
			self.domfield.childNodes[0].appendChild(newurl)
			main = self.domfield.childNodes[0]
			self._debugMsg('addLocation', "added new location: " +loc)
			return True, main.toxml()
		except:
			self._debugMsg('addLocation', "an exception occurred, adding the new location: " +loc)
			return False, None


############################################

# Examples using EpicClient

if __name__ == "__main__":

    baseuri = 'https://epic.sara.nl/epic1/'
    username = 'XXX'
    password = 'YYYYYY'
    accept_format = 'application/json'
    
    debug_enabled = False
    
    prefix=username

    ec = EpicClient(baseuri,username,password,accept_format,debug=debug_enabled)
    
    """
    print ec.createHandle(prefix + "/07cc0858-edb9-11e1-a27d-005056ae635a","/vzMPI/home/mpi-eudat/test.txt")

    """
    print ""
    print "Retrieving handle by url"
    print ec.searchHandle(prefix, "/vzMPI-REPLIX/bin/test.txt")

    print ""
    print "Retrieving handle info from " + prefix + "/TESTHANDLE"
    print ec.retrieveHandle(prefix,"TESTHANDLE")

    print ""
    print "Retrieving handle info from " + prefix + "/NONEXISTING (should be None)"
    print ec.retrieveHandle(prefix,"NONEXISTING")
    
    print ""
    print "Retrieving Value of EMAIL from " + prefix + "/TESTHANDLE"
    print ec.getValueFromHandle("" + prefix +"/TESTHANDLE","EMAIL")
    
    print ""
    print "Retrieving Value of FOO from " + prefix + "/TESTHANDLE (should be None)"
    print ec.getValueFromHandle(prefix,"FOO","TESTHANDLE")
    
    print ""
    print "Retrieving Value of FOO from " + prefix + "/NONEXISTING (should be None)"
    print ec.getValueFromHandle(prefix,"FOO","NONEXISTING")
    
    print ""
    print "Creating handle " + prefix + "/TEST_CR1 (should be True)"
    print ec.createHandle(prefix + "/TEST_CR1","http://www.bsc.es") #,"335f4dea94ef48c644a3f708283f9c54"
    
    print ""
    print "Retrieving handle info from " + prefix + "/TEST_CR1"
    print ec.retrieveHandle(prefix +"/TEST_CR1")
    
    print ""
    print "Modifying handle info from " + prefix + "/TEST_CR1 (should be True)"
    print ec.modifyHandle(prefix +"/TEST_CR1","uri","http://www.bsc.es/FY")
    
    print ""
    print "Adding new info to " + prefix + "/TEST_CR1 (should be True)"
    print ec.modifyHandle(prefix + "/TEST_CR1","EMAIL","xavi.abellan@bsc.es")    

    print ""
    print "Updating handle info with a new 10320/loc type location 846/157c344a-0179-11e2-9511-00215ec779a8"
    print "(should be True)"
    print ec.updateHandleWithLocation(prefix + "/TEST_CR1","846/157c344a-0179-11e2-9511-00215ec779a8")

    print ""
    print "Updating handle info with a new 10320/loc type location 846/157c344a-0179-11e2-9511-00215ec779a9"
    print "(should be True)"
    print ec.updateHandleWithLocation(prefix + "/TEST_CR1","846/157c344a-0179-11e2-9511-00215ec779a9")
    
    print ""
    print "Retrieving handle info from " + prefix + "/TEST_CR1"
    print ec.retrieveHandle(prefix + "/TEST_CR1")
    
    print ""
    print "Deleting EMAIL parameter from " + prefix + "/TEST_CR1 (should be True)"
    print ec.modifyHandle(prefix + "/TEST_CR1","EMAIL",None)  

    print ""
    print "Updating handle info with a new 10320/loc type location 846/157c344a-0179-11e2-9511-00215ec779a8"
    print "(should be False)"
    print ec.updateHandleWithLocation(prefix + "/TEST_CR1","846/157c344a-0179-11e2-9511-00215ec779a8")

    print ""
    print "Removing 10320/loc type location 846/157c344a-0179-11e2-9511-00215ec779a8"
    print "(should be True)"
    print ec.removeLocationFromHandle(prefix + "/TEST_CR1","846/157c344a-0179-11e2-9511-00215ec779a8")

    print ""
    print "Removing 10320/loc type location 846/157c344a-0179-11e2-9511-00215ec779a8"
    print "(should be False)"
    print ec.removeLocationFromHandle(prefix + "/TEST_CR1","846/157c344a-0179-11e2-9511-00215ec779a8")
    
    print ""
    print "Retrieving handle info from " + prefix + "/TEST_CR1"
    print ec.retrieveHandle(prefix + "/TEST_CR1")
    
    print ""
    print "Deleting " + prefix + "/TEST_CR1 (should be True)"
    print ec.deleteHandle(prefix + "/TEST_CR1")  
    
    print ""
    print "Deleting (again) " + prefix + "/TEST_CR1 (should be False)"
    print ec.deleteHandle(prefix + "/TEST_CR1")  
    
    print ""
    print "Retrieving handle info from non existing " + prefix + "/TEST_CR1 (should be None)"
    print ec.retrieveHandle(prefix + "/TEST_CR1")     
