################################################################################
#                                                                              #
# Persistent Identifiers management rule set                                   #
#                                                                              #
################################################################################

# Legend (the prefix i stands for iCAT and e for epic):
#
# ePID PID on the EPIC server
# iPID PID record in the iCAT
# eCHECKSUM checksum on the EPIC server
# iCHECKSUM checksum record on the iCAT

# List of the functions:
#
# EUDATCreatePID(*parent_pid, *path, *ror, *fio, *fixed, *newPID)
# EUDATSearchPID(*path, *existing_pid)
# EUDATSearchPIDchecksum(*path, *existing_pid, *existing_url)
# EUDATUpdatePIDWithNewChild(*parentPID, *childPID)
# EUDATGeteValPid(*pid, *key)
# EUDATiPIDcreate(*path, *PID)
# EUDATePIDcreate(*path, *extraType, *PID)
# EUDATePIDsearch(*field, *value, *PID)
# EUDATeCHECKSUMupdate(*PID, *path)
# EUDATeURLupdate(*PID, *newURL)
# EUDATeURLupdateColl(*PID, *newURL)
# EUDATePIDremove(*path, *force)
# EUDATiRORupdate(*source, *pid)
# EUDATeRORupdate(*pid,*newRor)
# EUDATeFIOupdate(*pid, *newFio)
# EUDATPidsForColl(*collPath, *fixed)


# Generate a new PID for a digital object.
# Fields stored in the PID record: URL, ROR and CHECKSUM
# adds a ROR field if (*ror != "None")
#
# Parameters:
#   *parent_pid [IN]    the PID of the digital object that was replicated to us (not necessarily the ROR)
#   *path       [IN]    the path of the object to store with the PID record
#   *ror        [IN]    the ROR PID of the digital object that we want to store.
#   *fio        [IN]    the FIO PID of the digital object that we want to store.
#   *fixed      [IN]    the boolean flag to define that the object related to this PID cannot change
#   *newPID     [OUT]   the pid generated for this object 
#
# Author: Willem Elbers, MPI-TLA
# Edited by Elena Erastova, RZG; Long Phan, JSC; Robert Verkerk, SURFsara, Javier Quinteros, GFZ
#-------------------------------------------------------------------------------
EUDATCreatePID(*parent_pid, *path, *ror, *fio, *fixed, *newPID) {

    logInfo("[EUDATCreatePID] create pid for *path");
    *version = "1";
    logDebug(  "[EUDATCreatePID] input parameters: parent=*parent_pid,"
            ++ " path=*path, ror=*ror, fio=*fio, fixed=*fixed");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);

    #check if PID already exists
    EUDATSearchPID(*path, *existing_pid);
   
    if((*existing_pid == "empty") || (*existing_pid == "None")) {
        # add extraType parameters
        *extraType = "empty";

        # add ror as extratype parameter
        if (*ror != "None" && *ror != "") {
            *extraType = "EUDAT/ROR=*ror";
            if (*ror != "pid") {
                EUDATCreateAVU("EUDAT/ROR", *ror, *path);
            }
        }

        # add ppid as extratype parameter
        if (*parent_pid != "None" && *parent_pid != "") {
            if (*extraType != "empty") {
                *extraType = "*extraType"++";EUDAT/PARENT=*parent_pid";
            } else {
                *extraType = "EUDAT/PARENT=*parent_pid";
            }
            EUDATCreateAVU("EUDAT/PARENT", *parent_pid, *path);
        }
        # add fio as extratype parameter
        if (*fio != "None" && *fio != "") {
            if (*extraType != "empty") {
                *extraType = "*extraType"++";EUDAT/FIO=*fio";
            } else {
                *extraType = "EUDAT/FIO=*fio";
            }
            if (*fio != "pid") {
                EUDATCreateAVU("EUDAT/FIO", *fio, *path);
            }            
        }            
        # add fixed_content as extratype parameter
        if (EUDATtoBoolean(*fixed)) {
            if (*extraType != "empty") {
                *extraType = "*extraType"++";EUDAT/FIXED_CONTENT=True";
            } else {
                *extraType = "EUDAT/FIXED_CONTENT=True";
            }
            EUDATCreateAVU("EUDAT/FIXED_CONTENT", "True", *path);
        }
        else {
            if (*extraType != "empty") {
                *extraType = "*extraType"++";EUDAT/FIXED_CONTENT=False";
            } else {
                *extraType = "EUDAT/FIXED_CONTENT=False";
            }
            EUDATCreateAVU("EUDAT/FIXED_CONTENT", "False", *path);                
        }

        # add version as extratype parameter
        if (*extraType != "empty") {
            *extraType = "*extraType"++";EUDAT/PROFILE_VERSION=*version";
        } else {
            *extraType = "EUDAT/PROFILE_VERSION=*version";
        }

        # create PID
        EUDATePIDcreate(*path, *extraType, *newPID);
        logInfo("[EUDATCreatePID] Created pid *newPID for *path with properties: *extraType");
        EUDATiPIDcreate(*path, *newPID);
        logInfo("[EUDATCreatePID] Created iCAT pid *newPID for *path");
        
        # creation of ROR in icat in case it has been set to pid
        if (*ror == "pid") {
            EUDATCreateAVU("EUDAT/ROR", *newPID, *path);
            logDebug("[EUDATCreatePID] Created iCAT EUDAT/ROR *newPID for *path");
        }
        # creation of FIO in icat in case it has been set to pid
        if (*fio == "pid") {
            EUDATCreateAVU("EUDAT/FIO", *newPID, *path);
            logDebug("[EUDATCreatePID] Created iCAT EUDAT/FIO *newPID for *path");
        }
    }
    else {
        *newPID = *existing_pid;
        logInfo("[EUDATCreatePID] PID already exists (*newPID)");
    }
}

# Searching for a PID using URL replacing "#", "%" and "&" with "*"
# Parameters:
#   *path       	[IN]    the path of the replica
#   *existing_pid	[OUT]   existing PID
#   *status             [REI]   false if no value is found, true elsewhere 
#
# Author: Elena Erastova, RZG
# -----------------------------------------------------------------------------
EUDATSearchPID(*path, *existing_pid) {
    logDebug("[EUDATSearchPID] search pid for *path");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    getHttpApiParameters(*serverApireg, *serverApipub);
    EUDATReplaceHash(*path, *path1);
    *status = EUDATePIDsearch("URL", "*serverApireg*path1", *existing_pid);
    if (!(*status)) {
        *status = EUDATePIDsearch("URL", "*serverApipub*path1", *existing_pid);
    }
    logDebug("[EUDATSearchPID] pid = *existing_pid");
    *status;
}

# Searching fo a PID using CHECKSUM
# Parameters:
#   *path       	[IN]    the path of the replica
#   *existing_pid	[OUT]   existing PID 
#
# Author: Elena Erastova (RZG), Claudio Cacciari (Cineca)
#-------------------------------------------------------------------------------
EUDATSearchPIDchecksum(*path, *existing_pid, *existing_url) {

    logDebug("[EUDATSearchPIDchecksum] searching checksum for *path");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);

    *resource = "";
    EUDATiCHECKSUMget(*path, *checksum, *modtime, *resource)
    EUDATePIDsearch("EUDAT/CHECKSUM", *checksum, *existing_pid);
    *existing_url = EUDATGeteValPid(*existing_pid, "URL");
    logDebug("[EUDATSearchPIDchecksum] PID = *existing_pid, URL = *existing_url");
}

# Update a PID record with a new child.
#
# Parameters:
#       *parentPID  [IN]    PID of the record that will be updated
#       *childPID   [IN]    PID to store as one of the child locations
#
# Author: Willem Elbers, MPI-TLA
# Modified by: Claudio Cacciari, CINECA
#-------------------------------------------------------------------------------
EUDATUpdatePIDWithNewChild(*parentPID, *childPID) {
    *replicaNew = "None";
    logDebug("[EUDATUpdatePIDWithNewChild] update parent pid (*parentPID) with new child (*childPID)");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    *replica = EUDATGeteValPid(*parentPID, "EUDAT/REPLICA");
    if ((*replica == "") || (*replica == "None")) {
        *replicaNew = *childPID;
    }
    else {
        msiExecCmd("regex_search_string.py","*childPID *replica", "null", "null", "null", *status);
        msiGetStdoutInExecCmdOut(*status, *response);
        if (*response not like "no match found!") {
           *replicaNew = *replica;
        }
        else {
           *replicaNew = *replica ++ "," ++ *childPID;
        }
    }
    msiExecCmd("epicclient.py", "*credStoreType *credStorePath modify *parentPID EUDAT/REPLICA *replicaNew",
               "null", "null", "null", *outUPwNC);
    msiGetStdoutInExecCmdOut(*outUPwNC, *response);
    logDebug("[EUDATUpdatePIDWithNewChild] update handle replica response = *response");
    if (*response != "True") { *replicaNew = "None" }
    *replicaNew;
}

# get the KEY entry for a PID
#
# Parameters:
#   *pid    [IN]     PID that you want to get the Key for
#   *key    [IN]     The name of the PID record field to retrieve
#
# Author: Claudio Cacciari (CINECA)
#-------------------------------------------------------------------------------
EUDATGeteValPid(*pid, *key) {
    logVerbose("[EUDATGeteValPid] get *key from *pid");
    if (*pid == "") {
        # throw error to avoid costly interaction with pid server that will fail anyway
        logError("[EUDATGeteValPid] No PID provided. This will fail.");
        *errorMsg = "Trying to read values from PID when no PID provided.";
        failmsg(-1, *errorMsg); # TODO Return a more suitable return code
    }
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    msiExecCmd("epicclient.py", "*credStoreType *credStorePath read *pid --key *key",
               "null", "null", "null", *outGRP);
    msiGetStdoutInExecCmdOut(*outGRP, *val);
    logVerbose("[EUDATGeteValPid] *key = *val");
    *val;
}

# The function write iPID given ePID.
#
# Parameters:
#   *PID             [IN] ePID
#   *path            [IN] path of the object
#
# Author: Giacomo Mariani, CINECA
# Modified: Elena Erastova, RZG, 27.08.2015
#------------------------------------------------------------------------------
EUDATiPIDcreate(*path, *PID) {
    logVerbose("[EUDATiPIDcreate] adding PID = *PID to *path"); 
    *FVALUE = "None";
    *status0 = bool("true");
    EUDATgetLastAVU(*path, "PID", *FVALUE);
    if(*FVALUE == "None") { 
        EUDATCreateAVU("PID", *PID, *path);
    }
    else if(*FVALUE != *PID) {
        logError("[EUDATiPIDcreate] iCAT attribute PID value *FVALUE != *PID");
        *status0 = bool("false");
    }
    logVerbose("[EUDATiPIDcreate] added PID = *PID");
    *status0;
}

# The function create ePID.
#
# Environment variable used:
#
# Arguments:
#   *path            [IN]   The full iRODS path of the object
#   *extraType       [IN]   extra parameters
#   *PID             [OUT]  The created ePID.
#
# Author: Giacomo Mariani, CINECA
# Edited by:  Robert Verkerk, SURFsara
#-------------------------------------------------------------------------------
EUDATePIDcreate(*path, *extraType, *PID) {

    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) ;
    getHttpApiParameters(*serverApireg, *serverApipub);
    
    *access = "private";
    # Verify that source input path is a collection
    msiGetObjType(*path, *type);
    if (*type != '-c') {
        msiSplitPath(*path, *parent, *child); 
        foreach ( *R in SELECT USER_NAME WHERE DATA_NAME = '*child' AND COLL_NAME = '*parent') {
            if (*R.USER_NAME == "anonymous") {
                *access = "public";
                break;
            }
        }
    }
    else {
        foreach ( *R in SELECT COLL_OWNER_NAME WHERE COLL_NAME = '*path' ) {
            if (*R.COLL_OWNER_NAME == "anonymous") {
                *access = "public";
                break;
            }
        }
    }

    if (*access == "public") {
        *url = "*serverApipub*path";
    }
    else {
        *url = "*serverApireg*path";
    }

    *resource = "";
    EUDATiCHECKSUMget(*path, *checksum, *modtime, *resource);
    if (*checksum != "") {
        if (*extraType != "empty") {
            *extraType = "*extraType"++";EUDAT/CHECKSUM=*checksum";
        } else {
            *extraType = "EUDAT/CHECKSUM=*checksum";
        }
        *execCmd=" epoch_to_iso8601  *modtime";
        msiExecCmd("timeconvert.py","*execCmd","null", "null", "null", *outGRP9);
        msiGetStdoutInExecCmdOut(*outGRP9, *modtime_iso8601);
        *modtime_iso8601 = trimr(*modtime_iso8601, "\n");
        *extraType = "*extraType"++";EUDAT/CHECKSUM_TIMESTAMP=*modtime_iso8601";
    }

    logDebug("[EUDATePIDcreate] Create PID (CHECKSUM:*checksum, OBJPATH:*path) as user: $userNameClient");
    *execCmd="*credStoreType *credStorePath create '*url'";       
    
    if (*extraType != "empty") {
        logVerbose("[EUDATePIDcreate] Create PID with extratype parameter: *extraType");
        *execCmd="*execCmd"++" --extratype \"*extraType\"";
    }

    msiExecCmd("epicclient.py","*execCmd","null", "null", "null", *outGRP2);
    msiGetStdoutInExecCmdOut(*outGRP2, *PID);
    logDebug("[EUDATePIDcreate] Created handle is: *PID");
}

# The function retrieve ePID searching for a field between URL, CHECKSUM. 
#
# Environment variable used:
#   $objPath
#
# Arguments:
#   *field           [IN]    The eField to look in
#   *value           [IN]    The value to search for
#   *PID             [OUT]   ePID
#   *status0         [REI]   false if no value is found, true elsewhere
#
# Author: Giacomo Mariani, CINECA
#-------------------------------------------------------------------------------
EUDATePIDsearch(*field, *value, *PID) {
    logDebug("[EUDATePIDsearch] search the PID with *field = *value");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    *status0 = bool("true");
    msiExecCmd("epicclient.py","*credStoreType *credStorePath search *field *value", "null", "null", "null", *outPidSearch);
    msiGetStdoutInExecCmdOut(*outPidSearch, *PID);
    logDebug("[EUDATePIDsearch] response = *PID");
    # before: 841/test. A single entry.
    # new   : ["841/test"]. An array/list of multiple PID's separated by "," and a space
    if ( str(*PID) == "empty" ) { 
        *status0=bool("false"); 
    } else {
        # remove brackets, quotes and spaces from the "*PID" string
        *outStr=str(*PID);
        foreach ( *char in list("[","]","\""," ") ) {
            *list = split("*outStr","*char");
            *n = "";
            foreach (*t in *list) {
                *n = *n ++ *t;
            }
            *outStr = *n;
        }

        # create a list of PID's
        *PIDlist = split(*outStr, ",");
        # extract the first element of the list 
        *PID=elem(*PIDlist, 0);
    }
    *status0;
}

# This function update the checksum field of the PID  
#
# Arguments:
#   *PID                [IN] The PID associated to the object
#   *path               [IN] Object path
#
# Author: Giacomo Mariani, CINECA
# -------------------------------------------------------------------------------
EUDATeCHECKSUMupdate(*PID, *path) {
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug); 
    logDebug("[EUDATeCHECKSUMupdate] modify checksum related to PID *PID");
    *resource = "";
    EUDATiCHECKSUMget(*path, *checksum, *modtime, *resource);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *PID CHECKSUM *checksum",
               "null", "null", "null", *outeCu);
    msiGetStdoutInExecCmdOut(*outeCu, *response);
    logDebug("[EUDATeCHECKSUMupdate] modify handle response = *response");
}


# This function update the URL field of the PID of $objPath    
#
# Arguments:
#   *PID                [IN] The PID associated to $objPath
#   *newURL             [IN] The new URL to be associated to the PID of $objPath
#
# Author: Giacomo Mariani, CINECA
#-------------------------------------------------------------------------------
EUDATeURLupdate(*PID, *newURL) {
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    logDebug("[EUDATeURLupdate] modify URL in PID *PID");
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *PID URL \"*newURL\"",
               "null", "null", "null", *outEUU);
    msiGetStdoutInExecCmdOut(*outEUU, *response);
    logDebug("[EUDATeURLupdate] modify handle response = *response");
}


# This function update the URL field of the PID of a collection 
# and all its sub-collections and objects.
#
# Arguments:
#   *PID                [IN] The PID associated to the collection
#   *newURL             [IN] The new URL to be associated to the PID of the collection
#
# Author: Claudio Cacciari, CINECA
#-------------------------------------------------------------------------------
EUDATeURLupdateColl(*PID, *newURL) {
    
    logDebug("[EUDATeURLupdateColl] updating collection *PID with URL *newURL and all its content");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    getHttpApiParameters(*serverApireg, *serverApipub);
    *oldURL = EUDATGeteValPid(*PID, "URL");
    if (*oldURL like "*serverApireg\*" ) {
        *serverApi = *serverApireg
    }
    else {
       *serverApi = *serverApipub
    }
    msiStrlen(*serverApi,*serverApiLength);
    msiSubstr(*oldURL, str(int(*serverApiLength)), "null", *sourcePath);
    msiSubstr(*newURL, str(int(*serverApiLength)), "null", *targetPath);
    msiStrlen(*targetPath, *pathLength);

    logDebug("[EUDATeURLupdateColl] loop over the sub-collections of *targetPath"); 
    foreach (*Row in SELECT COLL_NAME WHERE COLL_NAME = '*targetPath' || like '*targetPath/%') {
        logVerbose("[EUDATeURLupdateColl] updating collection " ++ *Row.COLL_NAME);
        msiSubstr(*Row.COLL_NAME, str(int(*pathLength)), "null", *subCollection);
        *sourceColl = "*sourcePath*subCollection"
        if (EUDATSearchPID(*sourceColl, *existing_pid)) {
            *targetColl = *serverApi ++ *Row.COLL_NAME;
            EUDATeURLupdate(*existing_pid, *targetColl);
        }
    }

    logDebug("[EUDATeURLupdateColl] loop over the objects of *targetPath");
    foreach (*Row in SELECT DATA_NAME,COLL_NAME WHERE COLL_NAME = '*targetPath' || like '*targetPath/%') {
        *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
        logVerbose("[EUDATeURLupdateColl] updating object *objPath");
        msiSubstr(*objPath, str(int(*pathLength)), "null", *subObjPath);
        *sourceObj = "*sourcePath*subObjPath";
        if (EUDATSearchPID(*sourceObj, *existing_pid)) {
            *targetObj = *serverApi ++ *objPath;           
            EUDATeURLupdate(*existing_pid, *targetObj);
        }
    }
}

# This function remove an ePID... even if its EUDAT/REPLICA field is not empty!
# To be improved.       
#
# Arguments:
#   *path           [IN]    The path of the object to be removed
#
# Author: Giacomo Mariani, CINECA
#-------------------------------------------------------------------------------
EUDATePIDremove(*path, *force) {
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    logDebug("[EUDATePIDremove] removing PID associated to: $userNameClient, *path");

    if (EUDATSearchPID(*path, *pid)) {
        msiExecCmd("epicclient.py","*credStoreType *credStorePath read --key EUDAT/REPLICA *pid", 
                   "null", "null", "null", *outEPR);
        msiGetStdoutInExecCmdOut(*outEPR, *replica);
        logDebug("[EUDATePIDremove] EUDAT/REPLICA = *replica");
        if (("*replica" like "Error*")||("*replica" == "")||("*replica" like "None*")) {
            logDebug("[EUDATePIDremove] No replicas found: PID *pid will be deleted");
            msiExecCmd("epicclient.py","*credStoreType *credStorePath delete *pid",
                       "null", "null", "null", *outEPR1);
            msiGetStdoutInExecCmdOut(*outEPR1, *response3);
            logDebug("[EUDATePIDremove] removing completed, response = *response3");
        }
        else if (EUDATtoBoolean(*force) == bool("true")){
            logDebug("[EUDATePIDremove] Found replicas: PID *pid will be deleted");
            msiExecCmd("epicclient.py","*credStoreType *credStorePath delete *pid",
                       "null", "null", "null", *outEPR2);
            msiGetStdoutInExecCmdOut(*outEPR2, *response3);
            logDebug("[EUDATePIDremove] removing completed, response = *response3");
        }
        else {
            # The PID record contains pointers to other DO copies.
            # What should we do?
            # Maybe all the copies should be deleted together with the master copy.
            logDebug("[EUDATePIDremove] Found replicas related to PID *pid");
            logDebug("[EUDATePIDremove] nothing has been deleted");
        }
    }
    else {
        logDebug("[EUDATePIDremove] no PID associated to *path found");
    }
} 

# Add or modify the ROR field of the PID of the object to iCAT
#
# Arguments:
#   *source            [IN] Object path
#   *pid               [IN] Object pid
#
# Author: Elena Erastova, RZG 27.08.2015
# -----------------------------------------------------------------------------
EUDATiRORupdate(*source, *pid) {
    logDebug("[EUDATiRORupdate] Add or modify the ROR of *source");
    *iRor = 'None';
    *eRor = EUDATGeteValPid(*pid, "EUDAT/ROR");
    if(*eRor != 'None') {
        EUDATgetLastAVU(*source, "EUDAT/ROR", *iRor);
        if(*iRor != *eRor) {
            EUDATCreateAVU("EUDAT/ROR", *eRor, *source)
        }
    }
    logDebug("[EUDATiRORupdate] EUDAT/ROR = *eRor for *source");
}

# Add or modify the ROR field of the PID in EPIC system
#
# Arguments:
#   *newRor            [IN] The new ROR
#   *pid               [IN] Object pid
#
# Author: Elena Erastova (RZG) [27.08.2015], Claudio Cacciari (CINECA)
#-----------------------------------------------------------------------------
EUDATeRORupdate(*pid, *newRor) {
    logDebug("[EUDATeRORupdate] Add or modify the ROR of *pid");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *pid EUDAT/ROR *newRor", 
               "null", "null", "null", *outRU);
    msiGetStdoutInExecCmdOut(*outRU, *response);
    logDebug("[EUDATeRORupdate] modify handle response = *response");
}

# Add or modify the FIO field of the PID in EPIC system
#
# Arguments:
#   *newFio            [IN] The new FIO
#   *pid               [IN] Object pid
#
# Author: Claudio Cacciari (CINECA)
#-----------------------------------------------------------------------------
EUDATeFIOupdate(*pid, *newFio) {
    logDebug("[EUDATeFIOupdate] Add or modify the FIO of *pid");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *pid EUDAT/FIO *newFio",
               "null", "null", "null", *outFU);
    msiGetStdoutInExecCmdOut(*outFU, *response);
    logDebug("[EUDATeFIOupdate] modify handle response = *response");
}

# Create PIDs for all collections and objects in the collection recursively
# ROR is assumed to be "None"
#
# Parameters:
# *collPath    [IN] path of the collection
# *fixed       [IN] [true | false] it is true if the content of the collection  
#                   and of the objects must not change
#
# Author: Elena Erastova (RZG), Claudio Cacciari (Cineca)
#-----------------------------------------------------------------------------
EUDATPidsForColl(*collPath, *fixed) {

    logInfo("[EUDATPidsForColl] Creating PIDs for collection *collPath and fixed = *fixed");

    # Verify that source input path is a collection
    msiGetObjType(*collPath, *type);
    if (*type != '-c') {
        logError("Input path *collPath is not a collection");
        fail;
    }
    # Create PIDs for all subcollections in collection recursively
    foreach(*RowC in SELECT COLL_NAME WHERE COLL_NAME = '*collPath' || like '*collPath/%') {
        *subCollPath = *RowC.COLL_NAME;
        EUDATCreatePID("None", *subCollPath, "None", "None", *fixed, *newPID);
    }
    # Create PIDs for all data objects in collection recursively
    foreach(*Row in SELECT DATA_NAME,COLL_NAME WHERE COLL_NAME = '*collPath' || like '*collPath/%') {
        *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
        EUDATCreatePID("None", *objPath, "None", "None", *fixed, *newPID);
    }
}
