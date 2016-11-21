################################################################################
#                                                                              #
# EUDAT Safe-Replication and PID management rule set                           #
#                                                                              #
################################################################################

# List of the functions:
#
#---- authorization ---
# EUDATAuthZ(*user, *action, *target, *response)
#---- utility ---
# EUDATisMetadata(*path)
# EUDATMessage(*queue, *message)
# EUDATLog(*message, *level)
# EUDATQueue(*action, *message, *number)
# ---- logging ---
# logInfo(*msg)
# logDebug(*msg)
# logError(*msg)
# logWithLevel(*level, *msg)
# ---- core ---
# EUDATtoBoolean(*var)
# EUDATReplaceHash(*path, *out)
# EUDATGetZoneNameFromPath(*path, *out)
# EUDATGetZoneHostFromZoneName(*zoneName, *conn)
# EUDATiCHECKSUMdate(*coll, *name, *resc, *modTime)
# EUDATiCHECKSUMretrieve(*path, *checksum, *modtime)
# EUDATiCHECKSUMget(*path, *checksum, *modtime)
# EUDATgetObjectTimeDiff(*filePath, *mode, *age)
# EUDATgetObjectAge(*filePath, *age) 
# EUDATfileInPath(*path,*subColl)
# EUDATCreateAVU(*Key,*Value,*Path)
# EUDATgetLastAVU(*Path, *Key, *Value)
# EUDATModifyAVU(*Path, *Key, *Value) DEPRECATED
# EUDATcountMetaKeys( *Path, *Key, *Value )
# EUDATStoreJSONMetadata(*path, *pid, *ror, *checksum, *modtime)
#---- repository packages ---
# EUDATrp_checkMeta(*source,*AName,*AValue)
# EUDATrp_ingestObject( *source )
# EUDATrp_transferInitiated( *source )
# EUDATrp_transferFinished( *source )

################################################################################
#                                                                              #
# Authorization functions                                                      #
#                                                                              #
################################################################################

#
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
#
EUDATAuthZ(*user, *action, *target, *response) {
    getAuthZParameters(*authZMapPath);
    logDebug("checking authorization for *user to perform: *action *target");
    msiExecCmd("authZmanager.py", "*authZMapPath check *user '*action' '*target'",
               "null", "null", "null", *outAuthZ);
    msiGetStdoutInExecCmdOut(*outAuthZ, *response);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outAuthZ);
    }
    if (*response == "False") {
        # here should be placed specific authorization rules 
        # EUDATsetFilterACL(*action, *target, null, null, *status);
        # if (*status == "false") {}
        logDebug("authorization denied");
        msiExit("-1", "user is not allowed to perform the requested action");
    }
    else {
        # here should be placed specific authorization rules 
        # EUDATsetFilterACL(*action, *target, null, null, *status);
        # if (*status == "true") {}
        logDebug("authorization granted");
    }
}

################################################################################
#                                                                              #
# Utility functions                                                            #
#                                                                              #
################################################################################

# It verifies if the current path is a special path reserved for metadata.
#
# Return
#  True or False
#
# Parameters:
#   *path     [IN]    the  path of the object/collection
#
# Author: Claudio Cacciari, Cineca
#
EUDATisMetadata(*path) {
    *isMeta = bool("false");
    if (*path like regex ".*\\.metadata.*") {
        logDebug("the path *path is a metadata special path");
        *isMeta = bool("true");
    }
    *isMeta;
}


# It manages the writing and reading of log messages to/from external log services.
# The current implementation writes the logs to specific log file.
#
# Return
#  no response is expected
#
# Parameters:
#   *queue     [IN]    the queue which will host the message
#   *message   [IN]    the message to be sent
#
# Author: Claudio Cacciari, Cineca
#
EUDATMessage(*queue, *message) {
    getMessageParameters(*msgLogPath, *enabled);
    if (*enabled) {
        logInfo("sending message '*message' to the queue '*queue'");
        msiExecCmd("messageManager.py", "-l *msgLogPath send *queue *message",
                   "null", "null", "null", *outMessage);
        getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
        if (*msiFreeEnabled) {
            msifree_microservice_out(*outMessage);
        }
    }
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
#
EUDATLog(*message, *level) {
    getLogParameters(*logConfPath);
    logInfo("logging message '*message'");
    msiExecCmd("logmanager.py", "*logConfPath log *level *message",
               "null", "null", "null", *outLog);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outLog);
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
#
EUDATQueue(*action, *message, *number) {
    getLogParameters(*logConfPath);
    *options = "";
    if (*action == 'pop' || *action == 'queuesize') {
        *message = "";
    }
    if (*action == 'pop' && int(*number) > 1) {
        *options = "-n "++str(*number);
    }
    logInfo("logging action '*action' for message '*message'");
    msiExecCmd("logmanager.py", "*logConfPath *action *options *message",
               "null", "null", "null", *outQueue);
    if (*action == 'pop' || *action == 'queuesize') {
        msiGetStdoutInExecCmdOut(*outQueue, *message);
    }
    if (*action == 'pop' && int(*number) > 1) {
        *message = triml(*message, "[");
        *message = trimr(*message, "]");
    }
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outQueue);
    }
}

#
# Logging policies
#

logDebug(*msg) {
    getEUDATLoggerLevel(*level);
    if (*level == 2) {
        logWithLevel("debug", *msg);
    }
}

logInfo(*msg) {
    getEUDATLoggerLevel(*level);
    if ((*level == 1) || (*level == 2)) {
        logWithLevel("info", *msg);
    }
}

logError(*msg) {
    getEUDATLoggerLevel(*level);
    if ((*level == 0) || (*level == 1) || (*level == 2)) {
        logWithLevel("error", *msg);
    }
}

logWithLevel(*level, *msg) {
    on (*level == "info") { writeLine("serverLog","INFO: *msg");}
    on (*level == "debug") { writeLine("serverLog","DEBUG: *msg");}
    on (*level == "error") { writeLine("serverLog","ERROR: *msg");}
}

#-----------------------------------------------
# Function: trsnsfrom string to boolean value
#
# Author: Claudio Cacciari (Cineca)
#-----------------------------------------------
EUDATtoBoolean(*var) {
    logDebug("[EUDATtoBoolean] converting variable *var to boolean");
    if (*var == "None" || *var == "" || *var == "False" || *var == "false" || *var == "FALSE") {
        *status = bool("false");
    }
    else {
        *status = bool("true");
    }
    *status
}

#
# Function: replace epicclient function
#
# Author: Robert Verkerk SURFsara
#
EUDATReplaceHash(*path, *out) {
 
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
}

#
# Function: replace microservice msiGetZoneNameFromPath (eudat.c)
#
# Author: Long Phan, JSC
#
EUDATGetZoneNameFromPath(*path, *out) {

    *list = split("*path","/");
    *out = elem(*list,0);
}

#
# Gets the connection details of an iRODS Zone.
#
# Arguments:
#   *zoneName      [IN]    the IRODS Zone
#   *conn          [OUT]   the connection details related to the input iRODS Zone (hostname:port)
#                       
# Author: Claudio Cacciari, Cineca
#----------------------------------------------------------
EUDATGetZoneHostFromZoneName(*zoneName, *conn) {

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
}

#
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
#
EUDATiCHECKSUMdate(*coll, *name, *resc, *modTime) {

    *metaName = 'eudat_dpm_checksum_date:*resc';
    
    foreach (*row in SELECT count(META_DATA_ATTR_VALUE) WHERE COLL_NAME = '*coll' AND DATA_NAME = '*name' AND META_DATA_ATTR_NAME = '*metaName') {
       *count = *row.META_DATA_ATTR_VALUE
        #*count = 0 means the attr was not set
        if (*count=="0"){
            logInfo("EUDATiCHECKSUMdate -> Setting *metaName for *coll/*name.");
            msiString2KeyValPair("*metaName=*modTime",*kvpaircs);
            msiSetKeyValuePairsToObj(*kvpaircs, "*coll/*name", "-d")
        }else{
            logDebug("EUDATiCHECKSUMdate -> *metaName already set for *coll/*name.");
        }   
    }   
}   
 

#
# The function retrieve iCHECKSUM for a given object.
#
# Environment variable used:
#
# Arguments:
#   *path               [IN]    the iRODS path of the object involved in the query
#   *checksum           [OUT]   iCHECKSUM
#   *modtime            [OUT]   modification time of the checksum
#   *status             [REI]   false if no value is found, true elsewhere
#
# Author: Giacomo Mariani, CINECA, Michal Jankowski PSNC
#
EUDATiCHECKSUMretrieve(*path, *checksum, *modtime) {
    *status = bool("false");
    *checksum = "";
    *modtime = "";
    logInfo("EUDATiCHECKSUMretrieve -> Looking at *path");
    msiSplitPath(*path, *coll, *name);
    #Loop over all resources, possibly the checksum was not computed for all of them
    foreach ( *c in SELECT DATA_CHECKSUM, DATA_RESC_NAME, DATA_MODIFY_TIME WHERE DATA_NAME = '*name' AND COLL_NAME = '*coll') {
        *checksumTmp = *c.DATA_CHECKSUM;
        *resc = *c.DATA_RESC_NAME;      
        *modtime = *c.DATA_MODIFY_TIME;

        if (*checksumTmp==""){
            logInfo("EUDATiCHECKSUMretrieve -> The iCHECKSUM on resource *resc is empty.");
        }else{
            *checksum=*checksumTmp;
            logInfo("EUDATiCHECKSUMretrieve -> Found iCHECKSUM = *checksum on resource *resc.");
            #EUDATiCHECKSUMdate is called here instead just after msiDataObjChksum in EUDATiCHECKSUMget
            #because it is not the only possible point the checksum may be computed
            #other ones are "ichksum", "iput -k", "irepl" (on checksumed source) called by the user.
            EUDATiCHECKSUMdate(*coll, *name, *resc, *modtime);
            *status = bool("true");
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
#
# Author: Giacomo Mariani, CINECA, Michal Jankowski PSNC

EUDATiCHECKSUMget(*path, *checksum, *modtime) {
    if (!EUDATiCHECKSUMretrieve(*path, *checksum, *modtime)) {
        #If it is a collection, do not calculate the checksum
        msiGetObjType(*path,*type);
        if (*type == '-d')  {
            msiDataObjChksum(*path, "forceChksum", *checksum);
        }
        #call again EUDATiCHECKSUMretrieve in order to set checksum date
        EUDATiCHECKSUMretrieve(*path, *checksum, *modtime);
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
#
EUDATgetObjectTimeDiff(*filePath, *mode, *age) {
    *age = -1;
    # Check if the file exists 
    if(errorcode(msiObjStat(*filePath,*out)) < 0) {
        logInfo("EUDATgetObjectTimeDiff -> File *filePath does not exist");
    }
    else {
        # Look when the file has been created in iRODS
        msiSplitPath(*filePath, *fileDir, *fileName);   
        foreach ( *ec in SELECT DATA_CREATE_TIME, DATA_MODIFY_TIME WHERE DATA_NAME = '*fileName' AND COLL_NAME = '*fileDir') {
            *creationTime = *ec.DATA_CREATE_TIME;
            logDebug("EUDATgetObjectTimeDiff -> Created at  *creationTime");
            *modifyTime = *ec.DATA_MODIFY_TIME;
            logDebug("EUDATgetObjectTimeDiff -> Modified at *modifyTime");
        }
        if (*mode == "1") {
            *age=int(*modifyTime)-int(*creationTime);
        }
        else if (*mode == "2") {
            msiGetSystemTime(*Now,"unix");
            *age=int(*Now)-int(*modifyTime);
        }
        logDebug("EUDATgetObjectTimeDiff -> Difference in time: *age seconds");
    }
}

#
# Calculate the difference between the current time and the modification time of an object.
# In seconds.
#
# Arguments:
#   *filePath      [IN]   The full iRODS path of the object
#   *age           [OUT]  The age of the object in seconds
#                         *age = -1 if the object does not exist
#
# Author: Claudio Cacciari, CINECA
#
EUDATgetObjectAge(*filePath, *age) {
    *age = -1;
    # Check if the file exists
    if(errorcode(msiObjStat(*filePath,*out)) >= 0) {
        EUDATgetObjectTimeDiff(*filePath, "2", *age);
    }
    else {
        logInfo("EUDATgetObjectAge -> File *filePath does not exist");
    }
    *age;
}

#
# Rules to check if a file is in a given path.
#
# Arguments:
#   *path               [IN]    The full iRODS path of the object
#   *subColl            [IN]    The iRODS path of the collection we are looking in for the object
#   *b                  [REI]   False if no value is found, trou elsewhere
#
# Author: Hao Xu, DICE; Giacomo Mariani, CINECA
#
EUDATfileInPath(*path,*subColl) {
    logInfo("conditional acPostProcForCopy -> EUDATfileInPath");
    msiSplitPath(*path, *coll, *name);
    *b = bool("false");
    foreach ( *c in SELECT count(DATA_NAME) WHERE COLL_NAME like '*subColl' AND DATA_NAME = '*name' ) {
        *num = *c.DATA_NAME;
        if(*num == '1') {
            logInfo("EUDATfileInPath -> found file *name in collection *subColl");
            *b = bool("true");
        }   
    }
    *b;
}

#
# Create AVU with INPUT *Key, *Value for DataObj *Path
#
# Parameters:
#	*Key	[IN]	Key in AVU
#	*Value	[IN]	Value in AVU
#	*Path	[IN]	Path of log_file
# 
# Author: Long Phan, JSC
# Modified: Elena Erastova, RZG, 27.08.2015
# 
EUDATCreateAVU(*Key,*Value,*Path) {
    logDebug("[EUDATCreateAVU] Adding AVU = *Key with *Value to metadata of *Path");
    msiAddKeyVal(*Keyval,*Key, *Value);
    writeKeyValPairs('serverLog', *Keyval, " is : ");
    msiGetObjType(*Path,*objType);
    msiSetKeyValuePairsToObj(*Keyval, *Path, *objType);
}

#-----------------------------------------------------------------------------
# get the single value of a specific metadata in ICAT
#
# Parameters:
# *Path  [IN] target object
# *Key   [IN] name of the MD
# *Value [OUT] value of the MD, None if not set.
#
# Author: Pascal Dugénie, CINES
#-----------------------------------------------------------------------------
EUDATgetLastAVU(*Path, *Key, *Value)
{
    *Value = 'None'
    msiSplitPath(*Path,*parent,*child);
    foreach ( *B in SELECT META_DATA_ATTR_VALUE WHERE META_DATA_ATTR_NAME = '*Key' AND COLL_NAME = '*parent' AND DATA_NAME = '*child') {
        *Value = *B.META_DATA_ATTR_VALUE;
    }
}

#-----------------------------------------------------------------------------
# Change a value in iCAT
#
# Parameters:
# *Path  [IN] target object to assign a new value
# *Key   [IN] target key to assign a new value
# *Value [IN] new value to be assigned
#
# Author: Pascal Dugénie, CINES
# Modified : S Coutin 23/01/2015
# Now it has the same functionality as EUDATCreateAVU : Erastova, 27.08.2015
#
# DEPRECATED
#-----------------------------------------------------------------------------
EUDATModifyAVU(*Path, *Key, *Value)
{
    msiSplitPath( *Path, *parent, *child );
    msiGetObjType( *Path, *objType );
	# Modified begin 
    EUDATcountMetaKeys( *Path, *Key, *key_exist );
    logInfo( "Set *Key into *Value (key_exist=*key_exist)" );
	# Modified end
    if ( *key_exist != "0" ){
        foreach ( *B  in SELECT META_DATA_ATTR_VALUE WHERE META_DATA_ATTR_NAME = '*Key' AND COLL_NAME = '*parent' AND DATA_NAME = '*child') {
            *val = *B.META_DATA_ATTR_VALUE ;
        }
        msiAddKeyVal( *mdkey, *Key, *val );
        msiRemoveKeyValuePairsFromObj( *mdkey, *Path, *objType );
    }
    msiAddKeyVal( *mdkey, *Key, *Value );
    msiAssociateKeyValuePairsToObj( *mdkey, *Path, *objType );
}

#-----------------------------------------------------------------------------
# count metadata in ICAT
#
# Parameters:
# *Path [IN] target object
# *Key  [IN] name of the MD
# *Value [OUT] number of AVUs with name=Key
#
# Author: Pascal Dugénie, CINES
#-----------------------------------------------------------------------------
EUDATcountMetaKeys( *Path, *Key, *Value )
{
    msiSplitPath(*Path, *parent , *child );
    foreach ( *B in SELECT count(META_DATA_ATTR_VALUE) WHERE META_DATA_ATTR_NAME = '*Key' AND COLL_NAME = '*parent' AND DATA_NAME = '*child') {
        *Value = *B.META_DATA_ATTR_VALUE;
    }
}


# Store the metadata PID, CHECKSUM, ROR, CHECKSUM Timestamp in a json file
# inside the special collection .metadata. It stores one file per DO plus
# one file for the collection.
# Checksum and related timestamp are calculated if not provided.
# 
# Parameters:
#       *path     [IN]   Path of the object/collection
#       *pid      [IN]   Persistent Identifier of the object/collection 
#       *ror      [IN]   Repository of Records, the repository of the master copy
#       *checksum [IN]   The checksum of the object
#       *modtime  [IN]   The modification time of the checksum
#
# Author: Claudio Cacciari, CINECA

EUDATStoreJSONMetadata(*path, *pid, *ror, *checksum, *modtime) {

    getMetaParameters(*metaConfPath,*enabled);
    if (*enabled) {
        *extraMetaData = "";
        if (*checksum == "" || *checksum == 'None') {
            EUDATiCHECKSUMget(*path, *checksum, *modtime);
        }
        if (*checksum != "") {
            *extraMetaData = "-c *checksum -t *modtime";
        }
        if (*ror == "" || *ror == 'None') {
            EUDATGeteRorPid(*pid, *ror);
        }
        if (*ror != "") {
            *extraMetaData = *extraMetaData ++ " -r *ror";
        }
        msiExecCmd("metadataManager.py","*metaConfPath $userNameClient store '*path'"
                ++ " -i *pid *extraMetaData", "null", "null", "null", *outMeta);
        msiGetStdoutInExecCmdOut(*outMeta, *resp);
        getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
        if (*msiFreeEnabled) {
            msifree_microservice_out(*outMeta);
        }
    }
}


################################################################################
#                                                                              #
# Repository Packages                                                          #
#                                                                              #
################################################################################

#-----------------------------------------------------------------------------
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

#-----------------------------------------------------------------------------
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
    EUDATiCHECKSUMget(*source, *checksum, *modtime);
    EUDATModifyAVU(*source, "INFO_Checksum" , *checksum );
# Modified begin 
    EUDATgetLastAVU(*source, "OTHER_original_checksum", *orig_checksum);
# Modified end
    if ( *checksum == *orig_checksum )
    {
        logInfo("ingestObject-> Checksum is same as original = *checksum");
        EUDATModifyAVU(*source, "ADMIN_Status" , "Checksum_ok" ) ;
        # Extract the ROR value from iCat
# Modified begin 
# TODO: clarify how the 'EUDAT/ROR' should be added as iCAT metadata pair
#       current version assumes the ROR is available in the EUDAT/ROR AVU, as this is done by repository package
#       *RorValue = ""
	EUDATgetLastAVU( *source, "EUDAT/ROR" , *RorValue );
# Modified end 
        EUDATCreatePID("None", *source, *RorValue, "true", *PID);
        # test PID creation
        if((*PID == "empty") || (*PID == "None") || (*PID == "error")) {
            logInfo("ingestObject-> ERROR while creating the PID for *source PID = *PID");
            EUDATModifyAVU(*source, "ADMIN_Status" , "ErrorPID" ) ;
        }
        else {
            logInfo("ingestObject-> PID created for *source PID = [*PID] ROR = [*RorValue]");
            EUDATModifyAVU(*source, "ADMIN_Status" , "Archive_ok" ) ;
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
        EUDATModifyAVU(*source, "ADMIN_Status" , "ErrorChecksum" ) ;
    }
}

#-----------------------------------------------------------------------------
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
   EUDATModifyAVU(*source, "ADMIN_Status" , "TransferStarted" ) ;
   msiGetSystemTime( *TimeNow, "human" );
   EUDATModifyAVU(*source, "INFO_TimeOfStart", *TimeNow ) ;
}

#-----------------------------------------------------------------------------
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
   EUDATModifyAVU(*source, "ADMIN_Status" , "TransferFinished" ) ;
   msiGetSystemTime( *TimeNow, "human" );
   EUDATModifyAVU(*source, "INFO_TimeOfTransfer" , *TimeNow ) ;
}
