################################################################################
#                                                                              #
# Module Replication:                                                          #
#        - enable transfer single file                                         #   
#        - enable transfer collection                                          #
#        - enable transfer all files whose transfers have previously failed    #
#                                                                              #
################################################################################

# List of the functions:
#
# EUDATUpdateLogging(*status_transfer_success, *source, *destination, *cause)
# EUDATCheckIntegrity(*source, *source_res, *destination, *dest_res, *logEnabled, *notification, *response)
# EUDATCheckIntegrity(*source, *destination, *logEnabled, *notification, *response)
# EUDATReplication(*source, *destination, *dest_res, *registered, *recursive, *response)
# EUDATReplication(*source, *destination, *registered, *recursive, *response)
# EUDATTransferUsingFailLog(*buffer_length, *stats)
# EUDATRegDataRepl(*source, *destination, *dest_res, *recursive, *response)
# EUDATRegDataRepl(*source, *destination, *recursive, *response)
# EUDATPIDRegistration(*source, *destination, *notification, *registration_response)
# EUDATSearchAndCreatePID(*path, *pid)
# EUDATSearchAndDefineField(*path, *pid, *key)
# EUDATCheckIntegrityColl(*sCollPath, *source_res, *dCollPath, *dest_res, *logEnabled, *response) 
# EUDATCheckIntegrityColl(*sCollPath, *dCollPath, *logEnabled, *check_response)
# EUDATCheckIntegrityDO(*source, *source_res, *destination, *dest_res, *logEnabled, *response)
# EUDATCheckIntegrityDO(*source, *destination, *logEnabled, *response)


# Update the logging files specific for EUDAT B2SAFE
# 
# Parameters:
#    *status_transfer_success    [IN] Status of transfered file (true or false)     
#    *source                     [IN] path of transfered file in iRODS
#    *destination                [IN] path of the destination file in iRODS
#    *cause                      [IN] cause of the failed transfer
#
# Author: Long Phan, JSC
# Modified by Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
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

# Checks differences about checksum and size between two paths
# 
# Parameters:
#    *source         [IN] source path in iRODS
#    *source_res     [IN]  iRODS resource name of the source
#    *destination    [IN] detination path in iRODS
#    *dest_res       [IN]  iRODS resource name of the destination
#    *logEnabled     [IN] boolean value: "true" to enable the logging system, 
#                                        "false" to silence it.
#    *notification   [IN] value [0|1]: if 1 enable the notification via messaging system
#    *response       [OUT] the reason of the failure
#
# Author: Long Phan, JSC
# Modified by Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATCheckIntegrity(*source, *source_res, *destination, *dest_res, 
                    *logEnabled, *notification, *response) {

    *status_transfer_success = bool("true");

    msiGetObjType(*source,*source_type);
    if (*source_type == '-c') {
        logDebug("source path *source is a collection");
        *status_transfer_success = EUDATCheckIntegrityColl(*source, *source_res,
                                                           *destination, *dest_res,
                                                           *logEnabled, *response);
    } else if (*source_type == '-d') {
        logDebug("source path *source is a data object");
        *status_transfer_success = EUDATCheckIntegrityDO(*source, *source_res, 
                                                         *destination, *dest_res, 
                                                         *logEnabled, *response);
    }
  
    if (!*status_transfer_success) {
        logError("[EUDATCheckIntegrity] *source and *destination are not coherent: *response");
    } else {
        logInfo("[EUDATCheckIntegrity] *source and *destination are coherent");
    }

#    if (*notification == 1) {
#        EUDATGetZoneNameFromPath(*source, *zone);
#        *queue = *zone ++ "_" ++ $userNameClient;
#        *message = "status:*status_transfer_success;response:*source::*destination::*response";
#        EUDATMessage(*queue, *message);
#    }

    *status_transfer_success;
}

EUDATCheckIntegrity(*source, *destination, *logEnabled, *notification, *response) {
    *source_res = "null";
    *dest_res = "null";
    *status_transfer_success = EUDATCheckIntegrity(*source, *source_res, *destination, *dest_res, 
                                                   *logEnabled, *notification, *response);
    *status_transfer_success;
}

# Data set replication
#
# Parameters:
#    *source      [IN] path of the source data set in iRODS
#    *destination [IN] destination of replication in iRODS
#    *dest_res    [IN] resource of the destination
#    *registered  [IN] boolean value: "true" for registered data, "false" otherwise
#    *recursive   [IN] boolean value: "true" to enable the recursive replication
#                      of registered data, "false" otherwise.
#    *response    [OUT]the result of the replication
# 
# Author: Long Phan, JSC
# Modified by Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATReplication(*source, *destination, *dest_res, *registered, *recursive, *response) {

    logInfo("[EUDATReplication] transfering *source to *destination"); 
    *status = bool("true");
    *response = "";
    if ((*dest_res == "") || (*dest_res == "None")) {
        *dest_res = "null";
    }

    # Catch Error CAT_NO_ACCESS_PERMISSION before replication
    if (errormsg(EUDATCatchErrorDataOwner(*source,*msg), *errmsg) < 0) {

        logDebug("[EUDATReplication] *errmsg");
        *status = bool("false");
        *response = "no access permission to the path *source for user $userNameClient";
        EUDATUpdateLogging(*status,*source,*destination,*response);

    } else {

        logInfo("[EUDATReplication] *msg");
        if (EUDATtoBoolean(*registered)) {
            logDebug("[EUDATReplication] replicating registered data");
            *status = EUDATRegDataRepl(*source, *destination, *dest_res, EUDATtoBoolean(*recursive), *response);
        } else {
            logDebug("[EUDATReplication] replicating data without PID registration");
            msiGetObjType(*source,*source_type);
            if (*source_type == '-c')  {
                msiCollRsync(*source,*destination,*dest_res,"IRODS_TO_IRODS",*rsyncStatus);
            }
            else if (*source_type == '-d') {            
                msiDataObjRsync(*source,"IRODS_TO_IRODS",*dest_res,*destination,*rsyncStatus);
            }
            if (*rsyncStatus != 0) {
                logDebug("[EUDATReplication] perform a further verification about checksum and size");
                *logEnabled = bool("true");
                *notification = 0;
                *source_res = "null";
                *status = EUDATCheckIntegrity(*source, *source_res, *destination, *dest_res,
                                              *logEnabled, *notification, *response);
            }
        }
    }   

    if (*status) { 
        *response = "*source::*destination::*dest_res"
                 ++ "::registered=*registered::recursive=*recursive";
    }
    logDebug("[EUDATReplication] response = *response");

    *status;
}

EUDATReplication(*source, *destination, *registered, *recursive, *response) {
    *dest_res = "null";
    *status = EUDATReplication(*source, *destination, *dest_res, *registered, *recursive, *response);
    *status;
}

# Transfer all data object saved in the logging system,
# according to the format: cause::path_of_transfer_file::target_of_transfer_file.
#
# Parameters:
#   *buffer_length    [IN] max number of failed transfers to process.
#                          It has to be > 1.
#   *stats           [OUT] the number of successful transfers
#
# Author: Long Phan, JSC
# Modified by Claudio Cacciari, Cineca;
#-------------------------------------------------------------------------------
EUDATTransferUsingFailLog(*buffer_length, *stats) {

    logInfo("[EUDATTransferUsingFailLog] checking the last *buffer_length failed transfers");   
#TODO check the single error causes 
    *success_counter = 0;
    *failure_counter = 0;
#TODO add these parameters to the fail log messages
    *registered = "true";
    *recursive = "true";
 
    # get size of queue-log before transfer.    
    EUDATQueue("queuesize", *l, 0);
    EUDATQueue("pop", *messages, *buffer_length);
    
    *msg_list = split("*messages",",");    
    foreach (*message in *msg_list) {
        *message = triml(*message, "'");
        *message = trimr(*message, "'");
        logDebug("message: *message");
        *list = split("*message","::");

        *counter = 0;
        foreach (*item_LIST in *list) {
            if (*counter == 0) {*source = *item_LIST;}
            else if (*counter == 1) {*destination = *item_LIST;}
            else if (*counter == 3) {*cause = *item_LIST;}
            *counter = *counter + 1;
            if (*counter == 4) {break;}
        }
        logDebug("cause:*cause");
        logDebug("source:*source; target:*destination");
        *repl_status = EUDATReplication(*source, *destination, *registered, *recursive, *response);
        if (*repl_status) { *success_counter = *success_counter + 1; }
        else { *failure_counter = *failure_counter + 1; }
    }

    *stats = "# of successes:*success_counter, # of failures:*failure_counter";

    # get size of queue-log after transfer. 
    EUDATQueue("queuesize", *la, 0);
    logDebug("AFTER TRANSFER: Length of Queue = *la");
    if (int(*l) == int(*la)) {
        logDebug("No Data Objects have been transfered");
    } 
      
}

# Data object replication and PID management based on remote execution
# It is assumed that iRODS zone federation is established
#  and the replicated file is accessible from the source
#
# Parameters:
# *source       [IN] source path of the data object to be replicated
# *destination  [IN] destination path of the replicated data object
# *dest_res     [IN] resource of the destination
# *recursive    [IN] boolean value: "true" to consider all the sub-collections 
#                    and objects under the root collection, "false" to consider 
#                    only the root path.
# *response     [OUT] message about the reason of the failure
#
# Authors: Elena Erastova, RZG; Claudio Cacciari, Cineca
#-----------------------------------------------------------------------------
EUDATRegDataRepl(*source, *destination, *dest_res, *recursive, *response) {

    *status = bool("true");
    *response = "";
    if ((*dest_res == "") || (*dest_res == "None")) {
        *dest_res = "null";
    }    

    # initial value of parentPID
    *parentPID = "None";

    # search and create pid related to the source of the replication
    EUDATSearchAndCreatePID(*source, *parentPID);
    if (*parentPID == "empty" || (*parentPID == "None")) {
        *status = bool("false");
        *response = "PID is empty, no replication will be executed for *source";
        EUDATUpdateLogging(*status,*source,*destination,"empty PID");
        logDebug(*response);
    }
    else {
        logDebug("[EUDATRegDataRepl] PID exist for *source");
        msiGetObjType(*source,*source_type);
        if (*source_type == '-c')  {

            logDebug("[EUDATRegDataRepl] The path *source is a collection");
            logDebug("[EUDATRegDataRepl] Replication's beginning ...... ");
            msiCollRsync(*source,*destination,*dest_res,"IRODS_TO_IRODS",*rsyncStatus);
            if (*rsyncStatus != 0) {
                logDebug("[EUDATRegDataRepl] perform a further verification about checksum and size");
                *logEnabled = bool("true");
                *notification = 0;
                *source_res = "null";
                *status = EUDATCheckIntegrity(*source, *source_res, *destination, *dest_res,
                                              *logEnabled, *notification, *response);
            }
            
            if (*status) {
                *notification = 0;
                EUDATPIDRegistration(*source, *destination, *notification, *response);
                if (*response != "None") { *status = bool("false") }
                # update the parent PID of each replica with the related child PID
                if (*status && *recursive) {
               
                    *responses = "";
                    logDebug("[EUDATRegDataRepl] loop over the sub-collections"); 
                    msiStrlen(*source,*pathLength);
                    # loop over the sub-collections of the collection
                    foreach (*Row in SELECT COLL_NAME WHERE COLL_NAME like '*source/%') {
                        msiSubstr(*Row.COLL_NAME, str(int(*pathLength)+1), "null", *subCollection);
                        *target = "*destination/*subCollection";
                        EUDATPIDRegistration(*Row.COLL_NAME, *target, *notification, *singleRes);
                        if (*singleRes != "None") { 
                            *contents = *Row.COLL_NAME ++ '::*target::false::*singleRes';
                            *responses = *responses ++ *contents ++ ",";
                        }
                        *status = (*singleRes == "None") && *status;
                    }
                    logDebug("[EUDATRegDataRepl] loop over the objects of the collection");
                    # loop over the objects of the collection
                    foreach (*Row in SELECT DATA_NAME,COLL_NAME WHERE COLL_NAME = '*source' || like '*source/%') {
                        *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
                        msiSubstr(*objPath, str(int(*pathLength)+1), "null", *subCollection);
                        *target = "*destination/*subCollection";
                        EUDATPIDRegistration(*objPath, *target, *notification, *singleRes);
                        if (*singleRes != "None") {                       
                            *contents = "*objPath::*target::false::*singleRes";
                            *responses = *responses ++ *contents ++ ",";
                        }
                        *status = (*singleRes == "None") && *status;
                    }
                    *response = trimr(*responses, ",");
                }
            }

        } else {
            
            logDebug("[EUDATRegDataRepl] Replication's beginning ...... ");
            msiDataObjRsync(*source,"IRODS_TO_IRODS",*dest_res,*destination,*rsyncStatus);
            if (*rsyncStatus != 0) {
                 logDebug("[EUDATRegDataRepl] perform a further verification about checksum and size");
                 *logEnabled = bool("true");
                 *notification = 0;
                 *source_res = "null";
                 *status = EUDATCheckIntegrity(*source, *source_res, *destination, *dest_res,
                                               *logEnabled, *notification, *response);
            }
            if (*status) {
                *notification = 0;
                # update the parent PID of the replica with the related child PID
                EUDATPIDRegistration(*source, *destination, *notification, *response);
                logDebug("[EUDATRegDataRepl] registration's response: *response");
                if (*response != "None") { *status = bool("false") }
            }
        }
    }

    *status;
}

EUDATRegDataRepl(*source, *destination, *recursive, *response) {
    *dest_res = "null";
    *status = EUDATRegDataRepl(*source, *destination, *dest_res, *recursive, *response);
    *status;
}

# Verify that a PID exist for a given path and optionally create it 
# if not found.
#
# Parameters:
# *source                [IN]  source iRODS path
# *destination           [IN]  target iRODS path
# *notification          [IN]  enable messaging for async call [0|1]
# *registration_response [OUT] a message containing the reason of the failure
#
# Author: Claudio, Cineca
#-----------------------------------------------------------------------------
EUDATPIDRegistration(*source, *destination, *notification, *registration_response) {

    logInfo("[EUDATPIDRegistration] registration of PIDs for replication from *source to *destination");

    *registration_response = "None";
    *parentPID = "None";
    *parentROR = "None";
    *childPID = "None";
    *fio = "None";
    *fixed = "False";

    EUDATGetZoneNameFromPath(*destination, *zoneName);
    EUDATGetZoneHostFromZoneName(*zoneName, *zoneConn);
    logDebug("[EUDATPIDRegistration] remote zone name: *zoneName, connection contact: *zoneConn");

    EUDATSearchAndCreatePID(*source, *parentPID);
    if (*parentPID == "empty" || (*parentPID == "None")) {
        *registration_response = "PID of source *source is None";
        logDebug(*registration_response);
        # Update Logging (Statistic File and Failed Files)
        EUDATUpdateLogging(bool("false"),*source,*destination,*registration_response);
    }
    else {
        *parentROR = EUDATSearchAndDefineField(*source, *parentPID, "EUDAT/ROR");
        if (*parentROR == "None") {
            logDebug("EUDAT/ROR was empty, using parent PID");
            *parentROR = *parentPID;
        }
        *fio = EUDATSearchAndDefineField(*source, *parentPID, "EUDAT/FIO");
        if (*fio == "None") {
            logDebug("EUDAT/FIO was empty, using parent PID");
            *fio = *parentPID;
        }
        *fixed = EUDATSearchAndDefineField(*source, *parentPID, "EUDAT/FIXED_CONTENT");
        logDebug("[EUDATPIDRegistration] the path *destination has EUDAT/PARENT=*parentPID, "
                 ++ "EUDAT/ROR=*parentROR, EUDAT/FIO=*fio, EUDAT/FIXED_CONTENT=*fixed");
        # create a PID for the replica which is done on the remote server
        # using remote execution
        remote(*zoneConn,"null") {
            EUDATCreatePID(*parentPID, *destination, *parentROR, *fio, *fixed, *childPID);
        }
        # update parent PID with a child one 
        # if the child exists in ICAT on the remote server
        if (*childPID != "None") {
            *replica = EUDATUpdatePIDWithNewChild(*parentPID, *childPID);
            if (*replica != "None") {
                EUDATCreateAVU("EUDAT/REPLICA", *replica, *source);
            }
            else {
                *registration_response = "REPLICA attribute of source *source is None";
                logDebug(*registration_response);
                EUDATUpdateLogging(bool("false"),*source,*destination,*registration_response);
            }
        }
        else {
            *registration_response = "PID of destination *destination is None";
            logDebug(*registration_response);
            EUDATUpdateLogging(bool("false"),*source,*destination,*registration_response);
        }
    }
   
#    if (*notification == 1) { 
#        if (*registration_response == "None") { *statusMsg = "true"; }
#        else { *statusMsg = "false"; }
#        EUDATGetZoneNameFromPath(*source, *zone);
#        *queue = *zone ++ "_" ++ $userNameClient;
#        *message = "status:*statusMsg;response:*source::*destination::*registration_response";
#        EUDATMessage(*queue, *message);
#    }
}

# Search PID for a given path and in case it is not found, 
# it creates a new PID.
#
# Parameters:
# *path    [IN] iRODS path
# *pid     [OUT] the related PID
#
# Author: Claudio, Cineca
#-----------------------------------------------------------------------------
EUDATSearchAndCreatePID(*path, *pid) {

    logDebug("[EUDATSearchAndCreatePID] query PID of path *path");
    EUDATgetLastAVU(*path, "PID", *pid);
    logDebug("[EUDATSearchAndCreatePID] retrieved the iCAT PID value *pid for path *path");
    # if there is no entry for the PID in ICAT, get it from EPIC
    if (*pid == "None") {
        EUDATCreatePID("None", *path, "None", "None", "false", *pid);
        EUDATiPIDcreate(*path, *pid);
    }
}

# Search key/value pair for a given path
#
# Parameters:
# *path       [IN]  iRODS path
# *pid        [IN]  the PID associated to path
# *key        [IN]  The name of the PID field
#
# Author: Claudio, Cineca
#-----------------------------------------------------------------------------
EUDATSearchAndDefineField(*path, *pid, *key) {

    logDebug("[EUDATSearchAndDefineField] query PID *pid and path *path to get *key");
    *val = "None";
    # get *key of the *path from ICAT
    EUDATgetLastAVU(*path, *key, *val);
    logDebug("[EUDATSearchAndDefineField] got *key=*val from iCAT");
    # if there is no entry for the *key in ICAT, get it from EPIC
    if (*val == "None") {
        *val = EUDATGeteValPid(*pid, *key);
        logDebug("[EUDATSearchAndDefineField] got *key=*val from PID service");
        # if there is a *key in EPIC create it in ICAT
        if (*val != "None") {
            EUDATCreateAVU(*key, *val, *path);
        }
    }
    *val
}

# Compare cheksums of data objects in the source and destination
#  collection recursively
#
# Parameters:
# *sCollPath    [IN] path of the source collection
# *source_res   [IN]  iRODS resource name of the source
# *dCollPath    [IN] path of the destination collection
# *dest_res     [IN]  iRODS resource name of the destination
# *logEnabled   [IN] boolean value: "true" to enable the logging system, 
#                                     "false" to silence it.
# *response     [OUT] the reason of the failure
#
# 
# return a boolean value: true: checksums of the DOs in the collections match
#                         false: checksums of the DOS in the collections
#                                do not match
#
# Author: Elena Erastova, RZG
# Author: Claudio Cacciari, Cineca
#-----------------------------------------------------------------------------
EUDATCheckIntegrityColl(*sCollPath, *source_res, *dCollPath, *dest_res, *logEnabled, *check_response) {

    if (*source_res == "" || *source_res == "None") { *source_res = "%" }
    *check_response = "";
    logInfo("[EUDATCheckIntegrityColl] Compare the size and the checksum"
            ++ " of DOs in *sCollPath:*source_res: and *dCollPath:*dest_res:");

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

    *totalResult = bool("true");
    # Get the length of the source collection string
    msiStrlen(*sCollPath,*pathLength);
    # For each DO in the sorce collection recursively compare checksum amd size
    # with the DO in the destination collection.
    # If they do not match, write an error in the b2safe log
    foreach(*Row in SELECT DATA_NAME, DATA_RESC_NAME, COLL_NAME 
            WHERE DATA_RESC_NAME like '*source_res' and COLL_NAME = '*sCollPath' || like '*sCollPath/%') {
        *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
        msiSubstr(*objPath, str(int(*pathLength)+1), "null", *subCollection);
        *destination = "*dCollPath/*subCollection";
        *result = EUDATCheckIntegrityDO(*objPath, *source_res, *destination, *dest_res, *logEnabled, *singleRes);
        if (!*result) {
            *contents = "*objPath::*destination::*result::*singleRes";
            *check_response = *check_response ++ *contents ++ ",";
        }
        *totalResult = *result && *totalResult;
    }
    *check_response = trimr(*check_response, ",");

    *totalResult;
}

EUDATCheckIntegrityColl(*sCollPath, *dCollPath, *logEnabled, *check_response) {
    *source_res = "null";
    *dest_res = "null";
    *totalResult =  EUDATCheckIntegrityColl(*sCollPath, *source_res, *dCollPath, *dest_res, 
                                            *logEnabled, *check_response);
    *totalResult;
}

# Checks differences about checksum and size between two Data Objects
# and log the result to the B2SAFE logging system
# 
# Parameters:
#    *source         [IN] path of source file in iRODS
#    *source_res     [IN]  iRODS resource name of the source
#    *destination    [IN] path of target file in iRODS
#    *dest_res       [IN]  iRODS resource name of the destination
#    *logEnabled     [IN] boolean value: "true" to enable the logging system, 
#                                        "false" to silence it.
#    *response       [OUT] the reason of the failure
#
# Author: Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATCheckIntegrityDO(*source, *source_res, *destination, *dest_res, *logEnabled, *response) {
        
    *status = bool("true");
    *response = "";

    *err = errorcode(msiObjStat(*destination, *objStat));
    if (*err < 0) {
        *response = "missing replicated object";
        *status = bool("false");
    } else if (!EUDATCatchErrorSize(*source, *source_res, *destination, *dest_res, *response)) {
        *status = bool("false");
    } else if (!EUDATCatchErrorChecksum(*source, *source_res, *destination, *dest_res, *response)) {
        *status = bool("false");
    }
    if (*logEnabled) {
        EUDATUpdateLogging(*status, *source, *destination, *response);
    }

    *status;
}

EUDATCheckIntegrityDO(*source, *destination, *logEnabled, *response) {
    *source_res = "null";
    *dest_res = "null";
    *status = EUDATCheckIntegrityDO(*source, *source_res, *destination, *dest_res, 
                                    *logEnabled, *response);
    *status;
}
