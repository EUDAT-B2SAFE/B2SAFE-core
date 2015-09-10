#!/usr/bin/env python
# -*- python -*-

import logging
import logging.handlers
import json
import ConfigParser
import argparse
import subprocess
import os
import tempfile
import pprint
import sys

logger = logging.getLogger('Metadata')

##############################################################################
# Metadata management Class #
##############################################################################

class Metadata():
    """Class implementing the metadata management."""

    
    def __init__( self, conf, user ):
        """Initialize object with configuration parameters."""
        
        self.conf = conf
        self.user = user
        self.irodsu = IRODSUtils()
    
    
    def store(self, path, keyValuePairs, dryrun):
       
        if not path.endswith('.metadata'):
            logger.info("Going to store metadata about " + path)
            query = "SELECT COLL_NAME WHERE COLL_NAME = '" + path + "'"
            (rc, out1) = self.irodsu.execute_icommand(["iquest", query],self.user)
            if out1 is not None:
                collPath = path
                objPath = None
                mcoll = MetadataItem(collPath, objPath, self.user, dryrun)
                mcoll.store(keyValuePairs)
            else:
                (parent, child) = path.rsplit('/',1)
                query = "SELECT DATA_NAME WHERE COLL_NAME = '" + parent + "' and "\
                      + "DATA_NAME = '" + child + "'"
                (rc, out2) = self.irodsu.execute_icommand(["iquest", query],self.user)
                if out2 is not None:
                    mobj = MetadataItem(parent, child, self.user, dryrun)
                    mobj.store(keyValuePairs)
                else:
                    logger.error('Wrong path: ' + path)
        else:  
            logger.debug('skipping directory metadata: %s', path)
       
 
class MetadataItem():
    """Class implementing the single metadata record"""
    
    def __init__( self, collPath, objPath, user, dryrun):
        """Initialize object with iRODS path parameters."""
        
        self.dryrun = dryrun
	self.irodsu = IRODSUtils()
        self.objPath = objPath
        self.user = user

        # verify that .metadata exists, if not create it
        self.metaPath = collPath + '/.metadata'
        (rc, out1) = self.irodsu.execute_icommand(["ils", self.metaPath],
                                                  self.user)
        if out1 is None:
            (rc, out2) = self.irodsu.execute_icommand(["imkdir", self.metaPath],
                                                      self.user)
            if out2 is None:
                logger.error("impossible to create the path " + self.metaPath)
                sys.exit()
        
                
    def store(self, keyValuePairs):
        """Store the metadata key-value pairs."""
        
	logger.info("Going to store the following metadata")
	logger.info(pprint.pformat(keyValuePairs, indent=4))
        
        if self.objPath is None:
            # check if json of root_collection exists
            logger.debug("check if json of root_collection exists")
            metaObj = self.metaPath + '/root_collection.json'
        else:
            metaObj = self.metaPath + '/' + self.objPath + '_metadata.json'

        (rc, out) = self.irodsu.execute_icommand(["ils", metaObj], self.user)
        if out is not None:
            # get the json of root_collection
            logger.debug("get the json of root_collection")
            (rc, out2) = self.irodsu.execute_icommand(["iget", metaObj, "-"],
                                                      self.user)
            if out2:
                rootCollectionMetaData = json.loads(out2)
            else:
                rootCollectionMetaData = {}
            logger.debug("loaded the following metadata")
            logger.debug(pprint.pformat(rootCollectionMetaData, indent=4))
            for key, value in keyValuePairs.iteritems():
                logger.debug("modifying the pair (%s,%s)" % (key,value))
                rootCollectionMetaData[key] = value
                if not self.dryrun:
                    self._writeMetadata(rootCollectionMetaData, metaObj)
                else:
                    logger.info("writing the following metadata to " + metaObj)
                    logger.info(pprint.pformat(rootCollectionMetaData,indent=4))
        else:
            if not self.dryrun:
                self._writeMetadata(keyValuePairs, metaObj)
            else:
                logger.info("writing the following metadata to " + metaObj)
                logger.info(pprint.pformat(keyValuePairs,indent=4))


        
    def _writeMetadata(self, keyValuePairs, irodsObj):
        """Write the metadata key-value pair to a file."""

        with tempfile.NamedTemporaryFile() as tempJsonFile:
            logger.debug("writing the metadata to file " + tempJsonFile.name)
            tempJsonFile.write(json.dumps(keyValuePairs, indent=2))
            tempJsonFile.seek(0)
            logger.debug("Temp file content: " + tempJsonFile.read())
            logger.debug("uploading the file %s to irods location %s"
                         % (tempJsonFile.name, irodsObj))
            (rc, out) = self.irodsu.execute_icommand(["iput", "-f",
                                                      tempJsonFile.name,
                                                      irodsObj],self.user)
            if out is None:
                logger.error("impossible to upload the object: " + irodsObj)


##############################################################################
# iRODS Admin Utility Class #
##############################################################################

class IRODSUtils():
    """ 
    utility for irods management
    """
    

    def __init__(self):
        """initialize the object"""
        logger.debug("iRODS utility class initialization")
        
        
    def execute_icommand(self, command, user):
        """Execute a shell command and manage error conditions"""
   
        envKey = 'clientUserName' 
        (rc, output) = self._shell_command(command, envKey, user)
        if rc != 0:
            logger.error('Error running %s, rc = %d' % (' '.join(command),
                                                             rc))
            logger.error("output: %s", output[1])
            if output[0] is not None and len(output[0].strip()) > 0:
                logger.error("error message: %s", output[0])
            return (rc, None)
        
        logger.debug('executed %s, rc = %d' % (' '.join(command), rc))
        logger.debug('output: %s', output[1])
        if (output[1].startswith('CAT_NO_ROWS_FOUND')): return (rc, None)
        return (rc, output[1])


    def _shell_command(self, command_list, envKey, envValue):
        """
        Performs a shell command using the subprocess object
        input list of strings that represent the argv of the process to create
        return tuple (return code, output object from subprocess.communicate)
        """
 
        if not command_list:
            return None
 
        try:
            d = dict(os.environ)
            d[envKey] = envValue
            process = subprocess.Popen(command_list, env=d, 
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            (out, err) = process.communicate()
            return (process.returncode, [err, out])
        except Exception, e:
            logger.debug('Failure with error: ' + str(e))
            return (-1, [None, None])
        
    
###############################################################################
# Configuration Class #
###############################################################################
 
class Configuration():
    """ 
    Get properties from filesystem
    """

    def __init__(self, file, logger):
   
        self.file = file
        self.log_level = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, \
                          'ERROR': logging.ERROR, 'WARNING': logging.WARNING, \
                          'CRITICAL': logging.CRITICAL}


    def parseConf(self):
        """Parse the configuration file."""

        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(open(self.file))
        
        logfilepath = self._getConfOption('Logging', 'log_file')
        loglevel = self._getConfOption('Logging', 'log_level')
        logger.setLevel(self.log_level[loglevel])
        rfh = logging.handlers.RotatingFileHandler(logfilepath, \
                                                   maxBytes=8388608, \
                                                   backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: '
                                    + '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)


    def _getConfOption(self, section, option, boolean=False):
        """
        get the options from the configuration file
        """

        if (self.config.has_option(section, option)):
            opt = self.config.get(section, option)
            if boolean:
                if opt in ['True', 'true']: return True
                else: return False
            return opt
        else:
            logger.warning('missing parameter %s:%s' % (section,option))
            return None


###############################################################################
# Metadata script Command Line Interface #
###############################################################################

def store(args):

    configuration = Configuration(args.confpath, logger)
    configuration.parseConf();
    meta = Metadata(configuration, args.user)
    
    kv = {}
    if args.pid: kv['pid'] =  args.pid
    if args.checksum: kv['checksum'] = args.checksum
    if args.ror: kv['ror'] = args.ror
    if args.checksum_timestamp: 
        kv['checksum_timestamp'] = args.checksum_timestamp
    
    logger.info("Metadata storing starting ...")
    meta.store(args.path, kv, args.dryrun)
    logger.info("Metadata storing completed")

    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='EUDAT metadata management '
                                               + 'tool')
    parser.add_argument("confpath",default="NULL",help='path to the '
                                                     + 'configuration file')
    parser.add_argument("-d", "--dryrun", action="store_true",\
                        help="execute a command without performing any real" 
                           + "change")
    parser.add_argument("user", help="the owner of the metadata")

    subparsers = parser.add_subparsers(title='Actions', \
                                       description='metadata '
                                                 + 'management operations', \
                                       help='allowed operations')

    parser_store = subparsers.add_parser('store', help='store metadata')
    parser_store.add_argument('path', help='the iRODS object/collection path')
    parser_store.add_argument('-i', '--pid', help='persistent identifier')
    parser_store.add_argument('-c', '--checksum', help='checksum')
    parser_store.add_argument('-r', '--ror', help='Repository of Records')
    parser_store.add_argument('-t', '--checksum_timestamp', \
                             help='timestamp of the last checksum calculation')
    parser_store.set_defaults(func=store)

    args = parser.parse_args()
    
    if not (args.pid or args.checksum or args.ror or args.checksum_timestamp):
        parser.error('No key value pair in input, add at least one among '
                    +'pid, checksum, ror, checksum timestamp.')    
    
    args.func(args)
