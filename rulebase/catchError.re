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
# EUDATCheckOwnershipObj(*path)
# EUDATCheckOwnershipColl(*path)

#
# Check if 2 replicas have the same checksum
#
# Parameters:
#	*source         [IN] path source of data object
#	*destination	[IN] path destination of replicated data object
# 
# Author: Long Phan, JSC
#
EUDATCatchErrorChecksum(*source,*destination) {
    logInfo("[EUDATCatchErrorChecksum] Check if 2 replicas have the same checksum. " ++
            "Source = *source, destination = *destination");

    *b = bool("true");

    *checksum0 = "";
    EUDATiCHECKSUMget(*source, *checksum0, *modtime);
    *checksum1 = "";
    EUDATiCHECKSUMget(*destination, *checksum1, *modtime);

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
    foreach ( *BS in SELECT DATA_SIZE WHERE COLL_NAME = '*parentS' AND DATA_NAME = '*childS' ) {
        *size0 = *BS.DATA_SIZE;
        logDebug("Size *source = *size0");
    }

    *size1 = "";
    msiSplitPath(*destination,*parentD,*childD);
    foreach ( *BD in SELECT DATA_SIZE WHERE COLL_NAME = '*parentD' AND DATA_NAME = '*childD') {
        *size1 = *BD.DATA_SIZE;
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
        logDebug("checking the ownership of the collection *path for the user $userNameClient");
        msiCheckAccess(*path,"own",*result);
        if (*result != 1) {
            if (EUDATCheckOwnershipColl(*path) != 1 ) {
                *msg = "ownership check failed on path: *path";
                failmsg(-1, *msg);
            }
        }
        # check the ownership of the sub-collections and their related data objects
        logDebug("checking the ownership of the collections under the path *path");
        foreach(*Row in SELECT DATA_NAME,COLL_NAME WHERE COLL_NAME = '*path' || like '*path/%') {
            if (*Row.COLL_NAME != *path) {
                msiCheckAccess(*Row.COLL_NAME,"own",*result);
                if (*result != 1) {
                    if (EUDATCheckOwnershipColl(*Row.COLL_NAME) != 1 ) {
                        *msg = "ownership check failed on path: *Row.COLL_NAME";
                        failmsg(-1, *msg);
                    }
                }
            }
            *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
            msiCheckAccess(*objPath,"own",*result);
            logDebug("the object *objPath has result: *result");
            if (*result != 1) {
                if (EUDATCheckOwnershipObj(*objPath) != 1 ) {
                    *msg = "ownership check failed on path: *objPath";
                    failmsg(-1, *msg);
                }
            }
        }
    }
    else if (*type == '-d') {
        logDebug("checking the ownership of the object *path for the user $userNameClient");
        msiCheckAccess(*path,"own",*result);
        if (*result != 1) {
            if (EUDATCheckOwnershipObj(*path) != 1) {
                *msg = "ownership check failed on path: *path";
                failmsg(-1, *msg);
            }
        }
    }
}


# Check if a user is or is not owner of the data object, 
# but comparing the session var "userNameClient" with the owners of the object
#
# Parameters:
#       *path                   [IN]  path source of data object
#       *message                [OUT] response message
#
# Author: Claudio Cacciari, Cineca;
#----------------------------------------------------
EUDATCheckOwnershipObj(*path) {

    msiSplitPath(*path, *collPath, *objPath);
    *owner = 0;
    foreach(*Row in SELECT USER_NAME,COLL_NAME,DATA_NAME WHERE COLL_NAME = '*collPath' and DATA_NAME = '*objPath')
    {
        if (*Row.USER_NAME == $userNameClient) { *owner = 1; }
    }

    *owner;
}

# Check if a user is or is not owner of the data collection, 
# but comparing the session var "userNameClient" with the owners of the collection
# 
# Parameters:
#       *path                   [IN]  path source of data collection
#       *message                [OUT] response message
#
# Author: Claudio Cacciari, Cineca;
# ----------------------------------------------------
EUDATCheckOwnershipColl(*path) {

    *owner = 0;
    foreach(*Row in SELECT USER_NAME,COLL_NAME WHERE COLL_NAME = '*path') {
        if (*Row.USER_NAME == $userNameClient) { *owner = 1; }
    }

    *owner;
}
