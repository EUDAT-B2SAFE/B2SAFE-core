#!/usr/bin/env python
# -*- python -*-

##################################
# Michal Jankowski PSNC
# EUDAT-PRACE integration
# 11.2017
##################################

import sys
import traceback
import ConfigParser

from irods.session import iRODSSession
from irods.exception import *
from irods.models import User, UserGroup, UserAuth
from irods.message import GeneralAdminRequest, iRODSMessage
from irods.api_number import api_number
from utilities.password_file import *

class IrodsApiException(Exception):
	'''Base class for Irods API exceptions
	'''
	def __init__(self, message):
		super(IrodsApiException, self).__init__('iRODS API exception. ' + message)

class IrodsApiInitException(IrodsApiException):
	'''Class for Irods API initialization exception
	'''
	def __init__(self, message):
		super(IrodsApiInitException, self).__init__('iRODS API initialization. ' + str(message))

class IrodsApiCallException(IrodsApiException):
	'''Class for Irods API call incorrect status exception
	'''

	def __init__(self, lowLevelMessage, highLevelMessage):
		super(IrodsApiCallException, self).__init__(lowLevelMessage +'/n'+ highLevelMessage)


class IrodsApiFacade :

	def __init__(self, conf, confSection='iRods', parentLogger=None):
		"""
		Initialize the object.
		
		Args:
			parentLogger: the parent logger
    """

		try:
			#initialize logger
			if (parentLogger): 
				self.logger = parentLogger.getChild(__name__)
			else: 
				self.logger = logging.getLogger(__name__)
				
			self.session=iRODSSession(host=    conf.get(confSection,'host'),
																port=    conf.get(confSection,'port'),
																user=    conf.get(confSection,'rods_user'),
																password=PasswordFile(conf.get(confSection,'rods_password_file')).password,
																zone=    conf.get(confSection,'rods_zone'))
			self.connection=self.session.pool.get_connection()
			self.userType=conf.get(confSection,'user_type') 
			self.userZone=conf.get(confSection,'user_zone')
			
			
		except ConfigParser.Error, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			raise IrodsApiInitException('Configuration error.')
			
		except IOError, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			raise IrodsApiInitException('Cannot read password file '+conf.get(confSection,'rods_password_file')+'.')
			
		except iRODSException, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.__class__.__name__)
			raise IrodsApiInitException(e.__class__.__name__)
			
		except Exception, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			raise IrodsApiInitException(e.message)

	def __repr__(self):
		return "<IRODSAPIFacade {session} {connection} >".format(**vars(self))
		
		
	def getUserName(self,dn):
		"""
		Get user name based on DN.
		
		Args:
			dn: distinguished name of the user
			
		Returns:
			name of the user
		"""
		
		try:
			result=self.session.query(User.name).filter(UserAuth.user_dn == dn).execute()
			if len(result)==0:
				self.logger.debug(dn+' does not map to any user.')
				return None
			elif len(result) > 1:
				#TODO: no good idea how to solve the problem, normally it shall not happen
				self.logger.error('Ambigious mapping. '+dn+" maps to multiple users.")
				
			self.logger.debug(dn+' maps to user '+result[0][User.name]+'.')
			return result[0][User.name]
			
		except iRODSException, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			raise IrodsApiCallException(e.__class__.__name__, 'Cannot get the user based on DN '+dn+'.')
	
	def getUserGroups(self,userName):
		"""
		Gets list of groups the user is member.
		
		Args:
			userName: name of the user
			
		Returns:
			List with group names
		"""
		
		try:
			result=self.session.query(UserGroup.name).filter(User.name == userName).get_results()
			return [row[UserGroup.name] for row in result]
			
		except iRODSException, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			raise IrodsApiCallException(e.__class__.__name__, 'Cannot get user '+userName+' groups.')
	
	def userExists(self,userName):
		"""
		Checks if the user exists.
		
		Args:
			userName: name of the user
			
		Returns:
			True if the user exist.
		"""
		
		try:
			result=self.session.query(User.id).filter(User.name==userName).limit(1).execute()
			return len(result) > 0
			
		except iRODSException, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			raise IrodsApiCallException(e.__class__.__name__, 'Cannot check if user '+userName+' exists.')

	
	def groupExists(self,groupName):
		"""
		Checks if the group exists.
		
		Args:
			groupName: name of the group
			
		Returns:
			True if the group exist.
		"""
		
		try:
			result=self.session.query(UserGroup.id).filter(UserGroup.name==groupName).limit(1).execute()
			return len(result) > 0
			
		except iRODSException, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			raise IrodsApiCallException(e.__class__.__name__, 'Cannot check if group '+groupName+' exists.')

	def createUser(self,userName):
		"""
		Create the user.
		
		Args:
			userName: name of the user
		"""
		self.__adminRequest('User '+userName+' created.',
												'Cannot create user '+userName+'.',
												'add','user',userName,self.userType,self.userZone, '')
	
	def createGroup(self,groupName):
		"""
		Create the group.
		
		Args:
			groupName: name of the group
		
		Returns:
			True on success
		"""
		self.__adminRequest('Group '+groupName+' created.',
												'Cannot create group '+groupName+'.',
												'add','user',groupName,'rodsgroup','', '')

	def addUserAuth(self, userName, dn):
		"""
		Add DN-user mapping.
		
		Args:
			userName: name of the user
			dn: distinguished name of the user
		
		Returns:
			True on success
		"""
		self.__adminRequest('DN '+dn+' added to user '+userName+'.',
												'Cannot add DN '+dn+' to user '+userName+'.',
												'modify','user',userName,'addAuth', dn)

	def removeUserAuth(self, userName, dn):
		"""
		Remove DN-user mapping.
		
		Args:
			userName: name of the user
			dn: distinguished name of the user
		"""
		self.__adminRequest('DN '+dn+' removed from user '+userName+'.',
												'Cannot remove DN '+dn+' from user '+userName+'.',
												'modify','user',userName,'rmAuth', dn)

	def addUserToGroup(self, userName, groupName):
		"""
		Add the user to given group.
		
		Args:
			userName: name of the user
			groupName: name of the group
		"""
		if not self.groupExists(groupName) : self.createGroup(groupName)
		self.__adminRequest('User '+userName+' added to group '+groupName+'.',
												'Cannot add user ' + userName + ' to group ' + groupName + '.',
												'modify','group',groupName,'add', userName, self.userZone)
	
	def removeUserFromGroup(self, userName, groupName):
		"""
		Remove the user from given group.
		
		Args:
			userName: name of the user
			groupName: name of the group
		"""
		self.__adminRequest('User '+userName+' removed from group '+groupName+'.',
												'Cannot remove user ' + userName + ' from group ' + groupName + '.',
												'modify','group',groupName,'remove', userName, self.userZone)
	

	def __adminRequest(self, onOkMsg, onErrMsg, *args):
		"""
		Performs an admin request
		
		Args:
			onOkMsg: string to be logged on success
			onErrMsg: string to be logged on error
			args: arguments to be passed to build the message
		
		Returns:
			True on success			
		"""
	
		try:
			self.connection.send(iRODSMessage("RODS_API_REQ", msg=GeneralAdminRequest(*args), int_info=api_number['GENERAL_ADMIN_AN']))
			self.connection.recv()
			self.logger.info(onOkMsg)
			
		except CAT_SUCCESS_BUT_WITH_NO_INFO, e:
			#this is not really an exception, ignore it
			self.logger.info(onOkMsg)
			
		except iRODSException, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.__class__.__name__)
			print(e)
			raise IrodsApiCallException(e.__class__.__name__, onErrMsg)
