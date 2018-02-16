eudatReplColl{
    writeLine("stdout", "userNameClient: $userNameClient");
    writeLine("stdout", "rodsZoneClient: $rodsZoneClient");
    if (*home == '') {
        *home="/$rodsZoneClient/home/$userNameClient";
    }

    *tcoll="*home/t_coll";
    msiCollCreate(*tcoll, "0", *status0);
    writeLine("stdout","Created collection *tcoll");

    *tdata="*tcoll/test_data.txt";
    msiDataObjCreate(*tdata, "", *fd);
    msiDataObjWrite(*fd, "Hello World!", "");
    msiDataObjClose(*fd, *status1);
    writeLine("stdout", "Object *tdata written with success!");
    writeLine("stdout", "Object contents:")
    msiDataObjOpen("*tcoll/test_data.txt", *S_FD);
    msiDataObjRead(*S_FD, 12,*R_BUF);
    writeBytesBuf("stdout", *R_BUF);
    msiDataObjClose(*S_FD, *status2);
    writeLine("stdout", "");
    
    # PID creation
    # EUDATCreatePID(*parent_pid, *path, *ror, *fio, *fixed, *newPID) 
    EUDATCreatePID("None", *tcoll, "None", "None", "true", *newPID);
    writeLine("stdout", "The Collection *tcoll has PID = *newPID");
    writeLine("stdout", "");

    *tcoll2="*home/t_coll2";
    # Data set replication
    # with PID registration (3rd argument "true")
    # and recursive (4th argument "true")
    # EUDATReplication(*source, *destination, *registered, *recursive, *response)
    *res = EUDATReplication(*tcoll, *tcoll2, "true", "true", *response);
    if (*res) {
        writeLine("stdout", "Collection *tcoll replicated to Collection *tcoll2!");
        writeLine("stdout", "The content of the replicated collection is: *tcoll2/test_data.txt");
        writeLine("stdout", "The content of the replicated object *tcoll2/test_data.txt is: ");
        msiDataObjOpen("*tcoll2/test_data.txt", *S_FD);
        msiDataObjRead(*S_FD, 12,*R_BUF);
        writeBytesBuf("stdout", *R_BUF);
        msiDataObjClose(*S_FD, *status2);
        writeLine("stdout", "");
        writeLine("stdout", "");

        writeLine("stdout", "PIDs for data:");
        EUDATgetLastAVU("*tdata", "PID", *origPID);
        writeLine("stdout", "The Original *tdata has PID = *origPID");
        EUDATgetLastAVU("*tcoll2/test_data.txt", "PID", *value);
        writeLine("stdout", "The Replica *tcoll2/test_data.txt has PID = *value");

        writeLine("stdout", "Remove replicated data object");
        EUDATePIDremove("*tcoll2/test_data.txt", "true");
        writeLine("stdout", "PID *value removed");
        msiDataObjUnlink("*tcoll2/test_data.txt",*status3);
        writeLine("stdout", "Replicated object removed");

        writeLine("stdout", "");
        writeLine("stdout", "PIDs for collections:");
        EUDATgetLastAVU(*tcoll, "PID", *origCollPID);
        writeLine("stdout", "The Original *tcoll has PID = *origCollPID");
        EUDATgetLastAVU(*tcoll2, "PID", *value);
        writeLine("stdout", "The Replica *tcoll2 has PID = *value");
        
       writeLine("stdout", "Remove replica Collection and PID.");
        EUDATePIDremove(*tcoll2, "true");
        writeLine("stdout", "PID *value removed");
        msiRmColl(*tcoll2, "", *status4);
        writeLine("stdout", "Replicated collection removed");

    }
    else {
        writeLine("stdout", "Replication failed: *response");
    }
    writeLine("stdout", "");
    writeLine("stdout", "Remove original data and their PIDs");

    EUDATePIDremove("*tdata", "true");
    writeLine("stdout", "PID *origPID removed");
    msiDataObjUnlink("*tcoll/test_data.txt",*status5);
    writeLine("stdout", "Object *tcoll/test_data.txt removed");

    EUDATePIDremove(*tcoll, "true");
    writeLine("stdout", "PID *origCollPID removed");
    msiRmColl(*tcoll, "", *status6);
    writeLine("stdout","Removed collection *tcoll");
}
INPUT *home=''
OUTPUT ruleExecOut
    
