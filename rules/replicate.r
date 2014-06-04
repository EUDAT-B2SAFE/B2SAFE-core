# 
# Test triggerReplication
#
replicate {
        msiWriteRodsLog("starting replication", *status);
        getSharedCollection(*source,*collectionPath);
        msiWriteRodsLog("source = *source", *status);
        msiWriteRodsLog("collectionPath = *collectionPath", *status);
        msiWriteRodsLog("shared collection = *collectionPath*commandFile", *status);
        triggerReplication("*collectionPath*commandFile",*pid,*source,*destination);
}
INPUT *pid="842/07cc0858-edb9-11e1-a27d-005056ae635a",*source="/vzMPI/bin/test.txt",*destination="/vzMPI-REPLIX/bin/test.txt",*commandFile="test.replicate"
OUTPUT ruleExecOut
