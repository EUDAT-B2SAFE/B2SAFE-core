#
# Test for transfer complete Collection Dir and all of data objects inside it from *Path to *replicaPath. 
#
test {
     #transferCollection(*Path,*replicaPath);
     transferCollectionStressMemory(*Path,*replicaPath);
     #transferCollectionAVU(*Path,*replicaPath);
	    
}

INPUT *Path="/CINECA/home/testuser/testPID/1000x3nested.dir",*replicaPath="/CINECA2/home/testuser#CINECA/testData/"
OUTPUT ruleExecOut
~                 
