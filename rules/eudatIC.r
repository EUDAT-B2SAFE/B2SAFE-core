eudatIC{
    # Compare cheksums of data objects in the source and destination
    # collection recursively
    EUDATCheckIntegrityColl(*source, *destination, bool("true"), *response)
}
INPUT *source='/vzRZGEUDAT/home/eudat/11', *destination='/devRZG/home/eudat#vzRZGEUDAT/11-6'
OUTPUT ruleExecOut

