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

    # PID creation
    # with PID registration in iCAT (4th argument "true")
    # EUDATCreatePID(*parent_pid, *source, *ror, "true", *newPID);
    EUDATCreatePID("None", "*home/test_data.txt", "None", "true", *newPID);
    writeLine("stdout", "The Object *home/test_data.txt has PID = *newPID");

    EUDATePIDremove("*home/test_data.txt", "true");
    writeLine("stdout", "PID *newPID removed");

    msiDataObjUnlink("*home/test_data.txt",*status2);
    writeLine("stdout", "Object *home/test_data.txt removed");
}
INPUT *home=''
OUTPUT ruleExecOut
