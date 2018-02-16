eudatSimulateRecovery{
    writeLine("stdout", "userNameClient: $userNameClient");
    writeLine("stdout", "rodsZoneClient: $rodsZoneClient");
    if (*home == '') {
        *home="/$rodsZoneClient/home/$userNameClient";
    }
    writeLine("stdout", "Create data");
    msiDataObjCreate("*home/test_data.txt", "", *fd);
    msiDataObjWrite(*fd, "Hello World!", "");
    msiDataObjClose(*fd, *status1);
    writeLine("stdout", "Object *home/test_data.txt written with success!");
    writeLine("stdout", "Its content is: Hello World!");

    # PID creation
    # EUDATCreatePID(*parent_pid, *path, *ror, *fio, *fixed, *newPID)
    EUDATCreatePID("None", "*home/test_data.txt", "None", "None", "true", *newPID);
    writeLine("stdout", "The Object *home/test_data.txt has PID = *newPID");
    writeLine("stdout", "");
    # Data set replication
    # with PID registration (3rd argument "true")
    # and not recursive (4th argument "false")
    writeLine("stdout", "Replicating file:");
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
        writeLine("stdout", "");
        # Alter the content of the replica to simulate a failure
        writeLine("stdout", "Simulating interruption of file transfer");
        msiDataObjOpen("objPath=*home/test_data2.txt++++openFlags=O_WRONLY", *rfd);
        msiDataObjWrite(*rfd, "Hello Wor        ", "");
        msiDataObjClose(*rfd, *status3);
        writeLine("stdout", "Now the content of the altered replica is:");
        msiDataObjOpen("*home/test_data2.txt", *S_FD);
        msiDataObjRead(*S_FD, 13,*R_BUF);
        writeBytesBuf("stdout", *R_BUF);
        msiDataObjClose(*S_FD, *status4);
        writeLine("stdout", "");

        # Data set integrity check
        # with logging enabled (3rd argument "true")
        # EUDATCheckIntegrityDO(*source, *destination, *logEnabled, *response);
        *status_check = EUDATCheckIntegrityDO("*home/test_data.txt", "*home/test_data2.txt", bool("true"), *response);
        if (*status_check) {
            writeLine("stdout", "Integrity check after replication: successful!");
        }
        else {
            writeLine("stdout", "Integrity check after replication: failed: *response");
            *buffer_length = 1;
            EUDATTransferUsingFailLog(*buffer_length, *stats);
            writeLine("stdout", "Recovered failed transfer with the following stats: *stats");
            writeLine("stdout", "Now the content of the fixed replica is:");
            msiDataObjOpen("*home/test_data2.txt", *S_FD);
            msiDataObjRead(*S_FD, 12,*R_BUF);
            writeBytesBuf("stdout", *R_BUF);
            msiDataObjClose(*S_FD, *status4);
            writeLine("stdout", "");
        }

        EUDATePIDremove("*home/test_data2.txt", "true");
        writeLine("stdout", "PID *value removed"); 
        msiDataObjUnlink("*home/test_data2.txt",*status5);
        writeLine("stdout", "Replica removed");
    }
    else {
        writeLine("stdout", "Replication failed: *response");
    }    

    EUDATePIDremove("*home/test_data.txt", "true");
    writeLine("stdout", "PID *newPID removed");   
    msiDataObjUnlink("*home/test_data.txt",*status6);
    writeLine("stdout", "Object *home/test_data.txt removed");
}
INPUT *home=''
OUTPUT ruleExecOut
