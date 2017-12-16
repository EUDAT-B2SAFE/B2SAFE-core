# !/usr/bin/env python


##################################
# Michal Jankowski PSNC
# EUDAT-PRACE integration
# 03.2017
##################################

import ldap
import ConfigParser
import traceback

from utilities.password_file import *

class PraceLdapError(Exception):

	def __init__(self, message):
		super(PraceLdapError, self).__init__('PRACE LDAP. '+message)

class PraceLdap:

	'''Class to access PRACE LDAP
	
	Attributes: 
		logger : the logger object
		ldapObj : the LDAP object
		usercertdnAttrname : the LDAP attribute name for DN from the user certificate
		useridAttrname : the LDAP attribute name for user id
		usernameAttrname : he LDAP attribute name for user name
	'''

	def __init__(self, conf, confSection='PRACE', parentLogger=None):
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
				
			#set configurable attributes
			self.usercertdnAttrname=conf.get(confSection,'usercertdn')
			self.useridAttrname=conf.get(confSection,'userid')
			self.usernameAttrname=conf.get(confSection,'username')

			#bind to LDAP
			self.logger.debug('Binding to ' +conf.get(confSection,'host')+ ' as ' +conf.get(confSection,'binddn'))
			self.ldapObj=ldap.initialize(conf.get(confSection,'host'))
			self.ldapObj.protocol_version = ldap.VERSION3	
			self.ldapObj.simple_bind_s(conf.get(confSection,'binddn'), PasswordFile(conf.get(confSection,'password_file')).password)

		except ldap.INVALID_CREDENTIALS:
			self.logger.debug(traceback.format_exc())
			self.logger.error('Invalid credentials.')
			raise PraceLdapError('Invalid credentials.')

		except ldap.LDAPError, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error('Bind error ' + str(e))
			raise PraceLdapError('Bind error.')
 
		except ConfigParser.Error, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error(e.message)
			raise PraceLdapError('Configuration error.')




	def _search(self, searchBase, searchFilter, searchAttrs):
		''' Performs ldapsearch
		Args: 
			searchBase : search base
			searchFilter :search filter
			searchAttrs : attributes to be retrieved
		Returns:
			list with the search result
		'''
				
		try:
			self.logger.debug('Search: base=' + searchBase + '; filter=' + searchFilter + '; attrs=' + str(searchAttrs))
			rid = self.ldapObj.search(searchBase, ldap.SCOPE_SUBTREE, searchFilter, searchAttrs)

			result = []
			while 1:
				rtype, rdata = self.ldapObj.result(rid, 0)
				if (rdata == []):
					break
				else:
					if rtype == ldap.RES_SEARCH_ENTRY:
						result.append(rdata)

			return result

		except ldap.LDAPError, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error('Bind error ' + str(e))
			raise PraceLdapError('Bind error.')
		
		return None




	def getUsers(self, searchBase, searchFilter):
		''' Gets users from LDAP
		Args: 
			searchBase : search base
			searchFilter :search filter
		Returns:
			list of users, each user is dict of relevant user attributes
		'''
		
		self.logger.debug('Get users from base '+searchBase+" with filter "+searchFilter)
		usersLdap=self._search(searchBase, searchFilter, [self.usercertdnAttrname, self.useridAttrname, self.usernameAttrname])

		users = []
		try:
			for userLdap in usersLdap:
				dn, attrs = userLdap[0]
				users.append({'ldapdn': dn, 'certdn': attrs[self.usercertdnAttrname][0], 'id':attrs[self.useridAttrname][0], 'name':attrs[self.usernameAttrname][0]}) 

		except KeyError, e:
			self.logger.debug(traceback.format_exc())
			self.logger.error('Missing LDAP attribute: ' + e.message)
			raise PraceLdapError('Missing LDAP attribute.')

		self.logger.debug('Users : '+str(users))
		return users
