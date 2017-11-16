#!/usr/bin/env python
# -*- python -*-

##################################
# Michal Jankowski PSNC
# EUDAT-PRACE integration
# 10.2017
##################################
import ConfigParser
import logging
import logging.handlers 

def configureLogger(logger, config, confSection='common'):
	""" 
	Configure logging.
	
	Args:
		logger: the logger to be configured
		config: the config
		confSection: the section in config with the logger configuration
	"""
	
	#set level
	loglevels = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
	logger.setLevel(loglevels[config.get(confSection,'loglevel')])
	
	#set file handler
	fileHandler = logging.handlers.RotatingFileHandler(config.get(confSection,'logfile'), config.get(confSection,'logmaxbytes'), config.get(confSection,'logbackupcnt'))
	fileHandler.setFormatter(logging.Formatter(config.get(confSection,'logformat',True)))
	logger.addHandler(fileHandler)

