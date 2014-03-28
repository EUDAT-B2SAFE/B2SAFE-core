# Module Replication: 
#		- enable transfer single file
#		- enable transfer collection
#		- enable transfer all files which have been logged in AVU (failFiles.log)from the last transfers
#

#
# Update Logging Files
# 
# Parameters:
#	*status_transfer_success	[IN] Status of transfered file (true or false)	 
#	*path_of_transfered_file	[IN] path of transfered file in iRODS
#   *target_transfered_file     [IN] path of the destination file in iRODS
#   *cause                      [IN] cause of the failed transfer
#
# Author: Long Phan, Juelich
# Modified by Claudio Cacciari, Cineca
#
updateLogging(*status_transfer_success, *path_of_transfered_file, 
              *target_transfered_file, *cause) {

    # Update Logging Statistical File
    *level = "INFO";
    *message = "*path_of_transfered_file::*target_transfered_file::" ++
               "*status_transfer_success::*cause";
    if (*status_transfer_success == bool("false")) {
        EUDATQueue("push", *message);
        *level = "ERROR";
    }
    EUDATLog(*message, *level);
}

#
# Check Error of Checksum and Size during transfer
# 
# Parameters:
#	*path_of_transfered_file	[IN] path of transfered file in iRODS
#	*target_of_transfered_file	[IN] destination of replication in iRODS
#
# Author: Long Phan, Juelich
# Modified by Claudio Cacciari, Cineca
#
checkError(*path_of_transfered_file,*target_of_transfered_file) {
	
    *status_transfer_success = bool("true");
    *cause = "";
    if (catchErrorChecksum(*path_of_transfered_file,*target_of_transfered_file) == bool("false")) {
        *cause = "different checksum";
        *status_transfer_success = bool("false");
    } else if (catchErrorSize(*path_of_transfered_file,*target_of_transfered_file) == bool("false")) {
        *cause = "different size";
		*status_transfer_success = bool("false");
	} 
	if (*status_transfer_success == bool("false")) {
        logInfo("replication from *path_of_transfered_file to *target_of_transfered_file failed: *cause");
    } else {
        logInfo("replication from *path_of_transfered_file to *target_of_transfered_file succeeded");
    }

    updateLogging(*status_transfer_success,*path_of_transfered_file,
                  *target_of_transfered_file, *cause);
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
    	#writeLine("serverLog",size(*list));
    	*s = size(*list) - 1;
    	#writeLine("serverLog",elem(*list,*s));
    	*n = elem(*list,*s)    	
    	*Collection_Name = "*n";
    	
}
 
#
# Transfer single file
#
# Parameters:
#	*path_of_transfered_file	[IN] path of transfered file in iRODS
#	*target_of_transfered_file	[IN] destination of replication in iRODS
# 
# Author: Long Phan, Juelich
# Modified by Claudio Cacciari, Cineca
#
tranferSingleFile(*path_of_transfered_file,*target_of_transfered_file) {
	
    # ----------  Transfer Data using EUDAT-Module triggerReplication(...) ---------------
		
    writeLine("serverLog","query PID of DataObj *path_of_transfered_file");
    searchPID(*path_of_transfered_file, *pid)

    if (*pid == "empty") {
        writeLine("serverLog","PID is empty, no replication will be executed");
			
        # Update Logging (Statistic File and Failed Files)
        *status_transfer_success = bool("false");
        updateLogging(*status_transfer_success,*path_of_transfered_file,
                      *target_of_transfered_file, "empty PID");				
    } else {
        writeLine("serverLog","PID exist, Replication's beginning ...... ");
        getSharedCollection(*path_of_transfered_file,*sharedCollection);
        msiSplitPath(*path_of_transfered_file, *collection, *file);
        msiReplaceSlash(*target_of_transfered_file, *controlfilename);
        writeLine("serverLog","ReplicateFile: *sharedCollection*controlfilename");	        
			
        # Catch Error CAT_NO_ACCESS_PERMISSION before replication
        catchErrorDataOwner(*path_of_transfered_file,*status_identity);
			
        if (*status_identity == bool("true")) {
            triggerReplication("*sharedCollection*controlfilename.replicate",*pid,
                                *path_of_transfered_file,*target_of_transfered_file);			
            writeLine("serverLog","Perform the last checksum and checksize of transfered data object");		
	    checkError(*path_of_transfered_file,*target_of_transfered_file);	
	} else {
	    writeLine("serverLog","Action is canceled. Error is caught in function catchErrorDataOwner"); 
	    # Update fail_log				
	    *status_transfer_success = bool("false");
	    updateLogging(*status_transfer_success,*path_of_transfered_file,
                          *target_of_transfered_file, "no access permission");
	}			
    }		
}

#
# Transfer all data object saved in the logging system,
# according to the format: cause::path_of_transfer_file::target_of_transfer_file.
# It can potentially be a never-ending loop.
#
#TODO: add an escape clause based on the "cause" of the failure.
#      If the original cause has not been fixed then skip the transfer.
#
# Author: Long Phan, Juelich
# Modified by Claudio Cacciari, Cineca
#
transferUsingFailLog() {
	
    *message = "";
    EUDATQueue("pop", *message);
    logInfo("looking for failed transfer: *message");
    while (*message != "None") {
        *list = split("*message","::");
        *path_of_transfer_file = elem(*list,0);
        *target_of_transfer_file = elem(*list,1);
 	tranferSingleFile(*path_of_transfer_file, *target_of_transfer_file);
        EUDATQueue("pop", *message);
    }		    
}


####################################################################################
# Collection replication management                                                #
####################################################################################

#TODO All the following functions need to be reviewed according 
#     to the new logging mechanism

#
# Transfer Collection
#
# Parameters:
#	*path_of_transfered_collection		[IN] path of transfered collection in iRODS
#	*target_of_transfered_collection	[IN] destination of replication in iRODS
# 
# Author: Long Phan, Juelich
#
transferCollection(*path_of_transfered_collection,*target_of_transfered_collection){
		
	msiStrlen(*path_of_transfered_collection,*path_originallength);
	
	# ----------------- Build Path for sourcePATH --------------
	msiStrchop(*path_of_transfered_collection,*out);
	msiStrlen(*out,*choplength);
	*sourcePATH = "*out"; 
	*SubCollection = "";
	*listfiles = "";						
			
	# ----------------- Build condition for iCAT --------------- 
	
	*sPATH = "*sourcePATH" ++ "%"; 
		
	*Condition = "COLL_NAME like '*sPATH'";
	*ContInxOld = 1;
	*i = 0;
		
	msiSplitPath(*sourcePATH,*sourceParent,*sourceChild);
	msiStrlen(*sourceParent,*pathLength);
	
	# ----------------------------------------------------------
	msiMakeGenQuery("COLL_NAME,DATA_NAME",*Condition, *GenQInp);
	msiExecGenQuery(*GenQInp, *GenQOut);
	msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
	while(*ContInxOld > 0) {
		foreach(*GenQOut) {
			msiGetValByKey(*GenQOut, "DATA_NAME", *Name);
			msiGetValByKey(*GenQOut, "COLL_NAME", *Collection);
			
			# get length of *Collection
			msiStrlen(*Collection,*lengthtemp);
			# get SubCollection
			msiSubstr(*Collection,"0","*path_originallength",*subcollname);
			
			# Compare to eliminate paths with similar Collection 
			if (*subcollname == *path_of_transfered_collection || *choplength == *lengthtemp) {
			
					# --------------------  Get SubCollection. --------------------			
					*PATH = *Collection++"/"++*Name;										
					msiSubstr(*PATH,str(int(*pathLength)+1),"null",*SubCollection);							
							
					# ---------------- Save *SubCollection into *list -------------
					*listfiles = "*listfiles" ++ "*SubCollection" ++ "\n";					
			}					
		}
		
		*ContInxOld = *ContInxNew;
		
		# get more rows in case data > 256 rows.
		if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
	}
	
	# get size of list (number of elements inside list)
	*list = split(*listfiles,"\n");
	*Start = size(*list);
	logInfo("Size of list = *Start");		
	
	# loop on list to transfer data object one by one using transferSingleFile
	while (*i < *Start) {
			logInfo("------- Transfer *i of *Start ---------- ");	
			*SubCollection = elem(*list,*i);
			
			*Source = "*sourceParent" ++ "/" ++ "*SubCollection"; 
			*Destination = "*target_of_transfered_collection"++"*SubCollection"
			
			tranferSingleFile(*Source,*Destination); 
			*i = *i + 1;
	}
	
}

#
# Transfer Collection Stress Memory
# WARNING: 
# " ---->	This method could cause PROBLEM OUT OF MEMORY in irods 3.2 when transfer_data inside foreach-loop !!!	<-----  
# " ----> 	TODO: NEED TEST on both versions irods 3.2 and irods 3.3, also irods 3.3.1 								<-----  
#
# Parameters:
#	*path_of_transfered_collection		[IN] path of transfered collection in iRODS
#	*target_of_transfered_collection	[IN] destination of replication in iRODS
# 
# Author: Long Phan, Juelich
#
transferCollectionStressMemory(*path_of_transfered_collection,*target_of_transfered_collection){
	
	msiStrlen(*path_of_transfered_collection,*path_originallength);
		
	# ----------------- Build Path for sourcePATH --------------
	msiStrchop(*path_of_transfered_collection,*out);
	msiStrlen(*out,*choplength);	
	*sourcePATH = "*out"; 
	*SubCollection = "";					
			
	# ----------------- Build condition for iCAT --------------- 
	*sPATH = "*sourcePATH" ++ "%";
	*Condition = "COLL_NAME like '*sPATH'";
	*ContInxOld = 1;	
		
	msiSplitPath(*sourcePATH,*sourceParent,*sourceChild);
	msiStrlen(*sourceParent,*pathLength);
	
	# ----------------------------------------------------------
	msiMakeGenQuery("COLL_NAME,DATA_NAME",*Condition, *GenQInp);
	msiExecGenQuery(*GenQInp, *GenQOut);
	msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
	while(*ContInxOld > 0) {
		foreach(*GenQOut) {
			msiGetValByKey(*GenQOut, "DATA_NAME", *Name);
			msiGetValByKey(*GenQOut, "COLL_NAME", *Collection);
			
			# get length of *Collection
			msiStrlen(*Collection,*lengthtemp);
			# get SubCollection
			msiSubstr(*Collection,"0","*path_originallength",*subcollname);
			
			# Compare to eliminate paths with similar Collection 
			if (*subcollname == *path_of_transfered_collection || *choplength == *lengthtemp) {
			
					# --------------------  Get SubCollection. --------------------			
					*PATH = *Collection++"/"++*Name;										
					msiSubstr(*PATH,str(int(*pathLength)+1),"null",*SubCollection);
					
					# -------------------- Transfer Data Obj ----------------------
					*Source = "*sourceParent" ++ "/" ++ "*SubCollection"; 
					*Destination = "*target_of_transfered_collection"++"*SubCollection"
					
					tranferSingleFile(*Source,*Destination);		
			}
						
		}
		
		*ContInxOld = *ContInxNew;
		
		# get more rows in case data > 256 rows.
		if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
	}
			
}

#
# Transfer Collection exploits using AVU 
# ---> NOTICE: this function will create one file *Collection_transfer.log is saved in the same directory Collection_Log
#
# Parameters:
#	*path_of_transfered_collection		[IN] path of transfered collection in iRODS
#	*target_of_transfered_collection	[IN] destination of replication in iRODS
# 
# Author: Long Phan, Juelich
#
transferCollectionAVU(*path_of_transfered_collection,*target_of_transfered_collection){
	
	msiStrlen(*path_of_transfered_collection,*path_originallength);
	
	# ----------------- Build Path for sourcePATH --------------
	msiStrchop(*path_of_transfered_collection,*out);
	msiStrlen(*out,*choplength);	
	*sourcePATH = "*out"; 
	*SubCollection = "";					
			
	# ----------------- Build condition for iCAT --------------- 
	*sPATH = "*sourcePATH" ++ "%";
	*Condition = "COLL_NAME like '*sPATH'";
	*ContInxOld = 1;	
		
	msiSplitPath(*sourcePATH,*sourceParent,*sourceChild);
	msiStrlen(*sourceParent,*pathLength);
	
	# ----------------------------------------------------------
	setLogFiles(*logStatisticFilePath,*logFailedFilePath, *ReplFr, *ReplTo);
	msiSplitPath(*logStatisticFilePath,*coll,*child);
	
	# Create new Log_File for transfer using AVU
	*contents = "------------- Using imeta to get Information AVU defined in file (ex. imeta ls -d /tempZone/file.log) --------------- ";
	
	# Create Name for log file
	getCollectionName(*path_of_transfered_collection,*Collection_Name);
	*logname = "*Collection_Name"++"_"++"transfer.log";
	
	*path_of_logfile = "*coll" ++ "/" ++ "*logname";		
	writeFile(*path_of_logfile, *contents);		
	
	*Key = "Path_of_transfered_Files";
	# Initiate Value for transfer.log = empty
	createAVU(*Key,"empty",*path_of_logfile);	
		
	msiMakeGenQuery("COLL_NAME,DATA_NAME",*Condition, *GenQInp);
	msiExecGenQuery(*GenQInp, *GenQOut);
	msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
	while(*ContInxOld > 0) {
		foreach(*GenQOut) {
			msiGetValByKey(*GenQOut, "DATA_NAME", *Name);
			msiGetValByKey(*GenQOut, "COLL_NAME", *Collection);
			
			# get length of *Collection
			msiStrlen(*Collection,*lengthtemp);
			# get SubCollection
			msiSubstr(*Collection,"0","*path_originallength",*subcollname);
			
			# Compare to eliminate paths with similar Collection 
			if (*subcollname == *path_of_transfered_collection || *choplength == *lengthtemp) {
					# ---------------- Get SubCollection. --------------------			
					*PATH = *Collection++"/"++*Name;										
					msiSubstr(*PATH,str(int(*pathLength)+1),"null",*SubCollection);
					
					# ---------------- Add SubCollection into Log_File -------					
					*Value = "*SubCollection";
					createAVU(*Key,*Value,*path_of_logfile);
			}
						
		}
		
		*ContInxOld = *ContInxNew;
		
		# get more rows in case data > 256 rows.
		if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
	}
			
	# -------------------- Transfer Data Obj ----------------------
		
	# Query Value of *Key = "Path_of_failed_Files"		
	*d = SELECT META_DATA_ATTR_VALUE WHERE DATA_NAME = '*logname' AND COLL_NAME = '*coll' AND META_DATA_ATTR_NAME = '*Key';
	foreach(*c in *d) {
	        msiGetValByKey(*c, "META_DATA_ATTR_VALUE", *SubCollection);
	        msiWriteRodsLog("EUDATiFieldVALUEretrieve -> *Key equal to= *SubCollection", *status);
			 if (*SubCollection != "empty") {
				*Source = "*sourceParent" ++ "/" ++ "*SubCollection"; 
				*Destination = "*target_of_transfered_collection"++"*SubCollection";			
				tranferSingleFile(*Source,*Destination);
				
				# remove Key Value
				*Str = *Key ++ "=" ++ "*SubCollection";						
				msiString2KeyValPair(*Str,*Keyval);			
				msiRemoveKeyValuePairsFromObj(*Keyval,*path_of_logfile,"-d");
				writeLine("serverLog","Removed Value *SubCollection"); 
			} 
	}
		    	
}

#
# Transfer all data objects at Parent_Collection without recursion on subCollection
#
# Parameters:
#	*path_of_transfered_collection		[IN] path of transfered collection in iRODS
#	*target_of_transfered_collection	[IN] destination of replication in iRODS
# 
# Author: Long Phan, Juelich
#
transferCollectionWithoutRecursion(*path_of_transfered_collection,*target_of_transfered_collection) {
		
	# ----------------- Build Path for sourcePATH --------------
	# Query only works without '/'
	msiStrchop(*path_of_transfered_collection,*out);
	msiStrlen(*out,*choplength);	
	*sourcePATH = "*out"; 
	*SubCollection = "";
	
	
	# ----------------- Build condition for iCAT ---------------		
	*Condition = "COLL_NAME = '*out'";
	*ContInxOld = 1;	
	
	msiSplitPath(*sourcePATH,*sourceParent,*sourceChild);
	msiStrlen(*sourceParent,*pathLength);
	
	# ----------------- Query and transfer ---------------------				
	
	msiMakeGenQuery("DATA_NAME",*Condition, *GenQInp);
	msiExecGenQuery(*GenQInp, *GenQOut);
	msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
	while(*ContInxOld > 0) {
		foreach(*GenQOut) {
			msiGetValByKey(*GenQOut, "DATA_NAME", *Name);				

			*PATH = "*path_of_transfered_collection"++"*Name";										
			msiSubstr(*PATH,str(int(*pathLength)+1),"null",*SubCollection);
					
			# -------------------- Transfer Data Obj ----------------------
			*Source = "*sourceParent" ++ "/" ++ "*SubCollection"; 
			*Destination = "*target_of_transfered_collection"++"*SubCollection";				
								
			tranferSingleFile(*Source,*Destination);									
		}
		
		*ContInxOld = *ContInxNew;		
		# get more rows in case data > 256 rows.
		if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
	}
}
