#!/usr/bin/env python
# -*- python -*-

##################################
# Michal Jankowski PSNC
# EUDAT-PRACE integration
# 11.2017
##################################

from hashlib import *
from time import time
import os
import errno

class ExpirationGuard :
	"""
	An object of this class keeps information about last call to refresh() member
	as a modification time of an empty file.
	Loosing this information sporadically is allowable as we assume, 
	that in the worst case the guarded object will be refreshed.
	
		Attributes:
			path : path to the guard file
			expPeriod : period of time in which the guarded object expires
			logger : the logger object
	"""

	def __init__(self, name, guardDir, expPeriod, parentLogger=None):
		"""
		Initialization
		
		Args:
			guardName: name of the guarded object
			guardDir: directory for the guard file
			expPeriod: period of time in which the guarded object expires
			parentLogger: the parent logger
		"""
	
		#The guard name is hashed in order to avoid problems with incorrect filename
		self.name=name
		self.path=guardDir+'/'+sha512(name).hexdigest()
		self.expPeriod=expPeriod
		
		if (parentLogger): 
			self.logger = parentLogger.getChild(__name__)
		else: 
			self.logger = logging.getLogger(__name__)
			
	def __repr__(self):
		return "<ExpirationGuard {name} {path} {expPeriod} >".format(**vars(self))
    
	def expired(self):
		"""
		Checks if the guard expired.
		
		Returns: 
			True if the guard expired else False.
		"""
		expired=not os.path.exists(self.path) or time()-os.stat(self.path).st_mtime > int(self.expPeriod)
		self.logger.debug(self.path+' expiration status: '+str(expired))
		return expired
		
	def refresh(self):	
		"""
		Refreshes the guard. 
		If the guard file not exist, it is created altogether with parent dirs.
		Else only the 
		"""
		if not os.path.exists(self.path):
			dirname=os.path.dirname(self.path)
			if not os.path.exists(dirname):
				try:
					os.makedirs(dirname)
					self.logger.debug(dirname+' created.')
				except OSError as e:
					#EEXIST means race condition while creating the dir -ignore it
					if e.errno != errno.EEXIST:
						raise e
			open(self.path, 'a').close()
			self.logger.debug(self.path+' created.')
		else:
			os.utime(self.path, None)
			self.logger.debug(self.path+' updated.')
