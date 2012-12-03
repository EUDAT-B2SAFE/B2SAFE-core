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

getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *epicDebug) {
    *credStoreType="os";
    *credStorePath="/srv/irods/current/modules/EUDAT/cmd/credentials_test";
    *epicApi="http://hdl.handle.net/"; 
    *epicDebug=2; 
}

#
# Return the absolute path to the iRODS collection where all command files are stored.
#   typically "<zone>/replicate". Make sure all users and remote users have write permissions here.
#
# Parameters:
#       *zonePath           [IN]    a iRODS path name including the zone
#       *collectionPath     [OUT]   the iRODS absolute path to the collection used to store command files
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
#       *file       [IN]    iRODS location of the file to read
#       *contents   [OUT]   the command contents
#
# Author: Willem Elbers, MPI-TLA
#
readFile(*file, *contents) {
	msiDataObjOpen("objPath=*file++++replNum=0++++openFlags=O_RDONLY",*S_FD);
                msiDataObjRead(*S_FD,"1024",*R_BUF);
                msiBytesBufToStr(*R_BUF, *contents);
        msiDataObjClose(*S_FD,*closeStatus);
}

#
# Rename a command file.
# Appends the current timestamp and a ".succes" or ."failed" identifier 
#
# Parameters:
#       *cmdPath    [IN]    the command file to rename
#       *status     [OUT]   status, 0 = ok, <0 = error
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
#       *file   [IN]    start a monitor on the specified iRODS file
#
# Author: Willem Elbers, MPI-TLA
#
updateMonitor(*file) {
        logInfo("updateMonitor(*file)");
        delay("<PLUSET>30s</PLUSET>") {
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
#
# Parameters:
#       *path       [IN]    the path of the object in iRODS
#       *checksum   [OUT]   the checksum retrieved from the iCAT
#
# Author: Willem Elbers, MPI-TLA
#
retrieveChecksum(*path, *checksum) {
    *checksum = -1;
    msiSplitPath(*path,*parent,*child);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parent' AND DATA_NAME = '*child'" ,*B);
    foreach   ( *B )    {
        msiGetValByKey(*B,"DATA_CHECKSUM", *checksum);
        logDebug(*checksum);
    }
    #use shell script to compute checksum if we cannot retrieve it from icat?
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
#       *commandFile    [IN]    the absolute filename to store the command in
# 	*pid            [IN]    pid of the digital object
#	*source         [IN] 	source path of the object to replicate
# 	*destination    [IN] 	destination path of the object to replicate
#
# Author: Willem Elbers, MPI-TLA
#
triggerReplication(*commandFile,*pid,*source,*destination) {
	logInfo("startReplication(*commandFile,*pid,*source,*destination)");
	writeFile("*commandFile","*pid;*source;*destination");
}

#
# Start a PID created by writing a .pid command file
#
# Parameters:
#       *commandFile    [IN]    the absolute filename to store the command in
# 	*pid            [IN]    pid of the digital object
#	*source         [IN] 	source path of the object to replicate
# 	*destination    [IN] 	destination path of the object to replicate
#
# Author: Willem Elbers, MPI-TLA
#
triggerCreatePID(*commandFile,*pid,*destination) {
        logInfo("triggerCreatePID(*commandFile,*pid,*destination)");
        writeFile("*commandFile", "create;*pid;*destination");
}

#
# Author: Willem Elbers, MPI-TLA
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
        foreach(*out_STRING) {
            *list = split(*out_STRING, ";");
            if(size(*list)==3) {
                    *pid = elem(*list,0);
                    *source = elem(*list,1);
                    *destination = elem(*list,2);
                    doReplication(*pid,*source,*destination,*status);       
            } else {
                    logError("incorrect list");
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

    	if(size(*list)==3) {
                *pidAction = elem(*list,0);

                if(*pidAction == "create") {
                    *pid = elem(*list,1);
                    *destination = elem(*list,2);

                    #manage pid in this repository 
                    createPID(*pid, *destination, *new_pid);
                    getSharedCollection(*destination,*collectionPath);    		
                    msiSplitPath(*destination, *parent, *child);
                    triggerUpdateParentPID("*collectionPath*child.pid.update", *pid, *new_pid);
                } else if(*pidAction=="update") {
                    updatePIDWithNewChild(elem(*list,1), elem(*list,2));
                }
    	} else {
    		logError("incorrect list");
    	}

#	updateCommandName(*cmdPath,*status); 	
}

#
# Start a replication
#
# Parameters:
#	*pid            [IN]    pid of the digital object
#	*source		[IN]    source path of the object to replicate
#	*destination	[IN]    destination path of the object to replicate
#       *status         [OUT]   status, 0 = ok, <0 = error
#
# Author: Willem Elbers, MPI-TLA
#
doReplication(*pid,*source,*destination,*status) {
        logInfo("doReplication(*pid,*source,*destination)");

        #rsync object (make sure to supply "null" if dest resource should be the default one) 
        msiDataObjRsync(*source, "IRODS_TO_IRODS", "null", *destination, *rsyncStatus);

        #trigger pid management in destination
        getSharedCollection(*destination,*collectionPath); 
        msiSplitPath(*destination, *parent, *child);
	triggerCreatePID("*collectionPath*child.pid.create",*pid,*destination);
	updateMonitor("*collectionPath*child.pid.update");
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
#
# Parameters:
#   *rorPID     [IN]    the PID of the repository of record (RoR), should be stored with all child PIDs
#   *path       [IN]    the path of the replica to store with the PID record
#   *newPID     [OUT]   the pid generated for this replica 
#
# Author: Willem Elbers, MPI-TLA
#
createPID(*rorPID, *path, *newPID) {
	logInfo("create pid for *path and save *rorPID as ror");

        getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *epicDebug);

        #check if PID already exists
        if(*epicDebug > 1) {
            logDebug("epicclient.py *credStoreType *credStorePath search URL *path");
        }
        msiExecCmd("epicclient.py", "*credStoreType *credStorePath search URL *path", "null", "null", "null", *out);
        msiGetStdoutInExecCmdOut(*out, *existing_pid);

        if(*existing_pid == "empty") {
            # create PID
            if(*epicDebug > 1) {
                logDebug("epicclient.py *credStoreType *credStorePath create *path");
            }
            msiExecCmd("epicclient.py", "*credStoreType *credStorePath create *path", "null", "null", "null", *out);
            msiGetStdoutInExecCmdOut(*out, *newPID);
            logDebug("created handle = *newPID");

            # add RoR to PID record
            if(*epicDebug > 1) {
                logDebug("epicclient.py *credStoreType *credStorePath modify *newPID ROR *epicApi*rorPID");
            }
            msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *newPID ROR *epicApi*rorPID", "null", "null", "null", *out2);
            msiGetStdoutInExecCmdOut(*out2, *response2);
            logDebug("modify handle response = *response2");

            # add CHECKSUM to PID record
            retrieveChecksum(*path, *checksum);
            if(*epicDebug > 1) {
                logDebug("epicclient.py *credStoreType *credStorePath modify *newPID CHECKSUM *checksum");
            }
            msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *newPID CHECKSUM *checksum", "null", "null", "null", *out3);
            msiGetStdoutInExecCmdOut(*out3, *response3);
            logDebug("modify handle response = *response3");
        } else {
            *newPID = *existing_pid;
            logInfo("PID already exists (*newPID)");
        }
}

#
# Update a PID record.
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

        getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *epicDebug);
        if(*epicDebug > 1) {
            logDebug("epicclient.py *credStoreType *credStorePath relation *parentPID *childPID");
        }
	msiExecCmd("epicclient.py","*credStoreType *credStorePath relation *parentPID *childPID", "null", "null", "null", *out);
        msiGetStdoutInExecCmdOut(*out, *response);
        logDebug("update handle location response = *response");
}
