#!/usr/bin/env python
# -*- python -*-

##################################
# Michal Jankowski PSNC
# EUDAT-PRACE integration
# 11.2017
##################################

from os.path import expanduser

class PasswordFile :

	def __init__(self, filename):
			with open(expanduser(filename)) as f:
				self.password=f.read().split('\n')[0]

