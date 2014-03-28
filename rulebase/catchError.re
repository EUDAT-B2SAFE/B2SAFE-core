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
#	*source			[IN] path source of data object
#	*destination	[IN] path destination of replicated data object
# 
# Author: Long Phan, Juelich
#
catchErrorChecksum(*source,*destination){
	logInfo("Check if 2 replicas have the same checksum. Source = *source, destination = *destination");

	*b = bool("true");
 	*checksum0 = "";
    msiSplitPath(*source,*parentS,*childS);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parentS' AND DATA_NAME = '*childS'" ,*BS);
    foreach ( *BS ) {
        msiGetValByKey(*BS,"DATA_CHECKSUM", *checksum0);
        logInfo("checksum0 = *checksum0");
    }

    *checksum1 = "";
    msiSplitPath(*destination,*parentD,*childD);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parentD' AND DATA_NAME = '*childD'" ,*BD);
    foreach ( *BD ) {
        msiGetValByKey(*BD,"DATA_CHECKSUM", *checksum1);
        logInfo("checksum1 = *checksum1");
    }

    if(*checksum0 != *checksum1) {
        searchPID(*source, *pid);
        logInfo("*checksum0 != *checksum1, existing_pid = *pid");
        logInfo("replication from *source to *destination");
        *b = bool("false"); 
    } 
    *b;
    
}

#
# Catch error Size of file
#
# Parameters:
#	*source			[IN] path source of data object
#	*destination	[IN] path destination of replicated data object
#  
# Author: Long Phan, Juelich
#
catchErrorSize(*source,*destination) {
	logInfo("Check if 2 replicas have the same size. Source = *source, destination = *destination");

	*b = bool("true"); 	
    msiSplitPath(*source,*parentS,*childS);
    msiExecStrCondQuery("SELECT DATA_SIZE WHERE COLL_NAME = '*parentS' AND DATA_NAME = '*childS'" ,*BS);
    foreach   ( *BS )    {
        msiGetValByKey(*BS,"DATA_SIZE", *size0);
        logInfo("Size *source = *size0");
    }

    msiSplitPath(*destination,*parentD,*childD);
    msiExecStrCondQuery("SELECT DATA_SIZE WHERE COLL_NAME = '*parentD' AND DATA_NAME = '*childD'" ,*BD);
    foreach   ( *BD )    {
        msiGetValByKey(*BD,"DATA_SIZE", *size1);
        logInfo("Size *destination = *size1");
    }

    if(*size0 != *size1) {
        searchPID(*source, *pid);
        logInfo("*size0 != *size1, existing_pid = *pid");
        logInfo("replication from *source to *destination");
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
# Author: Long Phan, Juelich
#
processErrorUpdatePID(*path_of_transfered_file) {
		
	setLogFiles(*logStatisticFilePath,*logFailedFilePath, *ReplFr, *ReplTo);
	
	logInfo("Error update PID at *path_of_transfered_file failed, logged in ICAT at *logFailedFilePath");
	*status_transfer_success = bool("false");
	updateLogging(*status_transfer_success,*path_of_transfered_file);
		
	# Check the existence of file .replicate.$ftime.success at /replicate/ with 
	# EUDATfileInPath(*logStatisticFilePath,*collection)
}

#
# Catch error Data Owner if user is not owner of Data from *path
# (Reference: https://www.irods.org/index.php/iRODS_Error_Codes or /iRODS/lib/core/include/rodsErrorTable.h)
#
# Author: Long Phan, Juelich
#
catchErrorDataOwner(*path,*status){
    *status = bool("true");
		
    # CAT_NO_ACCESS_PERMISSION	    
    msiCheckAccess(*path,"own",*Result);								    									    
    if (*Result == 0) {
        writeLine("serverLog","++++++++++++++++++ WARNING: Error CAT_NO_ACCESS_PERMISSION ");
    	*status = bool("false");
    } else {
    	writeLine("serverLog","Identity of user is confirmed! ");
    }    	
}

#
# Catch error if user_on_session is trying to transfer data from one Collection where access right is not allowed.
# This function is used for transferCollection
#
# TODO: ...
#
catchErrorCollectionOwner(*path_of_transfered_collection) {

}
