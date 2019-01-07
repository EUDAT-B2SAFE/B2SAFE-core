#!/usr/bin/env python
# -*- python -*-

##################################
# Michal Jankowski PSNC
# EUDAT-PRACE integration
# 03.2017
##################################

import sys
import traceback

import argparse
import ConfigParser
import logging
import re

from utilities.drivers.unity_api import *
from utilities.drivers.irods_api_facade import *
from utilities.conf_logger import *
from utilities.expiration_guard import *


logger = logging.getLogger(__name__) 


class IrodsUserSync:
	
	def __init__(self):
		"""
		Initialize the object.
		Anything fails here, the script must return an error.
		The error is printed as logging not configured yet.
		"""
		
		try:
			""" 
			Parse arguments --------------------------------------------------
			"""
			argParser = argparse.ArgumentParser(description='Synchronizing single user between B2ACCESS and iRods')
			argParser.add_argument('-c', '--config', dest='conf',	default='conf/irods_user_sync.conf', help='path to the configuration file')
			argParser.add_argument('-d', '--dn', dest='dn',	required=True, help='DN from user certificate')
			argParser.add_argument('-dr', '--dry-run', dest='dryRunFlag',	action='store_true', help='do not modify iRODS if set, only print output')
			arguments = argParser.parse_args()
			
			self.dn = arguments.dn
			self.dryRun = arguments.dryRunFlag

			"""
			Read and parse config file ---------------------------------------
			"""
			self.config = ConfigParser.ConfigParser()
			self.config.optionxform=str
			self.config.readfp(open(arguments.conf))
			
			""" 
			Configure and start logging
			"""
			self.logger = logger
			configureLogger(self.logger, self.config, 'common')
			self.logger.info('Script started #################################################################')
			self.logger.info('User '+self.dn)
			
		except IOError, e:
			print 'Cannot read config file.'
			print e.message
			sys.exit(1)
			
		except ConfigParser.Error, e:
			print 'Configuration error.'
			print e.message
			sys.exit(1)
		
		except Exception, e:
			tbck = traceback.format_exc()
			print tbck
			print e.message
			sys.exit(1)


	def main(self):
		"""
		Synchronizing user between B2SAFE and IRods
		"""
	
		try:
			#check if the user authorization info is up to date, if so, there is no need to go on
			guard=ExpirationGuard(self.dn, 
														self.config.get('common','expiration_tempdir'), 
														self.config.get('common','expiration_period_sec'),
														parentLogger=self.logger)
			if guard.expired() :
		
				#get Unity entity and groups related to the user
				unityEntity,unityEntityGroups = self.__getUnityData()
				
				#process group mapping
				irodsGroupsMember, irodsGroupsNonMember = self.__processGroupMaps(unityEntity,unityEntityGroups)
				
				#process iRODS user
				#the user is authorized if member of any iRods group: bool(irodsGroupsMember)
				self.__processIrodsUser(self.dn, bool(irodsGroupsMember),irodsGroupsMember, irodsGroupsNonMember, unityEntity)
				
				#user info is refreshed, refresh the guard
				guard.refresh()
			
		except ConfigParser.Error, e:
			self.logger.error(e.message)
			print e.message
			print 'Configuration error.'
			sys.exit(1)
			
		except UnityApiException, e:
			self.logger.error(e.message)
			print e.message
			print 'Unity API error.'
			sys.exit(1)
			
		except IrodsApiException, e:
			self.logger.error(e.message)
			print e.message
			print 'iRODS API error.'
			sys.exit(1)
			
		except Exception, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			print e.message
			print 'Error.'
			sys.exit(1)
		
		print 'Success.'
		self.logger.info('Finished with success')
		sys.exit(0)
	
	
		
	def __getUnityData(self):
		"""
		Get data from B2ACCESS -if the user exists in the service and belongs to at least one group..
		Handle exceptions -in case of error assume the user is not authorized and try to communicate it to iRODS
		
		Returns:
			Info on Unity entity
			List of Unity groups the user is member of
		"""
		
		"""
		Change the format of dn suitable for Unity API
		"""
		unityDn = ','.join(reversed(self.dn.split('/')))[:-1]
		self.logger.debug('DN suitable for Unity : '+ unityDn )
		
		"""
		Determine if the certificate issuer is B2ACCESS
		Then set unityId and unityIdType depending on the issuer
		"""
		dnPattern=self.config.get('usercert','dn_pattern')
		self.logger.debug('Checking DN '+unityDn+' against pattern '+dnPattern)
		matchObj = re.match(dnPattern, unityDn, re.I)
		if matchObj:
			self.logger.info('The certificate is issued by B2ACCESS.')
			unityId=matchObj.group(int(self.config.get('usercert','id_match')))
			unityIdType=self.config.get('usercert','id_type')
			self.logger.debug('User '+unityIdType+' = '+unityId)
		else:
			self.logger.info('The certificate is NOT issued by B2ACCESS.')
			unityId=unityDn
			unityIdType='x500Name'
		
		"""
		Get data from B2ACCESS
		"""
		# init connection
		unityApi = UnityApi(self.config, confSection='B2ACCESS', parentLogger=self.logger)
		# get entity
		unityEntity = unityApi.getEntity(unityId, unityIdType)
		if unityEntity is None or unityEntity['entityInformation']['state'] != 'valid':
			self.logger.info('User not authorized by B2ACCESS.')
			return None, []
			
		# get entity groups
		unityEntityGroups = unityApi.getEntityGroups(unityId, unityIdType)
		self.logger.debug(' User belongs to B2ACCESS groups : '+str(unityEntityGroups))
		
		return unityEntity, unityEntityGroups


	
	def __getExpectedIrodsUname(self, unityEntity):
		""" 
		Compute irods expected user name.
		
		Args :
			unityEntity: info on Unity entity
			
		Returns:
			expected user name
		"""
		if unityEntity is None :
			return None
			
		try:
			expectedUname = self.config.get('iRods','account_prefix')
			if self.config.get('iRods','account_identity_type') == 'entityId' :
				expectedUname += str(unityEntity['entityInformation']['entityId'])
			elif self.config.get('iRods','account_identity_type') == 'persistent':
				persistentId=None
				for identity in unityEntity['identities']:	
					if identity['typeId'] == 'persistent':
						persistentId = identity['value']
						break
				if persistentId is None :
					raise Exception('No persistent identity for user '+self.dn)
				expectedUname +=	persistentId
			else:
				raise Exception('"account_identity" incorrectly configured')
				
			self.logger.debug('Expected iRods user name is '+expectedUname)
			
			return expectedUname
			
			
		except Exception, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			print e.message
			raise Exception('Cannot determine expected iRODS user name.')

	
	def __processGroupMaps(self,unityEntity,unityEntityGroups):
		"""
		Process group maps by comparing Unity groups the user belongs with groupmap configuration.
		
		Args:
			unityEntity: info on Unity entity
			unityEntityGroups: list of Unity groups the user is member
			
		Returns:
			List of iRODS groups the user must be a member of (groupmap intersect unityEntityGroups)
			iRODS groups the user must not be a member of (groupmap diff unityEntityGroups diff irodsGroupsMember) 
		"""
		
		irodsGroupsMember=set()
		irodsGroupsNonMember=set()
		
		if unityEntity is None or not unityEntityGroups:
			for unityGroup,irodsGroupsStr in self.config.items('groupmap') :
				irodsGroupsNonMember|=set([group.strip() for group in irodsGroupsStr.split(',')])
		else:
			for unityGroup,irodsGroupsStr in self.config.items('groupmap') :
				irodsGroups=[group.strip() for group in irodsGroupsStr.split(',')] 
				if unityGroup.replace('//',':') in unityEntityGroups : #workaround for Python 2.x where ':' (often used in Unity group names) is a hardcoded delimiter
					irodsGroupsMember|=set(irodsGroups)
				else:
					irodsGroupsNonMember|=set(irodsGroups)
			irodsGroupsNonMember-=irodsGroupsMember
			
		self.logger.debug(' User belongs to iRODS groups : '+str(irodsGroupsMember))
		self.logger.debug(' User does not belong to iRODS groups : '+str(irodsGroupsNonMember))
			
		return irodsGroupsMember, irodsGroupsNonMember

	def __processIrodsUser(self, dn, isAuthorized, irodsGroupsMember, irodsGroupsNonMember, unityEntity):
		"""
		Use existing iRods user and mapping or create them, providing the user is authorized
		return iRODS user name and info if the user has existed before 
		Note: do not throw an exception on iRods operation failure -instead try to continue and 
		perform as many authorization related operations as possible. TODO: this could be configurable
		
		Args:
			dn: user's distinguished name'
			isAuthorized: true if the user shall be authorized
			expectedIrodsUname: expected iRODS user name
		"""
		
		#initialize iRODS interface
		irodsFacade=IrodsApiFacade(self.config, confSection='iRods', parentLogger=self.logger)
		
		irodsUname=irodsFacade.getUserName(dn)
		irodsFacade.userExists(irodsUname)
		
		if not isAuthorized and irodsUname is None:
			self.logger.info("DN "+dn+" not authorized by B2ACCESS and not found in iRODS.")
			return
		
		#get user's groups
		irodsGroupsAlreadyMember = irodsFacade.getUserGroups(irodsUname)

		if not isAuthorized :
			self.logger.info("DN "+dn+" not authorized by B2ACCESS, but mapping to "+irodsUname+" found in iRODS.")
			irodsFacade.removeUserAuth(irodsUname,dn)
			for irodsGname in irodsGroupsNonMember:
				if irodsGname in irodsGroupsAlreadyMember : irodsFacade.removeUserFromGroup(irodsUname,irodsGname)
			return
		
		#compute expected iRODS user name
		expectedIrodsUname=self.__getExpectedIrodsUname(unityEntity)
		
		if irodsUname is None:
			#DN mapping and possibly iRODS account are missing
			irodsUname = expectedIrodsUname
			if not irodsFacade.userExists(irodsUname) : irodsFacade.createUser(irodsUname)
			irodsFacade.addUserAuth(irodsUname, dn)
		elif expectedIrodsUname != irodsUname:
			#DN is mapped to an account named different than expected
			if self.config.get('iRods','replace_mapping') != 0 :
				self.logger.warning("DN " +dn+ " already mapped to " +str(irodsUname) +', while expected to ' +expectedIrodsUname + ', use the new mapping.')
				irodsFacade.removeUserAuth(irodsUname,dn)
				irodsFacade.addUserAuth(expectedIrodsUname,dn)
				irodsUname=expectedIrodsUname
			else:
				self.logger.warning("DN " +dn+ " already mapped to " +str(irodsUname) +', while expected to ' +expectedIrodsUname + ', use the old mapping.')
		else:
			#existing DN mapping is ok
			self.logger.info("DN " +dn+ " already mapped to " +irodsUname)
		
		for irodsGname in irodsGroupsNonMember: 
			if irodsGname in irodsGroupsAlreadyMember: irodsFacade.removeUserFromGroup(irodsUname,irodsGname)
		for irodsGname in irodsGroupsMember:
			if irodsGname not in irodsGroupsAlreadyMember: irodsFacade.addUserToGroup(irodsUname,irodsGname)
	
		return


if __name__ == '__main__':
	IrodsUserSync().main()
