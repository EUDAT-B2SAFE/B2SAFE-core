################################################################################
#                                                                              #
# Module Replication:                                                          #
#		- enable transfer single file                                  #   
#		- enable transfer collection                                   #
#		- enable transfer all files which have been logged             #
#                 from the last transfers                                      #
#                                                                              #
################################################################################

# List of the functions:
#
# updateLogging(*status_transfer_success, *path_of_transfered_file, 
#               *target_transfered_file, *cause)
# checkError(*path_of_transfered_file,*target_of_transfered_file)
# tranferSingleFile(*path_of_transfered_file,*target_of_transfered_file)
# transferUsingFailLog(*buffer_length)
# checkReplicas(*source, *destination)

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
        EUDATQueue("push", *message, 0);
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
		
    logInfo("query PID of DataObj *path_of_transfered_file");
    EUDATSearchPID(*path_of_transfered_file, *pid);

    if (*pid == "empty") {
        logInfo("PID is empty, no replication will be executed");		
        # Update Logging (Statistic File and Failed Files)
        *status_transfer_success = bool("false");
        updateLogging(*status_transfer_success,*path_of_transfered_file,
                      *target_of_transfered_file, "empty PID");				
    } else {
        logInfo("PID exist, Replication's beginning ...... ");
        getSharedCollection(*path_of_transfered_file,*sharedCollection);
        msiSplitPath(*path_of_transfered_file, *collection, *file);
        msiReplaceSlash(*target_of_transfered_file, *controlfilename);
        logInfo("ReplicateFile: *sharedCollection*controlfilename");	        
			
        # Catch Error CAT_NO_ACCESS_PERMISSION before replication
        catchErrorDataOwner(*path_of_transfered_file,*status_identity);
			
        if (*status_identity == bool("true")) {
            triggerReplication("*sharedCollection*controlfilename.replicate",*pid,
                                *path_of_transfered_file,*target_of_transfered_file);			
            logInfo("Perform the last checksum and checksize of transfered data object");		
	    checkError(*path_of_transfered_file,*target_of_transfered_file); 	 	    		
	} else {
	    logInfo("Action is canceled. Error is caught in function catchErrorDataOwner"); 
	    # Update fail_log				
	    *status_transfer_success = bool("false");
	    updateLogging(*status_transfer_success,*path_of_transfered_file,*target_of_transfered_file,
                          "no access permission");
	}			
    }		
}

#
# Transfer all data object saved in the logging system,
# according to the format: cause::path_of_transfer_file::target_of_transfer_file.
#
# Parameters:
#   *buffer_length    [IN] max number of failed transfer to process.
#                          It has to be > 1.
#
# Author: Long Phan, Juelich
# Modified by Claudio Cacciari, Cineca;
#
transferUsingFailLog(*buffer_length) {
	
    # get size of queue-log before transfer.    
    EUDATQueue("queuesize", *l, 0);
    EUDATQueue("pop", *messages, *buffer_length);
    
    *msg_list = split("*messages",",");	
    foreach (*message in *msg_list) {
        *message = triml(*message, "'");
        *message = trimr(*message, "'");
        *list = split("*message","::");

        *counter = 0;
        foreach (*item_LIST in *list) {
            if (*counter == 0) {*path_of_transfer_file = *item_LIST; }
            else if (*counter == 1) {*target_of_transfer_file = *item_LIST; }
            *counter = *counter + 1;
            if (*counter == 2) {break;}
        }
        tranferSingleFile(*path_of_transfer_file, *target_of_transfer_file);
    }

    # get size of queue-log after transfer. 
    EUDATQueue("queuesize", *la, 0);
    logInfo("AFTER TRANSFER: Length of Queue = *la");
    if (int(*l) == int(*la)) {
        logInfo("Transfer Data Objects got problems. No Data Objects have been transfered");
    } else {
        logInfo("There are *la Data Objects in Queue-log");
    }
	  
}

#
# Check whether two files are available and identical
# If they are not identical, do the following:
#    1. find the pid of the object and modify checksum in the pid or create a new pid
#    2. create pid in the iCAT if it does not exist
#    3. add/update ROR in iCAT
#    4. tregger replication from source to destination
#
# Parameters:
#   *source         [IN]     source of the file
#   *destination    [IN]     destination of the file
# Author: Elena Erastova, RZG
#
checkReplicas(*source, *destination) {
    logInfo("Check if 2 replicas have the same checksum. Source = *source, destination = *destination");
    if (catchErrorChecksum(*source, *destination) == bool("false") || 
        catchErrorSize(*source, *destination) == bool("false")) 
    {
        EUDATeiPIDeiChecksumMgmt(*source, *pid, bool("true"), bool("true"), 0);
        EUDATiRORupdate(*source, *pid);
        logInfo("replication from *source to *destination");
        getSharedCollection(*source,*collectionPath);
        msiReplaceSlash(*destination,*filepathslash);
        triggerReplication("*collectionPath*filepathslash.replicate",*pid,*source,*destination);
    }
}


####################################################################################
# Collection replication management                                                #
####################################################################################

# TODO: verify and consolidate the following functions
# 	  
#####################################################################################
#
# Transfer Collection
#
# Parameters:
#	*path_of_transfered_collection		[IN] path of transfered collection in iRODS	
#                                                    (ex. /COMMUNITY/DATA/Dir9/)
#	*target_of_transfered_collection	[IN] destination of replication in iRODS	
#                                                    (ex. /DATACENTER/DATA/)
# 
# Author: Long Phan, Juelich
#
#transferCollection(*path_of_transfered_collection,*target_of_transfered_collection){
#
#	msiStrlen(*path_of_transfered_collection,*path_originallength);
#	
#	# ----------------- Build Path for sourcePATH --------------
#	msiStrchop(*path_of_transfered_collection,*out);
#	msiStrlen(*out,*choplength);
#	*sourcePATH = "*out"; 
#	*SubCollection = "";
#	*listfiles = "";						
#			
#	# ----------------- Build condition for iCAT --------------- 
#	
#	*sPATH = "*sourcePATH" ++ "%"; 
#		
#	*Condition = "COLL_NAME like '*sPATH'";
#	*ContInxOld = 1;
#	*i = 0;
#		
#	msiSplitPath(*sourcePATH,*sourceParent,*sourceChild);
#	msiStrlen(*sourceParent,*pathLength);
#	
#	# ----------------------------------------------------------
#	msiMakeGenQuery("COLL_NAME,DATA_NAME",*Condition, *GenQInp);
#	msiExecGenQuery(*GenQInp, *GenQOut);
#	msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
#	while(*ContInxOld > 0) {
#		foreach(*GenQOut) {
#			msiGetValByKey(*GenQOut, "DATA_NAME", *Name);
#			msiGetValByKey(*GenQOut, "COLL_NAME", *Collection);
#			
#			# get length of *Collection
#			msiStrlen(*Collection,*lengthtemp);
#			# get SubCollection
#			msiSubstr(*Collection,"0","*path_originallength",*subcollname);
#			
#			# Compare to eliminate paths with similar Collection 
#			if (*subcollname == *path_of_transfered_collection || *choplength == *lengthtemp) {
#			
#			# --------------------  Get SubCollection. -#-------------------	
#          		*PATH = *Collection++"/"++*Name;	
#	                msiSubstr(*PATH,str(int(*pathLength)+1),"null",*SubCollection);		
#							
#			# ---------------- Save *SubCollection into *list -------------
#			*listfiles = "*listfiles" ++ "*SubCollection" ++ "\n";					
#			}					
#		}
#		
#		*ContInxOld = *ContInxNew;
#		
#		# get more rows in case data > 256 rows.
#		if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
#	}
#	
#	# get size of list (number of elements inside list)
#	*list = split(*listfiles,"\n");
#	*Start = size(*list);
#	logInfo("Size of list = *Start");		
#	
#	# loop on list to transfer data object one by one using transferSingleFile
#	while (*i < *Start) {
#			logInfo("------- Transfer *i of *Start ---------- ");	
#			*SubCollection = elem(*list,*i);
#			
#			*Source = "*sourceParent" ++ "/" ++ "*SubCollection"; 
#			*Destination = "*target_of_transfered_collection"++"*SubCollection"
#			
#			tranferSingleFile(*Source,*Destination); 
#			*i = *i + 1;
#	}
#	
#}


# Transfer Collection Stress Memory
# WARNING: 
# " ---->	This method could cause PROBLEM OUT OF MEMORY in irods 3.2 when transfer_data inside foreach-loop !!!	<-----  
# " ----> 	TODO: NEED TEST on both versions irods 3.2 and irods 3.3, also irods 3.3.1 								<-----  
#
# Parameters:
#	*path_of_transfered_collection		[IN] path of transfered collection in iRODS (ex. /COMMUNITY/DATA/Dir9/)
#	*target_of_transfered_collection	[IN] destination of replication in iRODS	(ex. /DATACENTER/DATA/)
#
# Author: Long Phan, Juelich
#
#transferCollectionStressMemory(*path_of_transfered_collection,*target_of_transfered_collection){
#	
#	msiStrlen(*path_of_transfered_collection,*path_originallength);
#		
#	# ----------------- Build Path for sourcePATH --------------
#	msiStrchop(*path_of_transfered_collection,*out);
#	msiStrlen(*out,*choplength);	
#	*sourcePATH = "*out"; 
#	*SubCollection = "";					
#			
#	# ----------------- Build condition for iCAT --------------- 
#	*sPATH = "*sourcePATH" ++ "%";
#	*Condition = "COLL_NAME like '*sPATH'";
#	*ContInxOld = 1;	
#		
#	msiSplitPath(*sourcePATH,*sourceParent,*sourceChild);
#	msiStrlen(*sourceParent,*pathLength);
#	
#	# ----------------------------------------------------------
#	msiMakeGenQuery("COLL_NAME,DATA_NAME",*Condition, *GenQInp);
#	msiExecGenQuery(*GenQInp, *GenQOut);
#	msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
#	while(*ContInxOld > 0) {
#		foreach(*GenQOut) {
#			msiGetValByKey(*GenQOut, "DATA_NAME", *Name);
#			msiGetValByKey(*GenQOut, "COLL_NAME", *Collection);
#			
#			# get length of *Collection
#			msiStrlen(*Collection,*lengthtemp);
#			# get SubCollection
#			msiSubstr(*Collection,"0","*path_originallength",*subcollname);
#			
#			# Compare to eliminate paths with similar Collection 
#			if (*subcollname == *path_of_transfered_collection || *choplength == *lengthtemp) {
#			
#					# --------------------  Get SubCollection. --------------------	
#					*PATH = *Collection++"/"++*Name;					
#					msiSubstr(*PATH,str(int(*pathLength)+1),"null",*SubCollection);
#					
#					# -------------------- Transfer Data Obj ----------------------
#					*Source = "*sourceParent" ++ "/" ++ "*SubCollection"; 
#					*Destination = "*target_of_transfered_collection"++"*SubCollection"
#					
#					tranferSingleFile(*Source,*Destination);		
#			}
#						
#		}
#		
#		*ContInxOld = *ContInxNew;
#		
#		# get more rows in case data > 256 rows.
#		if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
#	}
#			
#}


#
# Transfer all data objects at Parent_Collection without recursion on subCollection
#
# Parameters:
#	*path_of_transfered_collection		[IN] path of transfered collection in iRODS (ex. /COMMUNITY/DATA/Dir9/)
#	*target_of_transfered_collection	[IN] destination of replication in iRODS	(ex. /DATACENTER/DATA/)
#
# Author: Long Phan, Juelich
#
#transferCollectionWithoutRecursion(*path_of_transfered_collection,*target_of_transfered_collection) {
#		
#	# ----------------- Build Path for sourcePATH --------------
#	# Query only works without '/'
#	msiStrchop(*path_of_transfered_collection,*out);
#	msiStrlen(*out,*choplength);	
#	*sourcePATH = "*out"; 
#	*SubCollection = "";
#	
#	
#	# ----------------- Build condition for iCAT ---------------		
#	*Condition = "COLL_NAME = '*out'";
#	*ContInxOld = 1;	
#	
#	msiSplitPath(*sourcePATH,*sourceParent,*sourceChild);
#	msiStrlen(*sourceParent,*pathLength);
#	
#	# ----------------- Query and transfer ---------------------				
#	
#	msiMakeGenQuery("DATA_NAME",*Condition, *GenQInp);
#	msiExecGenQuery(*GenQInp, *GenQOut);
#	msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
#	while(*ContInxOld > 0) {
#		foreach(*GenQOut) {
#			msiGetValByKey(*GenQOut, "DATA_NAME", *Name);				
#
#			*PATH = "*path_of_transfered_collection"++"*Name";
#			msiSubstr(*PATH,str(int(*pathLength)+1),"null",*SubCollection);
#					
#			# -------------------- Transfer Data Obj ----------------------
#			*Source = "*sourceParent" ++ "/" ++ "*SubCollection"; 
#			*Destination = "*target_of_transfered_collection"++"*SubCollection";			
#								
#			tranferSingleFile(*Source,*Destination);
#		}
#		
#		*ContInxOld = *ContInxNew;		
#		# get more rows in case data > 256 rows.
#		if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
#	}
#}


#
# Transfer Collection exploits using AVU of iCAT (iRODS)
# ---> NOTICE: this function will create one file *Collection_transfer.log is saved in the same directory Collection_Log
#
# Parameters:
#	*path_of_transfered_collection		[IN] path of transfered collection in iRODS (ex. /COMMUNITY/DATA/Dir9/)
#	*target_of_transfered_collection	[IN] destination of replication in iRODS	(ex. /DATACENTER/DATA/)
#	*path_of_logfile					[IN] path of log file in iRODS (after transfer: with 'imeta ls -d *path_of_logfile' to check whether all files have been transfered)  
# 
# Author: Long Phan, Juelich
#
#transferCollectionAVU(*path_of_transfered_collection,*target_of_transfered_collection, *path_of_logfile){
#	
#	msiStrlen(*path_of_transfered_collection,*path_originallength);
#	
#	# ----------------- Build Path for sourcePATH --------------
#	msiStrchop(*path_of_transfered_collection,*out);
#	msiStrlen(*out,*choplength);	
#	*sourcePATH = "*out"; 
#	*SubCollection = "";					
#			
#	# ----------------- Build condition for iCAT --------------- 
#	*sPATH = "*sourcePATH" ++ "%";
#	*Condition = "COLL_NAME like '*sPATH'";
#	*ContInxOld = 1;	
#		
#	msiSplitPath(*sourcePATH,*sourceParent,*sourceChild);
#	msiStrlen(*sourceParent,*pathLength);
#	
#	# ----------------------------------------------------------
#	msiSplitPath(*path_of_logfile,*coll,*child);
#	
#	# Create new Log_File for transfer using AVU
#	*contents = "- Using imeta to get Information AVU defined in file (ex. imeta ls -d /tempZone/file.log) -";
#	writeFile(*path_of_logfile, *contents);		
#	
#	*Key = "Path_of_transfered_Files";
#	# Initiate Value for transfer.log = empty
#	createAVU(*Key,"empty",*path_of_logfile);	
#		
#	msiMakeGenQuery("COLL_NAME,DATA_NAME",*Condition, *GenQInp);
#	msiExecGenQuery(*GenQInp, *GenQOut);
#	msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
#	while(*ContInxOld > 0) {
#		foreach(*GenQOut) {
#			msiGetValByKey(*GenQOut, "DATA_NAME", *Name);
#			msiGetValByKey(*GenQOut, "COLL_NAME", *Collection);
#			
#			# get length of *Collection
#			msiStrlen(*Collection,*lengthtemp);
#			# get SubCollection
#			msiSubstr(*Collection,"0","*path_originallength",*subcollname);
#			
#			# Compare to eliminate paths with similar Collection 
#			if (*subcollname == *path_of_transfered_collection || *choplength == *lengthtemp) {
#					# ---------------- Get SubCollection. --------------------	
#					*PATH = *Collection++"/"++*Name;					
#					msiSubstr(*PATH,str(int(*pathLength)+1),"null",*SubCollection);
#					
#					# ---------------- Add SubCollection into Log_File -------		
#					*Value = "*SubCollection";
#					createAVU(*Key,*Value,*path_of_logfile);
#			}						
#		}
#		
#		*ContInxOld = *ContInxNew;
#		
#		# get more rows in case data > 256 rows.
#		if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
#	}
#			
#	# -------------------- Transfer Data Obj ----------------------
#		
#	# Query Value of *Key = "Path_of_failed_Files"		
#	*d = SELECT META_DATA_ATTR_VALUE WHERE DATA_NAME = '*child' AND COLL_NAME = '*coll' AND META_DATA_ATTR_NAME = '*Key';
#	foreach(*c in *d) {
#	        msiGetValByKey(*c, "META_DATA_ATTR_VALUE", *SubCollection);
#	        msiWriteRodsLog("EUDATiFieldVALUEretrieve -> *Key equal to= *SubCollection", *status);
#			if (*SubCollection != "empty") {
#				*Source = "*sourceParent" ++ "/" ++ "*SubCollection"; 
#				*Destination = "*target_of_transfered_collection"++"*SubCollection";	
#				tranferSingleFile(*Source,*Destination);
#				
#				# remove Key Value
#				*Str = *Key ++ "=" ++ "*SubCollection";						
#				msiString2KeyValPair(*Str,*Keyval);			
#				msiRemoveKeyValuePairsFromObj(*Keyval,*path_of_logfile,"-d");
#				writeLine("serverLog","Removed Value *SubCollection"); 
#			} 
#	}
#		    	
#}


#
# Show status of Collection (Size, count of data objects, collection owner, location, date) and save it  
# This function is optional and run independently to support observing status of replication
# Result will be saved into a file in iRODS *logStatisticFilePath
# 
# TODO additional feature: only data objects of User on Session ($userNameClient 
#      and $rodsZoneClient) at *path_of_collection will be recorded in case collection 
#      contains data of many people.
#
# Parameter:
# 	*path_of_collection		[IN]	Path of collection in iRODS (ex. /COMMUNITY/DATA)
#	*logStatisticFilePath	[IN]	Path of statistic file in iRODS
#
# Author: Long Phan, Juelich
#
#getStatCollection(*path_of_collection, *logStatisticFilePath) {
#
#		# --- create optional content of logfile for collection ---
#		*contents = "------------- Log Information of Collection *path_of_collection --------------- \n";
#		msiGetCollectionACL(*path_of_collection,"",*Buf);		
#		*contents = *contents ++ "Collection Owner: \n*Buf \n";
#		
#		msiExecStrCondQuery("SELECT RESC_LOC, RESC_NAME WHERE COLL_NAME = '*path_of_collection'" ,*BS);
#		foreach   ( *BS )    {
#	        msiGetValByKey(*BS,"RESC_LOC", *resc_loc);
#	        msiGetValByKey(*BS,"RESC_NAME", *resc_name);
#	    }
#		*contents = *contents ++ "Resource Name: *resc_name\nResource Location: *resc_loc \n";
#		
#		msiGetSystemTime(*time,"human");		
#		*contents = *contents ++ "Date.Time: *time \n\n";
#				
#		msiSplitPath(*logStatisticFilePath, *coll, *name);
#						
#		# --- record *contents of collection and all sub_collection from *path_of_collection ---
#			*wildcard = "%";
#			
#			# loop on collection
#			*ContInxOld = 1;
#			# Path:
#			*COLLPATH = "*path_of_collection"++"*wildcard";
#			*Condition = "COLL_NAME like '*COLLPATH'";
#				
#			*sum = 0;
#			*count = 0;
#			msiStrlen(*path_of_collection,*originallength);
#			*comparelink = *path_of_collection ++ "/";
#			msiStrlen(*comparelink,*pathlength);
#			
#			msiMakeGenQuery("COLL_NAME,count(DATA_NAME), sum(DATA_SIZE)",*Condition, *GenQInp);
#			msiExecGenQuery(*GenQInp, *GenQOut);
#			msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
#			
#			while(*ContInxOld > 0) {
#				foreach(*GenQOut) {			
#					msiGetValByKey(*GenQOut, "COLL_NAME", *collname);			
#					msiGetValByKey(*GenQOut, "DATA_NAME", *dc);
#					msiGetValByKey(*GenQOut, "DATA_SIZE", *ds);
#										
#					msiStrlen(*collname,*lengthtemp);
#					# msiSubString of *collname and compare with *path_of_collection	
#					msiSubstr(*collname,"0","*pathlength",*subcollname);
#					
#					if (*subcollname == *comparelink || *originallength == *lengthtemp) {
#						*contents = "*contents" ++ "*collname count = *dc, sum = *ds\n";
#						*count = *count + double(*dc);
#						*sum = *sum + double(*ds);
#					}		
#					
#				}
#				
#				*ContInxOld = *ContInxNew;
#				# get more rows in case data > 256 rows.
#				if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
#			}
#				
#		#writeLine("stdout","In *logStatisticFilePath \n--Number of files: *count\n"++"Capacity:*sum \n");
#				
#		*contents = *contents ++ "\nIn *logStatisticFilePath \n--Number of files: *count\n"++"-- Capacity: *sum \n";
# #-----------------------------------------------------------------------------------------------											
#		writeLine("stdout","*contents");
#		writeFile(*logStatisticFilePath, *contents);
#								
#}
