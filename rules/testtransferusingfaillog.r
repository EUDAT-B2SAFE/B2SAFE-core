#
# Test for transfer complete Collection Dir and all of data objects in its from *Path to *replicaPath. 
#
test {
	transferUsingFailLog(*destination_Collection,*logFailedFilePath, *Key);
     
}

INPUT *destination_Collection="/DATACENTER/Data17/", *Key = "Path_of_failed_Files"
OUTPUT ruleExecOut
~                 
