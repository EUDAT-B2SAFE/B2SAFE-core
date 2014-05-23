#
# Test for transfer complete Collection Dir and all of data objects inside it from *Path to *replicaPath. 
#
test {

     EUDATTransferCollection(*Path,*replicaPath,bool("false"),bool("true"));
}

INPUT *Path="/CINECA/home/testuser/testPID/10x10nested.dir",*replicaPath="/CINECA2/home/testuser#CINECA/testData"
OUTPUT ruleExecOut
~                 
