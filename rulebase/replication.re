################################################################################
#                                                                              #
# Module Replication:                                                          #
#        - enable transfer single file                                         #   
#        - enable transfer collection                                          #
#        - enable transfer all files which have been logged                    #
#                 from the last transfers                                      #
#                                                                              #
################################################################################

# List of the functions:
#
# EUDATUpdateLogging(*status_transfer_success, *path_of_transfered_file, 
#               *target_transfered_file, *cause)
# EUDATCheckIntegrity(*source,*destination)
# EUDATReplication(*source, *destination, *registered)
# EUDATTransferUsingFailLog(*buffer_length)
# EUDATCheckReplicas(*source, *destination, *registered)
#---- collection management ---
#TODO:update EUDATIntegrityCheck(*srcColl,*destColl)
#EUDATRegDataRepl(*source, *destination)
#EUDATCheckIntegrityDO(*source,*destination)

#
# Update the logging files specific for EUDAT B2SAFE
# 
# Parameters:
#    *status_transfer_success    [IN] Status of transfered file (true or false)     
#    *path_of_transfered_file    [IN] path of transfered file in iRODS
#    *target_transfered_file     [IN] path of the destination file in iRODS
#    *cause                      [IN] cause of the failed transfer
#
# Author: Long Phan, JSC
# Modified by Claudio Cacciari, Cineca
#
EUDATUpdateLogging(*status_transfer_success, *source, *destination, *cause) {

    # Update Logging Statistical File
    *level = "INFO";
    *message = "*source::*destination::" ++ "*status_transfer_success::*cause";
    if (!*status_transfer_success) {
        EUDATQueue("push", *message, 0);
        *level = "ERROR";
    } 
    EUDATLog(*message, *level);
}

#
# Checks differences about checksum and size between two files
# 
# Parameters:
#    *source         [IN] path of source file in iRODS
#    *destination    [IN] path of target file in iRODS
#
# Author: Long Phan, JSC
# Modified by Claudio Cacciari, Cineca
#
EUDATCheckIntegrity(*source,*destination) {

    *status_transfer_success = bool("true");

    msiGetObjType(*source,*source_type);
    if (*source_type == '-c') {
        logDebug("source path *source is a collection");
        *status_transfer_success = EUDATChksColl(*source, *destination);
    } else if (*source_type == '-d') {
        logDebug("source path *source is a data object");
        *status_transfer_success = EUDATCheckIntegrityDO(*source,*destination);
    }
  
    if (!*status_transfer_success) {
        logError("[EUDATCheckIntegrity] replication from *source to *destination failed");
    } else {
        logInfo("[EUDATCheckIntegrity] replication from *source to *destination succeeded");
    }

    *status_transfer_success;
}

#
# Transfer single file
#
# Parameters:
#    *source      [IN] path of the source object in iRODS
#    *destination [IN] destination of replication in iRODS
#    *registered  [IN] boolean value: "true" for registered data, "false" otherwise
# 
# Author: Long Phan, JSC
# Modified by Claudio Cacciari, Cineca
#
EUDATReplication(*source, *destination, *registered) {

    logInfo("[EUDATReplication] transfering *source to *destination"); 
    *status_transfer_success = bool("true");

    # Catch Error CAT_NO_ACCESS_PERMISSION before replication
    if (errormsg(EUDATCatchErrorDataOwner(*source,*msg), *errmsg) < 0) {

        logDebug("*errmsg");
        # Update fail_log                
        *status_transfer_success = bool("false");
        EUDATUpdateLogging(*status_transfer_success,*source,*destination,"no access permission");

    } else {

        logInfo("[EUDATReplication] *msg");

        if (*registered) {
            logDebug("replicating registered data");
            *status_repl = EUDATRegDataRepl(*source,*destination);
            if (*status_repl != 0) {
                logDebug("registered data replication failed");
                *status_transfer_success = bool("false");
                EUDATUpdateLogging(*status_transfer_success,*source,*destination,
                                   "registered data replication failure");
            }
        } else {
            logDebug("replicating data without PID registration");
            msiGetObjType(*source,*source_type);
            if (*source_type == '-c')  {
                msiCollRsync(*source,*destination,"null","IRODS_TO_IRODS",*rsyncStatus);
            }
            else if (*source_type == '-d') {            
                msiDataObjRsync(*source,"IRODS_TO_IRODS","null",*destination,*rsyncStatus);
            }
            if (*rsyncStatus != 0) {
                logDebug("perform a further verification about checksum and size");
                EUDATCheckIntegrity(*source,*destination);
            }
        }
    }   
         
}

#
# Transfer all data object saved in the logging system,
# according to the format: cause::path_of_transfer_file::target_of_transfer_file.
#
# Parameters:
#   *buffer_length    [IN] max number of failed transfers to process.
#                          It has to be > 1.
#
# Author: Long Phan, JSC
# Modified by Claudio Cacciari, Cineca;
#
EUDATTransferUsingFailLog(*buffer_length) {
    
    # get size of queue-log before transfer.    
    EUDATQueue("queuesize", *l, 0);
    EUDATQueue("pop", *messages, *buffer_length);
    
    *msg_list = split("*messages",",");    
    foreach (*message in *msg_list) {
        *message = triml(*message, "'");
        *message = trimr(*message, "'");
        *list = split("*message","::");

        *counter = 0;
        foreach (*item_LIST in *list) {
            if (*counter == 0) {*path_of_transfer_file = *item_LIST; }
            else if (*counter == 1) {*target_of_transfer_file = *item_LIST; }
            *counter = *counter + 1;
            if (*counter == 2) {break;}
        }
        EUDATTransferSingleFile(*path_of_transfer_file, *target_of_transfer_file);
    }

    # get size of queue-log after transfer. 
    EUDATQueue("queuesize", *la, 0);
    logInfo("AFTER TRANSFER: Length of Queue = *la");
    if (int(*l) == int(*la)) {
        logInfo("Transfer Data Objects got problems. No Data Objects have been transfered");
    } else {
        logInfo("There are *la Data Objects in Queue-log");
    }
      
}

#
# Check whether two files are available and identical
# If they are not identical, do the following:
#    1. find the pid of the object and modify checksum in the pid or create a new pid
#    2. create pid in the iCAT if it does not exist
#    3. add/update ROR in iCAT
#    4. trigger replication from source to destination
#
# Parameters:
#   *source         [IN]     source of the file
#   *destination    [IN]     destination of the file
#   *registered     [IN]     bool, "true": replication using remote replication
#                                  "false": replication using control files
#
# Author: Elena Erastova, RZG
#
EUDATCheckReplicas(*source, *destination, *registered) {
    logInfo("Check if 2 replicas have the same checksum. Source = *source, destination = *destination");
    if (EUDATCatchErrorChecksum(*source, *destination) == bool("false") || 
        EUDATCatchErrorSize(*source, *destination) == bool("false")) 
    {
        EUDATeiPIDeiChecksumMgmt(*source, *pid, bool("true"), bool("true"), 0);
        EUDATiRORupdate(*source, *pid);
        logInfo("replication from *source to *destination");
        EUDATReplication(*source, *destination, *registered);
    }
}


####################################################################################
# Collection replication management                                                #
####################################################################################

#
# This function will check all errors between source-Collection and destination-Collection
# Data with error will be pushed into fail.log which are able to be transfered later.
# Parameter:
# 	*srcColl	[IN]	Path of transfered Collection
#	*destColl	[IN]	Path of replicated Collection
#
# Author: Long Phan, JSC
#
EUDATIntegrityCheck(*srcColl,*destColl) {
        # Verify that input path is a collection
        msiGetObjType(*srcColl, *type);
        if (*type != '-c') {
            logError("Input path *srcColl is not a collection");
            fail;
        }
        msiGetObjType(*destColl, *type);
        if (*type != '-c') {
            logError("Input path *destColl is not a collection");
            fail;
	}
        msiSplitPath(*srcColl,*sourceParent,*sourceChild);
        msiStrlen(*srcColl,*pathLength);

        foreach(*Row in SELECT DATA_NAME,COLL_NAME WHERE COLL_NAME like '*path_of_transfered_coll/%') {
            *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
            msiSubstr(*objPath, str(int(*pathLength)+1), "null", *subCollection);
            *destination = "*destColl/*subCollection";

                EUDATSearchPID(*objPath, *ppid);
                if (*ppid == "empty") {
                        logDebug("PPID is empty");
                        *status_transfer_success = bool("false");
                        *cause = "PPID is empty";
                        EUDATUpdateLogging(*status_transfer_success, *objPath, *destination, *cause);
                } else {
                        logDebug("PPID exists: *ppid");
                }
                # FIXME: is it possible to get CPID at source-location ?
                EUDATSearchPID(*destination, *cpid);
                if (*cpid == "empty") {
                        logDebug("CPID is empty");
                        *status_transfer_success = bool("false");
                        *cause = "CPID is empty";
                        EUDATUpdateLogging(*status_transfer_success, *objPath, *destination, *cause);
                } else {
                        logDebug("CPID exists: *cpid");
                }
                EUDATCheckError(*objPath, *destination);
            }
}

#-----------------------------------------------------------------------------
# Data object replication and PID management based on remote execution
# It is assumed that iRODS zone federation is established
#  and the replicated file is accessible from the source
#
# Parameters:
# *source       [IN] source path of the data object to be replicated
# *destination  [IN] destination path of the replicated data object
#
# Authors: Elena Erastova, RZG; Claudio Cacciari, Cineca
#-----------------------------------------------------------------------------
EUDATRegDataRepl(*source, *destination) {

    # initial values of parentPID, parentROR, childPID1
    *parentPID = "None";
    *parentROR = "None";
    *childPID1 = "None";

    EUDATGetZoneNameFromPath(*destination, *zoneName);
    EUDATGetZoneHostFromZoneName(*zoneName, *zoneConn);
    logDebug("Remote zone name: *zoneName, connection contact: *zoneConn");
    
    # get PID of the source file from ICAT
    logDebug("query PID of DataObj *source");
    EUDATiFieldVALUEretrieve(*source, "PID", *parentPID);
    logDebug("Retrieved the PID value *parentPID for Obj *source");
    
    # if there is no entry for the PID in ICAT, get it from EPIC
    if(*parentPID == "None") {
        EUDATSearchPID(*source, *parentPID);
        
        #TODO if there is no PID create it?
        
        if((*parentPID == "empty") || (*parentPID == "None")) {
            EUDATCreatePID("None",*source,"None",bool("true"),*parentPID);
        }
        
        # if there is a PID in EPIC create it in ICAT
        else {
            EUDATiPIDcreate(*source, *parentPID);
        }
    }

    if (*parentPID == "empty" || (*parentPID == "None")) {
        logDebug("PID is empty, no replication will be executed");
        # Update Logging (Statistic File and Failed Files)
        *status_transfer_success = bool("false");
        EUDATUpdateLogging(*status_transfer_success,*source,*destination, "empty PID");
    } else {
        logDebug("PID exist, replication's beginning ...... ");

        # get ROR of the source file from ICAT
        EUDATiFieldVALUEretrieve(*source, "EUDAT/ROR", *parentROR);
    
        # if there is no entry for the ROR in ICAT, get it from EPIC
        if(*parentROR == "None") {
            EUDATGetRorPid(*parentPID, *parentROR);
        
            # if there is a ROR in EPIC create it in ICAT
            if(*parentROR != "None") {
                EUDATCreateAVU("EUDAT/ROR", *parentROR, *source);
            }
        }
    
        # otherwise ROR for the replica will be parentPID
        if(*parentROR == "None") {
            *parentROR = *parentPID;
        }

        msiGetObjType(*source,*source_type);
        if (*source_type == '-c')  {
             msiCollRsync(*source,*destination,"null","IRODS_TO_IRODS",*rsyncStatus);
        } 
        else {
             msiDataObjRsync(*source,"IRODS_TO_IRODS","null",*destination,*rsyncStatus);
        }
    
        # create a PID for the replica which is done on the remote server
        # using remote execution
        remote(*zoneConn,"null") {
            EUDATCreatePID(*parentPID,*destination,*parentROR,bool("true"),*childPID);
        }
    
        # get the PID for the replica from ICAT on the remote server
        EUDATiFieldVALUEretrieve(*destination, "PID", *childPID1);
    
        # update parent PID with a child one 
        # if the child exists in ICAT on the remote server
        if(*childPID1 != "None") {
            EUDATUpdatePIDWithNewChild(*parentPID, *childPID1);
        }
    }
}

#-----------------------------------------------------------------------------
# Create PIDs for all collections and objects in the collection recursively
# ROR is assumed to be "None"
#
# Parameters:
# *collPath    [IN] path of the collection
#
# Author: Elena Erastova, RZG
#-----------------------------------------------------------------------------

EUDATPidsForColl(*collPath) {

    logInfo("[EUDATPidsForColl] Creating PIDs for collection *collPath");

    # Verify that source input path is a collection
    msiGetObjType(*collPath, *type);
    if (*type != '-c') {
        logError("Input path *collPath is not a collection");
        fail;
    }
    
    # Create PIDs for all subcollections in collection recursively
    foreach(*RowC in SELECT COLL_NAME WHERE COLL_NAME like '*collPath%') {
        *subCollPath = *RowC.COLL_NAME;
        EUDATCreatePID("None", *subCollPath, "None", bool("true"), *newPID);
    }
    
    # Create PIDs for all data objects in collection recursively
    foreach(*Row in SELECT DATA_NAME,COLL_NAME WHERE COLL_NAME like '*collPath%') {
        *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
        EUDATCreatePID("None", *objPath, "None", bool("true"), *newPID);
    }
}


#-----------------------------------------------------------------------------
# Compare cheksums of data objects in the source and destination
#  collection recursively
#
# Parameters:
# *sCollPath    [IN] path of the source collection
# *dCollPath    [IN] path of the destination collection
# 
# return a boolean value: true: checksums of the DOs in the collections match
#                         false: checksums of the DOS in the collections
#                                do not match
#
# Author: Elena Erastova, RZG
# Author: Claudio Cacciari, Cineca
#-----------------------------------------------------------------------------
#

EUDATChksColl(*sCollPath, *dCollPath) {

    *result = bool("true");
    logInfo("[EUDATChksColl] Compare cheksums of files in *sCollPath and *dCollPath");

    # Verify that source input path is a collection
    msiGetObjType(*sCollPath, *type);
    if (*type != '-c') {
        logError("Input path *collPath is not a collection");
        fail;
    }
    # Verify that destination input path is a collection
    msiGetObjType(*dCollPath, *type);
    if (*type != '-c') {
        logError("Input path *dCollPath is not a collection");
        fail;
    }
    # Get the length of the source collection string
    msiStrlen(*sCollPath,*pathLength);
    # For each DO in the sorce collection recursively compare checksum amd size
    # with the DO in the destination collection.
    # If they do not match, write an error in the b2safe log
    foreach(*Row in SELECT DATA_NAME,COLL_NAME WHERE COLL_NAME like '*sCollPath%') {
        *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
        msiSubstr(*objPath, str(int(*pathLength)+1), "null", *subCollection);
        *destination = "*dCollPath/*subCollection";
        *result = EUDATCheckIntegrityDO(*objPath,*destination);
    }

    *result;
}

#
# Checks differences about checksum and size between two Data Objects
# and log the result to the B2SAFE logging system
# 
# Parameters:
#    *source         [IN] path of source file in iRODS
#    *destination    [IN] path of target file in iRODS
#
# Author: Claudio Cacciari, Cineca
#
EUDATCheckIntegrityDO(*source,*destination) {
        
    *status = bool("true");
    *cause = "";

    *err = errorcode(msiObjStat(*destination, *objStat));
    if (*err < 0) {
        *cause = "missing replicated object";
        *status = bool("false");
    } else if (!EUDATCatchErrorSize(*source,*destination)) {
        *cause = "different size";
        *status = bool("false");
    } else if (!EUDATCatchErrorChecksum(*source,*destination)) {
        *cause = "different checksum";
        *status = bool("false");
    }
    EUDATUpdateLogging(*status, *source, *destination, *cause);

    *status;
}



