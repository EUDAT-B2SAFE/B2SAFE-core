#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import argparse
import logging
import logging.handlers
import ConfigParser
import manifest
import pprint
import hashlib

from py2neo import Graph, Node, Relationship, authenticate, GraphError


logger = logging.getLogger('GraphDBClient')

##################################################
# Person(name:'guybrush')
# Person - [:IS_DEFINED_IN] -> Zone
# DigitalEntity (EudatChecksum:'xyz', location:'/Zone/path/to/file')
# DigitalEntity - [:STORED_IN] -> Resource - [:IS_AVAILABLE_IN] -> Zone
# DigitalEntity - [:IS_OWNED_BY] -> Person
# DigitalEntity - [:BELONGS_TO] -> Aggregation
# DigitalEntity - [:IS_REPLICA_OF{PPID, ROR}] -> Pointer{type}
# DigitalEntity - [:IS_MASTER_OF{Replica}] -> Pointer{type}
# DigitalEntity - [:UNIQUELY_IDENTIFIED_BY] -> PID{EudatChecksum:'xyz'}

class GraphDBClient():
    
    def __init__(self, conf, rootPath):
        """
        Graph initialization
        """
    
        self.conf = conf
        self.root = rootPath

        self.irodsu = manifest.IRODSUtils(self.conf.irods_home_dir,
                                          logger,
                                          self.conf.irods_debug)

        logger.info("Connecting to " + self.conf.graphdb_addr
                    + " with user " + self.conf.graphdb_user)    
        authenticate(self.conf.graphdb_addr, self.conf.graphdb_user, 
                     self.conf.graphdb_passwd)
        logger.debug("Authenticated, now connecting ...")
        self.graph = Graph("http://" + self.conf.graphdb_addr + self.conf.graphdb_path)

        logger.debug("Searching if the initial nodes have been already created")
        self.zone = self.graph.find_one("Zone", "name", self.conf.irods_zone_name)
        if self.zone is None:
            logger.info('Node "Zone" ' + self.conf.irods_zone_name
                      + ' not found, so it will be created')
            try:
                self.graph.schema.create_uniqueness_constraint("Digital Entity", 
                                                               "location")
                self.graph.schema.create_uniqueness_constraint("Zone", "name")
                self.graph.schema.create_uniqueness_constraint("Resource", "name")
            except GraphError as ge:
                logger.warning('Graph error: %s', ge)
            self.zone = Node("Zone", name=self.conf.irods_zone_name, 
                                     endpoint=self.conf.irods_zone_ep)
            self.graph.create(self.zone)
            resources = self.conf.irods_res.split(',')
            for res in resources:
                res_name,res_path = res.split(':')
                self.resNode = Node("Resource", name=res_name, path=res_path)
                res_is_located_in_zone = Relationship(self.resNode, 
                                                      "IS_AVAILABLE_IN", 
                                                      self.zone)
                try:
                    self.graph.create_unique(res_is_located_in_zone)
                except GraphError as ge:
                    logger.warning('Graph error: %s', ge)
        else:
            logger.info('Node "Zone" found')


# dynamic data ###################################

    def push(self, structuralMap):

        logger.info('Start to upload metadata to the Graph DB')
        structList = self._structRecursion(structuralMap)


    def _structRecursion(self, d):

        if len(d['nestedObjects']) > 0:

            path = ''
            sumValue = ''
            agg = self._createUniqueNode("Aggregation", d['name'],
                                                        path[7:],
                                                        sumValue,
                                                        d['type'])
            if len(d['filePaths']) > 0:
                if len(d['filePaths']) == 1:
                    path = d['filePaths'][0]
                    if self.conf.dryrun: 
                        print "get the checksum based on path: " + str(path)
                    else:
                        agg.properties['location'] = path[7:]
                        agg.push()
                        logger.debug('Updated location of entity: ' + str(agg))
                        absolutePath = self.root + '/' + path[7:]
                        sumValue = self.irodsu.getChecksum(absolutePath)
                        if sumValue:
                            agg.properties['checksum'] = sumValue
                            agg.push()
                            logger.debug('Updated checksum of entity: ' + str(agg))
                        self._defineOwnershipRelation(agg)
                        self._definePIDRelation(agg)
                else:                
                    logger.warning('multiple file paths not allowed')

            for elem in d['nestedObjects']:
                nodes = self._structRecursion(elem)
                for n in nodes:
                    if self.conf.dryrun:
                        print ("create the graph relation ["+str(n)+","
                               "BELONGS_TO,"+str(agg)+"]")
                    else:
                        de_belongs_to_agg = Relationship(n, "BELONGS_TO", agg)
                        self.graph.create_unique(de_belongs_to_agg)
                        logger.debug('Created relation: ' + str(de_belongs_to_agg))

            return [agg]               

        else:
            leafs = []
            if len(d['filePaths']) > 0:
                for fp in d['filePaths']:
                    de = self._defineDigitalEntity(d['name'], fp[7:], d['type'])
                    leafs.append(de)
            else:
                de = self._defineDigitalEntity(d['name'], fp[7:], d['type'])
                leafs.append(de)

            return leafs
     
 
    def _defineDigitalEntity(self, name, path, dtype, absolute=False):
 
        if self.conf.dryrun: 
            sumValue = ''
        else:
            absolutePath = path
            if not absolute:
                absolutePath = self.root + '/' + path
            sumValue = self.irodsu.getChecksum(absolutePath)
#TODO what if checksum is null?
        de = self._createUniqueNode("Digital Entity",name,path,sumValue,dtype)
        logger.debug('Created node: ' + str(de))
        self._defineResourceRelation(de, absolute)
        self._definePIDRelation(de, absolute)
        self._defineMasterRelation(de, absolute)
        self._defineReplicaRelation(de, absolute)
        self._defineOwnershipRelation(de, absolute)
        return de


    def _definePIDRelation(self, de, absolute=False):

        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+","
                   "UNIQUELY_IDENTIFIED_BY,persistent_identifier]")
            return True

        path = de.properties["location"]
        sumValue = de.properties["checksum"]
        absolutePath = path
        if not absolute:
            absolutePath = self.root + '/' + path
        pids = self.irodsu.getMetadata(absolutePath, 'PID')
        if pids and len(pids) > 0:
            pidNode = Node("Persistent Identifier", value = pids[0],
                                                    checksum = sumValue)
            de_is_uniquely_identified_by_pid = Relationship(de,
                                                            "UNIQUELY_IDENTIFIED_BY",
                                                            pidNode)
            self.graph.create_unique(de_is_uniquely_identified_by_pid)
            logger.debug('Created relation: ' + str(de_is_uniquely_identified_by_pid))
            return True
    
        return False


    def _defineMasterRelation(self, de, absolute=False):

        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+","
                   "IS_MASTER_OF,replica]")
            return True

        path = de.properties["location"]
        absolutePath = path
        if not absolute:
            absolutePath = self.root + '/' + path
        replicas = self.irodsu.getMetadata(absolutePath, 'Replica')       
        for rpointer in replicas: 
            po = self._createPointer('iRODS', rpointer)
            de_is_master_of_po = Relationship(de, "IS_MASTER_OF", po)
            self.graph.create_unique(de_is_master_of_po)
            logger.debug('Created relation: ' + str(de_is_master_of_po))
            return True

        return False


    def _defineReplicaRelation(self, re, absolute=False):

        if self.conf.dryrun:
            print ("create the graph relation ["+str(re)+","
                   "IS_REPLICA_OF,replica]")
            return True

        parent = None
        path = re.properties["location"]
        absolutePath = path
        if not absolute:
            absolutePath = self.root + '/' + path
        masters = self.irodsu.getMetadata(absolutePath, 'ROR')
        if masters and len(masters) > 0:
            master = masters[0]
            parents = self.irodsu.getMetadata(absolutePath, 'PPID')
            if parents and len(parents) > 0:
                parent = parents[0]
        else:
            return False

        po = self._createPointer('unknown', master)
        re_is_replica_of_po = Relationship(re, "IS_REPLICA_OF", po)
        re_is_replica_of_po.properties["relation"] = 'ROR'
        self.graph.create_unique(re_is_replica_of_po)
        logger.debug('Created relation: ' + str(re_is_replica_of_po))
        if parent:
            po = self._createPointer('unknown', parent)
            re_is_replica_of_po = Relationship(re, "IS_REPLICA_OF", po)
            re_is_replica_of_po.properties["relation"] = 'PPID'
            self.graph.create_unique(re_is_replica_of_po)
            logger.debug('Created relation: ' + str(re_is_replica_of_po))

        return True


    def _defineOwnershipRelation(self, de, absolute=False):
      
        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+",IS_OWNED_BY,"
                                               "b2safe_owner_name]")
            return True
 
        path = de.properties["location"]
        absolutePath = path
        if not absolute:
            absolutePath = self.root + '/' + path
        owners = self.irodsu.getOwners(absolutePath)
        logger.debug('Got the list of owners: ' + str(owners))
        if owners:
            for owner in owners:
                person = self.graph.merge_one("Person", "name", owner)
                logger.debug('Got the person: ' + str(person))
                person_is_defined_in_zone = Relationship(person, "IS_DEFINED_IN",
                                                         self.zone)
                self.graph.create_unique(person_is_defined_in_zone)
                logger.debug('Created relation: ' + str(person_is_defined_in_zone))
                node_is_owned_by_person = Relationship(de, "IS_OWNED_BY", person)
                self.graph.create_unique(node_is_owned_by_person)
                logger.debug('Created relation: ' + str(node_is_owned_by_person))
            return True
        return False


    def _defineResourceRelation(self, de, absolute=False):

        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+",IS_STORED_IN,"
                                               "b2safe_resource_name]")
            return True

        path = de.properties["location"]
        absolutePath = path
        if not absolute:
            absolutePath = self.root + '/' + path
        resources = self.irodsu.getResources(absolutePath)
        if resources:
            for res in resources:
                resN = self.graph.find_one('Resource', 'name', res)
                if resN:
                    de_is_stored_in_res = Relationship(de, "IS_STORED_IN", resN)
                    self.graph.create_unique(de_is_stored_in_res)
                    logger.debug('Created relation: ' + str(de_is_stored_in_res))
            return True
        return False


    def _createUniqueNode(self, eudat_type, name, path, checksum, d_type):
   
        
        entityNew = Node(eudat_type, location = path,
                                     name = name,
                                     checksum = checksum,
                                     nodetype = d_type)
        if self.conf.dryrun: 
            print ("create the graph node ["+str(entity)+"]")
        else:
            if len(path) > 0:
                entity = self.graph.find_one(eudat_type, "location", path)
            else:
                entity = self.graph.find_one(eudat_type, "name", name)
            if entity is None:
                entity = entityNew  
            self.graph.create(entity)
            logger.debug('Entity created: ' + str(entity))

        return entity


    def _createPointer(self, pointer_type, value):

        hashVal = hashlib.md5(value).hexdigest()
        pointerNew = Node('Pointer', type = pointer_type,
                                  value = value,
                                  name = hashVal)
        if self.conf.dryrun:
            print ("create the graph node ["+str(pointer)+"]")
        else:
            pointer = self.graph.find_one('Pointer', "name", hashVal)
            if pointer is None:
                pointer = pointerNew
            self.graph.create(pointer)
            logger.debug('Created pointer: ' + str(pointer))

        return pointer


################################################################################
# Configuration Class #
################################################################################
 
class Configuration():
    """ 
    Get properties from filesystem
    """

    def __init__(self, conffile, debug, dryrun, logger):
   
        self.conffile = conffile
        self.debug = debug
        self.dryrun = dryrun
        self.logger = logger
        self.log_level = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, \
                          'ERROR': logging.ERROR, 'WARNING': logging.WARNING, \
                          'CRITICAL': logging.CRITICAL}

    def parseConf(self):
        """Parse the configuration file."""

        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(open(self.conffile))
        
        logfilepath = self._getConfOption('Logging', 'log_file')
        loglevel = self._getConfOption('Logging', 'log_level')
        if self.debug:
            loglevel = 'DEBUG'
        logger.setLevel(self.log_level[loglevel])
        rfh = logging.handlers.RotatingFileHandler(logfilepath, \
                                                   maxBytes=8388608, \
                                                   backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: '
                                    + '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)
        
        self.graphdb_addr = self._getConfOption('GraphDB', 'address')
        self.graphdb_user = self._getConfOption('GraphDB', 'username')
        self.graphdb_passwd = self._getConfOption('GraphDB', 'password')
        self.graphdb_path = self._getConfOption('GraphDB', 'path')

        self.irods_zone_name = self._getConfOption('iRODS', 'zone_name')
        self.irods_zone_ep = self._getConfOption('iRODS', 'zone_ep')
        self.irods_res = self._getConfOption('iRODS', 'resources')
        self.irods_home_dir = self._getConfOption('iRODS', 'irods_home_dir')
        self.irods_debug = self._getConfOption('iRODS', 'irods_debug', True)

        
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
            self.logger.warning('missing parameter %s:%s' % (section,option))
            return None


################################################################################
# B2SAFE GraphDB client Command Line Interface #
################################################################################

def sync(args):

    configuration = Configuration(args.confpath, args.debug, args.dryrun, logger)
    configuration.parseConf();
    path = args.path.rsplit('/',1)[0]
    gdbc = GraphDBClient(configuration, path)
     
    logger.info("Sync starting ...")
    mp = manifest.MetsParser(configuration, logger)
    logger.info("Reading METS manifest ...")
    irodsu = manifest.IRODSUtils(configuration.irods_home_dir, logger,
                                 configuration.irods_debug)
    xmltext = irodsu.getFile(args.path + '/manifest.xml')
    structuralMaps = mp.parse(xmltext)
    for smap in structuralMaps:
        gdbc.push(smap)
    logger.info("Sync completed")
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='B2SAFE graphDB client')
    parser.add_argument("confpath", help="path to the configuration file")
    parser.add_argument("-dbg", "--debug", action="store_true", 
                        help="enable debug")
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="run without performing any real change")
    parser.add_argument("path", help="irods path to the data")

    parser.set_defaults(func=sync) 

    args = parser.parse_args()
    args.func(args)
