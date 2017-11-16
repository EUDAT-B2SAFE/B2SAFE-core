# !/usr/bin/env python


##################################
# Michal Jankowski PSNC
# EUDAT-PRACE integration
# 03.2017
##################################

import requests
import ConfigParser
import traceback
from requests.utils import quote
from utilities.password_file import *

class UnityApiException(Exception):
	'''Base class for Unity API exceptions
	'''
	def __init__(self, message):
		super(UnityApiException, self).__init__('UNITY API exception. ' + message)

class UnityApiInitException(UnityApiException):
	'''Class for Unity API initialization exception
	'''
	def __init__(self, message):
		super(UnityApiInitException, self).__init__('UNITY API initialization. ' + message)

class UnityApiStatusException(UnityApiException):
	'''Class for Unity API call incorrect status exception
	'''

	def __init__(self, message, status):
		self.status = status
		super(UnityApiStatusException, self).__init__(message + ' responded with status ' + str(status) + '.')


class UnityApi:
	'''Class to access Unity API
	
		Attributes: 
			logger : the logger object
			url : the base url
			auth : the authentication object
			verify : path to CA boundle or directory or False if the verification shall be skipped
	  
	'''

	def __init__(self, conf, confSection='B2ACCESS', parentLogger=None):
		'''Initialization
			Args: 
				conf : config parser object
				confSection : section in the parser regarding Unity connection
				parentLogger : the parent logger object
		'''
		
		try:
			#initialize logger
			if (parentLogger): 
				self.logger = parentLogger.getChild(__name__)
			else: 
				self.logger = logging.getLogger(__name__)

			#set host
			self.url=conf.get(confSection,'base_url')
		
			#set authentication
			#	only username-password auth is supported at the moment
			self.auth=(conf.get(confSection,'username'), PasswordFile(conf.get(confSection,'password_file')).password)
		
			#set verification option
			verify=None
			if conf.has_option(confSection,'cert_verify') :
				verify = conf.get(confSection,'cert_verify')
			if verify is None:
				self.verify=False
				self.logger.warning('Initializing UnityApi: server certificate verification will be skipped.')
			else:
				self.verify=verify
			

		except ConfigParser.Error, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			raise UnityApiInitException('Configuration error.')
			
		except IOError, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			raise UnityApiInitException('Cannot read password file '+conf.get(confSection,'password_file')+'.')


	def __repr__(self):
		return "<EUnityApi {url} >".format(**vars(self))

	def _get(self, path, params=None, ignoreNotExist=True):
		''' Performs GET on given url/path
		Args: 
		   path : the path relative to the url
		   params : the quuery parameters
		Returns:
		   tuple: object containing deserialized JSON returned by API
		'''
		
		logStr='GET ' + self.url + path + ' params=' + str(params)
		try:
			self.logger.debug(logStr)
			response = requests.get(self.url + path, params=params, auth=self.auth, verify=self.verify)
			
			if response.status_code==200 :
				return response.json()
			elif ignoreNotExist and response.status_code==400 :
				return None
			else :
				raise UnityApiStatusException(logStr, response.status_code)

		except requests.exceptions.RequestException as e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(logStr + ' caused exception: ' + str(e), exc_info=True)
			raise


	def _post(self, path, params=None, data=None, json=None, expectContent=False):
		''' Performs POST on given url/path
		Args: 
		   path : the path relative to the url
		   params : the quuery parameters 
		   data : the data to be posted (Dictionary, bytes, or file-like object)
		   json : the data to be posted (JSON)
		Returns:
		   object containing deserialized JSON returned by API if any
		'''
		
		logStr='POST ' + self.url + path + ' params=' + str(params)
		try:
			self.logger.debug(logStr)
			response = requests.post(self.url + path, params=params, auth=self.auth, verify=self.verify)
			
			if response.status_code==200 :
				return response.json()
			elif not expectContent and response.status_code==204:
				return None
			else :
				raise UnityApiStatusException(logStr, response.status_code)
			
		except requests.exceptions.RequestException as e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(logStr + ' caused exception: ' + str(e), exc_info=True)
			raise


	def _delete(self, path, params=None):
		''' Performs DELETE on given url/path
		Args: 
		   path : the path relative to the url
		   params : the parameters
		Returns:
		   object containing deserialized JSON returned by API
		'''
		
		logStr='DELETE '+ self.url + path + ' params=' + str(params)
		try:
			self.logger.debug(logStr)
			response = requests.delete(self.url + path, params=params, auth=self.auth, verify=self.verify)
			
			if response.status_code!=200 and response.status_code!=204:
				raise UnityApiStatusException(logStr, response.status_code)
	
		except requests.exceptions.RequestException as e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(logStr + ' caused exception: ' + str(e), exc_info=True)
			raise

	def getGroup(self, groupName='/'):
		''' Returns all members and subgroups of a given group.
		Args: 
		   groupName : name of the group, default is root
		Returns:
		   all members and subgroups of a given group
		'''
		self.logger.debug('getGroup ' + groupName)
		return self._get('group/' + quote(groupName,''))
		
	def createGroup(self, groupName):	
		''' Creates a new group. The created group will be empty.
		Args: 
		   groupName : name of the group
		Returns:
		   nothing
		'''
		self.logger.debug('createGroup ' + groupName)
		self._post('group/' + quote(groupName,''))
		
	def deleteGroup(self, groupName, recursive=False):
		''' Removes a given group.
		Args: 
		   groupName : name of the group
		   recursive : enforce recursive removal 
		Returns:
		   nothing
		'''
		self.logger.debug('deleteGroup ' + groupName)
		if recursive :
			self._delete('group/' + quote(groupName,''), params={'recursive':'on'})
		else :
			self._delete('group/' + quote(groupName,''))
			
		 
	def getEntity(self, entityId, identityType=None):
		''' Returns information about a given entity, including its status and all identities.
		Args: 
		   entityId : id of the entity
		   identityType : type of the identity
		Returns:
		   information about a given entity, including its status and all identities
		'''
		self.logger.debug('getEntity ' + entityId)
		path = 'entity/' + entityId
		
		if identityType!=None : 
			return self._get(path, {'identityType': identityType})
		else :
			return self._get(path)
			
		 
	def createEntity(self, identityType, identityValue, credentialRequirement):
		''' Creates a new entity, with the given initial identity and credential requirement. The new entity is in valid state.
		Args: 
		   identityType : type of the identity
		   identityValue : value of the given type
		   credentialRequirement : sys:CredentialRequirements
		Returns:
		   entity id
		'''
		self.logger.debug('createEntity ' + identityType + ' ' + identityValue + ' ' + credentialRequirement)
		path = 'entity/identity/' + identityType + '/' + identityValue
		
		result = self._post(path, params={'credentialRequirement': credentialRequirement}, expectContent=True)
		
		if result == None or 'entityId' not in result.keys() : return None;
		
		return str(result['entityId'])
		
		 
	def deleteEntity(self, entityId, identityType=None):
		''' Removes the given entity.
		Args: 
		   entityId : id of the entity
		   identityType : type of the identity
		Returns:
		   nothing
		'''
		self.logger.debug('deleteEntity ' + entityId)
		path = 'entity/' + entityId
		
		if identityType!=None : 
			return self._delete(path, {'identityType': identityType})
		else :
			return self._delete(path)		
			
		 
	def createIdentity(self, entityId, identityType, identityValue, selIdentityType=None):
		''' Creates a new entity, with the given initial identity and credential requirement. The new entity is in valid state.
		Args: 
		   entityId : id of the entity or value of selIdentityType
		   identityType : type of the identity to be created
		   identityValue : value of the given type
		   selIdentityType : type of the identity 
		Returns:
		   nothing
		'''
		self.logger.debug('createIdentity ' + entityId + ' ' + identityType + ' ' + identityValue + ' ' + str(selIdentityType))
		path = 'entity/' +entityId + '/identity/' + identityType + '/' + identityValue
		
		if selIdentityType is None :
			return self._post(path)
		else :
			return self._post(path, params={'identityType': selIdentityType})

					 
	def deleteIdentity(self, identityType, identityValue):
		''' Removes the given identity.
		Args: 
		   identityType : type of the identity
		   identityValue : value of the given type
		Returns:
		   nothing
		'''
		self.logger.debug('deleteIdentity ' + identityType + ' ' + identityValue)
		path = 'entity/identity/' + identityType + '/' + identityValue

		return self._delete(path)				
		 
	def resolve(self, identityType, identityValue):
		''' Resolves a provided identity of a given type.
		Args: 
		   identityType : type of the identity
		   identityValue : identity value
		Returns:
		   information about a given entity, including its status and all identities
		'''
		self.logger.debug('getResolve ' + identityType + ',' + identityValue)
		return self._get('resolve/' + identityType + '/' + identityValue)
			   
		 
	def getEntityGroups(self, entityId, identityType=None):
		''' Returns all groups the entity is member of.
		Args: 
		   entityId : id of the entity
		   identityType : type of the identity
		Returns:
		   all groups the entity
		'''
		self.logger.debug('getEntityGroups ' + entityId)
		path = 'entity/' + entityId + '/groups'
		if identityType!=None : 
			return self._get(path, {'identityType': identityType})
		else :
			return self._get(path)
		
		 
	def addEntityGroup(self, groupPath, entityId, identityType=None):
		''' Adds the entity to the group.
		Args: 
		   groupPath : group path
		   entityId : id of the entity
		   identityType : type of the identity
		Returns:
		   nothing
		'''
		self.logger.debug('addEntityGroup ' + entityId + ' ' + groupPath)
		path = 'group/' + quote(groupPath, '') + '/entity/' + entityId
		if identityType!=None : 
			return self._post(path, {'identityType': identityType})
		else :
			return self._post(path)

		 
	def deleteEntityGroup(self, groupPath, entityId, identityType=None):
		''' Deletes the entity from group.
		Args: 
		   groupPath : group path
		   entityId : id of the entity
		   identityType : type of the identity
		Returns:
		   nothing
		'''
		self.logger.debug('deleteEntityGroup ' + entityId + ' ' + groupPath)
		path = 'group/' + quote(groupPath, '') + '/entity/' + entityId
		if identityType!=None : 
			return self._delete(path, {'identityType': identityType})
		else :
			return self._delete(path)
								 
	def getEntityAttributes(self, entityId, group, effective=True, identityType=None):
		''' Returns attributes of a given entity in a selected group.
		Args: 
		   entityId : id of the entity
		   group : the group
		   effective : controls whether only directly defined or effective attributes are queried
		   identityType : type of the identity
		Returns:
		   attributes of a given entity in a selected group
		'''
		self.logger.debug('getEntityAttributes ' + entityId + ', ' + group)
		path = 'entity/' + entityId + '/attributes'
		params = {'group':group, 'effective':str(effective)}
		if identityType!=None : params['identityType'] = identityType
		return self._get(path, params)

		
	def getAttributeTypes(self):
		''' Returns an array with all attribute types
		Returns:
		   array with all attribute types
		'''
		self.logger.debug('getAttributeTypes ')
		return self._get('attributeTypes')
		
		
	def getEndpoints(self):
		''' Returns all deployed endpoints
		Returns:
		   array with all deployed endpoints
		'''
		self.logger.debug('getEndpoints ')
		return self._get('endpoints')
		
