# Module: Catch all possible errors during data transfer related with
#		- PID
#		- checksum
#		- size
#		- error_code
#

#
# Catch error with Checksum (edited from function checkReplicas in eudat.re)
#
# Parameters:
#	*source         [IN] path source of data object
#	*destination	[IN] path destination of replicated data object
# 
# Author: Long Phan, JSC
#
EUDATCatchErrorChecksum(*source,*destination){
    logInfo("[EUDATCatchErrorChecksum] Check if 2 replicas have the same checksum. " ++
            "Source = *source, destination = *destination");

    *b = bool("true");
    *checksum0 = "";
    msiSplitPath(*source,*parentS,*childS);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parentS' AND DATA_NAME = '*childS'" ,*BS);
    foreach ( *BS ) {
        msiGetValByKey(*BS,"DATA_CHECKSUM", *checksum0);
        logDebug("checksum0 = *checksum0");
    }

    *checksum1 = "";
    msiSplitPath(*destination,*parentD,*childD);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parentD' AND DATA_NAME = '*childD'" ,*BD);
    foreach ( *BD ) {
        msiGetValByKey(*BD,"DATA_CHECKSUM", *checksum1);
        logDebug("checksum1 = *checksum1");
    }

    if(*checksum0 != *checksum1) {
        EUDATSearchPID(*source, *pid);
        logDebug("*checksum0 != *checksum1, existing_pid = *pid");
        *b = bool("false"); 
    } 
    *b;
    
}

#
# Catch error Size of file
#
# Parameters:
#	*source		[IN] path source of data object
#	*destination	[IN] path destination of replicated data object
#  
# Author: Long Phan, JSC
#
EUDATCatchErrorSize(*source,*destination) {
    logInfo("[EUDATCatchErrorSize] Check if 2 replicas have the same size." ++
            "Source = *source, destination = *destination");

    *b = bool("true"); 	
    *size0 = "";
    msiSplitPath(*source,*parentS,*childS);
    msiExecStrCondQuery("SELECT DATA_SIZE WHERE COLL_NAME = '*parentS' AND DATA_NAME = '*childS'" ,*BS);
    foreach   ( *BS )    {
        msiGetValByKey(*BS,"DATA_SIZE", *size0);
        logDebug("Size *source = *size0");
    }

    *size1 = "";
    msiSplitPath(*destination,*parentD,*childD);
    msiExecStrCondQuery("SELECT DATA_SIZE WHERE COLL_NAME = '*parentD' AND DATA_NAME = '*childD'" ,*BD);
    foreach   ( *BD )    {
        msiGetValByKey(*BD,"DATA_SIZE", *size1);
        logDebug("Size *destination = *size1");
    }

    if(*size0 != *size1) {
        EUDATSearchPID(*source, *pid);
        logDebug("*size0 != *size1, existing_pid = *pid");
        *b = bool("false"); 
    } 
    *b;
    
}


#
# Process error update PID at Parent_PID. Error update PID will be processed during replication_workflow, called by updateMonitor
# Save path of transferred data object into fail_log
# ----> add line "processErrorUpdatePID(*file) inside function updateMonitor in eudat.re below logInfo("*file does not exist yet"); to save path of wrong_updated_DataObject 
#
# TODO: Need Test
# TODO: to be updated with the new logging mechanism
#
# Author: Long Phan, JSC; Elena Erastova, RZG
#
EUDATProcessErrorUpdatePID(*updfile) {
		
    *status_transfer_success = bool("false");
    
    # Compose a name of a .replicate.time.sucess file in the local zone
    *list3 = split(*updfile, "/");
    *updfile1 = elem(*list3,2);
    *list = split(*updfile1, ".");
    *counter = 0;
    foreach (*item_LIST in *list) {
        *counter = *counter + 1;
    }
    *size = *counter;
    *counter = 0;
    *repfile = elem(*list,0);
    foreach (*item_LIST in *list) {
        if ((*counter != 0) && (*counter != (*size - 1)) && (*counter != (*size - 2))) {
            *repfile = "*repfile.*item_LIST";
        }
        *counter = *counter + 1;
    }
    *repfile=*repfile++".replicate";
    *list1 = split(*updfile, "_");
    *l2 = elem(*list1,0);
    *list2 = split(*l2, "/");
    *remoteZoneName = "/"++elem(*list2,0)++"/replicate";

    # Check if the remote zone is available
    if (errorcode(msiObjStat(*remoteZoneName,*out)) != 0) {
            logDebug("[EUDATProcessErrorUpdatePID] remote zone *remoteZoneName is not available");
    }
    else {
        # Look for a .replicate.time.sucess file in the local zone
        *coll = "/"++$rodsZoneProxy++"/replicate";
        msiExecStrCondQuery("SELECT DATA_NAME WHERE COLL_NAME like '*coll' AND DATA_NAME like '*repfile%'" ,*BS);
        foreach ( *BS ) {
            msiGetValByKey(*BS,"DATA_NAME", *dataName);
        }
        *d = SELECT count(DATA_NAME) WHERE COLL_NAME like '*coll' AND DATA_NAME like '*repfile%success';
        foreach(*c in *d) {
            msiGetValByKey(*c,"DATA_NAME",*num);
        }

        if(*num == "0") {
            *d = SELECT count(DATA_NAME) WHERE COLL_NAME like '*coll' AND DATA_NAME like '*repfile';
            foreach(*c in *d) {
                msiGetValByKey(*c,"DATA_NAME",*num);
            }
            if(*num == "0") {
                logDebug("[EUDATProcessErrorUpdatePID] replication went wrong, no .replicate file exists");
            }
            else if(*num == "1") {
                *cause = "replication went wrong but file *dataName exists";
                readReplicationCommandFile(*coll++"/"++*dataName, *pid,*path_of_transfered_file, 
                                           *target_transfered_file, *ror);
                updateLogging(*status_transfer_success,*path_of_transfered_file,*target_transfered_file,*cause);
            }
        }
        else if(*num == "1") {
            *cause = "replication went ok: file *dataName exists but *updfile does not exist";
            *openFile = *coll++"/"++*dataName;
            readReplicationCommandFile(*openFile,*pid,*path_of_transfered_file,*target_transfered_file,*ror);
            *status_transfer_success = bool("true");
            updateLogging(*status_transfer_success,*path_of_transfered_file,*target_transfered_file,*cause);
        }
    }
}

#
# Catch error Data Owner if user is not owner of Data from *path
# (Reference: https://www.irods.org/index.php/iRODS_Error_Codes or /iRODS/lib/core/include/rodsErrorTable.h)
#
# Parameters:
#	*path			[IN] path source of data object
#	*status			[OUT] status of data object ('true' = DATA OWNER or false = NO ACCESS PERMISSION)
#
# Author: Long Phan, JSC
#
EUDATCatchErrorDataOwner(*path,*status){
    *status = bool("true");
		
    # CAT_NO_ACCESS_PERMISSION	    
    msiCheckAccess(*path,"own",*Result);								    									    
    if (*Result == 0) {
        logInfo("++++++++++++++++++ WARNING: Error CAT_NO_ACCESS_PERMISSION ");
    	*status = bool("false");
    } else {
    	logInfo("Identity of user is confirmed! ");
    }    	
}

#
# Catch error if user_on_session is trying to transfer data from one Collection where access right is not allowed.
# This function is used for transferCollection
#
# TODO: ...
#
#catchErrorCollectionOwner(*path_of_transfered_collection) {
#
#}
