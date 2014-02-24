#
# Rule for replication single DataObj at Input from 1.DataCenter to 2.DataCenter
# Goal: transfer single DataObj from Path Source_A to Target_B without creating new PID at Source_A. 
#
# Author: Long Phan, Juelich
#  
replicate {
	# Transfer Status, default = 0
	*status = "";
	# loop on collection
	writeLine("serverLog","query PID von DataObj *PATH");
	getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
	msiExecCmd("epicclient.py", "*credStoreType *credStorePath search URL *serverID*PATH", "null", "null", "null", *out);
	msiGetStdoutInExecCmdOut(*out, *pid);
	writeLine("serverLog","PID is *pid, this Pid is supposed to be MASTER-PID in Jülich");

    if (*pid == "empty") {
		writeLine("serverLog","PID is empty, no replication will be executed");
	} else {
      	writeLine("serverLog","PID exist, Replication begin");
		getSharedCollection(*PATH,*sharedCollection);
		msiSplitPath(*PATH, *collection, *file);
        msiReplaceSlash(*replicaPATH, *controlfilename);
		writeLine("serverLog","ReplicateFile: *sharedCollection*controlfilename");
		# can comment this triggerReplication out in case you only want to test control-file file.statistic		        
		triggerReplication("*sharedCollection*controlfilename.replicate",*pid,*PATH,*replicaPATH);

		# ---------------------------  CheckReplicas (Author: Elena, Edited: Long) ---------------------------------
		*commandFile = "*controlfilename"++".replicate";

		logInfo("Check if 2 replicas have the same checksum. Source = *PATH, destination = *replicaPATH");

    	*checksum0 = "";
		msiSplitPath(*PATH,*parentS,*childS);
		msiExecStrCondQuery("SELECT DATA_CHECKSUM, DATA_SIZE WHERE COLL_NAME = '*parentS' AND DATA_NAME = '*childS'" ,*BS);
		foreach   ( *BS )    {
		        msiGetValByKey(*BS,"DATA_CHECKSUM", *checksum0);
		        logInfo("checksum0 = *checksum0");
				msiGetValByKey(*BS,"DATA_SIZE", *sizefile);
		    }

		*checksum1 = "";
		msiSplitPath(*replicaPATH,*parentD,*childD);
		msiExecStrCondQuery("SELECT DATA_CHECKSUM, DATA_SIZE WHERE COLL_NAME = '*parentD' AND DATA_NAME = '*childD'" ,*BD);
		foreach   ( *BD )    {
		        msiGetValByKey(*BD,"DATA_CHECKSUM", *checksum1);
		        logInfo("checksum1 = *checksum1");
		        msigetValByKey(*BD,"DATA_SIZE", *sizefile2);
		    }

		if(*checksum0 != *checksum1 && *sizefile != *sizefile2) {
		        searchPID(*PATH, *replicaPATH);
		        logInfo("*checksum0 != *checksum1, existing_pid = *pid");
		        logInfo("replication from *PATH to *replicaPATH");
		        # getSharedCollection(*PATH,*replicaPATH);
		        # triggerReplication("*collectionPath*commandFile",*pid,*PATH,*replicatePATH);
			*status = "0: File corrupted from *PATH to *replicaPATH";			
		} else {
			*status = "1: Success transfer *sizefile from *PATH to *replicaPATH ---- ";
		}
		# ----------------------------------------------------------------------

	}

	# also write log file to report stand even if everything went successful
	writeFile("/DATACENTER/standlog/file.stat",*status);
}
INPUT *PATH="/DATACENTER/PHANreplica/Coll17/csc10.ta",*replicaPATH="/DATACENTER2/JUELICHreplica/Coll17/csc10.ta"
OUTPUT ruleExecOut
