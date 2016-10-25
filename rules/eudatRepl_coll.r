eudatRepl{
    writeLine("stdout", "userNameClient: $userNameClient");
    writeLine("stdout", "rodsZoneClient: $rodsZoneClient");
    if (*home == '') {
        *home="/$rodsZoneClient/home/$userNameClient";
    }

    *tcoll="*home/test_coll";
    msiCollCreate(*tcoll, "0", *status0);
    writeLine("stdout","Created collection *home/test_coll");

    *tdata="*tcoll/test_data.txt";
    msiDataObjCreate(*tdata, "", *fd);
    msiDataObjWrite(*fd, "Hello World!", "");
    msiDataObjClose(*fd, *status1);
    writeLine("stdout", "Object *tdata written with success!");
    writeLine("stdout", "Its content is: Hello World!");

    # PID creation
    # with PID registration in iCAT (4th argument "true")
    # EUDATCreatePID(*parent_pid, *source, *ror, "true", *newPID);
    EUDATCreatePID("None", *tcoll, "None", "true", *newPID);
    writeLine("stdout", "The Collection *tcoll has PID = *newPID");

    *tcoll2="*home/test_coll2";
    # Data set replication
    # with PID registration (3rd argument "true")
    # and not recursive (4th argument "true")
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

        EUDATiFieldVALUEretrieve("*tcoll2/test_data.txt", "PID", *value);
        writeLine("stdout", "The Replica *tcoll2/test_data.txt has PID = *value");
        EUDATePIDremove("*tcoll2/test_data.txt", "true");
        writeLine("stdout", "PID *value removed"); 
        msiDataObjUnlink("*tcoll2/test_data.txt",*status3);
        writeLine("stdout", "Replicated object removed");
        EUDATiFieldVALUEretrieve(*tcoll2, "PID", *value);
        writeLine("stdout", "The Replica *tcoll2 has PID = *value");
        EUDATePIDremove(*tcoll2, "true");
        writeLine("stdout", "PID *value removed"); 
        msiRmColl(*tcoll2, "", *status4);
        writeLine("stdout", "Replicated collection removed");        
    }
    else {
        writeLine("stdout", "Replication failed: *response");
    }    

    EUDATePIDremove("*home/test_coll/test_data.txt", "true");
    writeLine("stdout", "PID *newPID removed");   
    msiDataObjUnlink("*home/test_coll/test_data.txt",*status5);
    writeLine("stdout", "Object *home/test_coll/test_data.txt removed");
    msiRmColl("*home/test_coll", "", *status6);
    writeLine("stdout","Removed collection *home/test_coll");
}
INPUT *home=''
OUTPUT ruleExecOut
