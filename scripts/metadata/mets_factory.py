#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import argparse
import logging
import logging.handlers
import ConfigParser
import pprint
import os
import xml.dom.minidom
import uuid
import json
import fnmatch
import tempfile
import re

from manifest import IRODSUtils
from manifest.libmets import *

logger = logging.getLogger('GraphDBClient')

class Collection():


    def __init__(self, config, logger):

        self.conf = config
        self.logger = logger
       
   
    def traverse(self, rootdir, absolute=True):
        """
        Creates a nested dictionary that represents the folder structure of 
        rootdir
        """
        self.logger.info('Traversing the path: ' + rootdir)
        dir = {}
        rootdir = rootdir.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        for path, dirs, files in os.walk(rootdir):
            self.logger.debug('Walking through the path: ' + path)
            if absolute:
                self.logger.debug('Using the absolute path as key')
                folders = []
                pparent = path
                while pparent != path[:start-1]:
                    folders.append(pparent)
                    pparent, pchild = pparent.rsplit(os.sep,1)
                folders.reverse()
            else:
                self.logger.debug('Using just the name as key')
                folders = path[start:].split(os.sep)
            parent = reduce(dict.get, folders[:-1], dir)
            parent[folders[-1]] = {'__files__': files}
        return dir


class MetsManifest():


    def __init__(self, ftree, config, logger):

        self.conf = config
        self.logger = logger 

        mf = mets(ID="_EUDATMETS_" + str(uuid.uuid4()), 
                  LABEL="EUDAT METS document")
        self.logger.debug('Building the METS file section')
        mf.fileSec = CTD_ANON_3()
        root = ''
        self.fileMap = self.buildGroupType(ftree, mf.fileSec.fileGrp, root)
        self.logger.debug('fileMap: ' + pprint.pformat(self.fileMap))
        self.logger.debug('Loading the metadata map from file {}'.format(
                          self.conf.md_jsonld_file))
        with open(self.conf.md_jsonld_file, 'r') as f:
            collStruct = json.load(f)
        self.logger.debug('Building the METS structural map section')
        rootName = ftree.keys()[0] + '_' + str(uuid.uuid4())
        smap = self.buildStructMap(rootName, collStruct)
        mf.structMap.append(smap)
        self.manifest = mf

   
    def getManifest(self):
        
        return self.manifest
 

    def buildGroupType(self, dirs, fileGrp, root):
        """Builds the METS section fileSec and return the mapping between
        the path of the file and the METS ID
        """
        fileMap = {}
        self.logger.debug('Building the METS fileGrpType')
        for coll in dirs:
            self.logger.debug('Processing dir: {}'.format(coll))
            if not self.conf.abs_path:
                # the path are absolute
                parent = root + '/' + coll
                groupId = coll + '_' + str(uuid.uuid4())
            else:
                # the path are relative
                parent = coll
                groupId = coll.rsplit('/', 1)[1] + '_' + str(uuid.uuid4())
            fgrp = fileGrpType(ID=groupId)
            fgrp_files = fileGrpType(ID=groupId+'__files__')
            for fp in dirs[coll]['__files__']:
                # loop over the files of the collection
                fileId = fp + '_' + str(uuid.uuid4())
                ft = fileType(ID=fileId)
                # create a METS element FLocat
                loc = CTD_ANON_19(LOCTYPE='URL')
                loc.type= 'simple'
                loc.href = 'file:/' + parent + '/' + fp
                ft.FLocat.append(loc)
                fgrp_files.append(ft)
                # create the map between file location and id
                fileMap[loc.href[7:]] = fileId
            fgrp.append(fgrp_files)
            if len(dirs[coll]) > 1:
                # there are also subdirs
                del dirs[coll]['__files__']
                fm = self.buildGroupType(dirs[coll], fgrp, parent)
                # merge the map dictionaries
                temp = fm.copy()
                temp.update(fileMap)
                fileMap = temp
            fileGrp.append(fgrp)

        return fileMap


    def buildStructMap(self, rootName, collStruct):
        """Builds the METS section structMap and return it
        """
        self.logger.debug('Building the METS structMapType')  
        # initialize the structural map section
        smap = structMapType(TYPE="Relational")
        divMain = divType(LABEL=rootName, TYPE="digitalCollection")
        temp_div = {}
        temp_rel = {}
        future_rel = {}
        processedPaths = []
        # loop over the metadata description of the collection provided 
        # as a jsonld doc
        for entity in collStruct['Structure']:

            self.logger.debug('Processing the jsonld entity: {}'.format(
                              pprint.pformat(entity)))
            normPath = entity['path'][2:]
            self.logger.debug('with path: ' + normPath)
#            pathSubSet = fnmatch.filter(self.fileMap.keys(), normPath)
            pathSubSet = self.patternMatch(normPath, self.fileMap.keys())
            self.logger.debug('which matches the following patterns: ' 
                              + pprint.pformat(pathSubSet.keys()))
            processedPaths += pathSubSet.keys()
            for path in pathSubSet.keys():
                self.entityRelMgmt(path, entity, pathSubSet[path], temp_div, 
                                   temp_rel, future_rel)

        divMainList = []
        # for each entity 
        for p in temp_div:
            # check if it is involved in relations
            if p in future_rel:
                # and with which other entities
                for relPath in future_rel[p]:
                    # find the related mets div and avoid to add it multiple times.
                    if (relPath in temp_rel 
                        and temp_rel[relPath] not in divMainList):
                        divMain.append(temp_rel[relPath])
                        divMainList.append(temp_rel[relPath])
            # otherwise just add a single entity
            elif p not in temp_rel.keys():
                divMain.append(temp_div[p])

        # apply defaults to remaining entities, not explicitly considered in the
        # metadata mapping
        pp = set(processedPaths)
        leftPaths = [x for x in self.fileMap.keys() if x not in pp]
        for path in leftPaths:
            divMain.append(self.divBuilder(self.conf.format_default, 
                                           self.conf.type_default, path))
    
        smap.append(divMain)
        return smap


    def divBuilder(self, label, etype, path):
 
        self.logger.debug('divBuilder for path: {}'.format(path))
        div = divType(LABEL=label, TYPE=etype)
        fptr = CTD_ANON_13(FILEID=self.fileMap[path])
        div.fptr.append(fptr)
        return div


    def entityRelMgmt(self, normPath, entity, templateDict, divDict, relDict, 
                      placeHolderDict):

        # for each path a mets div is created and stored in a temp list
        div = self.divBuilder(entity['format'], entity['type'], normPath)
        divDict[normPath] = div
        if 'isRelatedTo' in entity.keys():
            # analyze the relations of this entity with others
            label = 'rel_' + str(uuid.uuid4())
            divRel = divType(LABEL=label, TYPE="entityRelation")
            divRel.append(div)
            for relation in entity['isRelatedTo']:
                normPathRel = relation['@id'][2:]
                if len(templateDict) > 0:
                    for tkey in templateDict.keys():
                        normPathRel = normPathRel.replace('${'+ tkey +'}',
                                                          templateDict[tkey])
                print 'normPathRel: ' + normPathRel
                pathSubSet = fnmatch.filter(self.fileMap.keys(), normPathRel)
                for path in pathSubSet:
                    if path in divDict.keys():
                    # if the entity is associated to an already 
                    # defined mets div, then put the div inside 
                    # the same div container
                        divRel.append(divDict[path])
                    # anyway store the relation for later checks
                    if path in placeHolderDict:
                        placeHolderDict[path].append(normPath)
                    else:
                        placeHolderDict[path] = [normPath]
            relDict[normPath] = divRel
        # if this entity does not provide its own relations, check if 
        # is related to previously defined entities.
        if normPath in placeHolderDict.keys():
            for relatedPath in placeHolderDict[normPath]:
                relDict[relatedPath].append(div)        


    def patternMatch(self, pattern, targets):

        transRegex = fnmatch.translate(pattern)
        print 'transRegex: ' + transRegex
        templateNames = re.findall(r'\$\{(\w+)\}', pattern)
        if templateNames:
            for tNames in templateNames:
                transRegex = transRegex.replace('\$\{'+ tNames +'\}', r'(?P<'+ tNames +'>\w+)')
                print 'transRegex: ' + transRegex
        pathRegex = transRegex + '$'
        template = re.compile(pathRegex)
        pathSubSet = {}
        for item in targets:
            m = template.match(item)
            if m:
                pathSubSet[item] = {}
                for tNames in templateNames:
                    print tNames + ' = ' + str(m.group(tNames))
                    pathSubSet[item][tNames] = m.group(tNames)

        return pathSubSet 


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
       
        self.abs_path = self._getConfOption('METS', 'abs_path', True)
        self.md_jsonld_file = self._getConfOption('METS', 'md_jsonld_file')
        self.format_default = self._getConfOption('METS', 'format_default')
        self.type_default = self._getConfOption('METS', 'type_default')
      
        self.irods_home_dir = self._getConfOption('iRODS', 'irods_home_dir')
        self.irods_debug = self._getConfOption('iRODS', 'irods_debug', True)
        self.irods_resource = self._getConfOption('iRODS', 'irods_resource')

        
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
# METS Factory Command Line Interface #
################################################################################

def writeMets(args):

    configuration = Configuration(args.confpath, args.debug, args.dryrun, 
                                  logger)
    configuration.parseConf();
    logger.info("Starting ...")

    logger.info('Parsing the collection tree ...')
    if args.filesystem:
        logger.debug('on file system')
        coll = Collection(configuration, logger)
        res = coll.traverse(args.filesystem[0], configuration.abs_path)
    else:
        logger.debug('on iRODS namespace')
        irodsu = IRODSUtils(configuration.irods_home_dir, logger,
                            configuration.irods_debug)
        rc, res = irodsu.deepListDir(args.irods[0], configuration.abs_path)
    logger.debug('Collection tree:\n{}'.format(pprint.pformat(res)))

    logger.info('Building the METS manifest document')
    mm = MetsManifest(res, configuration, logger)
    manifest = mm.getManifest()
    dom = xml.dom.minidom.parseString(manifest.toxml("utf-8"))
    manifestXML = dom.toprettyxml(indent="  ", encoding="utf-8")

    if args.dryrun:
        print manifestXML
    else:
        logger.info('Writing the manifest to a file')
        if args.filesystem:
            target = args.filesystem[0] + os.sep + 'manifest.xml'
            logger.info('in the file system: {}'.format(target))
            with open(target, 'w') as f:
                f.write(manifestXML)
        else:
            temp = tempfile.NamedTemporaryFile()
            try:
                temp.write(manifestXML)
                target = args.irods[0] + '/' + 'manifest.xml'
                logger.info('in the irods namespace: {}'.format(target))
                irodsu.putFile(temp.name, target, configuration.irods_resource)
            finally:
                temp.close()

    logger.info("Completed")
    

if __name__ == "__main__":

    mfact = argparse.ArgumentParser(description='METS factory')
    mfact.add_argument("confpath", help="path to the configuration file")
    mfact.add_argument("-dbg", "--debug", action="store_true", 
                       help="enable debug")
    mfact.add_argument("-d", "--dryrun", action="store_true",
                       help="run without performing any real change")

    input_group = mfact.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-i", "--irods", nargs=1, help="irods path")
    input_group.add_argument("-f", "--filesystem", nargs=1, help="fs path")

    mfact.set_defaults(func=writeMets) 

    args = mfact.parse_args()
    args.func(args)
