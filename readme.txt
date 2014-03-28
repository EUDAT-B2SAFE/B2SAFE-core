#
# Replication with Logging
#
# Author: Long Phan, Juelich.
#

Summary: 
- Logging_files for replication (logging.re) will be created firstly. During data transfer between 2 sites error can be possibly caught (catchError.re), result will be logged and updated after every transfer. 
- Different Implementations for replication of Collection to assess performance (replication.re)

# -----------------  Some changes in case use function EUDATsetFilterACL  in eudat-i9.re -------------------------------
	# -> Configure acPreProcForExecCmd like following in core.re 
	
	acPreProcForExecCmd(*cmd, *args, *addr, *hint) {
	        EUDATsetFilterACL (*cmd, *args, *addr, *hint, *status);
	        if (*status == "false") {
	                fail;
	        }
	}
	
	# -> PID needs to be added into iCAT (see change in function createPID in eudat-i9.re)
			writeLine("serverLog","Begin to SAVE PID into field AVU -PID- of iCAT *path with PID = *newPID");
			EUDATiPIDcreate2(*newPID,*path);
# ----------------------------------------------------------------------------------------------------------------------

Test:
	(*)   Pre_transfer:
			1) Append 3 rulebases logging.re, replication.re, catchError.re into iRODS/server/config/server.config
			   Test these rulebases together with eudat.re of trunk_version or eudat-i9.re
			   	(-> suggest using eudat-i9.re attached in this branch, because eudat.re of trunk_version is still being merged and tested.)
			
			2) ireg -kf(C) file/ (collection) in iRODS or files are already there 
			   Setup location and name for log_files in logging.re (function setCollectionForLogFiles) 
			   Only data objects with PID can be transfered/ replicated. Otherwise, path_in_iRODS of data_objects without PID will be logged in failFiles.log
			
			3) transferSingleFile.jpg: sequence diagram, draft a relationship between transfer and logging 
	
	(**)  Transfer:	
			1) transferSingleFile: basic transfer source_file to destination_file.  
				(-> test.r)
			2) transferCollection, transferCollectionStressMemory, transferCollectionAVU: should give the same result, however possibly with different performance (NEED Performance_Test)			
			3) transferCollectionWithoutRecursion: should transfer only files at input_collection but not files in sub_collection.
				(-> testtransfercollection.r)
			4) transferUsingFailLog: should transfer only files saved in AVU of log_file
				(-> testtransferusingfaillog.r)
			
	(***) Post_transfer:
			- Log_files (*logStatisticFilePath and *logFailedFilePath in logging.re) will be updated during transfer
			- Using transferCollectionAVU will create one more log_file (named Collection_Name.log) 
			- Using icommand imeta to read AVU of this log_files in iCAT.		
				(-> imeta ls -d /COMMUNITY/logfile/statistic.log or imeta ls -d /COMMUNITY/logfile/failFiles.log)		

	(..)  Monitoring:
			- Besides log_files for data transfer, function createLogStatusCollection gives an overview statistic of collection (number of files in all possible recursively (sub)collections, size, collection_owner, date/time ) 
				(-> testLogStatusCollection.r)
			
	(..)  Others:
		- some functions to utilize log_files  (reset, remove, backup, exportXML ...)
				(-> test.r)