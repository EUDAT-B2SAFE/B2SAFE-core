#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import argparse
import logging
import logging.handlers
import ConfigParser
import manifest
import pprint
import hashlib
import uuid

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
        self.root = rootPath.rsplit('/',1)[0]
        self.collPath = rootPath
        # initializing the iRODS commands
        self.irodsu = manifest.IRODSUtils(self.conf.irods_home_dir,
                                          logger,
                                          self.conf.irods_debug)
        # authentication
        logger.info("Connecting to " + self.conf.graphdb_addr
                    + " with user " + self.conf.graphdb_user)    

        authenticate(self.conf.graphdb_addr, self.conf.graphdb_user, 
                     self.conf.graphdb_passwd)
        logger.debug("Authenticated, now connecting ...")
        self.graph = Graph( self.conf.graphdb_scheme + "://" 
                          + self.conf.graphdb_addr + self.conf.graphdb_path)
        # set up of the nodes related to the local B2SAFE service
        logger.debug("Searching if the initial nodes have been already created")
        self.zone = self.graph.find_one("Zone", "name", self.conf.irods_zone_name)
        if self.zone is None:
            logger.info('Node "Zone" ' + self.conf.irods_zone_name
                      + ' not found, so it will be created')
            try:
                self.graph.schema.create_uniqueness_constraint("DigitalEntity", 
                                                               "name")
                self.graph.schema.create_uniqueness_constraint("Aggregation",
                                                               "name")
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

#TODO this function is just a placeholder for further development.
#     The real function should be able to find the differences 
#     and add/remove nodes to/from the graph according to them.
    def analyze(self, structuralMap):
        """It performs a comparison between the existing graph 
           and the input mnifest doc.
        """
        logger.info('Compare the manifest with the DB graph')
        self._analyzeStructuralMap(structuralMap)


    def push(self, structuralMap):
        """It uploads new data to the graphDB
        """
        logger.info('Start to upload the new metadata to the Graph DB')
        structList = self._structRecursion(structuralMap)


    def _analyzeStructuralMap(self, struct):

        # start to look if the node has nested objects
        if len(struct['nestedObjects']) > 0:
            agg = {'label':'Aggregation', 'location':'', 'name':struct['name'],
                   'checksum':'', 'nodetype':struct['type']}
            graphAgg = self.graph.find_one('Aggregation', 'name', struct['name'])
            if not graphAgg:
                print 'Node Aggregation [{}] is missing'.format(struct['name'])
                return [None]
            else:
                print 'Node Aggregation [{}] found'.format(struct['name'])
            # if the aggregation has a file path, it means that it is a package
            if len(struct['filePaths']) > 0:
                if len(struct['filePaths']) == 1:
                    path = struct['filePaths'][0]
                    agg['location'] = path[7:]
                    absolutePath = self.root + '/' + path[7:]
                    sumValue = self.irodsu.getChecksum(absolutePath)
                    agg['checksum'] = sumValue
                    self._analyzeOwnershipRel(absolutePath, graphAgg)
                    self._analyzePIDRel(absolutePath, graphAgg)
                    self._analyzeResourceRel(absolutePath, graphAgg)
                    self._analyzeMasterRel(absolutePath, graphAgg)
                    self._analyzeReplicaRel(absolutePath, graphAgg)
                # the manifest supports multiple file paths, 
                # but they are not yet supported by this script
                else:
                    logger.warning('multiple file paths not allowed')
            # check the nested objects in a recursive way
            for elem in struct['nestedObjects']:
                nodes = self._analyzeStructuralMap(elem)
                for n in nodes:
                    self._searchRelationship(n, 'BELONGS_TO', graphAgg,       
                                             graphAgg.properties['name'])
                        
            return [graphAgg]
        # if nested objects are not present, then this is a leaf in the tree
        else:
            leafs = []
            # if there is at least one path, the leaf is a Digital Entity
            if len(struct['filePaths']) > 0:
                for fp in struct['filePaths']:
                    absolutePath = self.root + '/' + fp[7:]
                    sumValue = self.irodsu.getChecksum(absolutePath)
                    de = {'location':fp[7:], 'name':struct['name'], 
                          'checksum':sumValue, 'nodetype':struct['type']}
                    graphEnt = self.graph.find_one('DigitalEntity', 'location', 
                                                                    fp[7:])
                    if not graphEnt:
                        print 'Node Digital Entity [{}] is missing'.format(fp[7:])
                    else:
                        print 'Node Digital Entity [{}] found'.format(fp[7:])
                        self._analyzeOwnershipRel(absolutePath, graphEnt)
                        self._analyzePIDRel(absolutePath, graphEnt)
                        self._analyzeResourceRel(absolutePath, graphEnt)
                        self._analyzeMasterRel(absolutePath, graphEnt)
                        self._analyzeReplicaRel(absolutePath, graphEnt)
                    leafs.append(graphEnt)
            # if there is not a path, the leaf is an aggregation, even if an empty one.
            else:
                agg = {'location':'', 'name':struct['name'], 'checksum':'',
                      'nodetype':struct['type']}
                graphAgg = self.graph.find_one('Aggregation', 'name', struct['name'])
                if not graphAgg:
                    print 'Node Aggregation [{}] is missing'.format(struct['name'])
                else:
                    print 'Node Aggregation [{}] found'.format(struct['name'])                
                leafs.append(graphAgg)

            return leafs
        
     
    def _searchRelationship(self, start, rel, end, endProp):

        graphRel = self.graph.match_one(start_node=start, rel_type=rel, 
                                        end_node=end)
        message = 'Relationship [({},{}) {} {}]'.format(start.properties['name'], 
                   start.properties['location'], rel, endProp)
        if not graphRel:
            print message + ' is missing'
        else:
            print message + ' found'


    def _analyzeOwnershipRel(self, absolutePath, de):

        owners = self.irodsu.getOwners(absolutePath)
        if owners:
            for owner in owners:
                graphPers = self.graph.find_one('Person', 'name', owner)
                if not graphPers:
                    print 'Node Person [{}] is missing'.format(owner)
                else:
                    print 'Node Person [{}] found'.format(owner)

                    self._searchRelationship(de, 'IS_OWNED_BY', graphPers, 
                                             graphPers.properties['name'])


    def _analyzePIDRel(self, absolutePath, de):

        pids = self.irodsu.getMetadata(absolutePath, 'PID')
        if pids and len(pids) > 0:
            graphPid = self.graph.find_one('PersistentIdentifier', 'value', pids[0])
            if not graphPid:
                print 'Node PersistentIdentifier [{}] is missing'.format(pids[0])
            else:
                print 'Node PersistentIdentifier [{}] found'.format(pids[0])

                self._searchRelationship(de, 'UNIQUELY_IDENTIFIED_BY', graphPid,
                                         graphPid.properties['value'])


    def _analyzeMasterRel(self, absolutePath, de):

        replicas = self.irodsu.getMetadata(absolutePath, 'Replica')
        for rpointer in replicas:
            graphPo = self.graph.find_one('Pointer', 'value', rpointer)
            if not graphPo:
                print 'Node Pointer [{}] is missing'.format(rpointer)
            else:
                print 'Node Pointer [{}] found'.format(rpointer)
                self._searchRelationship(de, 'IS_MASTER_OF', graphPo,
                                         graphPo.properties['value'])


    def _analyzeReplicaRel(self, absolutePath, de):

        parent = None
        masters = self.irodsu.getMetadata(absolutePath, 'ROR')
        if masters and len(masters) > 0:
            master = masters[0]
            parents = self.irodsu.getMetadata(absolutePath, 'PPID')
            if parents and len(parents) > 0:
                parent = parents[0]
        else:
            return False

        graphMas = self.graph.find_one('Pointer', 'value', master)
        if not graphMas:
            print 'Node Pointer [{}] is missing'.format(master)
        else:
            print 'Node Pointer [{}] found'.format(master)
            self._searchRelationship(de, 'IS_REPLICA_OF', graphMas,
                                     graphMas.properties['value'])
        if parent:
            graphPar = self.graph.find_one('Pointer', 'value', parent)
            if not graphMas:
                print 'Node Pointer [{}] is missing'.format(parent)
            else:
                print 'Node Pointer [{}] found'.format(parent)
                self._searchRelationship(de, 'IS_REPLICA_OF', graphPar,
                                         graphPar.properties['value'])


    def _analyzeResourceRel(self, absolutePath, de):

        resources = self.irodsu.getResources(absolutePath)
        if resources:
            for res in resources:
                resN = self.graph.find_one('Resource', 'name', res)
                if resN:
                    self._searchRelationship(de, 'IS_STORED_IN', resN,
                                             resN.properties['name'])

# functions related to the upload of the data to the graph DB.

    def _structRecursion(self, d):

        # start to look if the node has nested objects
        if len(d['nestedObjects']) > 0:

            # add the root path of the collection. 
            # It should happen just once, for the root collection,
            # the only one of the type 'digitalCollection'
            if (d['type'] == 'digitalCollection'):
                path = self.collPath
            else:
                path = ''
            sumValue = ''
            agg = self._createUniqueNode("Aggregation", d['name'],
                                                        path[7:],
                                                        sumValue,
                                                        d['type'])
            # if the aggregation has a file path, it means that it is a package
            if len(d['filePaths']) > 0:
                if (len(d['filePaths']) == 1 
                    and len(d['filePaths'][d['filePaths'].keys()[0]]) == 1):
                    pathId = d['filePaths'].keys()[0]
                    path = d['filePaths'][pathId][0]
                    if self.conf.dryrun: 
                        print "get the checksum based on path: " + str(path)
                    else:
                        agg.properties['location'] = path[7:]
                        agg.push()
                        logger.debug('Updated location of entity: ' + str(agg))
                        agg = self._defineDigitalEntity(None, path[7:], 
                                                        d['type'], d['name'], agg)
                # the manifest supports multiple file paths, 
                # but they are not yet supported by this script                
                else:                
                    logger.warning('multiple file paths not allowed')
            # check the nested objects in a recursive way
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
        # if nested objects are not present, then this is a leaf in the tree
        else:
            leafs = []
            if len(d['filePaths']) > 0:
                for fid in d['filePaths']:
                    for fp in d['filePaths'][fid]:
                        de = self._defineDigitalEntity(d['name'], fp[7:], 
                                                       d['type'], fid)
                        leafs.append(de)
            # if there is not a path, the leaf is an aggregation, even if an empty one.
            else:
                path = ''
                sumValue = ''
                agg = self._createUniqueNode("Aggregation", d['name'],
                                                            path[7:],
                                                            sumValue,
                                                            d['type'])
                leafs.append(agg)

            return leafs
     
 
    def _defineDigitalEntity(self, fmt, path, dtype, name, de=None, absolute=False):
 
        absolutePath = path
        # if the path of the files in the manifest a relative,
        # then the absolute path has to be built to get the file properties.
        if not absolute:
            absolutePath = self.root + '/' + path
        # calculate the checksum
        if self.conf.dryrun: 
            sumValue = ''
        else:
            sumValue = self.irodsu.getChecksum(absolutePath)
        if de is not None:
            if sumValue:
                de.properties['checksum'] = sumValue
                de.push()
                logger.debug('Updated checksum of entity: ' + str(de))
#TODO what if checksum is null?
        else:
            # build the digital entity
            de = self._createUniqueNode("DigitalEntity", name, path, sumValue,
                                                         dtype)
            de.properties['format'] = fmt
            if not self.conf.dryrun:
                de.push()
            logger.debug('Created node: ' + str(de))
        # check the entity relationships
        self._defineResourceRelation(de, absolutePath)
        self._definePIDRelation(de, absolutePath)
        self._defineMasterRelation(de, absolutePath)
        self._defineReplicaRelation(de, absolutePath)
        self._defineOwnershipRelation(de, absolutePath)
        return de


    def _definePIDRelation(self, de, absolutePath):

        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+","
                   "UNIQUELY_IDENTIFIED_BY,persistent_identifier]")
            return True

        path = de.properties["location"]
        sumValue = de.properties["checksum"]
        pids = self.irodsu.getMetadata(absolutePath, 'PID')
        if pids and len(pids) > 0:
            pidNode = Node("PersistentIdentifier", value = pids[0],
                                                   checksum = sumValue)
            de_is_uniquely_identified_by_pid = Relationship(de,
                                                            "UNIQUELY_IDENTIFIED_BY",
                                                            pidNode)
            self.graph.create_unique(de_is_uniquely_identified_by_pid)
            logger.debug('Created relation: ' + str(de_is_uniquely_identified_by_pid))
            return True
    
        return False


    def _defineMasterRelation(self, de, absolutePath):

        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+","
                   "IS_MASTER_OF,replica]")
            return True

        replicas = self.irodsu.getMetadata(absolutePath, 'Replica')       
        for rpointer in replicas: 
            po = self._createPointer('iRODS', rpointer)
            de_is_master_of_po = Relationship(de, "IS_MASTER_OF", po)
            self.graph.create_unique(de_is_master_of_po)
            logger.debug('Created relation: ' + str(de_is_master_of_po))
            return True

        return False


    def _defineReplicaRelation(self, re, absolutePath):

        if self.conf.dryrun:
            print ("create the graph relation ["+str(re)+","
                   "IS_REPLICA_OF,replica]")
            return True

        parent = None
        masters = self.irodsu.getMetadata(absolutePath, 'ROR')
        if masters and len(masters) > 0:
            master = masters[0]
            # check the parent pid only if the ROR is set
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


    def _defineOwnershipRelation(self, de, absolutePath):
      
        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+",IS_OWNED_BY,"
                                               "b2safe_owner_name]")
            return True
 
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


    def _defineResourceRelation(self, de, absolutePath):

        if self.conf.dryrun:
            print ("create the graph relation ["+str(de)+",IS_STORED_IN,"
                                               "b2safe_resource_name]")
            return True

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
            print ("create the graph node ["+str(entityNew)+"]")
            return entityNew
        else:
            # check if the node is already stored in the graph DB
            # basing the search on the property which is unique: the name
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
        
        self.graphdb_scheme = self._getConfOption('GraphDB', 'scheme')
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
    gdbc = GraphDBClient(configuration, args.path)
     
    logger.info("Sync starting ...")
    mp = manifest.MetsParser(configuration, logger)
    logger.info("Reading METS manifest ...")
    irodsu = manifest.IRODSUtils(configuration.irods_home_dir, logger,
                                 configuration.irods_debug)
    xmltext = irodsu.getFile(args.path + '/manifest.xml')
    structuralMaps = mp.parse(xmltext)
    for smap in structuralMaps:
        if args.analyze:
            gdbc.analyze(smap)
        else:
            gdbc.push(smap)
    logger.info("Sync completed")
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='B2SAFE graphDB client')
    parser.add_argument("confpath", help="path to the configuration file")
    parser.add_argument("-dbg", "--debug", action="store_true", 
                        help="enable debug")
    parser.add_argument("-d", "--dryrun", action="store_true",
                        help="run without performing any real change")
    parser.add_argument("-a", "--analyze", action="store_true",
                        help="compare the manifest with the DB graph")
    parser.add_argument("path", help="irods path to the data")

    parser.set_defaults(func=sync) 

    args = parser.parse_args()
    args.func(args)
