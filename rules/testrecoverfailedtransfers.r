#
# Test for the re-transfering of objects related to previously failed replications
#
test {
    EUDATTransferUsingFailLog(*buffer_length);     
}

INPUT *buffer_length=100
OUTPUT ruleExecOut
~                 
