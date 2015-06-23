################################################################################
#                                                                              #
# EUDAT Safe-Replication and PID management policies                           #
#                                                                              #
################################################################################

# List of the functions:
#
#---- authorization ---
# EUDATAuthZ(*user, *action, *target, *response)
#---- utility ---
# EUDATLog(*message, *level)
# EUDATQueue(*action, *message, *number)

#TODO:delete getSharedCollection(*zonePath, *collectionPath)

#TODO:delete?  writeFile(*file, *contents)
#TODO:delete?  readFile(*file, *contents)
#TODO:delete updateCommandName(*cmdPath, *status)
# logInfo(*msg)
# logDebug(*msg)
# logError(*msg)
# logWithLevel(*level, *msg)
# EUDATReplaceSlash(*path, *out)
# EUDATGetZoneNameFromPath(*path, *out)
# EUDATGetZoneHostFromZoneName(*zoneName, *conn)
# EUDATiCHECKSUMdate(*coll, *name, *resc, *modTime)
# EUDATiCHECKSUMretrieve(*path, *checksum)
# EUDATiCHECKSUMget(*path, *checksum)
# EUDATgetObjectTimeDiff(*filePath, *mode, *age)
# EUDATgetObjectAge(*filePath, *age) 
# EUDATfileInPath(*path,*subColl)
# EUDATCreateAVU(*Key,*Value,*Path)
# EUDATgetLastAVU(*Path, *Key, *Value)
# EUDATModifyAVU(*Path, *Key, *Value)
# EUDATcountMetaKeys( *Path, *Key, *Value )
# getCollectionName(*path_of_collection,*Collection_Name)
#---- command file triggers ---
#TODO:delete triggerReplication(*commandFile,*pid,*source,*destination)
#TODO:delete triggerCreatePID(*commandFile,*pid,*destination,*ror)
#TODO:delete triggerUpdateParentPID(*commandFile,*pid,*new_pid)
#---- process command file ---
#TODO:delete processReplicationCommandFile(*cmdPath)
#TODO:delete readReplicationCommandFile(*cmdPath,*pid,*source,*destination,*ror)
#TODO:delete processPIDCommandFile(*cmdPath)
#TODO:delete doReplication(*pid, *source, *destination, *ror, *status)
#TODO:delete updateMonitor(*file)
#---- data staging ---
# EUDATiDSSfileWrite(*DSSfile) # DEPRECATED
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
               "null", "null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *response);
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

#
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
               "null", "null", "null", *out);
}

#
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
               "null", "null", "null", *out);
    if (*action == 'pop' || *action == 'queuesize') {
        msiGetStdoutInExecCmdOut(*out, *message);
    }
    if (*action == 'pop' && int(*number) > 1) {
        *message = triml(*message, "[");
        *message = trimr(*message, "]");
    }
}

#
# Return the absolute path to the iRODS collection where all command files are stored.
#   typically "<zone>/replicate". Make sure all users and remote users have write permissions here.
#
# Parameters:
#   *zonePath           [IN]    a iRODS path name including the zone
#   *collectionPath     [OUT]   the iRODS absolute path to the collection used to store command files
#
# Author: Willem Elbers, MPI-TLA
#
#getSharedCollection(*zonePath, *collectionPath) {
    #msiGetZoneNameFromPath(*zonePath, *zoneName);
#    EUDATGetZoneNameFromPath(*zonePath, *zoneName)
#    *collectionPath = "/*zoneName/replicate/";
#}

#
# Write a command file
#
# Parameters:
#   *file       [IN]    iRODS location of the file to write
#   *contents   [IN]    the command contents
#
# Author: Willem Elbers, MPI-TLA
#
#writeFile(*file, *contents) {
#    *err = errorcode(msiObjStat(*file, *objStat));
#    if (*err >= 0) {
#        msiDataObjUnlink("objPath=*file++++replNum=0++++forceFlag=", *status);
#    }
#    msiDataObjCreate("*file", "forceFlag=", *filePointer);
#    logDebug("[writeFile] Created object: *file");
#    msiDataObjWrite(*filePointer, "*contents", *bytesWritten);
#    msiDataObjClose(*filePointer, *outStatus);
#}

#
# Read a command file
#
# Parameters:
#   *file       [IN]    iRODS location of the file to read
#   *contents   [OUT]   the command contents
#
# Author: Willem Elbers, MPI-TLA
#
#readFile(*file, *contents) {
#    msiDataObjOpen("objPath=*file++++replNum=0++++openFlags=O_RDONLY",*S_FD);
#    msiDataObjRead(*S_FD,"1024",*R_BUF);
#    #msiDataObjRead(*S_FD,null,*R_BUF);
#    msiBytesBufToStr(*R_BUF, *contents);
#    msiDataObjClose(*S_FD,*closeStatus);
#}

#
# Rename a command file.
# Appends the current timestamp and a ".success" or ."failed" identifier 
#
# Parameters:
#   *cmdPath    [IN]    the command file to rename
#   *status     [OUT]   status, 0 = ok, <0 = error
#
# Author: Willem Elbers, MPI-TLA
#
#updateCommandName(*cmdPath, *status) {
#    msiGetFormattedSystemTime(*ftime,"human","%d%02d%02dT%02d%02d%02d");
#    if(*status == 0) {
#        msiDataObjRename(*cmdPath,"*cmdPath.*ftime.success","0",*renameStatus);
#    } else {
#        msiDataObjRename(*cmdPath,"*cmdPath.*ftime.failed","0",*renameStatus);
#    }
#}

#
# Logging policies
#

logInfo(*msg) {
    logWithLevel("info", *msg);
}

logDebug(*msg) {
    logWithLevel("debug", *msg);
# replace "debug" with "info" to print even without
# changing the log level of iRODS
#   logWithLevel("info", *msg);
}

logError(*msg) {
    logWithLevel("error", *msg);
}

#logWithLevel(*level, *msg) {
#    msiWriteToLog(*level,"*msg");
#}

logWithLevel(*level, *msg) {
    on (*level == "info") { writeLine("serverLog","INFO: *msg");}
    on (*level == "debug") { writeLine("serverLog","DEBUG: *msg");}
    on (*level == "error") { writeLine("serverLog","ERROR: *msg");}
}

#
# Function: replace microservice msiReplaceSlash (eudat.c)
#
# Author: Long Phan, JSC
#
EUDATReplaceSlash(*path, *out) {
 
    *list = split("*path","/");
    *n = "";
    foreach (*t in *list) {
        *n = *n ++ *t ++ "_";
    }
    msiStrchop(*n,*n_chop);
    *out = *n_chop;
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
#
#
EUDATGetZoneHostFromZoneName(*zoneName, *conn) {

    *conn = ""
    *res = SELECT ZONE_CONNECTION WHERE ZONE_NAME = '*zoneName';
    foreach(*row in *res) {
        msiGetValByKey(*row, "ZONE_CONNECTION", *conn);
    }
    # the local zone does not store the connection details
    # then get them from the eudat.local rule set
    if (*conn == "") {
        *result = SELECT ZONE_TYPE WHERE ZONE_NAME = '*zoneName';
        foreach(*line in *result) {
            msiGetValByKey(*line, "ZONE_TYPE", *type);
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
    
    msiMakeGenQuery("count(META_DATA_ATTR_VALUE)", "COLL_NAME = '*coll' AND DATA_NAME = '*name' AND META_DATA_ATTR_NAME = '*metaName'", *GenQIn);
    msiExecGenQuery(*GenQIn, *GenQOut);
    
    foreach(*row in *GenQOut) {
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
#   *status             [REI]   false if no value is found, true elsewhere
#
# Author: Giacomo Mariani, CINECA, Michal Jankowski PSNC
#
EUDATiCHECKSUMretrieve(*path, *checksum) {
    *status = bool("false");
    *checksum = "";
    logInfo("EUDATiCHECKSUMretrieve -> Looking at *path");
    msiSplitPath(*path, *coll, *name);
    *d = SELECT DATA_CHECKSUM, DATA_RESC_NAME, DATA_MODIFY_TIME WHERE DATA_NAME = '*name' AND COLL_NAME = '*coll';
    #Loop over all resources, possibly the checksum was not computed for all of them
    foreach(*c in *d) {
        msiGetValByKey(*c, "DATA_CHECKSUM", *checksumTmp);
        msiGetValByKey(*c, "DATA_RESC_NAME", *resc);      
        msiGetValByKey(*c, "DATA_MODIFY_TIME", *modtime);

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
    *status;#
}

#
# The function obtain iCHECKSUM for a given object creating it if necessary.
#
# Environment variable used:
#
# Arguments:
#   *path               [IN]    the iRODS path of the object involved in the query
#   *checksum           [OUT]   iCHECKSUM
#
# Author: Giacomo Mariani, CINECA, Michal Jankowski PSNC
#
EUDATiCHECKSUMget(*path, *checksum) {
    if (!EUDATiCHECKSUMretrieve(*path, *checksum)) {
        *checksum = "";
        #If it is a collection, do not calculate the checksum
        msiGetObjType(*path,*type);
        if (*type == '-d')  {
            #NOTE: the 2. arg of msiDataObjChksum: "null" means only the default resc will be checksumed.
            #Consider "ChksumAll="
            msiDataObjChksum(*path, "null", *checksum);
        }
        #call again EUDATiCHECKSUMretrieve in order to set checksum date
        EUDATiCHECKSUMretrieve(*path, *checksum);
    }
}

#
# Calculate the difference between the creation time or the current time
# and the modification time of an object. In seconds.
#
# Arguments:
#   *filePath      [IN]   The full iRODS path of the object
#   *mode          [IN]   The way to calculate the time difference [1,2]
#                         mode 1: modification time - creation time
#                         mode 2: now - modification time
#   *age           [OUT]  The age of the object in seconds
#
# Author: Giacomo Mariani, CINECA
#
EUDATgetObjectTimeDiff(*filePath, *mode, *age) {
    # Look when the file has been created in iRODS
    msiSplitPath(*filePath, *fileDir, *fileName);   
    *ec = SELECT DATA_CREATE_TIME, DATA_MODIFY_TIME WHERE DATA_NAME = '*fileName' AND COLL_NAME = '*fileDir';
    foreach(*ec) {
        msiGetValByKey(*ec, "DATA_CREATE_TIME", *creationTime);
        logDebug("EUDATgetObjectTimeDiff -> Created at  *creationTime");
        msiGetValByKey(*ec, "DATA_MODIFY_TIME", *modifyTime);
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

#
# Calculate the difference between the current time and the modification time of an object.
# In seconds.
#
# Arguments:
#   *filePath      [IN]   The full iRODS path of the object
#   *age           [OUT]  The age of the object in seconds
#
# Author: Claudio Cacciari, CINECA
#
EUDATgetObjectAge(*filePath, *age) {
    EUDATgetObjectTimeDiff(*filePath, "2", *age);
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
    *d = SELECT count(DATA_NAME) WHERE COLL_NAME like '*subColl' AND DATA_NAME = '*name';
    foreach(*c in *d) {
        msiGetValByKey(*c,"DATA_NAME",*num);
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
# 
EUDATCreateAVU(*Key,*Value,*Path) {
    logDebug("[EUDATCreateAVU] Adding AVU = *Key with *Value to metadata of *Path");
    msiAddKeyVal(*Keyval,*Key, *Value);
    writeKeyValPairs('serverLog', *Keyval, " is : ");
    msiGetObjType(*Path,*objType);
    msiAssociateKeyValuePairsToObj(*Keyval, *Path, *objType);
}

#-----------------------------------------------------------------------------
# get the single value of a specific metadata in ICAT
#
# Parameters:
# *Path  [IN] target object
# *Key   [IN] name of the MD
# *Value [OUT] value of the MD
#
# Author: Pascal Dugénie, CINES
#-----------------------------------------------------------------------------
EUDATgetLastAVU(*Path, *Key, *Value)
{
    msiSplitPath(*Path,*parent,*child);
    msiExecStrCondQuery( "SELECT META_DATA_ATTR_VALUE WHERE META_DATA_ATTR_NAME = '*Key' AND COLL_NAME = '*parent' AND DATA_NAME = '*child'" , *B );
    foreach ( *B ) {
        msiGetValByKey( *B , "META_DATA_ATTR_VALUE" , *Value );
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
        msiExecStrCondQuery( "SELECT META_DATA_ATTR_VALUE WHERE META_DATA_ATTR_NAME = '*Key' AND COLL_NAME = '*parent' AND DATA_NAME = '*child'", *B );
        foreach ( *B ) {
            msiGetValByKey( *B, "META_DATA_ATTR_VALUE", *val ) ;
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
    msiExecStrCondQuery( "SELECT count(META_DATA_ATTR_VALUE) WHERE META_DATA_ATTR_NAME = '*Key' AND COLL_NAME = '*parent' AND DATA_NAME = '*child'" , *B );
    foreach ( *B ) {
        msiGetValByKey( *B , "META_DATA_ATTR_VALUE" , *Value );
    }
}

#
# get Name of Collection from Path
#
# Parameters:
#	*path_of_collection		[IN] 	path of collection in iRODS
#	*Collection_Name 		[OUT]	return Name of Collection 
#
# Author: Long Phan, JSC
#
getCollectionName(*path_of_collection,*Collection_Name){
    *list = split("*path_of_collection","/");
    *s = size(*list) - 1;
    *n = elem(*list,*s);
    *Collection_Name = "*n";
}

################################################################################
#                                                                              #
# Command file triggers                                                        #
#                                                                              #
################################################################################

#
# Start a replication by writing a .replicate command file
#
# Parameters:
#   *commandFile    [IN]    the absolute filename to store the command in
#   *pid            [IN]    pid of the digital object
#   *source         [IN]    source path of the object to replicate
#   *destination    [IN]    destination path of the object to replicate
#
# Author: Willem Elbers, MPI-TLA
#
#triggerReplication(*commandFile,*pid,*source,*destination) {
#    logInfo("startReplication(*commandFile,*pid,*source,*destination)");
#    EUDATGetRorPid(*pid, *ror);
#    if (*ror == "None"){
#        getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
#        *ror = "*epicApi"++"*pid";  
#        logDebug("No ROR available, so new ROR defined: *ror");
#    }
#    writeFile("*commandFile","*pid;*source;*destination;*ror");
#    doReplication(*pid,*source,*destination,*ror,*status);
#}

#
# Start a PID creation by writing a .pid.create command file
#
# Parameters:
#   *commandFile    [IN]    the absolute filename to store the command in
#   *pid            [IN]    PID of the digital object
#   *destination    [IN]    destination path of the object to replicate
#   *ror            [IN]    ROR of the original digital object
#
# Author: Willem Elbers, MPI-TLA
#
#triggerCreatePID(*commandFile,*pid,*destination,*ror) {
#    logInfo("triggerCreatePID(*commandFile,*pid,*destination,*ror)");
#    writeFile("*commandFile", "create;*pid;*destination;*ror");
#    EUDATGetZoneNameFromPath(*destination, *zoneName);
#    EUDATGetZoneHostFromZoneName(*zoneName, *zoneConn);
#    logInfo("Remote zone name: *zoneName, connection contact: *zoneConn");
#    remote("*zoneConn", logInfo("Starting remote execution"))
#    {
#         writeLine("serverLog","INFO: inside remote execution");        
#    }
#    EUDATCreatePID(*parent, *destination, *ror, bool("true"), *new_pid);
#    getSharedCollection(*destination,*collectionPath);
    #create .pid.update file based on absolute file path
#    EUDATReplaceSlash(*destination, *filepathslash);
#    triggerUpdateParentPID("*collectionPath*filepathslash.pid.update", *parent, *new_pid);
#}

#
# Start a PID update. 
# The PID is that of the parent of the current replicated object.
#
# Author: Willem Elbers, MPI-TLA
#
# Parameters:
#   *commandFile    [IN]    the absolute filename to store the command in
#   *pid            [IN]    PID of the digital object
#   *new_pid        [IN]    place of the replicated digital object.
#
#triggerUpdateParentPID(*commandFile,*pid,*new_pid) {
#    logInfo("triggerUpdateParentPID(*commandFile,*pid,*new_pid)");
#    writeFile("*commandFile", "update;*pid;*new_pid");
#}

################################################################################
#                                                                              #
# Process command files                                                        #
#                                                                              #
################################################################################

#
# Process a .replicate file and perform the replication
# format = "command1,command2,command2,..."
#
# command format = "source_pid;source_path;destination_path"
#
# Parameters:
#   *cmdPath    [IN]    the path to the .replicate file
#
# Author: Willem Elbers, MPI-TLA
#
#processReplicationCommandFile(*cmdPath) {
#    logInfo("processReplication(*cmdPath)");
#
#    readFile(*cmdPath, *out_STRING);    
#
#    #TODO: properly manage status here
#    *status = 0;    
#    *out_ARRAY = split(*out_STRING, "\n");
#    foreach(*out_STRING1 in *out_ARRAY) {
#        *list = split(*out_STRING1, ";");
#        # assign values from array to parameters
#        *ror = "None";
#        *counter=0;
#        foreach (*item_LIST in *list) {
#            if      ( *counter == 0 ) { *pid         = *item_LIST ; }
#            else if ( *counter == 1 ) { *source      = *item_LIST ; }
#            else if ( *counter == 2 ) { *destination = *item_LIST ; }
#            else if ( *counter == 3 ) { *ror         = *item_LIST ; }
#            *counter = *counter + 1;    
#        }
#        *list_size = *counter ;
#
#        if ((*list_size==4) || (*list_size==3)){
#            doReplication(*pid,*source,*destination,*ror,*status);
#        }
#       else {
#            logError("ignoring incorrect command: [*out_STRING]");
#            *status = -1;
#        }
#    }
#    updateCommandName(*cmdPath,*status);
#}

#
# Read a .replicate file
#
# command format = "source_pid;source_path;destination_path"
#
# Parameters:
#   *cmdPath     [IN]   the path to the .replicate file
#   *pid         [OUT]  source pid
#   *source      [OUT]  source path
#   *destination [OUT]  destination path
#   *ror         [OUT]  ror
#
# Author: Willem Elbers, MPI-TLA
# Edited: Elena Erastova, RZG
#
#readReplicationCommandFile(*cmdPath,*pid,*source,*destination,*ror) {
#    readFile(*cmdPath, *out_STRING);
#    *out_ARRAY = split(*out_STRING, "\n");
#    foreach(*out_STRING1 in *out_ARRAY) {
#        *list = split(*out_STRING1, ";");
#        # assign values from array to parameters
#        *ror = "None";
#        *counter=0;
#        foreach (*item_LIST in *list) {
#            if      ( *counter == 0 ) { *pid         = *item_LIST ; }
#            else if ( *counter == 1 ) { *source      = *item_LIST ; }
#            else if ( *counter == 2 ) { *destination = *item_LIST ; }
#            else if ( *counter == 3 ) { *ror         = *item_LIST ; }
#            *counter = *counter + 1;
#        }
#    }
#}

#
# Process a .pid file and perform the appropriate action
#   supported actions: create, update
#
# Parameters:
#   *cmdPath    [IN]    the iRODS path to the pid command file
#
# Author: Willem Elbers, MPI-TLA
# Edited: Elena Erastova, RZG
#
#processPIDCommandFile(*cmdPath) {
#    logInfo("processPID(*cmdPath)");
#    readFile(*cmdPath, *out_STRING);
#    *list = split(*out_STRING, ";");

    # assign values from array to parameters
#    *ror = "None";
#    *parent = "None";
#    *counter=0;
#    foreach (*item_LIST in *list) {
#        if      ( *counter == 0 ) { *pidAction   = *item_LIST ; }
#        else if ( *counter == 1 ) { *parent      = *item_LIST ; }
#        else if ( *counter == 2 ) { *destination = *item_LIST ; }
#        else if ( *counter == 3 ) { *ror         = *item_LIST ; }
#        *counter = *counter + 1;    
#    }
#    *list_size = *counter ;

    # process command/action
#    if ((*list_size==4) || (*list_size==3)){
#        if(*pidAction == "create") {
#            #manage pid in this repository
#            EUDATCreatePID(*parent, *destination, *ror, bool("true"), *new_pid);
#            getSharedCollection(*destination,*collectionPath);
#            #create .pid.update file based on absolute file path
#            #msiReplaceSlash(*destination,*filepathslash);
#	    EUDATReplaceSlash(*destination, *filepathslash);
#            triggerUpdateParentPID("*collectionPath*filepathslash.pid.update", *parent, *new_pid);
#        } 
#        else if(*pidAction=="update") {
#            *status = 0;
#            EUDATUpdatePIDWithNewChild(*parent, *destination);
#            updateCommandName(*cmdPath,*status);
#        }
#        else {
#            logError("ignoring incorrect command: [*out_STRING]");
#        }
#    }
#    else {
#        logError("ignoring incorrect list");
#    }
#}

#
# Start a replication
#
# Parameters:
#   *pid            [IN]    pid of the digital object
#   *source         [IN]    source path of the object to replicate
#   *destination    [IN]    destination path of the object to replicate
#   *ror            [IN]    ROR of the digital object
#   *status         [OUT]   status, 0 = ok, <0 = error
#
# Author: Willem Elbers, MPI-TLA
#
#doReplication(*pid, *source, *destination, *ror, *status) {
#   logInfo("doReplication(*pid, *source, *destination, *ror)");

    #make sure the parent collections exist
#    msiSplitPath(*destination, *parent, *child);
#    msiCollCreate(*parent, "1", *collCreateStatus);

    #rsync object (make sure to supply "null" if dest resource should be the default one) 
#    msiDataObjRsync(*source, "IRODS_TO_IRODS", "null", *destination, *rsyncStatus);

#    if(*pid != "null") {
        #trigger pid management in destination
#        getSharedCollection(*destination,*collectionPath);
        # create .pid.create file and monitor for .pid.update based on absolute file path
        #msiReplaceSlash(*destination,*filepathslash);
#        EUDATReplaceSlash(*destination, *filepathslash);
#        triggerCreatePID("*collectionPath*filepathslash.pid.create", *pid, *destination, *ror);
#        updateMonitor("*collectionPath*filepathslash.pid.update");
#    }
#    else {
#        logDebug("No pid management");
#    }
#
#}
#
##
## Monitor the specified pid command file
#
# Parameters:
#   *file   [IN]    start a monitor on the specified iRODS file
#
# Author: Willem Elbers, MPI-TLA
#
#updateMonitor(*file) {
#    logInfo("updateMonitor(*file)");
#    delay("<PLUSET>1m</PLUSET><EF>10m REPEAT UNTIL SUCCESS OR 12 TIMES</EF>") {
#        if(errorcode(msiObjStat(*file,*out)) >= 0) {
#            logInfo("*file exists");
#            processPIDCommandFile(*file);
#        } else {
#            logInfo("*file does not exist yet");
            # save *source of failed_transfered data object into fail_log 
#            EUDATProcessErrorUpdatePID(*file);
#        }
#    }
#}

################################################################################
#                                                                              #
# Data Staging                                                                 #
#                                                                              #
################################################################################

#
# Writes the file used to store the list of PIDs and URLs
# This is a list of key-value pairs used by data staging service via gridFTP.
# The tuples are PID-object path.
#
# Arguments:
#   *path          [IN]    The path of the file to write in.
#
# Author: Giacomo Mariani, CINECA
#
EUDATiDSSfileWrite(*DSSfile) {
    logDebug("Test PID -> acPostProcForCopy checks for *DSSfile");
    msiSplitPath(*DSSfile, *coll, *name);
    *b = bool("false");
    *d = SELECT count(DATA_NAME) WHERE COLL_NAME like '*coll' AND DATA_NAME = '*name';
    foreach(*c in *d) {
        msiGetValByKey(*c,"DATA_NAME",*num);
        if(*num == '1') {
            *b = bool("true");
        }  
    }
    if (!*b)
    {
        logDebug("Test PID -> acPostProcForCopy creates *DSSfile");
        msiDataObjCreate(*DSSfile,*OFlagsB,*DSSf);
        msiDataObjClose(*DSSf,*Status);
    }
    EUDATgetObjectAge(*DSSfile, *age);
    *minTime = int("86400");        # In seconds
    if ( *age >= *minTime ) then
    {
        logInfo("Test PID -> acPostProcForCopy *DSSfile is old. Removing it.");
        msiDataObjUnlink(*DSSfile,*Status);
        msiDataObjCreate(*DSSfile,*OFlagsB,*DSSf);
        msiDataObjClose(*DSSf,*Status);
    }
    msiDataObjOpen(*DSSfile++"++++openFlags=O_RDWR",*DSSf);
    logDebug("Test PID -> acPostProcForCopy Open OK.");
    msiDataObjLseek(*DSSf,"null","SEEK_END",*Status);
    logDebug("Test PID -> acPostProcForCopy Seek OK.");
    EUDATiPIDretrieve($objPath, *PID)
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug)
    *Buf="*serverID"++"$objPath,*PID\n";
    msiDataObjWrite(*DSSf,*Buf,*Len);
    logDebug("Test PID -> acPostProcForCopy Write OK.");
    msiDataObjClose(*DSSf,*Status);
    logDebug("Test PID -> acPostProcForCopy Close OK.");
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
    EUDATiCHECKSUMget(*source, *checksum);
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
        EUDATCreatePID("None", *source, *RorValue, bool("true"), *PID);
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
