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
# getSharedCollection(*zonePath, *collectionPath)
# writeFile(*file, *contents)
# readFile(*file, *contents)
# updateCommandName(*cmdPath, *status)
# logInfo(*msg)
# logDebug(*msg)
# logError(*msg)
# logWithLevel(*level, *msg)
# EUDATiCHECKSUMretrieve(*path, *checksum)
# EUDATiCHECKSUMget(*path, *checksum)
# EUDATgetObjectTimeDiff(*filePath, *age)
# EUDATfileInPath(*path,*subColl)
# EUDATCreateAVU(*Key,*Value,*Path)
# getCollectionName(*path_of_collection,*Collection_Name)
#---- command file triggers ---
# triggerReplication(*commandFile,*pid,*source,*destination)
# triggerCreatePID(*commandFile,*pid,*destination,*ror)
# triggerUpdateParentPID(*commandFile,*pid,*new_pid)
#---- process command file ---
# processReplicationCommandFile(*cmdPath)
# readReplicationCommandFile(*cmdPath,*pid,*source,*destination,*ror)
# processPIDCommandFile(*cmdPath)
# doReplication(*pid, *source, *destination, *ror, *status)
# updateMonitor(*file)

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
    msiExecCmd("authZ.manager.py", "*authZMapPath check *user '*action' '*target'",
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
#It manages the writing and reading of log messages to/from external log services.
#
#Return
# no response is expected
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
    msiExecCmd("log.manager.py", "*logConfPath log *level *message",
               "null", "null", "null", *out);
}

#
#It implements a FIFO queue for messages to/from external log services.
#
#Return
# no response is expected for action "push"
# The first message of the queue for action "pop"
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
    if (*action == 'pop' && *number > 1) {
        *options = "-n "++str(*number);
    }
    logInfo("logging action '*action' for message '*message'");
    msiExecCmd("log.manager.py", "*logConfPath *action *options *message",
               "null", "null", "null", *out);
    if (*action == 'pop' || *action == 'queuesize') {
        msiGetStdoutInExecCmdOut(*out, *message);
    }
    if (*action == 'pop' && *number > 1) {
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
getSharedCollection(*zonePath, *collectionPath) {
    msiGetZoneNameFromPath(*zonePath, *zoneName);
    *collectionPath = "*zoneName/replicate/";
}

#
# Write a command file
#
# Parameters:
#   *file       [IN]    iRODS location of the file to write
#   *contents   [IN]    the command contents
#
# Author: Willem Elbers, MPI-TLA
#
writeFile(*file, *contents) {
    msiDataObjCreate("*file", "forceFlag=", *filePointer);
    msiDataObjWrite(*filePointer, "*contents", *bytesWritten);
    msiDataObjClose(*filePointer, *outStatus);
}

#
# Read a command file
#
# Parameters:
#   *file       [IN]    iRODS location of the file to read
#   *contents   [OUT]   the command contents
#
# Author: Willem Elbers, MPI-TLA
#
readFile(*file, *contents) {
    msiDataObjOpen("objPath=*file++++replNum=0++++openFlags=O_RDONLY",*S_FD);
    msiDataObjRead(*S_FD,"1024",*R_BUF);
    #msiDataObjRead(*S_FD,null,*R_BUF);
    msiBytesBufToStr(*R_BUF, *contents);
    msiDataObjClose(*S_FD,*closeStatus);
}

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
updateCommandName(*cmdPath, *status) {
    msiGetFormattedSystemTime(*ftime,"human","%d%02d%02dT%02d%02d%02d");
    if(*status == 0) {
        msiDataObjRename(*cmdPath,"*cmdPath.*ftime.success","0",*renameStatus);
    } else {
        msiDataObjRename(*cmdPath,"*cmdPath.*ftime.failed","0",*renameStatus);
    }
}

#
# Logging policies
#

logInfo(*msg) {
    logWithLevel("info", *msg);
}

logDebug(*msg) {
#    logWithLevel("debug", *msg);
# replaced "debug" with "info" to print even without
# changing the log level of iRODS
     logWithLevel("info", *msg);
}

logError(*msg) {
    logWithLevel("error", *msg);
}

logWithLevel(*level, *msg) {
    msiWriteToLog(*level,"*msg");
}

#
# The function retrieve iCHECKSUM for a given object.
#
# Environment variable used:
#
# Arguments:
#   *path               [IN]    the iRODS path of the object involved in the query
#   *checksum           [OUT]   iCHECKSUM
#   *status             [REI]   false if no value is found, trou elsewhere
#
# Author: Giacomo Mariani, CINECA
#
EUDATiCHECKSUMretrieve(*path, *checksum) {
    *status = bool("false");
    logInfo("EUDATiCHECKSUMretrieve -> Looking at *path");
    msiSplitPath(*path, *coll, *name);
    *d = SELECT DATA_CHECKSUM WHERE DATA_NAME = '*name' AND COLL_NAME = '*coll'; 
    foreach(*c in *d) {
        msiGetValByKey(*c, "DATA_CHECKSUM", *checksum);
        if (*checksum==""){
            logInfo("EUDATiCHECKSUMretrieve -> The iCHECKSUM is empty");
        }else{
            logInfo("EUDATiCHECKSUMretrieve -> Found iCHECKSUM = *checksum");
            *status = bool("true");
        }
    }
    *status;
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
# Author: Giacomo Mariani, CINECA
#
EUDATiCHECKSUMget(*path, *checksum) {
    if (!EUDATiCHECKSUMretrieve(*path, *checksum)) {
        msiDataObjChksum(*path, "null", *checksum);
    }
}

#
# Calculate the difference between the creation time and the modification time of an object.
# In seconds.
#
# Arguments:
#   *filePath           [IN]   The full iRODS path of the object
#   *age                [OUT]  The age of the object in seconds
#
# Author: Giacomo Mariani, CINECA
#
EUDATgetObjectTimeDiff(*filePath, *age) {
    # Look when the file has been created in iRODS
    msiSplitPath(*filePath, *fileDir, *fileName);   
    *ec = SELECT DATA_CREATE_TIME, DATA_MODIFY_TIME WHERE DATA_NAME = '*fileName' AND COLL_NAME = '*fileDir';
    foreach(*ec) {
        msiGetValByKey(*ec, "DATA_CREATE_TIME", *creationTime);
        logInfo("EUDATgetObjectTimeDiff -> Created at  *creationTime");
        msiGetValByKey(*ec, "DATA_MODIFY_TIME", *modifyTime);
        logInfo("EUDATgetObjectTimeDiff -> Modified at *modifyTime");
    }
    *age=int(*modifyTime)-int(*creationTime);
    logInfo("EUDATgetObjectTimeDiff -> Difference in time: *age seconds");
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
# Author: Long Phan, Juelich
# 
EUDATCreateAVU(*Key,*Value,*Path) {
    logDebug("[EUDATCreateAVU] Adding AVU = *Key with *Value to metadata of *Path");
    msiAddKeyVal(*Keyval,*Key, *Value);
    writeKeyValPairs('serverLog', *Keyval, " is : ");
    msiGetObjType(*Path,*objType);
    msiAssociateKeyValuePairsToObj(*Keyval, *Path, *objType);
}

#
# get Name of Collection from Path
#
# Parameters:
#	*path_of_collection		[IN] 	path of collection in iRODS
#	*Collection_Name 		[OUT]	return Name of Collection 
#
# Author: Long Phan, Juelich
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
triggerReplication(*commandFile,*pid,*source,*destination) {
    logInfo("startReplication(*commandFile,*pid,*source,*destination)");
    EUDATGetRorPid(*pid, *ror);
    if (*ror == "None"){
        getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
        *ror = "*epicApi"++"*pid";  
    }
    writeFile("*commandFile","*pid;*source;*destination;*ror");
}

#
# Start a PID created by writing a .pid.create command file
#
# Parameters:
#   *commandFile    [IN]    the absolute filename to store the command in
#   *pid            [IN]    PID of the digital object
#   *destination    [IN]    destination path of the object to replicate
#   *ror            [IN]    ROR of the original digital object
#
# Author: Willem Elbers, MPI-TLA
#
triggerCreatePID(*commandFile,*pid,*destination,*ror) {
    logInfo("triggerCreatePID(*commandFile,*pid,*destination,*ror)");
    writeFile("*commandFile", "create;*pid;*destination;*ror");
}

#
# Author: Willem Elbers, MPI-TLA
#
# Parameters:
#   *commandFile    [IN]    the absolute filename to store the command in
#   *pid            [IN]    PID of the digital object
#   *new_pid        [IN]    place of the replicated digital object.
#
triggerUpdateParentPID(*commandFile,*pid,*new_pid) {
    logInfo("triggerUpdateParentPID(*commandFile,*pid,*new_pid)");
    writeFile("*commandFile", "update;*pid;*new_pid");
}

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
processReplicationCommandFile(*cmdPath) {
    logInfo("processReplication(*cmdPath)");

    readFile(*cmdPath, *out_STRING);    

    #TODO: properly manage status here
    *status = 0;    
    *out_ARRAY = split(*out_STRING, "\n");
    foreach(*out_STRING1 in *out_ARRAY) {
        *list = split(*out_STRING1, ";");
        # assign values from array to parameters
        *ror = "None";
        *counter=0;
        foreach (*item_LIST in *list) {
            if      ( *counter == 0 ) { *pid         = *item_LIST ; }
            else if ( *counter == 1 ) { *source      = *item_LIST ; }
            else if ( *counter == 2 ) { *destination = *item_LIST ; }
            else if ( *counter == 3 ) { *ror         = *item_LIST ; }
            *counter = *counter + 1;    
        }
        *list_size = *counter ;

        if ((*list_size==4) || (*list_size==3)){
            doReplication(*pid,*source,*destination,*ror,*status);
        }
        else {
            logError("ignoring incorrect command: [*out_STRING]");
            *status = -1;
        }
    }
    updateCommandName(*cmdPath,*status);
}

#
# Read a .replicate file and perform the replication
# format = "command1,command2,command2,..."
#
# command format = "source_pid;source_path;destination_path"
#
# Parameters:
#   *cmdPath    [IN]    the path to the .replicate file
#
# Author: Willem Elbers, MPI-TLA
# Edited: Elena Erastova, RZG
#
readReplicationCommandFile(*cmdPath,*pid,*source,*destination,*ror) {
    readFile(*cmdPath, *out_STRING);
    *out_ARRAY = split(*out_STRING, "\n");
    foreach(*out_STRING1 in *out_ARRAY) {
        *list = split(*out_STRING1, ";");
        # assign values from array to parameters
        *ror = "None";
        *counter=0;
        foreach (*item_LIST in *list) {
            if      ( *counter == 0 ) { *pid         = *item_LIST ; }
            else if ( *counter == 1 ) { *source      = *item_LIST ; }
            else if ( *counter == 2 ) { *destination = *item_LIST ; }
            else if ( *counter == 3 ) { *ror         = *item_LIST ; }
            *counter = *counter + 1;
        }
    }
}

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
processPIDCommandFile(*cmdPath) {
    logInfo("processPID(*cmdPath)");
    readFile(*cmdPath, *out_STRING);
    *list = split(*out_STRING, ";");

    # assign values from array to parameters
    *ror = "None";
    *parent = "None";
    *counter=0;
    foreach (*item_LIST in *list) {
        if      ( *counter == 0 ) { *pidAction   = *item_LIST ; }
        else if ( *counter == 1 ) { *parent      = *item_LIST ; }
        else if ( *counter == 2 ) { *destination = *item_LIST ; }
        else if ( *counter == 3 ) { *ror         = *item_LIST ; }
        *counter = *counter + 1;    
    }
    *list_size = *counter ;

    # process command/action
    if ((*list_size==4) || (*list_size==3)){
        if(*pidAction == "create") {
            #manage pid in this repository
            EUDATCreatePID(*parent, *destination, *ror, bool("true"), *new_pid);
            getSharedCollection(*destination,*collectionPath);
            #create .pid.update file based on absolute file path
            msiReplaceSlash(*destination,*filepathslash); 
            triggerUpdateParentPID("*collectionPath*filepathslash.pid.update", *parent, *new_pid);
        } 
        else if(*pidAction=="update") {
            *status = 0;
            EUDATUpdatePIDWithNewChild(*parent, *destination);
            updateCommandName(*cmdPath,*status);
        }
        else {
            logError("ignoring incorrect command: [*out_STRING]");
        }
    }
    else {
        logError("ignoring incorrect list");
    }
}

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
doReplication(*pid, *source, *destination, *ror, *status) {
    logInfo("doReplication(*pid, *source, *destination, *ror)");

    #make sure the parent collections exist
    msiSplitPath(*destination, *parent, *child);
    msiCollCreate(*parent, "1", *collCreateStatus);

    #rsync object (make sure to supply "null" if dest resource should be the default one) 
    msiDataObjRsync(*source, "IRODS_TO_IRODS", "null", *destination, *rsyncStatus);

    if(*pid != "null") {
        #trigger pid management in destination
        getSharedCollection(*destination,*collectionPath);
        # create .pid.create file and monitor for .pid.update based on absolute file path
        msiReplaceSlash(*destination,*filepathslash);
        triggerCreatePID("*collectionPath*filepathslash.pid.create", *pid, *destination, *ror);
        updateMonitor("*collectionPath*filepathslash.pid.update");
    }
    else {
        logDebug("No pid management");
    }

}

#
# Monitor the specified pid command file
#
# Parameters:
#   *file   [IN]    start a monitor on the specified iRODS file
#
# Author: Willem Elbers, MPI-TLA
#
updateMonitor(*file) {
    logInfo("updateMonitor(*file)");
    delay("<PLUSET>1m</PLUSET>") {
        if(errorcode(msiObjStat(*file,*out)) >= 0) {
            logInfo("*file exists");
            processPIDCommandFile(*file);
        } else {
            logInfo("*file does not exist yet");
            # save *source of failed_transfered data object into fail_log 
            EUDATProcessErrorUpdatePID(*file);
        }
    }
}
