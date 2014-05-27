#
# Test for transfer complete Collection Dir and all of data objects inside it from *Path to *replicaPath. 
# It use the delay mode to try again even in case of failure.
# It uses the EUDAT rule: EUDATTransferCollection(*path_of_transfered_coll,*target_of_transfered_coll,
#                                                 *incremental,*recursive)
#
test {
    delay("<EF>1s REPEAT UNTIL SUCCESS OR 10 TIMES</EF>") {
        EUDATTransferCollection(*Path,*replicaPath,bool("true"),bool("true"));
    }
}

INPUT *Path="/CINECA/home/testuser/testPID/1000x3nested.dir",*replicaPath="/CINECA2/home/testuser#CINECA/testData"
OUTPUT ruleExecOut
~                 
