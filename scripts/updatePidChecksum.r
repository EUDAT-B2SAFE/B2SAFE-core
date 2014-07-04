updatePidChecksum{
    EUDATSearchPID(*path, *pid);
    if ( str(*pid) == "empty" ) {
        EUDATePIDcreate(*path, *pid);
    }
    logInfo("DPM CHECKSUM update related to PID *pid");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *pid CHECKSUM 'none'", "null", "null", "null", *out);
    EUDATiCHECKSUMget(*path, *checksum);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *pid CHECKSUM *checksum", "null", "null", "null", *out);
    msiGetStdoutInExecCmdOut(*out, *response);
    logInfo("EUDATeCHECKSUMupdate -> modify handle response = *response");

}

INPUT *path=""
OUTPUT ruleExecOut

