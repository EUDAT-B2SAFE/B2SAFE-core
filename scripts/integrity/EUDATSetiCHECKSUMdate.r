#
# Set date of iCHECKSUM for all checksumed data objects, that doesn't have this set.
# This rule is intended to be run once on iRODS server that not supported iCHECKSUM periodic verification mechanism before.
# Note, that it may be time and resource consumig, as it needs loop over all data objects in iCAT.
# The task may be limited by setting *cond input parameter, e.g. *cond="COLL_NAME = '/some/collection'"
# limits to '/some/collection'.
#
# Input:
#       *cond   the conditioon to limit the task
#
# Output:
#
# Author: Michal Jankowski, PSNC
#

EUDATSetiCHECKSUMdate {

    if (*cond==""){
        *fullCond = "DATA_CHECKSUM <> ''";
    }
    else {
        *fullCond = "DATA_CHECKSUM <> '' AND *cond";
    }

    msiMakeGenQuery("COLL_NAME, DATA_NAME, DATA_RESC_NAME, DATA_MODIFY_TIME", *fullCond, *genQIn);
    msiExecGenQuery(*genQIn, *genQOut);

    *contOld=1;
    msiGetContInxFromGenQueryOut(*genQOut,*contNew);
    while (*contOld > 0) {
        foreach(*genQOut){

            msiGetValByKey(*genQOut, "COLL_NAME", *coll);
            msiGetValByKey(*genQOut, "DATA_NAME", *name);
            msiGetValByKey(*genQOut, "DATA_RESC_NAME", *resc);
            msiGetValByKey(*genQOut, "DATA_MODIFY_TIME", *modtime);
            writeLine("stdout", "*resc: *coll/*name ");
            EUDATiCHECKSUMdate(*coll, *name, *resc, *modtime);

        }
        *contOld=*contNew+0;
        if(*contOld > 0) {
          msiGetMoreRows(*genQIn,*genQOut,*contNew);
        }
    }


}
INPUT *cond=""
OUTPUT ruleExecOut
