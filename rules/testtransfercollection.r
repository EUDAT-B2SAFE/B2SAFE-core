#
# Test for transfer complete Collection Dir and all of data objects in its from *Path to *replicaPath. 
#
test {
	 #transferCollection(*Path,*replicaPath);
     #transferCollectionStressMemory(*Path,*replicaPath);
     transferCollectionAVU(*Path,*replicaPath);
	    
}

INPUT *Path="/COMMUNITY/DATA/Stresstest/Dir",*replicaPath="/DATACENTER/Data17/"
OUTPUT ruleExecOut
~                 