# Integrity Checking Mechanism

## Overview

Code to enable checksum verification of archive resident data.

This code allows for periodic or on-demand verification of the data by comparing the initial (ingest) checksum with that of the 
data resident in the archive.

The initial checksum is computed while data is ingested (e.g. just after iput) and replicated (e.g. in
BE2SAFE replication is done automatically using iRODS rules) and stored in the iCAT database. The first
computed checksum is the referential one and it is also stored in the PID service.

## Code Components

* Candidates collector selects candidate data replicas from the iCAT. The selection is based on
resource and time of the last verification. This module is implemented as eudat-get-checksum-verify-candidates script. 
The output of the module is candidates file.

* Checksum verifier performs the verification of replicas taken from candidates file and outputs to
the results file. The candidates file is removed. This is a storage specific module and thus will have
many implementations. It may be run on iRods server or on underlying storage server or partially
on both. 

* Metadata updater reads results file and updates the iCAT metadata (time of verification) of
verified objects or reports the problem if the verification failed. The results file is removed. This
module is implemented as eudat-update-checksums script. The script also calls the rule
updatePidChecksum.r, which updates the checksum in the PID record using
iRODS rules implemented in the rulebase of the B2SAFE module.


## Reference Implementations

Three reference implementations are provided:

* eudat-verify-checksums-disc - to be run on iRods server and local discs.

* eudat-verify-checksums-tsm - to be run on IBM Tivoli Storage Manager server, communicating via an NFS share provided for iRods server.

* eudat-verify-checksums-hpss-hsi - to be run on the iRODS server with HSI clients installed.


## Use cases

###Periodic check
All modules are run from cron daily or several times a day. Option -d of eudat-get-checksum-verify-candidates 
script is set to number of days of the period (e.g. 365 if the check is to be
performed every year). The mechanism will verify replicas with time of last verification between 365 and
366 days ago.

###On demand check
If check of all replicas from a resource is needed, eudat-get-checksum-verify-candidates
script must be run by the administrator with option -d set to 0. Then the rest of the modules must be run
either by the administrator or by cron mechanism.


##Deployment

There are example steps to deploy the mechanism, mainly with using default parameters. If you need
more specific implementation, each script provides detailed usage information.

1) Set cron task for eudat-get-checksum-verify-candidates on iRODS server, user irods_user.
2) Set cron task for eudat-update-checksums on iRODS server, user irods_user.
3) Set cron task for checksum verifier script.
a) for disc storage (may be on iRODS server, irods_user).
b) for hierarchical storage on TSM server, root user e.g.
c) for HPSS storage on iRODS server, using keytab and HSI client
4) Run EUDATSetiCHECKSUMdate.r rule.

