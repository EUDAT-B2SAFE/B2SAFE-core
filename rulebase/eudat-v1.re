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
    *credStorePath="/srv/irods/current/modules/EUDAT/cmd/credentials_test";
    *epicApi="http://hdl.handle.net/";
    *serverID="irods://<hostnameWithFullDomain>:1247"; 
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
# 	*pid            [IN]    pid of the digital object
#	*source         [IN] 	source path of the object to replicate
# 	*destination    [IN] 	destination path of the object to replicate
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
# 	*pid            [IN]    PID of the digital object
# 	*destination    [IN] 	destination path of the object to replicate
# 	*ror            [IN]    ROR of the original digital object
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
# 	*pid            [IN]    PID of the digital object
# 	*new_pid        [IN]    place of the replicated digital objekt.
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
#	*cmdPath    [IN]    the path to the .replicate file
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
#	*pid            [IN]    pid of the digital object
#	*source			[IN]    source path of the object to replicate
#	*destination	[IN]    destination path of the object to replicate
#	*ror	        [IN]    ROR of the digital object
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
