eudatReplCheckIntegrity{
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

    # PID creation
    # EUDATCreatePID(*parent_pid, *path, *ror, *fio, *fixed, *newPID)
    EUDATCreatePID("None", "*home/test_data.txt", "None", "None", "true", *newPID);
    writeLine("stdout", "The Object *home/test_data.txt has PID = *newPID");

    # Data set replication
    # with PID registration (3rd argument "true")
    # and not recursive (4th argument "false")
    *res = EUDATReplication("*home/test_data.txt", "*home/test_data2.txt", "true", "false", *response);
    if (*res) {
        writeLine("stdout", "Object *home/test_data.txt replicated to Object *home/test_data2.txt!");
        writeLine("stdout", "The content of the replica is:");
        msiDataObjOpen("*home/test_data2.txt", *S_FD);
        msiDataObjRead(*S_FD, 12,*R_BUF);
        writeBytesBuf("stdout", *R_BUF);
        msiDataObjClose(*S_FD, *status2);
        writeLine("stdout", "");
        EUDATgetLastAVU("*home/test_data2.txt", "PID", *value);
        writeLine("stdout", "The Replica *home/test_data2.txt has PID = *value");

        # Data set integrity check
        # with logging enabled (3rd argument "true")
        # EUDATCheckIntegrityDO(*source, *destination, *logEnabled, *response);
        *status_check = EUDATCheckIntegrityDO("*home/test_data.txt", "*home/test_data2.txt", bool("true"), *response);
        if (*status_check) {
            writeLine("stdout", "Integrity check after replication: successful!");
        }
        else {
            writeLine("stdout", "Integrity check after replication: failed: *response");
        }

        EUDATePIDremove("*home/test_data2.txt", "true");
        writeLine("stdout", "PID *value removed"); 
        msiDataObjUnlink("*home/test_data2.txt",*status3);
        writeLine("stdout", "Replica removed");
    }
    else {
        writeLine("stdout", "Replication failed: *response");
    }    

    EUDATePIDremove("*home/test_data.txt", "true");
    writeLine("stdout", "PID *newPID removed");   
    msiDataObjUnlink("*home/test_data.txt",*status4);
    writeLine("stdout", "Object *home/test_data.txt removed");
}
INPUT *home=''
OUTPUT ruleExecOut
