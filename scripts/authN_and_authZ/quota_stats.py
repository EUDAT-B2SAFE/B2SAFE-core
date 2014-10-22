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
# User Accounts Synchronization Class #
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

        
    def _getUsedSpace(self,proj_name):
        """Internal: get the used space from iRODS iCAT in GB"""

        query = "select sum(DATA_SIZE) where COLL_NAME like '/CINECA01/home/"+ proj_name +"%'"
        logger.debug("executing the following query: %s", query)
        [rc,out] = self.irodsu.queryIrodsIcat(query)
        if rc != 0:
            logger.error("Error: %s", err)
            return False
        [key,quota] = out.split('=')
        quotaGB = 0
        quota = quota.replace("\n------------------------------------------------------------\n","")
        if len(quota.strip()) > 0:
            quotaGB = int(quota.strip())/1074000000

        return quotaGB
 
    # Public methods
 
    def computeStats(self,dryrun):
        """Compute user/project stats.
        
        Parameters:
        Returns True if successful.
        
        """

        usage = self._parseUsageStats()
        # if log level is equal to DEBUG (level 10)
        if (logger.getEffectiveLevel() == 10):
            pp = pprint.PrettyPrinter(indent=4)
            print("Usage info:")
            pp.pprint(usage)
                
        for proj_name in [x for x in self._parseIrodsProj().keys()
                          if x not in self.conf.internal_project_list]:

            project_usage = {}
            if not(dryrun):
                quotaGB = self._getUsedSpace(proj_name)
            elif usage and (proj_name in usage.keys()):
                quotaGB = usage[proj_name]['used_space']
            else:
                quotaGB = 0
            limit = 0
            old_used_space_perc = 0
            if usage and (proj_name in usage.keys()):
                project_usage = usage[proj_name]
                project_usage['used_space'] = quotaGB
                limit = int(usage[proj_name]['quota_limit'])
                old_used_space_perc = usage[proj_name]['used_space_perc']
            if (len((str(limit)).strip()) > 0 and limit > 0):
                project_usage['used_space_perc'] = quotaGB*100/limit
            else:
                continue
            #TODO add the silent option to the notification mechanism
            message = ""
            threshold_soft = 95
            threshold_hard = 100
            if (proj_name in self.conf.mirrored_projects):
                threshold_soft = 95*2
                threshold_hard = 100*2
            if ((project_usage['used_space_perc'] > threshold_soft) and \
                (project_usage['used_space_perc'] > old_used_space_perc)):
                message = "project "+proj_name+" is reaching its quota limit (used space > 95%): "\
                          + str(quotaGB) + " GB"
            if (project_usage['used_space_perc'] >= threshold_hard):
                message = "project "+proj_name+" reached its quota limit (used space >= 100%): "\
                          + str(quotaGB) + " GB"
            if (len(message) > 0):
                mailsnd = MailSender()
                mailsnd.send(message, self.conf.notification_sender, self.conf.notification_receiver)
                logger.debug("sent alert for quota over limit related to project: "
                             + proj_name)
            if usage: usage[proj_name] = project_usage

        if usage: 
            self._writeUsageStats(usage)
            return True
        else:
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
        self.internal_project_list = (tmp['internal_project_list']).split(',')
        self.mirrored_projects = (tmp['mirrored_projects']).split(',')
        self.irods_home_dir = tmp['irods_home_dir']
        self.irods_debug = tmp['irods_debug']
        
        logger.setLevel(self.log_level[tmp['log_level']])
        rfh = logging.handlers.RotatingFileHandler(tmp['log_file'],maxBytes=8388608,backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: ' 
                                      + '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)
    
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

    parser = argparse.ArgumentParser(description='CINECA iRODS quota computation tool')
    parser.add_argument("confpath",default="NULL",help="path to the configuration file")
    parser.add_argument("-d", "--dryrun", action="store_true",\
        help="execute a command without performing any real change")

    subparsers = parser.add_subparsers(title='Actions',description='actions', \
        help='additional help')

    parser_compute = subparsers.add_parser('compute', help='compute statistics about resource consumption')
    parser_compute.set_defaults(func=compute) 

    args = parser.parse_args()
    args.func(args)
