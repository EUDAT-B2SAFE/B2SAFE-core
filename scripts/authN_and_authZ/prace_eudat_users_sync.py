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
import logging.handlers 
from pprint import pformat

from utilities.drivers.unity_api import *
from utilities.drivers.prace_ldap import *
from utilities.conf_logger import *

logger = logging.getLogger(__name__) 



class PraceEudatUsersSync:
	
	def __init__(self):
		"""initialize the object"""

		self.logger = logger


	def main(self):
		"""
		Synchronizing users between PRACE and EUDAT
		"""
		
		try:
			""" Parse arguments """
			argParser = argparse.ArgumentParser(description='Synchronizing users between PRACE and EUDAT')
			argParser.add_argument('-c', '--config', dest='conf',  default='conf/prace_eudat_users_sync.conf', help='path to the configuration file')
			arguments = argParser.parse_args()

			""" read and parse config file """
			self.config = ConfigParser.ConfigParser()
			self.config.readfp(open(arguments.conf))
			self.maps={}
			for section in self.config.sections():
				if section.startswith('MAP_') :
					self.maps[section] = ({k:v for k,v in self.config.items(section)})
			

			""" 
			Configure and start logging
			"""
			self.logger = logger
			configureLogger(self.logger, self.config, 'common')
			self.logger.info('Script started #################################################################')
			
			""" init connection to B2ACCESS """
			unityApi = UnityApi(self.config, confSection='B2ACCESS', parentLogger=self.logger)

			""" init connection to PRACE LDAP """
			praceLdap = PraceLdap(self.config, confSection='PRACE', parentLogger=self.logger)

			""" synchronize """
			for mapName in sorted(self.maps) :
				self._syncOneMap(mapName, praceLdap, self.maps[mapName]['prace_searchbase'], self.maps[mapName]['prace_userfilter'], unityApi, self.maps[mapName]['eudat_groups'].split())

			print 'Success.'
			self.logger.info('Finished with success')
			sys.exit(0)
		
		except ConfigParser.Error, e:
			tbck = traceback.format_exc()
			self.logger.error(tbck)
			self.logger.error(e.message)
			print tbck
			print 'Configuration error.'
			print e.message
			
		except Exception, e:
			tbck = traceback.format_exc()
			self.logger.error(tbck)
			self.logger.error(e.message)
			print tbck
			print e.message
	
		print 'Failure.'
		sys.exit(1)



	def _syncOneMap(self, mapName, praceLdap, praceSearchBase, praceUserFilter, unityApi, groupNames):
		"""
		performs synchronization for single map section
		"""

		""" get users from PRACE """
		usersInPrace = praceLdap.getUsers(praceSearchBase, praceUserFilter)

		for groupName in groupNames :
			""" get eudat group from B2ACCESS """
			self.logger.info("Performing synchronization for section "+mapName+" and group "+groupName)
			group = unityApi.getGroup(groupName)

			if group is None :
				""" create the group in B2ACCESS if necessary """
				self.logger.info('Adding group ' + groupName +'.')
				unityApi.createGroup(groupName)
				group = {'members': [], 'subGroups': []}

			groupMembers = group['members']
			groupMemberIds = [member['entityId'] for member in groupMembers]
			self.logger.debug('PRACE users ids in B2ACCESS group ' + groupName + ": " + pformat(groupMemberIds))

			""" loop over selected PRACE users """
			for userInPrace in usersInPrace :
				""" look for the user in B2ACCESS """
				userInEudat = unityApi.getEntity(userInPrace['certdn'], 'x500Name')
				if userInEudat is None :
					""" add the user to B2ACCESS and add him to all relevant groups"""
					self.logger.info('Adding user ' + userInPrace['certdn']+  '.')
					userInEudatId = unityApi.createEntity('x500Name', userInPrace['certdn'], self.config['EUDAT']['credentialreq'])
					self.logger.info('Adding user ' + userInPrace['certdn']+  ' to group ' + groupName +'.')
					unityApi.addEntityGroup(groupName, str(userInEudatId))
				else :
					""" check if the user belongs to relevant groups """
					self.logger.debug('PRACE user in B2ACCESS: ' + pformat(userInEudat))
					userInEudatId = userInEudat['entityInformation']['entityId']
					userInGroups = unityApi.getEntityGroups(str(userInEudatId))
					self.logger.debug('User ' + str(userInEudatId) + ' is in groups: '  + pformat(userInGroups))
					if not groupName in userInGroups :
						self.logger.info('Adding ' + userInPrace['certdn'] +  ' to ' + groupName +'.')
						unityApi.addEntityGroup(groupName, str(userInEudatId))
					else :
						""" remove user existing in both services from groupMembers """
						groupMemberIds.remove(userInEudatId)
				
			""" usersInEudatIds contains now only users in B2ACCESS, but not in PRACE, so remove them from relevant groups """
			for userInEudatId in groupMemberIds:
				self.logger.info('Removing user ' + str(userInEudatId) +  ' from ' + groupName +'.')
				unityApi.deleteEntityGroup(groupName, str(userInEudatId))


if __name__ == '__main__':
	PraceEudatUsersSync().main()
