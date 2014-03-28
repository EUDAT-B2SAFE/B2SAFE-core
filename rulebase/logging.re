#
# Logging Module: are used for Transferring/ replication
#

#
# Create one Log_File and save it into common log_path to get an overview 
# on status of Collection (Size, count of data objects, collection owner, location, date) 
# This function is optional and can be called independently to support observing status of replication
# Result after that will be saved into a file (named collection_name.log) 
# and stays in the same path of log_files.
# 
# TODO additional feature: only data objects of User on Session ($userNameClient 
#      and $rodsZoneClient) at *path_of_collection will be recorded in case collection 
#      contains data of many people.
# TODO to be updated with the new logging mechanism
#
# Parameter:
# 	*path_of_collection		[IN]	Path of collection in iRODS (ex. /COMMUNITY/DATA)
#
# Author: Long Phan, Juelich
#
createLogStatusCollection(*path_of_collection) {

		# --- create optional content of logfile for collection ---
		*contents = "------------- Log Information of Collection *path_of_collection --------------- \n";
		msiGetCollectionACL(*path_of_collection,"",*Buf);		
		*contents = *contents ++ "Collection Owner: \n*Buf \n";
		
		msiExecStrCondQuery("SELECT RESC_LOC, RESC_NAME WHERE COLL_NAME = '*path_of_collection'" ,*BS);
		foreach   ( *BS )    {
	        msiGetValByKey(*BS,"RESC_LOC", *resc_loc);
	        msiGetValByKey(*BS,"RESC_NAME", *resc_name);
	    }
		*contents = *contents ++ "Resource Name: *resc_name\nResource Location: *resc_loc \n";
		
		msiGetSystemTime(*time,"human");		
		*contents = *contents ++ "Date.Time: *time \n\n";
		
		setLogFiles(*logStatisticFilePath,*logFailedFilePath, *ReplFr, *ReplTo);
		msiSplitPath(*logStatisticFilePath, *coll, *name);
		
		# --- get Collection from path *path_of_collection ---		
		getCollectionName(*path_of_collection,*Collection_Name);		
    	*path_of_logfile = "*coll" ++ "/" ++ "*Collection_Name" ++ ".log";   	
    	writeLine("serverLog",*path_of_logfile);
		
		# -------------- record *contents of collection and all sub_collection from *path_of_collection -----------------------
			*wildcard = "%";
			
			# loop on collection
			*ContInxOld = 1;
			# Path:
			*COLLPATH = "*path_of_collection"++"*wildcard";
			*Condition = "COLL_NAME like '*COLLPATH'";
				
			*sum = 0;
			*count = 0;
			msiStrlen(*path_of_collection,*originallength);
			*comparelink = *path_of_collection ++ "/";
			msiStrlen(*comparelink,*pathlength);
			
			msiMakeGenQuery("COLL_NAME,count(DATA_NAME), sum(DATA_SIZE)",*Condition, *GenQInp);
			msiExecGenQuery(*GenQInp, *GenQOut);
			msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
			
			while(*ContInxOld > 0) {
				foreach(*GenQOut) {			
					msiGetValByKey(*GenQOut, "COLL_NAME", *collname);					
					msiGetValByKey(*GenQOut, "DATA_NAME", *dc);
					msiGetValByKey(*GenQOut, "DATA_SIZE", *ds);
										
					msiStrlen(*collname,*lengthtemp);
					# msiSubString of *collname and compare with *path_of_collection				
					msiSubstr(*collname,"0","*pathlength",*subcollname);
					
					if (*subcollname == *comparelink || *originallength == *lengthtemp) {									
								*contents = "*contents" ++ "*collname count = *dc, sum = *ds\n";
								*count = *count + double(*dc);
								*sum = *sum + double(*ds);									
					}		
					
				}
				
				*ContInxOld = *ContInxNew;
				# get more rows in case data > 256 rows.
				if (*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
			}
				
			#writeLine("stdout","In *path_of_collection \n---- Number of files : *count \n" ++ "---- Capacity: *sum \n");	
				
			*contents = *contents ++ "\nIn *path_of_collection \n---- Number of files : *count \n" ++ "---- Capacity: *sum \n";
		# ---------------------------------------------------------------------------------------------------------------------											
		
		writeFile(*path_of_logfile, *contents);
								
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
createAVU(*Key,*Value,*Path) {
	    msiAddKeyVal(*Keyval,*Key, *Value);
	    writeKeyValPairs('serverLog', *Keyval, " is : ");
	    msiGetObjType(*Path,*objType);
	    msiAssociateKeyValuePairsToObj(*Keyval, *Path, *objType);
	    msiWriteRodsLog("EUDAT create -> Added AVU = *Key with *Value to metadata of *Path", *status);
}
