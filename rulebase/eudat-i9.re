################################################################################
#                                                                              #
# EUDAT Safe-Replication and PID management policies                           #
#                                                                              #
################################################################################


################################################################################
#                                                                              #
# Utility functions                                                            #
#                                                                              #
################################################################################

getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) {
    *credStoreType="os";
    *credStorePath="/home/irods/epicv2_test848.ini";
    *epicApi="http://hdl.handle.net/";
    *serverID="irods://egi-cloud17.zam.kfa-juelich.de:1247"; 
    *epicDebug=2; 
}

getSearchWildcard(*wildc){
    *wildc = "*";   
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
# Logging policies
#

logInfo(*msg) {
    logWithLevel("info", *msg);
}

logDebug(*msg) {
    logWithLevel("debug", *msg);
}

logError(*msg) {
    logWithLevel("error", *msg);
}

logWithLevel(*level, *msg) {
    msiWriteToLog(*level,"*msg");
    #msiWriteRodsLog("startReplication(*commandFile,*pid,*source,*destination)", *status);
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
        }
    }
}

#
# Retrieve the checksum for an object stored in iRODS
# And compute it using msiDataObjChksum if the object does not have any yet
#
# Parameters:
#   *path       [IN]    the path of the object in iRODS
#   *checksum   [OUT]   the checksum retrieved from the iCAT
#
# Author: Willem Elbers, MPI-TLA, edited by Elena Erastova, RZG
#
retrieveChecksum(*path, *checksum) {
    *checksum = -1;
    msiSplitPath(*path,*parent,*child);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parent' AND DATA_NAME = '*child'" ,*B);
    foreach   ( *B )    {
        msiGetValByKey(*B,"DATA_CHECKSUM", *checksum);
        logDebug(*checksum);
    }
    #compute checksum using msiDataObjChksum if the object does not have any yet
    if(*checksum == ""){
        msiDataObjChksum(*path, "null", *checksum);
    } 
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
    getRorPid(*pid, *ror);
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
    logInfo("triggerCreatePID(*commandFile,*pid,*destination)");
    writeFile("*commandFile", "create;*pid;*destination;*ror");
}

#
# Author: Willem Elbers, MPI-TLA
#
# Parameters:
#   *commandFile    [IN]    the absolute filename to store the command in
#   *pid            [IN]    PID of the digital object
#   *new_pid        [IN]    place of the replicated digital objekt.
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
    logDebug("processReplication(*cmdPath)");

    readFile(*cmdPath, *out_STRING);    

    #TODO: properly manage status here
    *status = 0;    
    # make an array of the string
    *out_ARRAY = split(*out_STRING, "\n")
    foreach(*out_STRING1 in *out_ARRAY) {
        logInfo("The line is : (*out_STRING1)");
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
# Process a .pid file and perform the appropriate action
#   supported actions: create, update
#
# Parameters:
#   *cmdPath    [IN]    the iRODS path to the pid command file
#
# Author: Willem Elbers, MPI-TLA
#
processPIDCommandFile(*cmdPath) {
    logInfo("processPID(*cmdPath)");
    readFile(*cmdPath, *out_STRING);
    *list = split(*out_STRING, ";");

    # assign values from array to parameters
    *ror = "None";
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
            createPID(*parent, *destination, *ror, *new_pid);
            getSharedCollection(*destination,*collectionPath);
            #create .pid.update file based on absolute file path
            msiReplaceSlash(*destination,*filepathslash); 
            triggerUpdateParentPID("*collectionPath*filepathslash.pid.update", *parent, *new_pid);
        } 
        else if(*pidAction=="update") {
            *status = 0;
            updatePIDWithNewChild(*parent, *destination);
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
    logInfo("doReplication(*pid, *source, *destination)");

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
        logInfo("No pid management");
    }
}

################################################################################
#                                                                              #
# Hooks to the EPIC API, depend on wrapper scripts around the epicclient.py    #
# script                                                                       #
#                                                                              #
################################################################################

# Legend (the prefix i stands for iCAT and e for epic):
#
# ePID PID on the EPIC server
# iPID PID record in the iCAT
# eCHECKSUM checksum on the EPIC server
# iCHECKSUM checksum record on the iCAT

# List of the function:
#
# createPID(*parent_pid, *path, *ror, *newPID)
# createPIDgriffin(*path, *newPID)
# addPIDWithChecksum(*path, *newPID)
# searchPID(*path, *existing_pid)
# searchPIDchecksum(*path, *existing_pid)
# CheckReplicas(*source, *destination, *commandFile)
# updatePIDWithNewChild(*parentPID, *childPID)
# getRorPid(*pid, *ror)
# EUDATeiPIDeiChecksumMgmt
# EUDATiPIDcreate(*PID)
# EUDATiCHECKSUMretrieve(*path, *checksum)
# EUDATiCHECKSUMget(*path, *checksum)
# EUDATiPIDretrieve(*path, *PID)
# EUDATiFieldVALUEretrieve(*path, *FNAME, *FVALUE)
# EUDATePIDcreate(*path, *PID)
# EUDATePIDsearch(*field, *value, *PID)
# EUDATeCHECKSUMupdate(*PID)
# EUDATeURLupdate(*PID, *newURL)
# EUDATePIDremove(*location)
# EUDATgetObjectTimeDiff(*filePath, *age)
# EUDATfileInPath(*path,*subColl)

#
# Generate a new PID for a digital object.
# Fields stored in the PID record: URL, ROR and CHECKSUM
# adds a ROR field if (*ror != "None")
#
# Parameters:
#   *parent_pid [IN]    the PID of the digital object that was replicated to us (not necessarily the ROR)
#   *path       [IN]    the path of the replica to store with the PID record
#   *ror        [IN]    the ROR PID (absolute url) of the digital object that we want to store.
#   *newPID     [OUT]   the pid generated for this replica 
#
# Author: Willem Elbers, MPI-TLA, edited by Elena Erastova, RZG
#
#createPID(*rorPID, *path, *newPID, *ror) {
createPID(*parent_pid, *path, *ror, *newPID) {
    logInfo("create pid for *path and save *ror as ror");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    getSearchWildcard(*wildc);

    #check if PID already exists
    if(*epicDebug > 1) {
        logDebug("epicclient.py *credStoreType *credStorePath search URL *wildc*path");
    }
    msiExecCmd("epicclient.py", "*credStoreType *credStorePath search URL *wildc*path", "null", "null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *existing_pid);

    if((*existing_pid == "empty") || (*existing_pid == "None")) {
        # create PID
        if(*epicDebug > 1) {
            logDebug("epicclient.py *credStoreType *credStorePath create *serverID*path");
        }
        msiExecCmd("epicclient.py", "*credStoreType *credStorePath create *serverID*path", "null", "null", "null", *out);
        msiGetStdoutInExecCmdOut(*out, *newPID);
        logDebug("created handle = *newPID");
	
	# Add PID into iCAT
	writeLine("serverLog","Begin to SAVE PID into field AVU -PID- of iCAT *path with PID = *newPID");
	EUDATiPIDcreate2(*newPID,*path)
        #msiSetReplComment("null",*path,0,*newPID);
	
        writeLine("serverLog","---> PID's saved in iCAT with AVU PID");

        # add CHECKSUM to PID record
        retrieveChecksum(*path, *checksum);
        if(*epicDebug > 1) {
            logDebug("epicclient.py *credStoreType *credStorePath modify *newPID CHECKSUM *checksum");
        }
        msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *newPID CHECKSUM *checksum", "null", "null", "null", *out3);
        msiGetStdoutInExecCmdOut(*out3, *response3);
        logDebug("modify handle response = *response3");

        # add RoR to PID record if there is one defined
        if(*ror != "None") {
            # add RoR to PID record
            if(*epicDebug > 1) {
                logDebug("epicclient.py *credStoreType *credStorePath modify *newPID ROR *ror");
            }
            msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *newPID ROR *ror", "null", "null", "null", *out2);
            msiGetStdoutInExecCmdOut(*out2, *response2);
            logDebug("modify handle response = *response2");
        }
    } 
    else {
        *newPID = *existing_pid;
        logInfo("PID already exists (*newPID)");
    }
}

##
# Generate a new PID for a digital object.
# Fields stored in the PID record: URL, CHECKSUM
#
# griffin first writes an empty file with the same name to the destination and closes it; 
# then it opens it and writes the contents of the actual file and closes it.
# Which is why createPIDgriffin a PID without checksum on the first step.
# And ut adds cheksum on the second "put", when the PID already exists.
#
# Parameters:
#   *path       [IN]    the path of the replica to store with the PID record
#   *newPID     [OUT]   the pid generated for this replica 
#
# Author: CINECA, edited and added by Elena Erastova, RZG
#
createPIDgriffin(*path, *newPID) {
    logInfo("create pid for *path");

    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);

    #check if PID already exists
    if(*epicDebug > 1) {
        logDebug("epicclient.py *credStoreType *credStorePath search URL *serverID*path");
    }
    msiExecCmd("epicclient.py", "*credStoreType *credStorePath search URL *serverID*path", "null", "null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *existing_pid);

    if(*existing_pid == "empty") {
        # create PID
        if(*epicDebug > 1) {
            logDebug("epicclient.py *credStoreType *credStorePath create *serverID*path");
        }
        msiExecCmd("epicclient.py", "*credStoreType *credStorePath create *serverID*path", "null", "null", "null", *out);
        msiGetStdoutInExecCmdOut(*out, *newPID);
        logDebug("created handle = *newPID");
    } else {
        *newPID = *existing_pid;
        
        # add CHECKSUM to PID record
        msiDataObjChksum(*path, "null", *checksum);
        if(*epicDebug > 1) {
            logDebug("epicclient.py *credStoreType *credStorePath modify *newPID CHECKSUM *checksum");
        }
        msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *newPID CHECKSUM *checksum", "null", "null", "null", *out3);
        msiGetStdoutInExecCmdOut(*out3, *response3);
        logDebug("modify handle response = *response3");
        logInfo("PID *newPID already exists - added checksum *checksum to PID *newPID");
    }
}


#
# addPIDWithChecksum is meant as a faster version of above createPID. 
# It is better to use while injesting new files to iRODS which do not have PIDs yet.
# Be careful: It does not check if the PID already exists. And it does not add ROR field.
# And it does not use retrieveChecksum, but computes checksum with msiDataObjChksum.
# Adds checksum on the fly while creating the PID.
# Parameters:
#   *path       [IN]    the path of the replica to store with the PID record
#   *newPID     [OUT]   the pid generated for this replica 
#
# Author: CINECA, edited and added by Elena Erastova, RZG
#
addPIDWithChecksum(*path, *newPID) {
    logInfo("Add PID with CHECKSUM for *path");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    msiDataObjChksum(*path, "null", *checksum);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath create *serverID*path --checksum *checksum","null","null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *newPID);
    logDebug("added handle =*newPID with checksum = *checksum");
}


searchPID(*path, *existing_pid) {
    logInfo("search pid for *path");
    getSearchWildcard(*wildc);
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    #check if PID already exists
    if(*epicDebug > 1) {
        logDebug("epicclient.py *credStoreType *credStorePath search URL *wildc*path");
    }
    msiExecCmd("epicclient.py", "*credStoreType *credStorePath search URL *wildc*path", "null", "null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *existing_pid);
}

searchPIDchecksum(*path, *existing_pid) {
    logInfo("search pid for *path");
    getSearchWildcard(*wildc);
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    #check if PID already exists
    #msiDataObjChksum(*path, "null", *checksum);

    *checksum = "";
    msiSplitPath(*path,*parent,*child);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parent' AND DATA_NAME = '*child'" ,*B);
    foreach   ( *B )    {
        msiGetValByKey(*B,"DATA_CHECKSUM", *checksum);
        #logDebug(*checksum);
    }
    logDebug("search by CHECKSUM inside = *checksum");

    if(*checksum == "") {
        *existing_pid ="empty";
        logDebug("search by CHECKSUM inside if no checksum = *checksum");
    }
    else {
            msiExecCmd("epicclient.py", "*credStoreType *credStorePath search CHECKSUM *checksum", "null", "null", "null", *out);
            msiGetStdoutInExecCmdOut(*out, *existing_pid);
        logDebug("search by CHECKSUM inside call search = *existing_pid");
    }
        
}

#
# check whether two files are available and identical, if thats not the case replicate from source to destination
#
# Parameters:
#   *source         [IN]     source of the file
#   *destination    [IN]     destination of the file
#   *commandFile    [IN]     name of the replicate file.
#
# TODO: use our known solution for .replicate file names to make them more unique?

CheckReplicas(*source, *destination, *commandFile) {
    logInfo("Check if 2 replicas have the same checksum. Source = *source, destination = *destination");

    #msiDataObjChksum(*source, "null", *checksum0);
    #msiDataObjChksum(*destination, "null", *checksum1);

    *checksum0 = "";
    msiSplitPath(*source,*parentS,*childS);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parentS' AND DATA_NAME = '*childS'" ,*BS);
    foreach   ( *BS )    {
        msiGetValByKey(*BS,"DATA_CHECKSUM", *checksum0);
        logInfo("checksum0 = *checksum0");
    }

    *checksum1 = "";
    msiSplitPath(*destination,*parentD,*childD);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parentD' AND DATA_NAME = '*childD'" ,*BD);
    foreach   ( *BD )    {
        msiGetValByKey(*BD,"DATA_CHECKSUM", *checksum1);
        logInfo("checksum1 = *checksum1");
    }

    if(*checksum0 != *checksum1) {
        searchPID(*source, *pid);
        logInfo("*checksum0 != *checksum1, existing_pid = *pid");
        logInfo("replication from *source to *destination");
        getSharedCollection(*source,*collectionPath);
        triggerReplication("*collectionPath*commandFile",*pid,*source,*destination);
    }
}

#
# Update a PID record with a new child.
#
# Parameters:
#       *parentPID  [IN]    PID of the record that will be updated
#       *childPID   [IN]    PID to store as one of the child locations
#
# Author: Willem Elbers, MPI-TLA
# Modified by: Claudio Cacciari, CINECA
#
updatePIDWithNewChild(*parentPID, *childPID) {
    logInfo("update parent pid (*parentPID) with new child (*childPID)");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    if(*epicDebug > 1) {
        logDebug("epicclient.py *credStoreType *credStorePath relation *parentPID *epicApi*childPID");
    }
    msiExecCmd("epicclient.py","*credStoreType *credStorePath relation *parentPID *epicApi*childPID", "null", "null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *response);
    logDebug("update handle location response = *response");
}

#
# get the ROR entry for a PID
#
# Parameters:
#   *pid    [IN]     PID that you want to get the ROR for
#   *ror    [OUT]    ROR for *pid
#
getRorPid(*pid, *ror) {
    logInfo("get RoR from (*pid)");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    msiExecCmd("epicclient.py", "*credStoreType *credStorePath read *pid --key ROR", "null", "null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *ror);
}

#
# This function create a PID for $objPath and store its value and the checksum in the iCAT if it does ot exist.
# Otherwhise the function modify the PID.
#
# Environment variable used:
#   $objPath
#
# Arguments:
#
# Author: Giacomo Mariani, CINECA
#
EUDATeiPIDeiChecksumMgmt {    
    *ePIDcheck=bool("true");        # Should became an argument of the function          
    *minTime = int("86400");        # Should became an argument of the function          
    msiWriteRodsLog("EUDATeiPIDeiChecksumMgmt -> Look if the PID is in the iCAT", *status);
    # Search for iPID and, if it exists, enter the if below
    if (EUDATiFieldVALUEretrieve($objPath, "PID", *oldPID)) 
    {
        msiWriteRodsLog("EUDATeiPIDeiChecksumMgmt -> Update PID with CHECKSUM for: *oldPID, $userNameClient, $objPath", *status);
        EUDATeCHECKSUMupdate(*oldPID);             # Update the eCHECKSUM.
    }
    # iPID does not exist
    else
    {
        # If *ePIDcheck look for ePID
        *oldPID = "empty";
        if(*ePIDcheck){
            msiWriteRodsLog("EUDATeiPIDeiChecksumMgmt -> No PID registered in iCAT. Looking on the EPIC server.", *status);
            EUDATgetObjectTimeDiff($objPath, *liveTime);
            # If the file is older than a day look for ePID
            if ( *liveTime >= *minTime ) then
            {
                getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug)
                # Get ePID looking for one between: URL and CHECKSUM.
                #msiDataObjChksum($objPath, "null", *checksum);
                EUDATePIDsearch("URL", "*serverID"++"$objPath", *oldPID)
            }
        }
        # If ePID does not exist create both ePID and iPID
        if ( *oldPID == "empty" ) then
            { 
            msiWriteRodsLog("EUDATeiPIDeiChecksumMgmt -> No PID in epic server yet", *status);
            EUDATePIDcreate($objPath, *newPID);   # Create ePID
            EUDATiPIDcreate(*newPID);             # Create iPID
        }
        else
        {
            msiWriteRodsLog("EUDATeiPIDeiChecksumMgmt -> Modifying the PID in epic server: *oldPID", *status);  
            EUDATeCHECKSUMupdate(*oldPID);        # Update eCHECKSUM
            EUDATiPIDcreate(*oldPID);             # Create iPID
        }
    }
}

#
# The function write iPID given ePID.
#
# Environment variable used:
#   $objPath
#
# Arguments:
#   *PID             [IN] ePID
#
# Author: Giacomo Mariani, CINECA
#
EUDATiPIDcreate(*PID) {
    msiAddKeyVal(*Keyval,"PID", "*PID");
    writeKeyValPairs('serverLog', *Keyval, " is : ");
    msiGetObjType($objPath, *objType);
    msiAssociateKeyValuePairsToObj(*Keyval, $objPath, *objType);
    msiWriteRodsLog("EUDATiPIDcreate -> Added PID = *PID to metadata of $objPath", *status);
}

#
# The function write iPID given ePID.
#
# Arguments:
#   *PID             [IN] ePID
#   *PATH	     [IN] path of logical data object		
#
# Author: Giacomo Mariani, CINECA; Edited: Long Phan, Juelich
#
EUDATiPIDcreate2(*PID,*path) {
    msiAddKeyVal(*Keyval,"PID", "*PID");
    writeKeyValPairs('serverLog', *Keyval, " is : ");
    msiGetObjType(*path,*objType);
    msiAssociateKeyValuePairsToObj(*Keyval, *path, *objType);
    msiWriteRodsLog("EUDATiPIDcreate -> Added PID = *PID to metadata of *path", *status);
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
    msiWriteRodsLog("EUDATiCHECKSUMretrieve -> Looking at *path", *status1);
    msiSplitPath(*path, *coll, *name);
    *d = SELECT DATA_CHECKSUM WHERE DATA_NAME = '*name' AND COLL_NAME = '*coll'; 
    foreach(*c in *d) {
        msiGetValByKey(*c, "DATA_CHECKSUM", *checksum);
        if (*checksum==""){
            writeLine("serverLog","EUDATiCHECKSUMretrieve -> The iCHECKSUM is empty");
        }else{
            writeLine("serverLog","EUDATiCHECKSUMretrieve -> Found iCHECKSUM = *checksum");
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
    if (!EUDATiCHECKSUMretrieve(*objPath, *checksum)) {
        msiDataObjChksum(*path, "null", *checksum);
    }
}


#
# The function retrieve iPID. 
#
# Environment variable used:
#   $objPath
#
# Arguments:
#   *PID             [IN]    iPID
#   *status          [REI]   false if no value is found, trou elsewhere
#
# Author: Giacomo Mariani, CINECA
#
EUDATiPIDretrieve(*path, *PID) {
    *status = bool("false");
    msiSplitPath(*path, *coll, *name);
    writeLine ("serverLog","EUDATiPIDretrieve -> path = *path , coll = *coll , name = *name");
    *d = SELECT META_DATA_ATTR_VALUE WHERE DATA_NAME = '*name' AND COLL_NAME = '*coll' AND META_DATA_ATTR_NAME = 'PID'; 
    foreach(*c in *d) {
        msiGetValByKey(*c, "META_DATA_ATTR_VALUE", *PID);
        writeLine("serverLog","EUDATiPIDretrieve -> PID = *PID");
        *status = bool("true");
    }
    *status;
}

#
# The function retrieves the value of the required field.
#
# Environment variable used:
#
# Arguments:
#   *path               [IN]    the iRODS path of the object involved in the query
#   *FNAME              [IN]    the name of the iCAT field the function is going to look for
#   *FVALUE             [OUT]   the corresponding value, if any
#   *status0            [REI]   false if no value is found, trou elsewhere
#
# Author: Giacomo Mariani, CINECA
#
EUDATiFieldVALUEretrieve(*path, *FNAME, *FVALUE) {
    msiWriteRodsLog("EUDATiFieldVALUEretrieve -> looking for *FNAME of *path", *status);
    *status0 = bool("false");
    msiSplitPath(*path, *coll, *name);
    *d = SELECT META_DATA_ATTR_VALUE WHERE DATA_NAME = '*name' AND COLL_NAME = '*coll' AND META_DATA_ATTR_NAME = '*FNAME'; 
    foreach(*c in *d) {
        msiGetValByKey(*c, "META_DATA_ATTR_VALUE", *FVALUE);
        msiWriteRodsLog("EUDATiFieldVALUEretrieve -> *FNAME equal to= *FVALUE", *status);
        *status0 = bool("true");
    }
    *status0;
}

#
# The function create ePID.
#
# Environment variable used:
#
# Arguments:
#   *path            [IN]   The full iRODS path of the object
#   *PID             [OUT]    The created ePID.
#
# Author: Giacomo Mariani, CINECA
#
EUDATePIDcreate(*path, *PID) {
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) 
    msiWriteRodsLog("EUDATePIDcreate -> Add PID with CHECKSUM to: USER, OBJPATH: $userNameClient, *path", *status);
    msiDataObjChksum(*path, "null", *checksum);
    msiWriteRodsLog("EUDATePIDcreate -> The CHECKSUM is: *checksum", *status);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath create *serverID"++"*path --checksum *checksum", "null", "null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *PID);
    msiWriteRodsLog("EUDATePIDcreate -> Created handle is: *PID", *status);
}

#
# The function retrieve ePID searching for a field between URL, CHECKSUM. 
#
# Environment variable used:
#   $objPath
#
# Arguments:
#   *field           [IN]    The eField to look in
#   *value           [IN]    The valou to search for
#   *PID             [OUT]   ePID
#   *status0         [REI]   false if no value is found, trou elsewhere
#
# Author: Giacomo Mariani, CINECA
#
EUDATePIDsearch(*field, *value, *PID) {
    msiWriteRodsLog("EUDATePIDsearch -> search the PID with *field equal to *value", *status);
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) 
    *status0 = bool("true");
    msiExecCmd("epicclient.py","*credStoreType *credStorePath search *field \"*value\"", "null", "null", "null", *out);    
    msiGetStdoutInExecCmdOut(*out, *PID);
    msiWriteRodsLog("EUDATePIDsearch -> search handle response = *PID", *status);
    if ( str(*PID) == "empty" ) { 
        *status0=bool("false"); 
        msiWriteRodsLog("EUDATePIDsearch -> search handle response = no PID", *status);
    }
    *status0;
}

#
# This function update the checksum field of the PID of $objPath
#
# Environment variable used:
#   $objPath        
#
# Arguments:
#   *PID                [IN] The PID associated to $objPath
#
# Author: Giacomo Mariani, CINECA
#
EUDATeCHECKSUMupdate(*PID) {
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) 
    msiWriteRodsLog("EUDATeCHECKSUMupdate -> modify checksum related to PID *PID", *status);
    msiDataObjChksum($objPath, "null", *checksum);
    msiWriteRodsLog("EUDATeCHECKSUMupdate -> created checksum = *checksum", *status);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *PID CHECKSUM *checksum", "null", "null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *response);
    msiWriteRodsLog("EUDATeCHECKSUMupdate -> modify handle response = *response", *status);
}

#
# This function update the URL field of the PID of $objPath
#
# Environment variable used:
#   $objPath        
#
# Arguments:
#   *PID                [IN] The PID associated to $objPath
#   *newURL             [IN] The new URL to be associated to the PID of $objPath
#
# Author: Giacomo Mariani, CINECA
#
EUDATeURLupdate(*PID, *newURL) {
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) 
    msiWriteRodsLog("EUDATeCHECKSUMupdate -> modify URL in PID *PID", *status);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *PID URL \"*newURL\"", "null", "null", "null", *out);
    # WARNING: the following line clean all the 10320/LOC field instead of removing only the old entry... 
    #          This is good since it is the only one for EPOS. To be improved. 
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *PID 10320/LOC ''", "null", "null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *response);
    msiWriteRodsLog("EUDATeCHECKSUMupdate -> modify handle response = *response", *status);
}


#
# This function remove an ePID... even if its 10320/loc field is not empty!
# To be improved.
#
# Environment variable used:
#   $objPath        
#
# Arguments:
#   *location           [IN]    The location associated to $objPath in ePID
#
# Author: Giacomo Mariani, CINECA
#
EUDATePIDremove(*location) {
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) 
    msiWriteRodsLog("EUDATePIDremove -> Removing PID associated to: $userNameClient, $objPath ($filePath) \"*location\"", *status);
    if (EUDATePIDsearch("URL", "*location", *pid)){
      msiExecCmd("epicclient.py","*credStoreType *credStorePath read --key 10320/LOC *pid", "null", "null", "null", *out2);
      msiGetStdoutInExecCmdOut(*out2, *loc10320);
      msiWriteRodsLog("EUDATePIDremove -> get 10320/LOC from handle response = *loc10320", *status);
#      if ("*loc10320" like "Error*")||("*loc10320" == "")||("*loc10320" like "None*") then {
        msiWriteRodsLog("EUDATePIDremove -> 10320/LOC does not exist or is empty: PID will be deleted", *status);
#            msiExecCmd("deleteHandle.py","*pid","null", "null", "null", *out3);
            msiExecCmd("epicclient.py","*credStoreType *credStorePath delete *pid", "null", "null", "null", *out3);
            msiGetStdoutInExecCmdOut(*out3, *response3);
            msiWriteRodsLog("EUDATePIDremove -> delete handle response = *response3", *status);
        # The PID record could be associated to a replica.
        # The field 10320/LOC of the parent PID record should be updated
#   }
#   else {
#       # The PID record contains pointers to other DO copies.
#       # What should we do?
#       # Maybe all the copies should be deleted together with the master copy.
#       msiWriteRodsLog("EUDATePIDremove -> The PID record *pid contains pointers to other DO copies", *status);
#   }
    }else{
       msiWriteRodsLog("EUDATePIDremove -> No PID associated to *location found", *status);
    }
}

#
# Calculate the difference between the creation time and the modification time of an object.
# In seconds.
#
# Arguments:
#   *filePath           [IN]   The full iRODS path of the object
#   *age                [OUT]  The age of the object 
#
# Author: Giacomo Mariani, CINECA
#
EUDATgetObjectTimeDiff(*filePath, *age) {
    # Look when the file has been created in iRODS
    msiSplitPath(*filePath, *fileDir, *fileName);   
    *ec = SELECT DATA_CREATE_TIME, DATA_MODIFY_TIME WHERE DATA_NAME = '*fileName' AND COLL_NAME = '*fileDir';
    foreach(*ec) {
        msiGetValByKey(*ec, "DATA_CREATE_TIME", *creationTime);
        msiWriteRodsLog("EUDATgetObjectTimeDiff -> Created at  *creationTime", *status);
        msiGetValByKey(*ec, "DATA_MODIFY_TIME", *modifyTime);
        msiWriteRodsLog("EUDATgetObjectTimeDiff -> Modified at *modifyTime", *status);
    }
    *age=int(*modifyTime)-int(*creationTime);
    msiWriteRodsLog("EUDATgetObjectTimeDiff -> Difference in time: *age seconds", *status);
}

#
# Rules to chech if a file is in a given path.
#
# Arguments:
#   *path               [IN]    The full iRODS path of the object
#   *subColl            [IN]    The iRODS path of the collection we are looging in for the object
#   *b                  [REI]   False if no value is found, true elsewhere
#
# Author: Hao Xu, DICE; Giacomo Mariani, CINECA
#
EUDATfileInPath(*path,*subColl) {
    writeLine ("serverLog","conditional acPostProcForCopy -> EUDATfileInPath");
    msiSplitPath(*path, *coll, *name);
    *b = bool("false");
    #*fullColl = str(*subColl)++"/%"
    #writeLine ("serverLog","EUDATfileInPath -> fullColl = *fullColl");
    #*d = SELECT count(DATA_NAME) WHERE COLL_NAME like '*fullColl' AND DATA_NAME = '*name';
    *d = SELECT count(DATA_NAME) WHERE COLL_NAME like '*subColl' AND DATA_NAME = '*name';
    foreach(*c in *d) {
         msiGetValByKey(*c,"DATA_NAME",*num);
         if(*num == '1') {
             writeLine("serverLog","EUDATfileInPath -> found file *name in collection *subColl");
             *b = bool("true");
         }   
    }
    *b;
}

#
# Rule: setup permission for other User from other Zone, defined as GROUP
# Arguments:
#	*path		[IN] the full iRODS path of the object
#   *otherUser	[IN] name of user who will be appended into GROUP
#   *otherZone  [IN] name of zone of *otherUser
# Author: Long Phan, Juelich	
#
EUDATsetAccessZone(*path,*otherUser,*otherZone) {
		
	msiSplitPath(*path,*collname,*dataname);
		
	*c = SELECT DATA_OWNER_NAME, DATA_OWNER_ZONE WHERE COLL_NAME = '*collname' AND DATA_NAME = '*dataname';
	foreach (*d in *c) {
             msiGetValByKey(*d,"DATA_OWNER_NAME",*owner);
             msiGetValByKey(*d,"DATA_OWNER_ZONE",*zone);         
    }
	 
	*dataOwner   = "*owner"++"#"++"*zone";
	*sessionUser = "$userNameClient"++"#"++"$rodsZoneClient";
	
	# Only Owner of Data have access right to add User into GROUP
	if (*dataOwner == *sessionUser) {
			writeLine("serverLog","Identity of User *sessionUser is confirmed");
			*addUser = "*otherUser"++"#"++"*otherZone";
			msiAddKeyVal(*Keyval,"GROUP", "*addUser");
			writeKeyValPairs('serverLog', *Keyval, " is : ");
			msiGetObjType(*path,*objType);
			msiAssociateKeyValuePairsToObj(*Keyval, *path, *objType);
			msiWriteRodsLog("EUDATsetAccessZone -> Added user= *addUser  to metadata GROUP of *path", *status);
	} else {
			writeLine("serverLog","Identity of User *sessionUser is not confirmed with Owner *dataOwner of *path");
	}
}

# ------------------------------------------------------------------------------------------------------------------
# Modify this hook on core.re (iRODS3.3) like following:
# acPreProcForExecCmd(*cmd, *args, *addr, *hint) {
#        EUDATsetFilterACL (*cmd, *args, *addr, *hint, *status);
#        if (*status == "false") {
#                fail;
#        }
#}
# and comment this "acPreProcForExecCmd(*cmd, *args, *addr, *hint) { }"
# ------------------------------------------------------------------------------------------------------------------

#
# Rule: filter ACL
# Arguments:
# 	*cmd  			[IN]	name of remote-script (ex. epicclient.py)
# 	*args			[IN]	argument of *cmd
#	*addr, *hint	[IN]	( see iexecmd -h)  
# 	*status			[OUT]	status of variable to decide whether script will be executed (true = yes, false = no)
# Author: Long Phan, Juelich 
#
EUDATsetFilterACL (*cmd, *args, *addr, *hint, *status) {
	*status = "false";
	
	if (*cmd == 'epicclient.py')
        {
                writeLine("serverLog","PYTHON Script *cmd is being accessed (remotely) with argument *args by user $userNameClient comes from $rodsZoneClient");
                writeLine("serverLog","--- begin to analyze argument *args");
                # Use (python script/ irods-microservice/ C-new-microservice) to filter the action ex. modify/delete and PID from argument *args
                # PID will be searched in iCAT to get dataOwner
                # After that it will be compared with $userNameClient and $rodsZoneClient. If match, action will be executed.
                # NOTICE: for first approach only actions modify and delete will be processed.

                *subargs = split(*args, " ");
                if (strlen(*args) > 0) {
                        if (*args == "-h") {
                                writeLine("serverLog","--- Argument -h");
                                *status = "true";
                        } else {
                                *action = elem(*subargs,2);
                                if (*action == "read" || *action == "search" || *action == "relation" || *action == "test") {
                                        writeLine("serverLog","--- NOTICE action *action on PID");
										*status = "true";
								} else if (*action == "create") {
										
										# -------------------------------------- BEGIN TO FILTER ACTION CREATE --------------------------------------------------
										
										*param = elem(*subargs,3)
										# *param should have format of URL ----> ex. irods://egi-cloud17.zam.kfa-juelich.de:1247/COMMUNITY/DATA16/t13.test
										writeLine("serverLog","WARNUNG action CREATE PID with URL *param");																		
																				
										# Filter logical address of data Object from *param
										getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
										
										*templength = strlen(*serverID);
																														
										*tempID = substr(*param,0,*templength);
										writeLine("serverLog","Length of *serverID = *templength with substr from *param = *tempID");
										
										if (*tempID == *serverID) {
											msiSubstr(*param,"*templength","null",*stringout);
											*pathDataObject = *stringout;
											writeLine("serverLog","Path of Data Object = *pathDataObject");																					
											# figure out dataOwner of data Object and compare with user on session. If not dataOwner, fail
											msiSplitPath(*pathDataObject,*collname,*dataname);													
										    
										    # ------------- Check the existence of Data Object in iCAT, 
										    # ------------- if it exists in iCAT, continue check dataOwner. If it's NOT exist in iCAT, continue deliver CREATE right. 
										    # ------------- Base on rule EUDATfileInPath of Giacomo -----------------
										    
										    *t = bool("false");	
										    writeLine("serverLog","BEGIN TO CHECK WHETHER DATA EXIST");									    
										    *y = SELECT count(DATA_NAME) WHERE COLL_NAME = '*collname' AND DATA_NAME = '*dataname';
										    foreach(*x in *y) {
										         msiGetValByKey(*x,"DATA_NAME",*num);
										         if(*num == '1') {										         	 										         
										             *t = bool("true");
										             writeLine("serverLog"," Confirmed that DATA already existed under Coll_Name *collname with name *dataname");
										         }   
										    }
										    # -----------------------------------------------------------------------
										    
										    if (*t == bool("false")) {										    	
										    	writeLine("serverLog","Identity of user $userNameClient from $rodsZoneClient create PID without replication of data, script will be executed");
										    	
										    	# SHOULD USER BE ALLOWED TO CREATE PID WITHOUT REPLICATION ? If yes, *status = true. Otherwise, set *status = false.
										    	*status = "true";
										    	
										    } else {
										       		writeLine("serverLog","EUDATfileInPath -> found file *dataname in collection *collname. Begin to check identity of user");
										    										    									    
												    # -----------------------------------------------------------------------------------------------------											   
												    *y = SELECT DATA_OWNER_NAME, DATA_OWNER_ZONE WHERE COLL_NAME = '*collname' AND DATA_NAME = '*dataname';
													foreach (*x in *y) {
												            msiGetValByKey(*x,"DATA_OWNER_NAME",*owner);
												            msiGetValByKey(*x,"DATA_OWNER_ZONE",*zone);         
												    }
												    										    
												    if ($userNameClient == *owner && $rodsZoneClient == *zone) {			
														writeLine("serverLog","User $userNameClient from *zone is confirmed as DataOwner of DataObject, action creating PID keeps going");	
																
														# Check whether this data Object already has one PID (in iCAT). If yes, fail. 
														# ------------- Base on rule EUDATfileInPath of Giacomo -----------------
																													
														*h = "META_DATA_ATTR_NAME = 'PID' AND COLL_NAME = '*collname' AND DATA_NAME = '*dataname'";
														msiMakeGenQuery("count(META_DATA_ATTR_VALUE)",*h,*GenQInp);
														msiExecGenQuery(*GenQInp, *GenQOut);
														*b = bool("false");
														
														foreach(*GenQOut) {
															msiGetValByKey(*GenQOut,"META_DATA_ATTR_VALUE",*meta);
															if (*meta == '1') {
																#writeLine("serverLog","Name of file *dataname has AVU = *meta");
																*b = bool("true");														
															}														
														}
														
														if (*b == bool("false")) {
															writeLine("serverLog","Variable = *b, PID does not exist in AVU. Action CREATE PID will be executed");
															*status = "true";
														} else {
															writeLine("serverLog","Variable = *b, PID already exist in AVU. Action CREATE PID will be canceled");
															*status = "false";
														}																																			
														# -----------------------------------------------------------------------
																																														    	
												    } else {
												   		writeLine("serverLog","User $userNameClient from *zone is NOT confirmed as DataOwner of DataObject, action is being canceled");
												    	*status = "false";   
												    }
										    }											
										} else {
											writeLine("serverLog","serverID is not correct, action CREATE will be canceled");
											*status = "false";
										} 										
										
                               } else if (*action == "modify" || *action == "delete") {
                                
                                		# -------------------------------------- BEGIN TO FILTER ACTION MODIFY or DELETE --------------------------------------------------
                                		
                                        writeLine("serverLog","--- WARNUNG action *action on PID");
                                        *pid = elem(*subargs,3);
                                        writeLine("serverLog","--- Begin to check identity of user");
                                        writeLine("serverLog","--- Use PID *pid to search in iCAT to query dataOwner");

                                        #*d = SELECT DATA_OWNER_NAME, DATA_OWNER_ZONE WHERE DATA_COMMENTS = '*pid';
										*d = SELECT DATA_OWNER_NAME, DATA_OWNER_ZONE, COLL_NAME, DATA_NAME WHERE META_DATA_ATTR_NAME = 'PID' AND META_DATA_ATTR_VALUE = '*pid';
                                        foreach (*c in *d) {
                                                msiGetValByKey(*c,"DATA_OWNER_NAME",*owner);
                                                msiGetValByKey(*c,"DATA_OWNER_ZONE",*zone);
                                                msiGetValByKey(*c,"DATA_NAME",*dataname);
                                                msiGetValByKey(*c,"COLL_NAME",*collname);
                                                writeLine("serverLog","Owner = *owner at Zone = *zone of DataObject *collname/*dataname is being accessed");
                                        }
										
										if ($userNameClient == *owner && $rodsZoneClient == *zone) {
												*status = "true";
                                                writeLine("serverLog","Identity of user $userNameClient from Zone $rodsZoneClient is confirmed as OWNER of DATA, script will be executed");
                                        } else {
                                        	
												*user = "$userNameClient"++"#"++"$rodsZoneClient";																									
												*e = SELECT META_DATA_ATTR_VALUE WHERE META_DATA_ATTR_NAME = 'GROUP' AND COLL_NAME = '*collname' AND DATA_NAME = '*dataname';
												foreach (*f in *e) {
													msiGetValByKey(*f,"META_DATA_ATTR_VALUE",*otherUser);
													if (*otherUser == *user) {
														*status = "true";
														writeLine("serverLog","Access right of user $userNameClient from Zone $rodsZoneClient is confirmed in GROUP");
														break;
													}															
												}
												if (*status == "false") {
													writeLine("serverLog","Access right is NOT confirmed, user *user is not a part of GROUP");
												}
										}		
										
                                } else {                                		
                                        writeLine("serverLog","Action is NOT confirmed ---");                                        
                                }
                        }
                } else {
                        writeLine("serverLog","Argument is unknown");
						                        
                }
        }

}
 
