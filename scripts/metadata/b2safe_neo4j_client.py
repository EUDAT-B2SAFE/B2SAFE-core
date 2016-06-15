#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import argparse
import logging
import logging.handlers
import ConfigParser
import manifest
import pprint

from py2neo import Graph, Node, Relationship, authenticate, GraphError


logger = logging.getLogger('GraphDBClient')

##################################################
# Person(name:'guybrush')
# MetaData (Structural|Descriptive|Administrative)
# Data ()
# Composite ()
# Person - [:IS_DEFINED_IN] -> Zone
# DigitalEntity (EudatChecksum:'xyz', location:'/Zone/path/to/file')
# DigitalEntity - [:IS_OF_TYPE] -> MetaData|Data|Composite
# DigitalEntity - [:STORED_IN] -> Resource - [:IS_AVAILABLE_IN] -> Zone
# DigitalEntity - [:IS_OWNED_BY] -> Person
# DigitalEntity - [:BELONGS_TO] -> Aggregation
# DigitalEntity - [:IS_REPLICA_OF{PPID, ROR}] -> DigitalEntity
# DigitalEntity - [:UNIQUELY_IDENTIFIED_BY] -> PID{EudatChecksum:'xyz'}

class GraphDBClient():
    
    def __init__(self, conf):
        """
        Graph initialization
        """
    
        self.conf = conf

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

        logger.info("Initializing data and metadata nodes")
        
        metaStruct = Node("Metadata", "Structural")
        metaDescr = Node("Metadata", "Descriptive")
        metaAdmin = Node("Metadata", "Administrative")
        data = Node("Data")
        composite = Node("Composite")
 
        cquery = "MATCH n WHERE n:Metadata AND n:Structural RETURN n"
        rec_list = self.graph.cypher.execute(cquery)
        if rec_list.one:
            metaStruct = rec_list.one
        else:
            self.graph.create(metaStruct)
        cquery = "MATCH n WHERE n:Metadata AND n:Descriptive RETURN n"
        rec_list = self.graph.cypher.execute(cquery)
        if rec_list.one:
            metaDescr = rec_list.one
        else:
            self.graph.create(metaDescr)
        cquery = "MATCH n WHERE n:Metadata AND n:Administrative RETURN n"
        rec_list = self.graph.cypher.execute(cquery)
        if rec_list.one:
            metaAdmin = rec_list.one
        else:
            self.graph.create(metaAdmin)        

        if not self.graph.find_one("Data"):
            self.graph.create(data)
        if not self.graph.find_one("Composite"):
            self.graph.create(composite)

        self.eudat_type_map = { 'Descriptive': ['descriptive metadata entity'],
                                'Administrative': ['administrative metadata entity'],
                                'Structural': ['manifest'],
                                'Data': ['data entity'],
                                'Composite': ['mixed entity']
                              }

        self.eudat_type_node_map = { 'Descriptive': metaDescr,
                                     'Administrative': metaAdmin,
                                     'Structural': metaStruct,
                                     'Data': self.graph.find_one("Data"),
                                     'Composite': self.graph.find_one("Composite")
                                   }

# dynamic data ###################################

    def push(self, structuralMap):

        logger.info('Start to upload metadata to the Graph DB')
        structList = self._structRecursion(structuralMap)


    def _structRecursion(self, d):

        if len(d['nestedObjects']) > 0:

            path = ''
            sumValue = ''
            agg = self._createUniqueNode("Aggregation", d['name'],
                                                        path[6:],
                                                        sumValue,
                                                        d['type'])
            if len(d['filePaths']) > 0:
                if len(d['filePaths']) == 1:
                    path = d['filePaths'][0]
                    if self.conf.dryrun: 
                        print "get the checksum based on path: " + str(path)
                    else:
                        agg.properties['location'] = path[6:]
                        agg.push()
                        logger.debug('Updated location of entity: ' + str(agg))
                        sumValue = self.irodsu.getChecksum(path[6:])
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
                    de = self._defineDigitalEntity(d['name'], fp[6:], d['type'])
                    leafs.append(de)
            else:
                de = self._defineDigitalEntity(d['name'], fp[6:], d['type'])
                leafs.append(de)

            return leafs
     
 
    def _defineDigitalEntity(self, name, path, dtype):
 
        if self.conf.dryrun: 
            sumValue = ''
        else:
            sumValue = self.irodsu.getChecksum(path)
#TODO what if checksum is null?
        de = self._createUniqueNode("Digital Entity",name,path,sumValue,dtype)
        logger.debug('Created node: ' + str(de))
        self._defineTypeRelation(de)
        self._defineResourceRelation(de)
        self._definePIDRelation(de)
        self._defineOwnershipRelation(de)
        return de


    def _definePIDRelation(self, de):

        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+","
                   "UNIQUELY_IDENTIFIED_BY,persistent_identifier]")
            return True

        path = de.properties["location"]
        sumValue = de.properties["checksum"]
        pid = self.irodsu.getMetadata(path, 'PID')
        if pid:
            pidNode = Node("Persistent Identifier", value = pid['PID'],
                                                    checksum = sumValue)
            de_is_uniquely_identified_by_pid = Relationship(de,
                                                            "UNIQUELY_IDENTIFIED_BY",
                                                            pidNode)
            self.graph.create_unique(de_is_uniquely_identified_by_pid)
            logger.debug('Created relation: ' + str(de_is_uniquely_identified_by_pid))
            return True
    
        return False


    def _defineOwnershipRelation(self, de):
      
        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+",IS_OWNED_BY,"
                                               "b2safe_owner_name]")
            return True
 
        path = de.properties["location"]
        owners = self.irodsu.getOwners(path)
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


    def _defineResourceRelation(self, de):

        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+",IS_STORED_IN,"
                                               "b2safe_resource_name]")
            return True

        path = de.properties["location"]
        resources = self.irodsu.getResources(path)
        if resources:
            for res in resources:
                resN = self.graph.find_one('Resource', 'name', res)
                if resN:
                    de_is_stored_in_res = Relationship(de, "IS_STORED_IN", resN)
                    self.graph.create_unique(de_is_stored_in_res)
                    logger.debug('Created relation: ' + str(de_is_stored_in_res))
            return True
        return False


    def _defineTypeRelation(self, de):

        dtype = de.properties['nodetype']
        for eudat_type,type_list in self.eudat_type_map.items():
           if dtype in type_list:

               if self.conf.dryrun:
                   print ("create the graph relation ["+str(de)+","
                          "IS_OF_TYPE,"+eudat_type+"]")
                   return True

               tnode = self.eudat_type_node_map[eudat_type]
               de_is_of_type_tnode = Relationship(de, "IS_OF_TYPE", tnode)
               self.graph.create_unique(de_is_of_type_tnode)
               logger.debug('Created relation: ' + str(de_is_of_type_tnode))
               return True
        return False


    def _createUniqueNode(self, eudat_type, name, path, checksum, d_type):

        if self.conf.dryrun: 
            entity = Node(eudat_type, location = path,
                                      name = name,
                                      checksum = checksum,
                                      nodetype = d_type)
            print ("create the graph node ["+str(entity)+"]")
        else:

            if len(path) > 0:
                entity = self.graph.find_one(eudat_type, "location", path)
            else:
                entity = self.graph.find_one(eudat_type, "name", name)
            if entity is None:
                entity = Node(eudat_type, location = path,
                                          name = name,
                                          checksum = checksum,
                                          nodetype = d_type)
            self.graph.create(entity)
            logger.debug('Created entity: ' + str(entity))

        return entity

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
    gdbc = GraphDBClient(configuration)
     
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
