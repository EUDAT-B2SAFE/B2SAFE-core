################################################################################
#                                                                              #
# EUDAT error management rule set                                              #
#                                                                              #
################################################################################

# List of the functions:
# 
# EUDATCatchErrorChecksum(*source,*destination)
# EUDATCatchErrorSize(*source,*destination)
# EUDATCatchErrorDataOwner(*path,*msg)

#
# Check if 2 replicas have the same checksum
#
# Parameters:
#	*source         [IN] path source of data object
#	*destination	[IN] path destination of replicated data object
# 
# Author: Long Phan, JSC
#
EUDATCatchErrorChecksum(*source,*destination){
    logInfo("[EUDATCatchErrorChecksum] Check if 2 replicas have the same checksum. " ++
            "Source = *source, destination = *destination");

    *b = bool("true");

    *checksum0 = "";
    msiSplitPath(*source,*parentS,*childS);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parentS' AND DATA_NAME = '*childS'" ,*BS);
    foreach ( *BS ) {
        msiGetValByKey(*BS,"DATA_CHECKSUM", *checksum0);
        logDebug("checksum0 = *checksum0");
    }

    *checksum1 = "";
    msiSplitPath(*destination,*parentD,*childD);
    msiExecStrCondQuery("SELECT DATA_CHECKSUM WHERE COLL_NAME = '*parentD' AND DATA_NAME = '*childD'" ,*BD);
    foreach ( *BD ) {
        msiGetValByKey(*BD,"DATA_CHECKSUM", *checksum1);
        logDebug("checksum1 = *checksum1");
    }

    if(*checksum0 != *checksum1) {
        EUDATSearchPID(*source, *pid);
        logDebug("*checksum0 != *checksum1, existing_pid = *pid");
        *b = bool("false"); 
    } 
    *b;
    
}

#
# Check if 2 replicas have the same size.
#
# Parameters:
#	*source		[IN] path source of data object
#	*destination	[IN] path destination of replicated data object
#  
# Author: Long Phan, JSC
#
EUDATCatchErrorSize(*source,*destination) {
    logInfo("[EUDATCatchErrorSize] Check if 2 replicas have the same size." ++
            "Source = *source, destination = *destination");

    *b = bool("true"); 	
    *size0 = "";
    msiSplitPath(*source,*parentS,*childS);
    msiExecStrCondQuery("SELECT DATA_SIZE WHERE COLL_NAME = '*parentS' AND DATA_NAME = '*childS'" ,*BS);
    foreach   ( *BS )    {
        msiGetValByKey(*BS,"DATA_SIZE", *size0);
        logDebug("Size *source = *size0");
    }

    *size1 = "";
    msiSplitPath(*destination,*parentD,*childD);
    msiExecStrCondQuery("SELECT DATA_SIZE WHERE COLL_NAME = '*parentD' AND DATA_NAME = '*childD'" ,*BD);
    foreach   ( *BD )    {
        msiGetValByKey(*BD,"DATA_SIZE", *size1);
        logDebug("Size *destination = *size1");
    }

    if(*size0 != *size1) {
        EUDATSearchPID(*source, *pid);
        logDebug("*size0 != *size1, existing_pid = *pid");
        *b = bool("false"); 
    } 
    *b;
    
}

#
# Check if a user is or is not owner of the data object/collection
# (Reference: https://www.irods.org/index.php/iRODS_Error_Codes or /iRODS/lib/core/include/rodsErrorTable.h)
#
# Parameters:
#	*path			[IN] path source of data object
#	*msg			[OUT] response message
#
# Author: Long Phan, JSC;
# Author: Claudio Cacciari, Cineca;
#----------------------------------------------------
EUDATCatchErrorDataOwner(*path,*msg) {
    *msg = "ownership check passed";

    msiGetObjType(*path ,*type);
    if (*type == '-c') {
        # check the ownership of the root collection
        logDebug("checking the ownership of the collection *path");
        msiCheckAccess(*path,"own",*result);
        if (*result != 1) {
            *msg = "ownership check failed on path: *path";
            failmsg(-1, *msg);
        }
        # check the ownership of the sub-collections and their related data objects
        logDebug("checking the ownership of the collections under the path *path");
	foreach(*Row in SELECT DATA_NAME,COLL_NAME WHERE COLL_NAME = '*path' || like '*path/%') {
            if (*Row.COLL_NAME != *path) {
                msiCheckAccess(*Row.COLL_NAME,"own",*result);
                if (*result != 1) {
                    *msg = "ownership check failed on path: *Row.COLL_NAME";
                    failmsg(-1, *msg);
                }
            }
            *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
            msiCheckAccess(*objPath,"own",*result);
            logDebug("the object *objPath has result: *result");
            if (*result != 1) {
                *msg = "ownership check failed on path: *objPath";
                failmsg(-1, *msg);
            }
        }
    }
    else if (*type == '-d') {
        logDebug("checking the ownership of the object *path");
        msiCheckAccess(*path,"own",*result);
        if (*result != 1) {
            *msg = "ownership check failed on path: *path";
            failmsg(-1, *msg);
        }
    }
}
