################################################################################
#                                                                              #
# EUDAT error management rule set                                              #
#                                                                              #
################################################################################

# List of the functions:
# 
# EUDATCatchErrorChecksum(*source, *source_res, *destination, *dest_res, *response)
# EUDATCatchErrorSize(*source, *source_res, *destination, *dest_res, *response)
# EUDATCatchErrorDataOwner(*path,*msg)
# EUDATCheckOwnershipObj(*path)
# EUDATCheckOwnershipColl(*path)



# Check if 2 replicas have the same checksum
#
# Parameters:
#	*source         [IN]  path source of data object
#	*source_res     [IN]  iRODS resource name of the source
#	*destination	[IN]  path destination of replicated data object
#	*dest_res       [IN]  iRODS resource name of the destination
#	*response       [OUT] 
#	return          true/false
# 
# Author: Long Phan (JSC), Claudio Cacciari (Cineca)
#-------------------------------------------------------------------------------
EUDATCatchErrorChecksum(*source, *source_res, *destination, *dest_res, *response) {
    logInfo("[EUDATCatchErrorChecksum] Check if 2 replicas have the same checksum. " ++
            "Source = *source, destination = *destination");

    if (!EUDATObjExist(*source, *response) || !EUDATObjExist(*destination, *response)) {
        failmsg(-1, *response);
    }

    *b = bool("true");
    *checksum0 = "";
    EUDATiCHECKSUMget(*source, *checksum0, *modtime0, *source_res);
    *checksum1 = "";
    EUDATiCHECKSUMget(*destination, *checksum1, *modtime1, *dest_res);
    *response = "checksum(*source):*checksum0 = checksum(*destination):*checksum1"
    if(*checksum0 != *checksum1) {
        *response = "checksum(*source):*checksum0 != checksum(*destination):*checksum1,"
                 ++ " checksum(*source) modification time: *modtime0,"
                 ++ " checksum(*destination) modification time: *modtime1"
        logDebug("[EUDATCatchErrorChecksum] *response");
        *b = bool("false"); 
    } 
    logInfo("[EUDATCatchErrorChecksum] *response");
    *b;
    
}

EUDATCatchErrorChecksum(*source, *destination, *response) {
    *source_res = "null";
    *dest_res = "null";
    *b = EUDATCatchErrorChecksum(*source, *source_res, *destination, *dest_res, *response);
    *b;
}

# Check if 2 replicas have the same size.
#
# Parameters:
#	*source		[IN] path source of data object
#	*source_res     [IN]  iRODS resource name of the source
#	*destination	[IN] path destination of replicated data object
#	*dest_res       [IN]  iRODS resource name of the destination
#  
# Author: Long Phan, JSC
#-------------------------------------------------------------------------------
EUDATCatchErrorSize(*source, *source_res, *destination, *dest_res, *response) {
    logInfo("[EUDATCatchErrorSize] Check if 2 replicas have the same size." ++
            "Source = *source:*source_res:, destination = *destination:*dest_res:");

    if (!EUDATObjExist(*source, *response)) {
        failmsg(-1, *response);
    }
    if (!EUDATObjExist(*destination, *response)) {
        failmsg(-1, *response);
    }

    *b = bool("true"); 	
    *size0 = "";
    *s_res = *source_res;
    msiSplitPath(*source,*parentS,*childS);
    foreach ( *BS in SELECT DATA_SIZE,DATA_RESC_NAME WHERE COLL_NAME = '*parentS' 
              AND DATA_NAME = '*childS' ) {
        *size0 = *BS.DATA_SIZE;
        logVerbose("[EUDATCatchErrorSize] Size *source = *size0");
        *s_res = *BS.DATA_RESC_NAME;
        if (*BS.DATA_RESC_NAME == '*source_res') { break; }
    }
    *size1 = "";
    *d_res = *dest_res;
    msiSplitPath(*destination,*parentD,*childD);
    foreach ( *BD in SELECT DATA_SIZE,DATA_RESC_NAME WHERE COLL_NAME = '*parentD' 
              AND DATA_NAME = '*childD' ) {
        *size1 = *BD.DATA_SIZE;
        logVerbose("[EUDATCatchErrorSize] Size *destination = *size1");
        *d_res = *BD.DATA_RESC_NAME;
        if (*BD.DATA_RESC_NAME == '*dest_res') { break; }
    }
    *response = "size(*source:*s_res:):*size0 = size(*destination:*d_res:):*size1";
    if(*size0 != *size1) {
        *response = "size(*source:*s_res:):*size0 != size(*destination:*d_res:):*size1";
        logDebug("[EUDATCatchErrorSize] *response");
        *b = bool("false"); 
    } 
    logInfo("[EUDATCatchErrorSize] *response");
    *b;
}

EUDATCatchErrorSize(*source, *destination, *response) {
    *source_res = "null";
    *dest_res = "null";
    *b = EUDATCatchErrorSize(*source, *source_res, *destination, *dest_res, *response);
    *b;
}

# Check if a user is or is not owner of the data object/collection
# (Reference: https://www.irods.org/index.php/iRODS_Error_Codes or /iRODS/lib/core/include/rodsErrorTable.h)
#
# Parameters:
#	*path			[IN] path source of data object
#	*msg			[OUT] response message
#
# Author: Long Phan, JSC;
# Author: Claudio Cacciari, Cineca;
#-------------------------------------------------------------------------------
EUDATCatchErrorDataOwner(*path, *msg) {

    if (!EUDATObjExist(*path, *response)) {
        failmsg(-1, *response);
    }

    *msg = "ownership check passed";
    msiGetObjType(*path ,*type);
    if (*type == '-c') {
        # check the ownership of the root collection
        logDebug( "[EUDATCatchErrorDataOwner] checking the ownership of the collection"
               ++ " *path for the user $userNameClient");
        msiCheckAccess(*path,"own",*result);
        logVerbose("[EUDATCatchErrorDataOwner] msiCheckAccess(*path): *result");
        if (*result != 1) {
            if (EUDATCheckOwnershipColl(*path) != 1 ) {
                *msg = "ownership check failed on path: *path";
                failmsg(-1, *msg);
            }
        }
        # check the ownership of the sub-collections and their related data objects
        logDebug("[EUDATCatchErrorDataOwner] checking the ownership of the collections under the path *path");
        foreach(*Row in SELECT DATA_NAME,COLL_NAME WHERE COLL_NAME = '*path' || like '*path/%') {
            if (*Row.COLL_NAME != *path) {
                msiCheckAccess(*Row.COLL_NAME,"own",*result);
                logVerbose("[EUDATCatchErrorDataOwner] msiCheckAccess(" ++ *Row.COLL_NAME ++ "): *result");
                if (*result != 1) {
                    if (EUDATCheckOwnershipColl(*Row.COLL_NAME) != 1 ) {
                        *msg = "ownership check failed on path: *Row.COLL_NAME";
                        failmsg(-1, *msg);
                    }
                }
            }
            *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
            msiCheckAccess(*objPath,"own",*result);
            logVerbose("[EUDATCatchErrorDataOwner] the object *objPath has result: *result");
            if (*result != 1) {
                if (EUDATCheckOwnershipObj(*objPath) != 1 ) {
                    *msg = "ownership check failed on path: *objPath";
                    failmsg(-1, *msg);
                }
            }
        }
    }
    else if (*type == '-d') {
        logDebug( "[EUDATCatchErrorDataOwner] checking the ownership of the object "
               ++ " *path for the user $userNameClient");
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
# Return:           response message: 1 for success.
#
# Author: Claudio Cacciari (Cineca)
#-------------------------------------------------------------------------------
EUDATCheckOwnershipObj(*path) {

    logVerbose("[EUDATCheckOwnershipObj] checking *path");
    msiSplitPath(*path, *collPath, *objPath);
    *owner = 0;
    *perm = "";
    foreach(*Row in SELECT USER_NAME, COLL_NAME, DATA_NAME, DATA_ACCESS_NAME 
            WHERE COLL_NAME = '*collPath' and DATA_NAME = '*objPath') {
        *perm = *Row.DATA_ACCESS_NAME
        if (*Row.USER_NAME == $userNameClient) {
            if ( *perm == 'own' || *perm == 'write' || *perm == 'read') {
                *owner = 1; 
                break; 
            }
        }
    }
    logVerbose("[EUDATCheckOwnershipObj] result(*perm): *owner");
    *owner;
}

# Check if a user is or is not owner of the data collection, 
# but comparing the session var "userNameClient" with the owners of the collection
# 
# Parameters:
#       *path       [IN]  path source of data collection
# Return:           response message: 1 for success.
#
# Author: Claudio Cacciari (Cineca)
#-------------------------------------------------------------------------------
EUDATCheckOwnershipColl(*path) {

    logVerbose("[EUDATCheckOwnershipColl] checking *path");
    *owner = 0;
    *perm = "";
    foreach(*Row in SELECT USER_NAME, COLL_NAME, DATA_ACCESS_NAME WHERE COLL_NAME = '*path') {
        *perm = *Row.DATA_ACCESS_NAME;
        if (*Row.USER_NAME == $userNameClient) {
            if (*perm == 'own' || *perm == 'write' || *perm == 'read') {
                *owner = 1; 
                break; 
            }
        }
    }
    logVerbose("[EUDATCheckOwnershipColl] result(*perm): *owner");
    *owner;
}
