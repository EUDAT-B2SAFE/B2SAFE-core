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
    msiMakeGenQuery("COLL_NAME, DATA_NAME, DATA_RESC_NAME, DATA_MODIFY_TIME", *fullCond, *GenQIn);
    msiExecGenQuery(*GenQIn, *GenQOut);

    foreach(*row in *GenQOut) {

        msiGetValByKey(*row, "COLL_NAME", *coll);
        msiGetValByKey(*row, "DATA_NAME", *name);
        msiGetValByKey(*row, "DATA_RESC_NAME", *resc);
        msiGetValByKey(*row, "DATA_MODIFY_TIME", *modtime);
        writeLine("stdout", "*resc: *coll/*name ");
        EUDATiCHECKSUMdate(*coll, *name, *resc, *modtime);
    }
}
INPUT *cond=""
OUTPUT ruleExecOut
