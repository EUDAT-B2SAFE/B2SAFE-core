################################################################################
#                                                                              #
# Module Replication:                                                          #
#        - enable transfer single file                                  #   
#        - enable transfer collection                                   #
#        - enable transfer all files which have been logged             #
#                 from the last transfers                                      #
#                                                                              #
################################################################################

# List of the functions:
#
# EUDATUpdateLogging(*status_transfer_success, *path_of_transfered_file, 
#               *target_transfered_file, *cause)
# EUDATCheckError(*path_of_transfered_file,*target_of_transfered_file)
# EUDATTranferSingleFile(*path_of_transfered_file,*target_of_transfered_file)
# EUDATTransferUsingFailLog(*buffer_length)
# EUDATCheckReplicas(*source, *destination)
#---- collection management ---
# EUDATTransferCollection(*path_of_transfered_collection,*target_of_transfered_collection)

#
# Update Logging Files
# 
# Parameters:
#    *status_transfer_success    [IN] Status of transfered file (true or false)     
#    *path_of_transfered_file    [IN] path of transfered file in iRODS
#   *target_transfered_file     [IN] path of the destination file in iRODS
#   *cause                      [IN] cause of the failed transfer
#
# Author: Long Phan, Juelich
# Modified by Claudio Cacciari, Cineca
#
EUDATUpdateLogging(*status_transfer_success, *path_of_transfered_file, 
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
#    *path_of_transfered_file    [IN] path of transfered file in iRODS
#    *target_of_transfered_file    [IN] destination of replication in iRODS
#
# Author: Long Phan, Juelich
# Modified by Claudio Cacciari, Cineca
#
EUDATCheckError(*path_of_transfered_file,*target_of_transfered_file) {
    
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

    EUDATUpdateLogging(*status_transfer_success,*path_of_transfered_file,
                  *target_of_transfered_file, *cause);
}

#
# Transfer single file
#
# Parameters:
#    *path_of_transfered_file    [IN] path of transfered file in iRODS
#    *target_of_transfered_file  [IN] destination of replication in iRODS
# 
# Author: Long Phan, Juelich
# Modified by Claudio Cacciari, Cineca
#
EUDATTranferSingleFile(*path_of_transfered_file,*target_of_transfered_file) {
    
    # ----------  Transfer Data using EUDAT-Module triggerReplication(...) ---------------
        
    logInfo("query PID of DataObj *path_of_transfered_file");
    EUDATSearchPID(*path_of_transfered_file, *pid);

    if (*pid == "empty") {
        logInfo("PID is empty, no replication will be executed");        
        # Update Logging (Statistic File and Failed Files)
        *status_transfer_success = bool("false");
        EUDATUpdateLogging(*status_transfer_success,*path_of_transfered_file,
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
            EUDATCheckError(*path_of_transfered_file,*target_of_transfered_file);                      
        } else {
            logInfo("Action is canceled. Error is caught in function catchErrorDataOwner"); 
            # Update fail_log                
            *status_transfer_success = bool("false");
            EUDATUpdateLogging(*status_transfer_success,*path_of_transfered_file,*target_of_transfered_file,
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
EUDATTransferUsingFailLog(*buffer_length) {
    
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
        EUDATTranferSingleFile(*path_of_transfer_file, *target_of_transfer_file);
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
#    4. trigger replication from source to destination
#
# Parameters:
#   *source         [IN]     source of the file
#   *destination    [IN]     destination of the file
# Author: Elena Erastova, RZG
#
EUDATCheckReplicas(*source, *destination) {
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

#
# Parameters:
#     *path_of_transfered_coll     [IN] absolute iRODS path of the collection to be transfered
#     *target_of_transfered_coll   [IN] absolute iRODS path of the destination
#     *incremental                 [IN] bool('true') to perform an incremental transfer.
#
# Author: Long Phan, Juelich
#         Claudio Cacciari, Cineca
#
EUDATTransferCollection(*path_of_transfered_coll,*target_of_transfered_coll,*incremental) {

    msiStrlen(*path_of_transfered_coll,*path_originallength);

    # ----------------- Build Path for sourcePATH --------------
    msiStrchop(*path_of_transfered_coll,*out);
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
            if (*subcollname == *path_of_transfered_coll || *choplength == *lengthtemp) {
            
                # --------------------  Get SubCollection. --------------------    
                *PATH = *Collection++"/"++*Name;                    
                msiSubstr(*PATH,str(int(*pathLength)+1),"null",*SubCollection);
                   
                # -------------------- Transfer Data Obj ----------------------
                *Source = "*sourceParent" ++ "/" ++ "*SubCollection"; 
                *Destination = "*target_of_transfered_coll"++"*SubCollection"

                if (*incremental == bool("true") && 
                    (catchErrorChecksum(*Source, *Destination) == bool("false") || 
                     catchErrorSize(*Source, *Destination) == bool("false"))) {
                    
                    EUDATTranferSingleFile(*Source,*Destination);        
                }
                else if (*incremental == bool("false")) {
                    EUDATTranferSingleFile(*Source,*Destination);
                }
            }              
        }
        
        *ContInxOld = *ContInxNew;
        
        # get more rows in case data > 256 rows.
        if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
    }
            
}


#
# Transfer all data objects at Parent_Collection without recursion on subCollection
#
# Parameters:
#    *path_of_transfered_collection		[IN] path of transfered collection in iRODS (ex. /COMMUNITY/DATA/Dir9/)
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
#			EUDATTranferSingleFile(*Source,*Destination);
#		}
#		
#		*ContInxOld = *ContInxNew;		
#		# get more rows in case data > 256 rows.
#		if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
#	}
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
