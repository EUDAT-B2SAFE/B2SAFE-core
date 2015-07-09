eudatRepl{
    # Data set replication
    # registered data (with PID registration) (3rd argument - 1st bool("true"))
    # recursive (4th argument 2nd bool("true"))
    EUDATReplication(*source, *destination, bool("true"), bool("true"), *response)
}
INPUT *source='/vzRZGEUDAT/home/eudat/11', *destination='/devRZG/home/eudat#vzRZGEUDAT/11-6'
OUTPUT ruleExecOut

