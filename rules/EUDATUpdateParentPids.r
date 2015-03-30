#
# Updates parent pids by querying .pid.update command files and passing them to processPIDCommandFile.
# Limits the number of processed command files per one rule run. By default, at most *MaxSuccess
# command files are processed.
#
# Required rulebases: eudat, catchError
#
# Configuration: edit the *Coll INPUT parameter to match the target zone name and the command file collection.
#
# Arguments:
#   *Coll          [INPUT]    The path to the .pid.update files
#   *Suffix        [INPUT]    The suffix of the update files
#
# Author: Jani Heikkinen, CSC
#
update_parent_pid {
        *ContInxOld = 1;
        *SuccessCount = 0;
        *FailedCount = 0;
        *MaxSuccess = 100;
        *Condition="COLL_NAME = '*Coll' AND DATA_NAME like '*Suffix'";
        msiMakeGenQuery("COLL_NAME,DATA_NAME",*Condition,*GenQInp);
        msiExecGenQuery(*GenQInp, *GenQOut);
        msiGetContInxFromGenQueryOut(*GenQOut,*ContInxNew);
        while(*ContInxOld > 0) {
                if(*ContInxNew == 0) { *ContInxOld = 0; }
                foreach(*GenQOut) {
                        msiGetValByKey(*GenQOut, "COLL_NAME", *Cname);
                        msiGetValByKey(*GenQOut, "DATA_NAME", *Dname);
                        *CF="*Cname/*Dname";
                        if(errorcode(msiObjStat(*CF,*out)) >= 0) {
                                processPIDCommandFile(*CF);
                                *SuccessCount = *SuccessCount + 1;
                        } else {
                                logInfo("*CF does not exist");
                                EUDATProcessErrorUpdatePID(*CF);
                                *FailedCount = *FailedCount + 1;
                        }
                }
                *ContInxOld = *ContInxNew;
                if(*SuccessCount > *MaxSuccess) { *ContInxOld = 0; }
                if(*ContInxOld > 0) {msiGetMoreRows(*GenQInp,*GenQOut,*ContInxNew);}
        }
        logInfo("Updated parent PIDs: *SuccessCount . Failed updates: *FailedCount");
}
INPUT *Coll = "/zone/replicate", *Suffix="%%.pid.update"
OUTPUT ruleExecOut

