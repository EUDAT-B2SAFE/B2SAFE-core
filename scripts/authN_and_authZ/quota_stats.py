#!/usr/bin/env python
# -*- python -*-

import argparse
import subprocess
import re
import logging
import logging.handlers
import json
import tempfile
import pprint

from utilities.mailSender import MailSender
from utilities.irodsUtility import *
from utilities.jsonUtility import *

logger = logging.getLogger('QuotaStats')

################################################################################
# Collection Quota Stats Class #
################################################################################
 
class QuotaStats():
    """Class implementing the computation of statistics about resource consumption."""

    
    def __init__( self, conf ):
        """Initialize object with configuration parameters."""
        
        self.conf = conf
        self.irodsu = IRODSUtils(self.conf.irods_home_dir, 'QuotaStats',
                                 self.conf.irods_debug)


    def _parseIrodsProj(self):
        """Internal: Parse the projects irods info."""
   
        irods_zones = self.irodsu.getIrodsZones()
        out = self.irodsu.listIrodsGroups()
        groups = {}
        for line in out.splitlines():
            group = {}
            out2 = self.irodsu.getIrodsGroup(line)
            group['members'] = []
            # add member list to each group, if the zone is remote, it is kept, otherwise it is dropped
            for row in out2.splitlines()[1:]:
                if (row and row.strip() != 'No rows found'):
                    logger.debug("row: %s", row)
                    [member,zone] = row.split('#')
                    if (irods_zones[zone]['zone_type'] == 'local'):
                        group['members'].append(member)
                    else:
                        group['members'].append(row)
            groups[line] = group
                  
        return groups


    def _parseUsageStats(self):
        """Internal: Parse the quota info file."""
     
        usage = {}
        try:
            filehandle = open(self.conf.stat_output_file,"r")
            usage = json.load(filehandle, object_hook=JSONUtils().decode_dict)
            filehandle.close()
        except Exception, e:
            logger.warning("problem while reading usage file %s", self.conf.stat_output_file)
            logger.warning("Error: %s", e)
            return None
                
        return usage


    def _writeUsageStats(self,usage):
        """Internal: Write the quota info to the file."""

        try:
            filehandle = open(self.conf.stat_output_file,"w")
            json.dump(usage, filehandle, indent=2, sort_keys=True)
            filehandle.close()
        except Exception, e:
            logger.error("problem while writing usage file %s", self.conf.stat_output_file)
            logger.error("Error: %s", e)
            return False
     
        return True


    def _getStorageInfo(self, query):
        """Internal: get the storage info from iRODS iCAT"""

        logger.debug("executing the following query: %s", query)
        [rc,out] = self.irodsu.queryIrodsIcat(query)
        if rc != 0:
            logger.error("Error: the query '%s' failed", query)
            return None
        [key,info] = out.split('=')
        info = info.replace("\n------------------------------------"
                            + "------------------------\n","")
        return info

        
    def _getUsedSpace(self, proj_name):
        """Internal: get the used space from iRODS iCAT"""

        query = "select sum(DATA_SIZE) where COLL_NAME like '" \
                + self.conf.irods_home_dir + proj_name +"%'"
        info = self._getStorageInfo(query)
        if info is not None:
            if len(info.strip()) > 0:
                return self._fromBytes(int(info.strip()), 
                                       self.conf.storage_space_unity)
            else:
                return 0
        else:
            return None


    def _getTotalNumberObjects(self, proj_name):
        """Internal: get the total number of object stored under the specified
           project
        """

        query = "select count(DATA_ID) where COLL_NAME like '" \
                + self.conf.irods_home_dir + proj_name + "%'"
        info = self._getStorageInfo(query)
        if info is not None:
            return int(info.strip())
        else:
            return None


    def _fromBytes(self, size, unity):
        """Convert file size from byte"""
        size_map = {'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3,
                    'TB': 1024 ** 4}
        return size / size_map[unity]


    def _thresholdAlarm(self, project_usage, proj_name, old_used_space_perc):
        """Notification mechanism to alert about over quota events"""

        message = ""
        threshold_soft = 95
        threshold_hard = 100
        if (proj_name in self.conf.mirrored_projects):
            threshold_soft = 95*2
            threshold_hard = 100*2
        if ((project_usage['used_space_perc'] > threshold_soft) and 
            (project_usage['used_space_perc'] > old_used_space_perc)):
            message = "project " + proj_name + " is reaching its quota limit " \
                    + "(used space > 95%): " + str(project_usage['used_space'])\
                    + " " + self.conf.storage_space_unity
        if (project_usage['used_space_perc'] >= threshold_hard):
            message = "project " + proj_name + " reached its quota limit " \
                    + "(used space > 100%): " + str(project_usage['used_space'])\
                    + " " + self.conf.storage_space_unity
        if (len(message) > 0):
            mailsnd = MailSender()
            mailsnd.send(message, self.conf.notification_sender, 
                         self.conf.notification_receiver)
            logger.debug("sent alert for quota over limit related to project: "
                         + proj_name)


    # Public methods
 
    def computeStats(self,dryrun):
        """Compute user/project stats.
        
        Parameters:
        Returns True if successful.
        
        """

        logger.info("Getting storage info from file")
        usage = self._parseUsageStats()
        # if log level is equal to DEBUG (level 10)
        if (logger.getEffectiveLevel() == 10):
            pp = pprint.PrettyPrinter(indent=4)
            print("Storage info:")
            pp.pprint(usage)
                
        total_used_space = 0
        total_allocated_space = 0
        total_number_of_objects = 0
        for proj_name in [x for x in self._parseIrodsProj().keys()
                          if x not in self.conf.internal_project_list]:

            logger.info("Looking at project: " + proj_name)
            project_usage = {}

            logger.info("Getting storage info")
            if not(dryrun):
                quota = self._getUsedSpace(proj_name)
            elif usage and (proj_name in usage.keys()):
                logger.info("Running in dryrun mode")
                quota = usage[proj_name]['used_space']
            else:
                logger.info("No storage information available")
                quota = 0

            if quota is not None:

                logger.info("Getting the number of objects")
                if not(dryrun):
                    num_objs = self._getTotalNumberObjects(proj_name)
                elif usage and (proj_name in usage.keys()):
                    logger.info("Running in dryrun mode")
                    num_objs = usage[proj_name]['number_of_objects']
                else:
                    logger.info("No storage information available")
                    num_objs = 0

                limit = 0
                old_used_space_perc = 0
                if usage and (proj_name in usage.keys()):
                    project_usage = usage[proj_name]
                    project_usage['used_space'] = quota
                    project_usage['number_of_objects'] = num_objs
                    limit = int(usage[proj_name]['quota_limit'])
                    old_used_space_perc = usage[proj_name]['used_space_perc']
                if (len((str(limit)).strip()) > 0 and limit > 0):
                    logger.info("Calculating used space percentage")
                    project_usage['used_space_perc'] = quota*100/limit
                else:
                    logger.info("No storage space allocated")
                    continue
                if self.conf.notification_active:
                    self._thresholdAlarm(project_usage, proj_name, 
                                         old_used_space_perc)
                if usage: 
                    usage[proj_name] = project_usage
                    total_used_space += quota
                    total_allocated_space += limit
                    total_number_of_objects += num_objs

        if usage: 
            logger.info("Writing storage stats to file")
            self._writeUsageStats(usage)
            logger.info("Total used space: " + str(total_used_space)
                        + " " + self.conf.storage_space_unity)
            logger.info("Total allocated space: " + str(total_allocated_space)
                        + " " + self.conf.storage_space_unity)
            logger.info("Total number of objects: " + str(total_number_of_objects))
            return True
        else:
            logger.info("No storage stats to write")
            return False


################################################################################
# CINECA Client Configuration Class #
################################################################################
 
class Configuration():
    """ 
    get properties from filesystem
 
    Please store properties in the following format
    {
    "stat_output_file": "/ffff/wwww",
    "log_level": "DEBUG",
    "log_file": "/eeee/yyyy/ttt
    }
    """

    def __init__(self,file):
   
        self.file = file

        self.log_level = {}
        self.log_level['DEBUG'] = logging.DEBUG
        self.log_level['INFO'] = logging.INFO
        self.log_level['WARNING'] = logging.WARNING
        self.log_level['ERROR'] = logging.ERROR
        self.log_level['CRITICAL'] = logging.CRITICAL


    def parseConf(self):
        """Internal: Parse the configuration file."""

        try:
            filehandle = open(self.file,"r")
            tmp = eval(filehandle.read())
            filehandle.close()
        except Exception, e:
            print "problem while reading configuration file %s" % (self.file)
            print "Error:", e
            return False
 
        self.stat_output_file = tmp['stat_output_file']
        self.storage_space_unity = tmp['storage_space_unity']
        self.internal_project_list = (tmp['internal_project_list']).split(',')
        self.mirrored_projects = (tmp['mirrored_projects']).split(',')
        self.irods_home_dir = tmp['irods_home_dir']
        if tmp['irods_debug'] in ['True', 'true']:
             self.irods_debug = True
        else: 
            self.irods_debug = False
        
        logger.setLevel(self.log_level[tmp['log_level']])
        rfh = logging.handlers.RotatingFileHandler(tmp['log_file'],maxBytes=8388608,backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: ' 
                                      + '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)

        if tmp['notification_active'] in ['True', 'true']:
            self.notification_active = True
        else:
            self.notification_active = False
        self.notification_sender = tmp['notification_sender']
        self.notification_receiver = tmp['notification_receiver']
    
        return True


################################################################################
# CINECA User Quota Tool Command Line Interface #
################################################################################

def compute(args):

    configuration = Configuration(args.confpath)
    configuration.parseConf();
    us = QuotaStats(configuration)
     
    logger.info("Stats computation starting ...")
    us.computeStats(args.dryrun)
    logger.info("Stats computation completed")

    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='iRODS collection quota computation tool')
    parser.add_argument("confpath",help="path to the configuration file")
    parser.add_argument("-d", "--dryrun", action="store_true",\
        help="execute a command without performing any real change")

    subparsers = parser.add_subparsers(title='Actions',description='actions', \
        help='additional help')

    parser_compute = subparsers.add_parser('compute', help='compute statistics about resource consumption')
    parser_compute.set_defaults(func=compute) 

    args = parser.parse_args()
    args.func(args)
