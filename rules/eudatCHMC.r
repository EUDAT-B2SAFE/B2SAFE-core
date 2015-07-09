eudatCHMC{
    # Walk through the collection. For each object in the collection 
    # create a PID and stores its value and the object checksum 
    # in the iCAT if it does not exist.
    # IF the PID exists, modify its checksum value
    EUDATeiPIDeiChecksumMgmtColl(*sourceColl);
}
INPUT *sourceColl='/vzRZGEUDAT/home/eudat/11'
OUTPUT ruleExecOut

