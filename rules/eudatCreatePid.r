eudatCreatePID{
    writeLine("stdout", "userNameClient: $userNameClient");
    writeLine("stdout", "rodsZoneClient: $rodsZoneClient");
    if (*home == '') {
        *home="/$rodsZoneClient/home/$userNameClient";
    }

    msiDataObjCreate("*home/test_data.txt", "", *fd);
    msiDataObjWrite(*fd, "Hello World!", "");
    msiDataObjClose(*fd, *status1);
    writeLine("stdout", "Object *home/test_data.txt written with success!");
    writeLine("stdout", "Object contents:");
    msiDataObjOpen("*home/test_data.txt", *S_FD);
    msiDataObjRead(*S_FD, 12,*R_BUF);
    writeBytesBuf("stdout", *R_BUF);
    msiDataObjClose(*S_FD, *status2);
    writeLine("stdout", "");
    # PID creation

    # EUDATCreatePID(*parent_pid, *source, *ror, *fio, *fixed, *newPID);
    EUDATCreatePID("None", "*home/test_data.txt", "None", "None", "false", *newPID);
    writeLine("stdout", "The Object *home/test_data.txt has PID = *newPID");

    EUDATePIDremove("*home/test_data.txt", "true");
    writeLine("stdout", "PID *newPID removed");

    msiDataObjUnlink("*home/test_data.txt",*status2);
    writeLine("stdout", "Object *home/test_data.txt removed");
}
INPUT *home=''
OUTPUT ruleExecOut
