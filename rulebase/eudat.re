################################################################################
#                                                                              #
# EUDAT Safe-Replication and PID management rule set                           #
#                                                                              #
################################################################################

# List of the functions:
#
# ---- logging ---
# logVerbose(*msg)
# logInfo(*msg)
# logDebug(*msg)
# logError(*msg)
# logWithLevel(*level, *msg)
#---- authorization ---
# EUDATAuthZ(*user, *action, *target, *response)
# EUDATGetPAMusers(*json_map)
#---- utility ---
# EUDATObjExist(*path, *response)
# EUDATPushMetadata(*path, *queue)
# EUDATPushCollMetadata(*path, *queue)
# EUDATPushObjMetadata(*path, *queue)
# EUDATMessage(*queue, *message)
# EUDATLog(*message, *level)
# EUDATQueue(*action, *message, *number)
# ---- core ---
# EUDATtoBoolean(*var)
# EUDATReplaceHash(*path, *out)
# EUDATGetZoneNameFromPath(*path, *out)
# EUDATGetZoneHostFromZoneName(*zoneName, *conn)
# EUDATiCHECKSUMdate(*coll, *name, *resc, *modTime)
# EUDATiCHECKSUMretrieve(*path, *checksum, *modtime, *resource)
# EUDATiCHECKSUMget(*path, *checksum, *modtime, *resource)
# EUDATgetObjectTimeDiff(*filePath, *mode, *age)
# EUDATgetObjectAge(*filePath, *age) 
# EUDATfileInPath(*path,*subColl)
# EUDATCreateAVU(*Key,*Value,*Path)
# EUDATgetLastAVU(*Path, *Key, *Value)
# EUDATgetCollAVU(*path, *res)
# EUDATgetBulkMetadata(*path, *res)
# EUDATgetObjMetadata(*path, *res)
# EUDATcountMetaKeys( *Path, *Key, *Value )
#---- repository packages ---
# EUDATrp_checkMeta(*source,*AName,*AValue)
# EUDATrp_ingestObject( *source )
# EUDATrp_transferInitiated( *source )
# EUDATrp_transferFinished( *source )


################################################################################
#                                                                              #
# Logging policies                                                             #
#                                                                              #
################################################################################
logVerbose(*msg) {
    getEUDATLoggerLevel(*level);
    if (*level == 3) {
        logWithLevel("verbose", *msg);
    }
}

logDebug(*msg) {
    getEUDATLoggerLevel(*level);
    if (*level >= 2) {
        logWithLevel("debug", *msg);
    }
}

logInfo(*msg) {
    getEUDATLoggerLevel(*level);
    if (*level >= 1) {
        logWithLevel("info", *msg);
    }
}

logError(*msg) {
    getEUDATLoggerLevel(*level);
    if (*level >= 0) {
        logWithLevel("error", *msg);
    }
}

logWithLevel(*levelstring, *msg) {
    if (*levelstring == "info") { writeLine("serverLog","INFO: *msg");}
    else if (*levelstring == "debug") { writeLine("serverLog","DEBUG: *msg");}
    else if (*levelstring == "error") { writeLine("serverLog","ERROR: *msg");}
    else if (*levelstring == "verbose") { writeLine("serverLog","VERBOSE: *msg");}
}

################################################################################
#                                                                              #
# Authorization functions                                                      #
#                                                                              #
################################################################################

# Return a boolean value:
#   True, if the authorization request matches against, at least
#   one assertion listed in the authz.map.json file
#   False otherwise.
#
# Parameters:
#   *user           [IN]    a username, related to the user who request a permission
#   *action         [IN]    the action, which the user would like to perform
#   *target         [IN]    the target of the action
#   *response       [OUT]   True or False depending on authorization rights
#
# Author: Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATAuthZ(*user, *action, *target, *response) {
    getAuthZParameters(*authZMapPath);
    logVerbose("checking authorization for *user to perform: *action *target");
    msiExecCmd("authZmanager.py", "*authZMapPath check *user '*action' '*target'",
               "null", "null", "null", *outAuthZ);
    msiGetStdoutInExecCmdOut(*outAuthZ, *response);
    if (*response == "False") {
        # here should be placed specific authorization rules 
        # EUDATsetFilterACL(*action, *target, null, null, *status);
        # if (*status == "false") {}
        logVerbose("authorization denied");
        msiExit("-1", "user is not allowed to perform the requested action");
    }
    else {
        # here should be placed specific authorization rules 
        # EUDATsetFilterACL(*action, *target, null, null, *status);
        # if (*status == "true") {}
        logVerbose("authorization granted");
    }
}

################################################################################
#                                                                              #
# Utility functions                                                            #
#                                                                              #
################################################################################


# Push system level metadata to the messaging system.
# The metadata are extracted recursively for the root collection, all the sub-collections
# and the contained objects.
# 
# Parameters:
#   *path     [IN]    the  path of the object
#   *response [OUT]    response
# return:     true/false
# 
# Author: Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATObjExist(*path, *response) {
    *res = bool("true");
    *response = "*path exists and it is an object";
    if (errormsg(msiObjStat(*path,*out), *errmsg) < 0) {
        *response = "*path does not exist or it is not readable or it is not an object";
        logError("[EUDATObjExist] *response");
        *res = bool("false");
    }
    *res;
}

# Push system level metadata to the messaging system.
# The metadata are extracted recursively for the root collection, all the sub-collections
# and the contained objects.
# 
# Parameters:
#   *path     [IN]    the  path of the collection
#   *queue    [IN]    the messaging system queue
# 
# Author: Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATPushMetadata(*path, *queue) {

    logInfo("[EUDATPushMetadata] pushing metadata of collection *path to topic *queue")
    # loop over the sub-collections of the collection
    foreach (*Row in SELECT COLL_NAME WHERE COLL_NAME = '*path' || like '*path/%') {
        *msg = '{ ' ++ *Row.COLL_NAME ++ ':';
        EUDATgetCollAVU(*Row.COLL_NAME, *res_coll);
        EUDATgetBulkMetadata(*Row.COLL_NAME, *res_objs);
        *message = *msg ++ '{ *res_coll, objects: [*res_objs] } }';
        logDebug("[EUDATPushMetadata] message: *message");
        EUDATMessage(*queue, *message); 
    }
}

# Push system level metadata to the messaging system.
# The metadata are extracted for the collection
# 
# Parameters:
#   *path     [IN]    the  path of the collection
#   *queue    [IN]    the messaging system queue
# 
# Author: Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATPushCollMetadata(*path, *queue) {

    logInfo("[EUDATPushCollMetadata] pushing metadata of collection *path to topic *queue")
    *msg = '{ ' ++ *path ++ ':';
    EUDATgetCollAVU(*path, *res_coll);
    *message = *msg ++ '{ *res_coll, objects: [] } }';
    logDebug("[EUDATPushCollMetadata] message: *message");
    EUDATMessage(*queue, *message);
}    


# Push system level metadata to the messaging system.
# The metadata are extracted for an object.
# 
# Parameters:
#   *path     [IN]    the path of the object
#   *queue    [IN]    the messaging system queue
# 
# Author: Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATPushObjMetadata(*path, *queue) {

    logInfo("[EUDATPushObjMetadata] pushing metadata of obj *path to topic *queue")
    msiSplitPath(*path, *parent, *child);
    *msg = '{ ' ++ *parent ++ ':';
    EUDATgetObjMetadata(*path, *res_objs);
    *message = *msg ++ '{ objects: [*res_objs] } }';
    logDebug("[EUDATPushObjMetadata] message: *message");
    EUDATMessage(*queue, *message);
}


# It manages the writing and reading of log messages to/from external log services.
# The current implementation writes the logs to specific log file.
#
# Return
#  no response is expected
#
# Parameters:
#   *queue     [IN]    the queue which will host the message,
#                      set it to None if you want to use the control queue
#   *message   [IN]    the message to be sent
#
# Author: Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATMessage(*queue, *message) {

    *res = 'None';
    getMessageParameters(*msgConfPath, *ctrlQName, *enabled);
    if (*enabled) {
        logInfo("[EUDATMessage] sending message to the topic '*queue'");
        logVerbose("[EUDATMessage] message '*message'");
        if (*queue == 'None') {
            logDebug("[EUDATMessage] creating a new topic");
            msiExecCmd("messageManager.py", "*msgConfPath topic -m create '*message'",
                       "null", "null", "null", *outMessage1);
            msiGetStdoutInExecCmdOut(*outMessage1, *outResp1);
            logVerbose("[EUDATMessage] output: *outResp1");
            *res = trimr(*outResp1, "\n");
            *queue = *ctrlQName;
            logDebug("[EUDATMessage] creating a new subscription for topic: *res");
            *subName = *res ++ "_NOTIFY";
            msiExecCmd("messageManager.py", "*msgConfPath sub create '*subName' '*res'",
                       "null", "null", "null", *outMessage2);
            msiGetStdoutInExecCmdOut(*outMessage2, *outResp2);
            logVerbose("[EUDATMessage] output: *outResp2");
        }
        logDebug("[EUDATMessage] sending the message"); 
        msiExecCmd("messageManager.py", "*msgConfPath publish *queue *message", 
                   "null", "null", "null", *outMessage);
        msiGetStdoutInExecCmdOut(*outMessage, *outResp);
        logVerbose("[EUDATMessage] output: *outResp");
    }
    *res
}

# It manages the writing and reading of log messages to/from external log services.
# The current implementation writes the logs to specific log file.
#
# Return
#  no response is expected
#
# Parameters:
#   *message        [IN]    the message to be logged
#   *level          [IN]    the logging level 
#
# Author: Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATLog(*message, *level) {
    getLogParameters(*logConfPath);
    logVerbose("[EUDATLog] logging message '*message'");
    *err = errormsg(msiExecCmd("logmanager.py", "*logConfPath log *level *message",
                    "null", "null", "null", *outLog), *errmsg);
    if (*err < 0) {
        logError("[EUDATLog] Error: *errmsg");
    }
    else {
        logVerbose("[EUDATLog] message logged succesfully");
    }
}

# It implements a FIFO queue for messages to/from external log services.
#
# Return
#  no response is expected for action "push"
#  The first message of the queue for action "pop"
#
# Parameters:
#   *action         [IN]    the queueing action, which the user would like to perform
#                           [ push | pop ]
#   *message        [IN/OUT]the message to be queued or read.
#                           It can be a comma separated list of strings, each between single apices.
#   *number         [IN]    the number of elements to be extracted
#
# Author: Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATQueue(*action, *message, *number) {
    logDebug("[EUDATQueue] performing action *action");
    getLogParameters(*logConfPath);
    *options = "";
    if (*action == 'pop' || *action == 'queuesize') {
        *message = "";
    }
    if (*action == 'pop' && int(*number) > 1) {
        *options = "-n "++str(*number);
    }
    *err = errormsg(msiExecCmd("logmanager.py", "*logConfPath *action *options *message",
                    "null", "null", "null", *outQueue), *errmsg);
    if (*err < 0) {
        logError("[EUDATQueue] Error: *errmsg");
    }
    else {
        if (*action == 'pop' || *action == 'queuesize') {
            msiGetStdoutInExecCmdOut(*outQueue, *message);
            logVerbose("[EUDATQueue] output: *message");
        }
        if (*action == 'pop' && int(*number) > 1) {
            *message = triml(*message, "[");
            *message = trimr(*message, "]");
            logVerbose("[EUDATQueue] output: *message");
        }
    } 
}

# Function: transform string to boolean value
#
# Author: Claudio Cacciari (Cineca)
#-----------------------------------------------
EUDATtoBoolean(*var) {
    logVerbose("[EUDATtoBoolean] converting variable *var to boolean");
    if (*var == "None" || *var == "" || *var == "False" || *var == "false" || *var == "FALSE") {
        *status = bool("false");
    }
    else {
        *status = bool("true");
    }
    *status
}

# Function: replace epicclient function
#
# Author: Robert Verkerk SURFsara
#-------------------------------------------------------------------------------
EUDATReplaceHash(*path, *out) {
 
    logVerbose("[EUDATReplaceHash] replacing bad chars in *path");
    # replace #
    *out=*path;
    foreach ( *char in list("#","%","&") ) {
       *list = split("*out","*char");
       *n = "";
       foreach (*t in *list) {
          *n = *n ++ *t ++ "*";
       }
       msiStrchop(*n,*n_chop);
       *out = *n_chop;
    }
    logVerbose("[EUDATReplaceHash] replaced bad chars: *out");
}

# Function: replace microservice msiGetZoneNameFromPath (eudat.c)
#
# Author: Long Phan, JSC
#-------------------------------------------------------------------------------
EUDATGetZoneNameFromPath(*path, *out) {

    logVerbose("[EUDATGetZoneNameFromPath] getting zone name from: *path");
    *list = split("*path","/");
    *out = elem(*list,0);
    logVerbose("[EUDATGetZoneNameFromPath] got zone name: *out");
}

# Gets the connection details of an iRODS Zone.
#
# Arguments:
#   *zoneName      [IN]    the IRODS Zone
#   *conn          [OUT]   the connection details related to the input iRODS Zone (hostname:port)
#                       
# Author: Claudio Cacciari, Cineca
#-------------------------------------------------------------------------------
EUDATGetZoneHostFromZoneName(*zoneName, *conn) {

    logVerbose("[EUDATGetZoneHostFromZoneName] getting host from zone: *zoneName");    
    *conn = ""
    foreach ( *row in SELECT ZONE_CONNECTION WHERE ZONE_NAME = '*zoneName') {
        *conn = *row.ZONE_CONNECTION;
    }
    # the local zone does not store the connection details
    # then get them from the eudat.local rule set
    if (*conn == "") {
        foreach ( *line in SELECT ZONE_TYPE WHERE ZONE_NAME = '*zoneName') {
            *type = *line.ZONE_TYPE;
        }
        if (*type == "local") {
            getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
            # expected serverID = irods://hostname:port
            msiSubstr("*serverID", "8", "-1", *conn);
        }
    }
    logVerbose("[EUDATGetZoneHostFromZoneName] got host: *conn");
}

# Checks if date of the last computation of iCHECKSUM was set and set the date if not.
# The date is stored as metadata attribute of name 'eudat_dpm_checksum_date:<name of resc>'
#
# Environment variable used:
#
# Arguments:
#   *coll               [IN]    the collection of the data object
#   *name               [IN]    the name of the data object
#   *resc               [IN]    the resource on which the object is located
#   *modTime            [IN]    time of thee last modification of the object
#                               - will be assumed as time of the first computation of the iCHECKSUM
#
# Author: Michal Jankowski, PSNC
#-------------------------------------------------------------------------------
EUDATiCHECKSUMdate(*coll, *name, *resc, *modTime) {

    logDebug("[EUDATiCHECKSUMdate] setting checksum timestamp for *coll/*name");
    *metaName = 'eudat_dpm_checksum_date:*resc';    
    foreach (*row in SELECT count(META_DATA_ATTR_VALUE) WHERE COLL_NAME = '*coll' 
             AND DATA_NAME = '*name' AND META_DATA_ATTR_NAME = '*metaName') {
       *count = *row.META_DATA_ATTR_VALUE
        #*count = 0 means the attr was not set
        if (*count=="0"){
            logDebug("[EUDATiCHECKSUMdate] setting *metaName=*modTime for *coll/*name.");
            msiString2KeyValPair("*metaName=*modTime",*kvpaircs);
            msiSetKeyValuePairsToObj(*kvpaircs, "*coll/*name", "-d")
        }else{
            logDebug("[EUDATiCHECKSUMdate] *metaName already set for *coll/*name.");
        }   
    }   
}   
 
# The function retrieve iCHECKSUM for a given object.
#
# Environment variable used:
#
# Arguments:
#   *path               [IN]    the iRODS path of the object involved in the query
#   *checksum           [OUT]   iCHECKSUM
#   *modtime            [OUT]   modification time of the checksum
#   *resource           [IN]    irods resource name
#   *status             [REI]   false if no value is found, true elsewhere
#
# Author: Giacomo Mariani, CINECA, Michal Jankowski PSNC
#-------------------------------------------------------------------------------
EUDATiCHECKSUMretrieve(*path, *checksum, *modtime, *resource) {
    *status = bool("false");
    *checksum = "";
    *modtime = "";
    logDebug("[EUDATiCHECKSUMretrieve] getting checksum for *path");
    msiSplitPath(*path, *coll, *name);
    #Loop over all resources, possibly the checksum was not computed for all of them
    foreach ( *c in SELECT DATA_CHECKSUM, DATA_RESC_NAME, DATA_MODIFY_TIME WHERE DATA_NAME = '*name' AND COLL_NAME = '*coll') {
        *checksumTmp = *c.DATA_CHECKSUM;
        *resc = *c.DATA_RESC_NAME;      
        *modtime = *c.DATA_MODIFY_TIME;

        if (*checksumTmp=="") {
            logDebug("[EUDATiCHECKSUMretrieve] the iCHECKSUM on resource *resc is empty.");
        } 
        else {
            *checksum = *checksumTmp;
            logDebug("[EUDATiCHECKSUMretrieve] iCHECKSUM = *checksum on resource *resc");
            # EUDATiCHECKSUMdate is called here instead just after msiDataObjChksum in EUDATiCHECKSUMget
            # because it is not the only possible point the checksum may be computed
            # other ones are "ichksum", "iput -k", "irepl" (on checksumed source) called by the user.
            EUDATiCHECKSUMdate(*coll, *name, *resc, *modtime);
            *status = bool("true");
            if (*resource != "None" && *resource != "" && *resource == *resc) {
                break;
            }
        }
    }
    *status;
}

# The function obtain iCHECKSUM for a given object creating it if necessary.
#
# Arguments:
#   *path               [IN]    the iRODS path of the object involved in the query
#   *checksum           [OUT]   iCHECKSUM
#   *modtime            [OUT]   modification time of the checksum
#   *resource           [IN]    iRODS resource name
#
# Author: Giacomo Mariani, CINECA, Michal Jankowski PSNC
#-------------------------------------------------------------------------------
EUDATiCHECKSUMget(*path, *checksum, *modtime, *resource) {
    logDebug("[EUDATiCHECKSUMget] getting checksum for *path");
    if (!EUDATiCHECKSUMretrieve(*path, *checksum, *modtime, *resource)) {
        #If it is a collection, do not calculate the checksum
        msiGetObjType(*path,*type);
        if (*type == '-d')  {
            msiDataObjChksum(*path, "forceChksum", *checksum);
            logDebug("[EUDATiCHECKSUMget] got checksum: *checksum");
        }
        #call again EUDATiCHECKSUMretrieve in order to set checksum date
        EUDATiCHECKSUMretrieve(*path, *checksum, *modtime, *resource);
    }
}

# Calculate the difference between the creation time or the current time
# and the modification time of an object. In seconds.
#
# Arguments:
#   *filePath      [IN]   The full iRODS path of the object
#   *mode          [IN]   The way to calculate the time difference [1,2]
#                         mode 1: modification time - creation time
#                         mode 2: now - modification time
#   *age           [OUT]  The age of the object in seconds
#                         *age = -1 if the object does not exist
#
# Author: Giacomo Mariani, CINECA
#-------------------------------------------------------------------------------
EUDATgetObjectTimeDiff(*filePath, *mode, *age) {
    logDebug("[EUDATgetObjectTimeDiff] getting object *filePath time difference");
    *age = -1;
    # Check if the file exists 
    if(errormsg(msiObjStat(*filePath,*out), *errmsg) < 0) {
        logDebug("[EUDATgetObjectTimeDiff] object  does not exist");
        logError("[EUDATgetObjectTimeDiff] *errmsg");
    }
    else {
        # Look when the file has been created in iRODS
        msiSplitPath(*filePath, *fileDir, *fileName);   
        foreach ( *ec in SELECT DATA_CREATE_TIME, DATA_MODIFY_TIME WHERE DATA_NAME = '*fileName' 
                  AND COLL_NAME = '*fileDir') {
            *creationTime = *ec.DATA_CREATE_TIME;
            logVerbose("[EUDATgetObjectTimeDiff] Created at *creationTime");
            *modifyTime = *ec.DATA_MODIFY_TIME;
            logVerbose("[EUDATgetObjectTimeDiff] Modified at *modifyTime");
        }
        if (*mode == "1") {
            *age=int(*modifyTime)-int(*creationTime);
        }
        else if (*mode == "2") {
            msiGetSystemTime(*Now,"unix");
            *age=int(*Now)-int(*modifyTime);
        }
        logDebug("[EUDATgetObjectTimeDiff] Difference in time: *age seconds");
    }
}

# Calculate the difference between the current time and the modification time of an object.
# In seconds.
#
# Arguments:
#   *filePath      [IN]   The full iRODS path of the object
#   *age           [OUT]  The age of the object in seconds
#                         *age = -1 if the object does not exist
#
# Author: Claudio Cacciari, CINECA
#-------------------------------------------------------------------------------
EUDATgetObjectAge(*filePath, *age) {
    logDebug("[EUDATgetObjectAge] getting the difference between now"
             ++ " and the modification time of the object: *filePath");
    *age = -1;
    # Check if the file exists
    if(errormsg(msiObjStat(*filePath,*out), *errmsg) >= 0) {
        EUDATgetObjectTimeDiff(*filePath, "2", *age);
        logDebug("[EUDATgetObjectAge] the age is: *age");
    }
    else {
        logDebug("[EUDATgetObjectAge] object *filePath does not exist");
        logError("[EUDATgetObjectAge] *errmsg");
    }
    *age;
}

# Rules to check if a file is in a given path.
#
# Arguments:
#   *path               [IN]    The full iRODS path of the object
#   *subColl            [IN]    The iRODS path of the collection we are looking in for the object
#   *b                  [REI]   False if no value is found, trou elsewhere
#
# Author: Hao Xu, DICE; Giacomo Mariani, CINECA
#-------------------------------------------------------------------------------
EUDATfileInPath(*path,*subColl) {
    logInfo("[EUDATfileInPath] checking if object *path is in collection *subColl");
    msiSplitPath(*path, *coll, *name);
    *b = bool("false");
    foreach ( *c in SELECT count(DATA_NAME) WHERE COLL_NAME like '*subColl' AND DATA_NAME = '*name' ) {
        *num = *c.DATA_NAME;
        if(*num == '1') {
            logDebug("[EUDATfileInPath] found object *name in collection *subColl");
            *b = bool("true");
            break;
        }   
    }
    *b;
}

# Create AVU with INPUT *Key, *Value for DataObj *Path
#
# Parameters:
#	*Key	[IN]	Key in AVU
#	*Value	[IN]	Value in AVU
#	*Path	[IN]	Path of log_file
# 
# Author: Long Phan, JSC
# Modified: Elena Erastova, RZG, 27.08.2015
#------------------------------------------------------------------------------- 
EUDATCreateAVU(*Key, *Value, *Path) {
    logDebug("[EUDATCreateAVU] Adding AVU: *Key = *Value to metadata of *Path");
    msiAddKeyVal(*Keyval, *Key, *Value);
    msiGetObjType(*Path, *objType);
    msiSetKeyValuePairsToObj(*Keyval, *Path, *objType);
}

# get the single value of a specific metadata in ICAT
#
# Parameters:
# *path  [IN] target object/collection
# *key   [IN] name of the MD
# *value [OUT] value of the MD, None if not set.
#
# Author: Pascal Dugénie (CINES), Claudio Cacciari (Cineca)
#-----------------------------------------------------------------------------
EUDATgetLastAVU(*path, *key, *value) {
    logVerbose("[EUDATgetLastAVU] getting the last value of the AVUs with key *key in path *path");
    *value = 'None';
    *avus = list();
    msiGetObjType(*path, *type);
    if (*type == '-c')  {
        *d = SELECT META_COLL_ATTR_VALUE WHERE COLL_NAME = '*path' AND META_COLL_ATTR_NAME = '*key';
        foreach(*c in *d) {
            *avus = cons(*c.META_COLL_ATTR_VALUE, *avus);
        }
    }
    else {
        msiSplitPath(*path, *parent, *child);
        foreach ( *B in SELECT META_DATA_ATTR_VALUE WHERE META_DATA_ATTR_NAME = '*key' 
                  AND COLL_NAME = '*parent' AND DATA_NAME = '*child') {
            *avus = cons(*B.META_DATA_ATTR_VALUE, *avus);
        }
    }
    if (size(*avus) > 0) {
        *value = hd(*avus);
    }
    logVerbose("[EUDATgetLastAVU] got the value *value");
}

# Get all the AVUs of a collection
#
# Parameters:
# *path  [IN]  target collection
# *res   [OUT] the AVUs
#
# Author: Claudio Cacciari, Cineca
#-----------------------------------------------------------------------------
EUDATgetCollAVU(*path, *res)
{
    logDebug("[EUDATgetCollAVU] getting AVU for collection *path");
    *res = '';
    *owner = '';
    foreach ( *R in SELECT COLL_OWNER_NAME WHERE COLL_NAME = '*path' ) {
        *owner = *R.COLL_OWNER_NAME
        *res = *res ++ "owner:" ++ *owner;
    }
    foreach ( *R in SELECT META_COLL_ATTR_NAME,META_COLL_ATTR_VALUE WHERE COLL_NAME = '*path' ) {
        *res = *res ++ *R.META_COLL_ATTR_NAME ++ ":" ++*R.META_COLL_ATTR_VALUE ++ ",";
    }
    logVerbose("[EUDATgetCollAVU] AVUs: *res");
}

# Get all the AVUs of the objects under a collection
#
# Parameters:
# *path  [IN]  target collection
# *res   [OUT] the AVUs
#
# Author: Claudio Cacciari, Cineca
#-----------------------------------------------------------------------------
EUDATgetBulkMetadata(*path, *res) {
    logDebug("[EUDATgetBulkMetadata] getting objects' metadata for collection *path");
    *res = '';
    *name_old = '';
    foreach ( *R in SELECT META_DATA_ATTR_NAME, META_DATA_ATTR_VALUE, DATA_CHECKSUM, 
                           DATA_NAME, DATA_OWNER_NAME, DATA_RESC_NAME 
                           WHERE COLL_NAME = '*path' AND DATA_REPL_NUM = '0') {
        if (*name_old != *R.DATA_NAME) {
            *res = *res ++ *R.DATA_NAME ++ "=:=resource=:=" ++ *R.DATA_RESC_NAME ++ ",";           
            *res = *res ++ *R.DATA_NAME ++ "=:=owner=:=" ++ *R.DATA_OWNER_NAME ++ ",";
            *res = *res ++ *R.DATA_NAME ++ "=:=checksum=:=" ++ *R.DATA_CHECKSUM ++ ",";
        }
        *res = *res ++ *R.DATA_NAME ++ "=:=" ++ *R.META_DATA_ATTR_NAME ++ "=:=" ++ *R.META_DATA_ATTR_VALUE ++ ",";
        *name_old = *R.DATA_NAME
    }
    *res = trimr(*res, ',');
    logVerbose("[EUDATgetBulkMetadata] metadata: *res");
}

# Get all the AVUs of the object
#
# Parameters:
# *path  [IN]  target object
# *res   [OUT] the AVUs
#
# Author: Claudio Cacciari, Cineca
#-----------------------------------------------------------------------------
EUDATgetObjMetadata(*path, *res) {
    logDebug("[EUDATgetObjMetadata] getting object's metadata for path *path");
    *res = '';
    msiSplitPath(*path, *parent, *child);
    foreach ( *R in SELECT DATA_CHECKSUM, DATA_NAME, DATA_OWNER_NAME, DATA_RESC_NAME
                           WHERE COLL_NAME = '*parent' AND DATA_NAME = '*child' AND DATA_REPL_NUM = '0') {
        *res = *res ++ *R.DATA_NAME ++ "=:=resource=:=" ++ *R.DATA_RESC_NAME ++ ",";
        *res = *res ++ *R.DATA_NAME ++ "=:=owner=:=" ++ *R.DATA_OWNER_NAME ++ ",";
        *res = *res ++ *R.DATA_NAME ++ "=:=checksum=:=" ++ *R.DATA_CHECKSUM ++ ",";
    }
    foreach ( *R in SELECT META_DATA_ATTR_NAME, META_DATA_ATTR_VALUE
                           WHERE COLL_NAME = '*parent' AND DATA_NAME = '*child' AND DATA_REPL_NUM = '0') {
        *res = *res ++ *R.DATA_NAME ++ "=:=" ++ *R.META_DATA_ATTR_NAME ++ "=:=" ++ *R.META_DATA_ATTR_VALUE ++ ",";
    }
    *res = trimr(*res, ',');
    logVerbose("[EUDATgetObjMetadata] metadata: *res");
}


# count metadata in ICAT
#
# Parameters:
# *Path [IN] target object
# *Key  [IN] name of the MD
# *Value [OUT] number of AVUs with name=Key
#
# Author: Pascal Dugénie, CINES
#-----------------------------------------------------------------------------
EUDATcountMetaKeys( *Path, *Key, *Value ) {
    logDebug("[EUDATcountMetaKeys] counting the AVUs with key *Key in path *Path");
    msiSplitPath(*Path, *parent , *child );
    foreach ( *B in SELECT count(META_DATA_ATTR_VALUE) WHERE META_DATA_ATTR_NAME = '*Key' 
              AND COLL_NAME = '*parent' AND DATA_NAME = '*child') {
        *Value = *B.META_DATA_ATTR_VALUE;
    }
    logVerbose("[EUDATcountMetaKeys] got count = *Value");     
}

# get the content of the user map file for OAuth2 authentication in json format
# 
# Parameters:
#     *json_map     [OUT] a string representing the user mapping
#
# Author: Claudio Cacciari, CINECA
# -----------------------------------------------------------------------------
EUDATGetPAMusers(*json_map) {
    logVerbose("[EUDATGetPAMusers] checking authorization for $userNameClient to read users");
    EUDATAuthZ($userNameClient, "read", "users", *response);
    msiExecCmd("pam_user_reader.py", "null", "null", "null", "null", *outUsersJson);
    msiGetStdoutInExecCmdOut(*outUsersJson, *json_map);    
    logVerbose("[EUDATGetPAMusers] json user map = *json_map");
}

################################################################################
#                                                                              #
# Repository Packages                                                          #
#                                                                              #
################################################################################

# Check if the ADMIN_Status value is set to Ready ToArchive and then kicks off ingestion
#
# Parameters:
# *source [IN] target object
# *AName [IN] name of the MD that has been modified
# *AValue [IN] value of the MD that has been modified
#
# Author: Pascal Dugénie, CINES
# updated : Stéphane Coutin (CINES) - 26/8/14 (Use ROR instead of EUDAT_ROR as attribute name)
#-----------------------------------------------------------------------------
EUDATrp_checkMeta(*source,*AName,*AValue)
{
    if ((*AName == "n:ADMIN_Status") && ( *AValue == "v:ReadyToArchive"))
    {
        EUDATrp_ingestObject(*source);
    }
}

# Manage the ingestion in B2SAFE
# Check the checksum
# Create PID
#
# Parameters:
# *source [IN] target object to assign a PID
#
# Author: Stephane Coutin (CINES)
# updated : Stéphane Coutin (CINES)
# 23/10/14 (use EUDATiCHECKSUMget to avoid duplicate checksum calculation)
#-----------------------------------------------------------------------------
EUDATrp_ingestObject( *source )
{
    rp_getRpIngestParameters(*protectArchive, *archiveOwner);
    logInfo("ingestObject-> Check for (*source)");
    *resource = "";
    EUDATiCHECKSUMget(*source, *checksum, *modtime, *resource);
    EUDATCreateAVU("INFO_Checksum", *checksum, *source);
# Modified begin 
    EUDATgetLastAVU(*source, "OTHER_original_checksum", *orig_checksum);
# Modified end
    if ( *checksum == *orig_checksum )
    {
        logInfo("ingestObject-> Checksum is same as original = *checksum");
        EUDATCreateAVU("ADMIN_Status", "Checksum_ok", *source);
	EUDATgetLastAVU( *source, "EUDAT/ROR" , *RorValue );
        EUDATCreatePID("None", *source, *RorValue, "None", "false", *PID);
        # test PID creation
        if((*PID == "empty") || (*PID == "None") || (*PID == "error")) {
            logInfo("ingestObject-> ERROR while creating the PID for *source PID = *PID");
            EUDATCreateAVU("ADMIN_Status", "ErrorPID", *source);
        }
        else {
            logInfo("ingestObject-> PID created for *source PID = [*PID] ROR = [*RorValue]");
            EUDATCreateAVU("ADMIN_Status", "Archive_ok", *source);
            if (*protectArchive) {
                logInfo("ingestObject-> changing *source owner to = *archiveOwner with read access to$userNameClient");
                msiSetACL("default","read",$userNameClient,*source);
                msiSetACL("default","own",*archiveOwner,*source);
            }
        }
    }
    else
    {
        logInfo("ingestObject-> Checksum (*checksum) is different than original (*orig_checksum)");
        EUDATCreateAVU("ADMIN_Status", "ErrorChecksum", *source);
    }
}

# Process executed when a transfer has been initiated
# (this process is triggered by the iputPreProc hook)
#
# Parameters:
# *source [IN] target object to assign a new value
#
# Author: Pascal Dugénie, CINES
#-----------------------------------------------------------------------------
EUDATrp_transferInitiated( *source )
{
   EUDATCreateAVU("ADMIN_Status", "TransferStarted", *source);
   msiGetSystemTime( *TimeNow, "human" );
   EUDATCreateAVU("INFO_TimeOfStart", *TimeNow, *source);
}

# Process executed after a transfer is finished
# (this process is triggered by the iputPostProc hook)
#
# Parameters:
# *source [IN] target object to assign a new value
#
# Author: Pascal Dugénie, CINES
#-----------------------------------------------------------------------------
EUDATrp_transferFinished( *source )
{
   EUDATCreateAVU("ADMIN_Status", "TransferFinished", *source);
   msiGetSystemTime( *TimeNow, "human" );
   EUDATCreateAVU("INFO_TimeOfTransfer", *TimeNow, *source);
}
