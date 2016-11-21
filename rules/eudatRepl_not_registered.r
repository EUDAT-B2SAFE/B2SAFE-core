eudatRepl{
    writeLine("stdout", "userNameClient: $userNameClient");
    writeLine("stdout", "rodsZoneClient: $rodsZoneClient");
    if (*home == '') {
        *home="/$rodsZoneClient/home/$userNameClient";
    }

    msiDataObjCreate("*home/test_data.txt", "", *fd);
    msiDataObjWrite(*fd, "Hello World!", "");
    msiDataObjClose(*fd, *status1);
    writeLine("stdout", "Object *home/test_data.txt written with success!");
    writeLine("stdout", "Its content is: Hello World!");

    # Data set replication
    # without PID registration (3rd argument "false")
    # and not recursive (4th argument "false")
    *res = EUDATReplication("*home/test_data.txt", "*home/test_data2.txt", "false", "false", *response);
    if (*res) {
        writeLine("stdout", "Object *home/test_data.txt replicated to Object *home/test_data2.txt!");
        writeLine("stdout", "The content of the replica is:");
        msiDataObjOpen("*home/test_data2.txt", *S_FD);
        msiDataObjRead(*S_FD, 12,*R_BUF);
        writeBytesBuf("stdout", *R_BUF);
        msiDataObjClose(*S_FD, *status2);
        msiDataObjUnlink("*home/test_data2.txt",*status3);
        writeLine("stdout", "");
        writeLine("stdout", "Replica removed");
    }
    else {
        writeLine("stdout", "Replication failed: *response");
    }    

    msiDataObjUnlink("*home/test_data.txt",*status4);
    writeLine("stdout", "Object *home/test_data.txt removed");
}
INPUT *home=''
OUTPUT ruleExecOut
