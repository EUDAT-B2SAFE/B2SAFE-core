eudatTD{
    # Calculate the difference between the creation time
    # and the modification time of an object. In seconds.
    EUDATgetObjectTimeDiff(*filePath, *mode, *age);
    
    # Calculate the difference between the current time 
    # and the modification time of an object. In seconds.
    EUDATgetObjectAge(*filePath, *age1);
}
INPUT *filePath='/vzRZGEUDAT/home/eudat/11/11.txt', *mode='1'
OUTPUT *age,*age1,ruleExecOut

