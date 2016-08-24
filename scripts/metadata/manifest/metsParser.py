#!/usr/bin/env python
# -*- python -*-

import ConfigParser
import argparse
import logging
import logging.handlers
import libmets
import pprint
import uuid

from nested_lookup import nested_lookup
from irodsUtility import *

logger = logging.getLogger('MetsParser')


###############################################################################
# METS parser Class #
###############################################################################


class MetsParser(object):
    """Class implementing a METS parser."""

    def __init__(self, conf, logger):
        """Initialize object with configuration parameters."""
        self.conf = conf
        self.logger = logger

    def _parseDivType(self, divElemList, fileGroups):
        """parse divType
        :rtype: dict
        :type divElemList: list
        """

        collectionObjs = []
        for div_element in divElemList:
            obj = {}
            self.logger.debug('DIV TYPE: ' + div_element.TYPE)
            obj_name = div_element.LABEL
            if div_element.LABEL is None:
                obj_name = ''
            obj['name'] = obj_name
            obj['type'] = div_element.TYPE
            filePaths = []
            for fptr_element in div_element.fptr:
                self.logger.debug('FPTR: ' + fptr_element.FILEID)
                pathList = self._pathListExtractor(fptr_element.FILEID,
                                                   fileGroups)
                filePaths += pathList
            obj['filePaths'] = filePaths
            obj['nestedObjects'] = self._parseDivType(div_element.div,
                                                      fileGroups)
            self.logger.debug(pprint.pformat(obj))
            collectionObjs.append(obj)

        return collectionObjs

    def _parseFileGrpType(self, fileGrpElemList):
        """parse fileGrpType
        :rtype: dict
        """

        fileGrpList = {}
        for fileGrp_element in fileGrpElemList:
            fileGrp = {}
            if fileGrp_element.ID is None:
                fileGrp_element.ID = 'GROUP_' + str(uuid.uuid4())
            self.logger.debug('File group ID: ' + fileGrp_element.ID)
            fileGrp['files'] = self._parseFileType(fileGrp_element.file)
            fileGrp['groups'] = self._parseFileGrpType(fileGrp_element.fileGrp)
            fileGrpList[fileGrp_element.ID] = fileGrp

        return fileGrpList

    def _parseFileType(self, fileElemList):
        """parse fileType
        :rtype: dict
        """

        collectionFiles = {}
        for file_element in fileElemList:
            fileElem = {}
            self.logger.debug('File ID: ' + file_element.ID)
            fileElem['locations'] = []
            fileElem['files'] = []
            for loc in file_element.FLocat:
                if loc.LOCTYPE == 'URL':
                    # TODO: validate here the path
                    fileElem['locations'].append(loc.href)

            fileElem['files'] = self._parseFileType(file_element.file)
            self.logger.debug(pprint.pformat(fileElem))
            collectionFiles[file_element.ID] = fileElem

        return collectionFiles

    def _pathListExtractor(self, fileId, fileGroups):
        "get the list of file paths under a single file ID"

        fileList = nested_lookup(fileId, fileGroups)
        self.logger.debug('file ID: ' + fileId)
        pathList = []
        for phisicalFileElement in fileList:
            pathList += phisicalFileElement['locations']
            for childKey, childValue in phisicalFileElement['files']:
                pathList += self._pathListExtractor(childKey,
                                                    phisicalFileElement['files'])
        self.logger.debug('Path list: ' + pprint.pformat(pathList))

        return pathList

    def parse(self, xmltext):
        "parse a METS document"

        mets = libmets.CreateFromDocument(xmltext)
        self.logger.debug(pprint.pformat('METS document: '
                                         + (mets.toxml("utf-8",
                                                       element_name='mets'))))
        groups = self._parseFileGrpType(mets.fileSec.fileGrp)
        collMaps = []
        for smap in mets.structMap:
            name = smap.div.LABEL
            if smap.div.LABEL is None:
                name = ''
            collectionObjs = self._parseDivType(smap.div.div, groups)

            filePaths = []
            for fptr_element in smap.div.fptr:
                self.logger.debug('FPTR: ' + fptr_element.FILEID)
                pathList = self._pathListExtractor(fptr_element.FILEID,
                                                   fileGroups)
                filePaths += pathList

            collectionMap = {'name': name,
                             'type': smap.div.TYPE,
                             'filePaths': filePaths,
                             'nestedObjects': collectionObjs}
            self.logger.debug('Structural map: '
                              + pprint.pformat(collectionMap))
            collMaps.append(collectionMap)

        return collMaps


###############################################################################
# Configuration Class #
###############################################################################

class Configuration():
    """
    Get properties from filesystem
    """

    def __init__(self, file, logger, debug=False):

        self.file = file
        self.logger = logger
        self.log_level = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG,
                          'ERROR': logging.ERROR, 'WARNING': logging.WARNING,
                          'CRITICAL': logging.CRITICAL}
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(open(self.file))

        logfilepath = self._getConfOption('Logging', 'log_file')
        loglevel = self._getConfOption('Logging', 'log_level')
        if debug:
            logger.setLevel(self.log_level['DEBUG'])
        else:
            logger.setLevel(self.log_level[loglevel])
        rfh = logging.handlers.RotatingFileHandler(logfilepath,
                                                   maxBytes=8388608,
                                                   backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: '
                                      + '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)

        self.irods_home_dir = self._getConfOption('iRODS', 'irods_home_dir')
        self.irods_debug = self._getConfOption('iRODS', 'irods_debug', True)

    def _getConfOption(self, section, option, boolean=False):
        """
        get the options from the configuration file
        :type option: string
        """

        if self.config.has_option(section, option):
            opt = self.config.get(section, option)
            if boolean:
                if opt in ['True', 'true']:
                    return True
                else:
                    return False
            return opt
        else:
            self.logger.warning('missing parameter %s:%s' % (section, option))
            return None


###############################################################################
# EUDAT METS parser Command Line Interface #
###############################################################################

def metsToDict(args):
    configuration = Configuration(args.confpath, logger, args.debug)
    mp = MetsParser(configuration, logger)

    logger.info("Parsing METS manifest ...")
    if args.irods:
        irodsu = IRODSUtils(configuration.irods_home_dir, logger,
                            configuration.irods_debug)
        xmltext = irodsu.getFile(args.irods[0] + '/manifest.xml')
    else:
        xmltext = args.file.read()

    pprint.pprint(mp.parse(xmltext))
    logger.info("Parsing completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='EUDAT Mets parser.')
    parser.add_argument("confpath", default="NULL",
                        help="path to the configuration file")
    parser.add_argument("-d", "--debug", help="Show debug output",
                        action="store_true")

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-i", "--irods", nargs=1,
                             help="input irods METS file")
    input_group.add_argument("-f", "--file", type=file, help="input METS file")

    parser.set_defaults(func=metsToDict)

    args = parser.parse_args()
    args.func(args)
