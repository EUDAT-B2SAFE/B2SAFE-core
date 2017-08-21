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
# EUDATSearchPIDchecksum(*path, *existing_pid)
# EUDATUpdatePIDWithNewChild(*parentPID, *childPID)
# EUDATGeteValPid(*pid, *key)
# EUDATeiChecksumMgmt(*path, *PID)
# EUDATiPIDcreate(*path, *PID)
# EUDATiFieldVALUEretrieve(*path, *FNAME, *FVALUE)
# EUDATePIDcreate(*path, *extraType, *PID)
# EUDATePIDsearch(*field, *value, *PID)
# EUDATeCHECKSUMupdate(*PID, *path)
# EUDATeURLupdate(*PID, *newURL)
# EUDATeURLsearch(*PID, *URL)
# EUDATePIDremove(*path, *force)
# EUDATeiChecksumMgmtColl(*sourceColl)
# EUDATiRORupdate(*source, *pid)
# EUDATeRORupdate(*pid,*newRor)
# EUDATeFIOupdate(*pid, *newFio)
# EUDATPidsForColl(*collPath)
# EUDATePIDcreateCurl(*path, *extraType, *PID, *ifchecksum)
# EUDATSearchPIDCurl(*path, *existing_pid)


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
    logDebug("[EUDATCreatePID] input parameters: parent=*parent_pid, path=*path, ror=*ror, fio=*fio, fixed=*fixed");
    if (!EUDATisMetadata(*path)) {
        getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
        getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);

        #check if PID already exists
        if (*msiCurlEnabled) {
            EUDATSearchPIDCurl(*path, *existing_pid);
        } else {
            EUDATSearchPID(*path, *existing_pid);
        }
   
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
            

            # Verify the type of the input path (collection / data object)
            msiGetObjType(*path, *type);

            # create PID
            EUDATePIDcreate(*path, *extraType, *newPID);
            EUDATiPIDcreate(*path, *newPID);
        
            if (*msiCurlEnabled) {
                # Verify the type of the input path (collection / data object)
                msiGetObjType(*path, *type);
                # If it is a collection - do not compute checksum
                if (*type == '-c') {
                    EUDATePIDcreateCurl(*path, *extraType, *newPID, bool("false"));
                }
                # If it is a data object - compute checksum and add it to PID
                else if (*type == '-d') {
                    EUDATePIDcreateCurl(*path, *extraType, *newPID, bool("true"));
                }
            }
            # creation of ROR in icat in case it has been set to pid
            if (*ror == "pid") {
                EUDATCreateAVU("EUDAT/ROR", *newPID, *path);
            }
            # creation of FIO in icat in case it has been set to pid
            if (*fio == "pid") {
                EUDATCreateAVU("EUDAT/FIO", *newPID, *path);
            }

            # creation of the file based metadata record
            *checksum = "";
            *modtime = "";
            EUDATStoreJSONMetadata(*path, *newPID, *ror, *checksum, *modtime);
        }
        else {
            *newPID = *existing_pid;
            logInfo("[EUDATCreatePID] PID already exists (*newPID)");
        }
    }
    else {
        logInfo("Skipped PID creation on metadata path: *path");
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
    logInfo("[EUDATSearchPID] search pid for *path");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    EUDATReplaceHash(*path, *path1);
    *status = EUDATePIDsearch("URL", "*serverID*path1", *existing_pid);
    *status;
}

# Searching fo a PID using CHECKSUM
# Parameters:
#   *path       	[IN]    the path of the replica
#   *existing_pid	[OUT]   existing PID 
#
# Author: Elena Erastova, RZG
#-------------------------------------------------------------------------------
EUDATSearchPIDchecksum(*path, *existing_pid) {
    logInfo("search pid for *path");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);

    #check if checksum already exists
    *checksum = "";
    msiSplitPath(*path,*parent,*child);
    EUDATiCHECKSUMretrieve(*path, *checksum, *modtime);
    
    if(*checksum == "") {
        *existing_pid ="empty";
    }
    else {
        EUDATePIDsearch("CHECKSUM", *checksum, *existing_pid);
        msiExecCmd("epicclient.py", "*credStoreType *credStorePath read *existing_pid --key URL",
                   "null", "null", "null", *outSPC);
        msiGetStdoutInExecCmdOut(*outSPC, *URL);
        getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
        if (*msiFreeEnabled) {
            msifree_microservice_out(*outSPC);
        }
        if("*serverID*parent" != *parent1) {
            *existing_pid ="empty";
            logInfo("parent  = *serverID*parent ; parent1 = *parent1");
        }

        logInfo("search by CHECKSUM inside PID registry, got PID = *existing_pid");
    }
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
    *replicaNew = "None"
    logInfo("[EUDATUpdatePIDWithNewChild] update parent pid (*parentPID) with new child (*childPID)");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    *replica = EUDATGeteValPid(*parentPID, "EUDAT/REPLICA");
    if ((*replica == "") || (*replica == "None")) {
        *replicaNew = *childPID;
    }
    else {
        *replicaNew = *replica ++ "," ++ *childPID;
    }
    logDebug("[EUDATUpdatePIDWithNewChild] epicclient.py *credStoreType *credStorePath modify *parentPID EUDAT/REPLICA *replicaNew");
    msiExecCmd("epicclient.py", "*credStoreType *credStorePath modify *parentPID EUDAT/REPLICA *replicaNew",
               "null", "null", "null", *outUPwNC);
    msiGetStdoutInExecCmdOut(*outUPwNC, *response);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outUPwNC);
    }
    logDebug("[EUDATUpdatePIDWithNewChild] update handle replica response = *response");
    if (*response != "True") { *replicaNew = "None" }
    *replicaNew
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
    logInfo("[EUDATGeteValPid] get *key from *pid");
    if (*pid == "") {
        logError("[EUDATGeteValPid] No PID provided. This will fail.");
        # TODO throw error here to avoid costly interaction with pid server that will fail anyway.
    }
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    msiExecCmd("epicclient.py", "*credStoreType *credStorePath read *pid --key *key",
               "null", "null", "null", *outGRP);
    msiGetStdoutInExecCmdOut(*outGRP, *val);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outGRP);
    }
    if(*val == "None") {
        logInfo("[EUDATGeteValPid] no *key for *pid ");
    }
    *val
}

# This function creates a PID and stores its value and the checksum in the iCAT if it does not exist.
# Otherwhise the function modifies the PID.
#
# Arguments:
#   *path            [IN]    Path of the source file
#   *PID             [OUT]   PID of the source file
#
# Author: Giacomo Mariani, CINECA; Claudio Cacciari CINECA;
#-------------------------------------------------------------------------------
EUDATeiChecksumMgmt(*path, *PID) {

    *PID = "empty";
    logInfo("[EUDATeiChecksumMgmt] Look if the PID is in the iCAT");
    if (!EUDATiFieldVALUEretrieve(*path, "PID", *PID)) {
        EUDATSearchPID(*path, *PID);
    }
    if ( *PID != "empty" ) {
        logInfo("[EUDATeiChecksumMgmt] Update PID *PID with CHECKSUM for obj *path"); 
        EUDATeCHECKSUMupdate(*PID, *path);  
    }
    else {
        logError("[EUDATeiChecksumMgmt] no PID found")
    }  
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

    *FVALUE = "None";
    *status0 = bool("false");
    EUDATiFieldVALUEretrieve(*path, "PID", *FVALUE);
    if(*FVALUE == "None") { 
        EUDATCreateAVU("PID", *PID, *path);
        *status0 = bool("true");
    }
    else if(*FVALUE != *PID) {
        logError("EUDATiFieldVALUEretrieve (path *path PID *PID) -> "
              ++ "Existing iCAT attribute PID value *FVALUE does not match the input value *PID.");
        *status0 = bool("false");
    }
    else {
        logInfo("EUDATiFieldVALUEretrieve (path *path PID *PID) -> "
             ++ "Attribute PID with value *FVALUE already exists. Nothing to do.");
        *status0 = bool("true");
    }
    *status0;
}

# The function retrieves the value of the required field from iCAT.
#
# Arguments:
#   *path               [IN]    the iRODS path of the object involved in the query
#   *FNAME              [IN]    the name of the iCAT field the function is going to look for
#   *FVALUE             [OUT]   the corresponding value, if any
#   *status0            [REI]   false if no value is found, true elsewhere
#
# Author: Giacomo Mariani, CINECA
#-------------------------------------------------------------------------------
EUDATiFieldVALUEretrieve(*path, *FNAME, *FVALUE) {
    logInfo("EUDATiFieldVALUEretrieve -> looking for *FNAME of *path");
    *status0 = bool("false");
    msiGetObjType(*path,*type);
    if (*type == '-c')  {
        *d = SELECT META_COLL_ATTR_VALUE WHERE COLL_NAME = '*path' AND META_COLL_ATTR_NAME = '*FNAME';
        foreach(*c in *d) {
            *FVALUE = *c.META_COLL_ATTR_VALUE;
            logInfo("EUDATiFieldVALUEretrieve -> *FNAME equal to *FVALUE");
            *status0 = bool("true");
        }
    }
    else {
        msiSplitPath(*path, *coll, *name);
        *d = SELECT META_DATA_ATTR_VALUE WHERE DATA_NAME = '*name' AND COLL_NAME = '*coll' AND META_DATA_ATTR_NAME = '*FNAME'; 
        foreach(*c in *d) {
            *FVALUE = *c.META_DATA_ATTR_VALUE;
            logInfo("EUDATiFieldVALUEretrieve -> *FNAME equal to *FVALUE");
            *status0 = bool("true");
        }
    }
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
    
    *url="*serverID*path";

    EUDATiCHECKSUMget(*path, *checksum, *modtime);
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
        getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
        if (*msiFreeEnabled) {
            msifree_microservice_out(*outGRP9);
        }
         *extraType = "*extraType"++";EUDAT/CHECKSUM_TIMESTAMP=*modtime_iso8601";
    }

    logInfo("[EUDATePIDcreate] Create PID (CHECKSUM:*checksum, OBJPATH:*path) as user: $userNameClient");
    *execCmd="*credStoreType *credStorePath create '*url'";       
    
    if (*extraType != "empty") {
        logInfo("[EUDATePIDcreate] Create PID with extratype parameter: *extraType");
        *execCmd="*execCmd"++" --extratype \"*extraType\"";
    }

    msiExecCmd("epicclient.py","*execCmd","null", "null", "null", *outGRP2);
    msiGetStdoutInExecCmdOut(*outGRP2, *PID);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outGRP2);
    }
    logInfo("[EUDATePIDcreate] Created handle is: *PID");
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
    logInfo("[EUDATePIDsearch] search the PID with *field = *value");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    *status0 = bool("true");
    msiExecCmd("epicclient.py","*credStoreType *credStorePath search *field *value", "null", "null", "null", *outPidSearch);
    msiGetStdoutInExecCmdOut(*outPidSearch, *PID);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outPidSearch);
    }
    logInfo("[EUDATePIDsearch] response = *PID");
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
    EUDATiCHECKSUMget(*path, *checksum, *modtime);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *PID CHECKSUM *checksum",
               "null", "null", "null", *outeCu);
    msiGetStdoutInExecCmdOut(*outeCu, *response);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outeCu);
    }
    logDebug("[EUDATeCHECKSUMupdate] modify handle response = *response");
    *ror = 'None';
    EUDATStoreJSONMetadata(*path, *PID, *ror, *checksum, *modtime);
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
    EUDATeURLsearch(*PID, *oldURL);
    logInfo("EUDATeURLupdate -> modify URL in PID *PID");
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *PID URL \"*newURL\"",
               "null", "null", "null", *outEUU);
    msiGetStdoutInExecCmdOut(*outEUU, *response);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outEUU);
    }
    logInfo("EUDATeURLupdate -> modify handle response = *response");
}

# This function search the URL field of the PID
#
# Arguments:
#   *PID                [IN] The PID associated to $objPath
#   *newURL             [IN] The new URL to be associated to the PID
#
# Author: Giacomo Mariani, CINECA
#-------------------------------------------------------------------------------
EUDATeURLsearch(*PID, *URL) {
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    logInfo("EUDATeURLsearch -> search URL in PID *PID");
    msiExecCmd("epicclient.py","*credStoreType *credStorePath read *PID --key URL ",
               "null", "null", "null", *outEUS);
    msiGetStdoutInExecCmdOut(*outEUS, *URL);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outEUS);
    }
    logInfo("EUDATeURLsearch -> response = *URL");
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
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) 
    logInfo("[EUDATePIDremove] removing PID associated to: $userNameClient, *path");

    if (EUDATSearchPID(*path, *pid)) {
        msiExecCmd("epicclient.py","*credStoreType *credStorePath read --key EUDAT/REPLICA *pid", "null", "null", "null", *outEPR);
        msiGetStdoutInExecCmdOut(*outEPR, *replica);
        getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
        if (*msiFreeEnabled) {
            msifree_microservice_out(*outEPR);
        }
        logDebug("[EUDATePIDremove] EUDAT/REPLICA = *replica");
        if (("*replica" like "Error*")||("*replica" == "")||("*replica" like "None*")) {
            logDebug("[EUDATePIDremove] No replicas found: PID *pid will be deleted");
            msiExecCmd("epicclient.py","*credStoreType *credStorePath delete *pid",
                       "null", "null", "null", *outEPR1);
            msiGetStdoutInExecCmdOut(*outEPR1, *response3);
            getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
            if (*msiFreeEnabled) {
                msifree_microservice_out(*outEPR1);
            }
            logInfo("[EUDATePIDremove] removing completed, response = *response3");
        }
        else if (EUDATtoBoolean(*force) == bool("true")){
            logDebug("[EUDATePIDremove] Found replicas: PID *pid will be deleted");
            msiExecCmd("epicclient.py","*credStoreType *credStorePath delete *pid",
                       "null", "null", "null", *outEPR2);
            msiGetStdoutInExecCmdOut(*outEPR2, *response3);
            getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
            if (*msiFreeEnabled) {
                msifree_microservice_out(*outEPR2);
            }
            logInfo("[EUDATePIDremove] removing completed, response = *response3");
        }
        else {
            # The PID record contains pointers to other DO copies.
            # What should we do?
            # Maybe all the copies should be deleted together with the master copy.
            logDebug("[EUDATePIDremove] Found replicas related to PID *pid");
            logInfo("[EUDATePIDremove] nothing has been deleted");
        }
    }
    else {
        logInfo("[EUDATePIDremove] no PID associated to *path found");
    }
} 

# Walk through the collection. For each object in the collection 
# it creates the object checksum in the iCAT if it does not exist.
# Otherwhise the function modify the PID.
#
# Arguments:
#   *sourceColl      [IN]    Source colection path
#
# Author: Elena Erastova, RZG
# -----------------------------------------------------------------------------
EUDATeiChecksumMgmtColl(*sourceColl) {
    foreach(*Row in SELECT DATA_NAME,COLL_NAME WHERE COLL_NAME like '*sourceColl/%') {
        *objPath = *Row.COLL_NAME ++ '/' ++ *Row.DATA_NAME;
        logInfo("EUDATeiPIDeiChecksumMgmtColl: object *objPath");
	EUDATeiPIDeiChecksumMgmt(*objPath, *pid);
        EUDATiRORupdate(*objPath, *pid);
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
    
    *iRor = 'None';
    *eRor = EUDATGeteValPid(*pid, "EUDAT/ROR");
    if(*eRor != 'None') {
        EUDATiFieldVALUEretrieve(*source, "EUDAT/ROR", *iRor);
        if(*iRor != *eRor) {
            logInfo("EUDATiRORupdate -> Adding/modifying iCAT EUDAT/ROR value 
                     *iRor according to EUDAT/ROR value *eRor for object 
                     *source with PID *pid");
            EUDATCreateAVU("EUDAT/ROR", *eRor, *source)
        }
    }
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

    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *pid EUDAT/ROR *newRor", 
               "null", "null", "null", *outRU);
    msiGetStdoutInExecCmdOut(*outRU, *response);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outRU);
    }
    logInfo("[EUDATeRORupdate] modify handle response = *response");
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
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    msiExecCmd("epicclient.py","*credStoreType *credStorePath modify *pid EUDAT/FIO *newFio",
               "null", "null", "null", *outFU);
    msiGetStdoutInExecCmdOut(*outFU, *response);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outFU);
    }
    logInfo("[EUDATeFIOupdate] modify handle response = *response");
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

    logInfo("[EUDATPidsForColl] Creating PIDs for collection *collPath");

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


# The function create ePID.
#
# Arguments:
#   *path            [IN]   The full iRODS path of the object
#   *extraType       [IN]   extra parameters
#   *ifcheksum       [IN]   boolean value: True if the checksum has to be added
#   *PID             [OUT]  The created ePID.
#
# Author: Giacomo Mariani, CINECA
# Edited by: Robert Verkerk, SURFsara
# Edited by: Javier Quinteros, GFZ
# -------------------------------------------------------------------------------
EUDATePIDcreateCurl(*path, *extraType, *PID, *ifcheksum) {
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) ;

    # Construct here the query to build the PID record
    EUDATReplaceHash(*path, *path1);
    *fullPath = *serverID ++ *path1;
    *PIDRecord = '[{"type": "URL", "parsed_data": "*fullPath"},';
    *PIDRecord = *PIDRecord ++ '{"type": "10320/LOC", "parsed_data": "<locations><location href=\\"*fullPath\\" id=\\"0\\"/></locations>"},';

    # Include field CHECKSUM only if I requested it and I was able to calculate it
    if (*ifcheksum == bool("true") ) {
        logInfo("EUDATePIDcreateCurl -> Add PID with CHECKSUM to: USER, OBJPATH: $userNameClient, *path");
        EUDATiCHECKSUMget(*path, *checksum, *modtime);
        if (*checksum != '') {
            *PIDRecord = *PIDRecord ++ '{"type": "CHECKSUM", "parsed_data": "*checksum"},';
        }
    }

    if (*extraType != "empty") {
        logInfo("EUDATePIDcreateCurl -> Add PID with extratype parameter: *extraType");
        *listET = split("*extraType",";");
        foreach (*kv in *listET) {
            *tupleET = split(*kv, "=");
            *keyET = elem(*tupleET,0);
            *valueET = elem(*tupleET,1);
            *PIDRecord = *PIDRecord ++ '{"type": "*keyET", "parsed_data": "*valueET"},';
        }
    }

    *PIDRecord = trimr(*PIDRecord, ',');
    *PIDRecord = *PIDRecord ++ ']';

    parseCredentials(*baseuri, *user, *prefix, *password);

    if (*baseuri like "http://*") {
        *url = triml(*baseuri, 'http://');
        *protocol = 'http://';
    }
    if (*baseuri like "https://*") {
        *url = triml(*baseuri, 'https://');
        *protocol = 'https://';
    }

    *BaseRequest = *protocol ++ *user ++ ":" ++ *password ++ "@*url*prefix/";

    *postFields."data" = *PIDRecord
    *postFields."headers" = 'Content-type: application/json'

    *PID = 'empty';

    *attempt = 0;
    while ((*PID == 'empty') && (*attempt < 3))
    {
        logInfo("EUDATePIDcreateCurl -> CURL request to create a new PID");
        logDebug("EUDATePIDcreateCurl -> CurlPost(*BaseRequest, *postFields, response)");
        msiCurlPost(*BaseRequest, *postFields, *response);
#        logDebug("EUDATePIDcreateCurl -> Response: *response");
        EUDATSearchPIDCurl(*path1, *PID);
        if (*PID == 'empty')
        {
            logError('Error trying to get PID for *fullPath . Retrying...');
        }
        *attempt = *attempt+1;
    }

    *PID = *prefix ++ '/' ++ *PID
    logInfo("EUDATePIDcreateCurl -> Created handle is: *PID");
}

# Searching for a PID using URL replacing "#", "%" and "&" with "*"
# Parameters:
#   *path               [IN]    the path of the replica
#   *existing_pid       [OUT]   existing PID
#   *status             [REI]   false if no value is found, true elsewhere 
#
# Author: Javier Quinteros, GFZ
# -----------------------------------------------------------------------------
EUDATSearchPIDCurl(*path, *existing_pid) {
    logInfo("search pid for *path");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    parseCredentials(*baseuri, *user, *prefix, *password);

    if (*baseuri like "http://*") {
        *url = triml(*baseuri, 'http://');
        *protocol = 'http://';
    }
    if (*baseuri like "https://*") {
        *url = triml(*baseuri, 'https://');
        *protocol = 'https://';
    }
    *BaseRequest = *protocol ++ *user ++ ":" ++ *password ++ "@*url*prefix/?URL=*serverID";

    # Search if the given file has already an EPIC PID and save in *Path
    EUDATReplaceHash(*path, *path1);
    *Request = *BaseRequest ++ *path1;
    logDebug("EUDATSearchPIDCurl -> msiCurlGetStr(*Request, existing_pid)");
    msiCurlGetStr(*Request, *existing_pid);

    # Read the response and append to the result
    *existing_pid = trimr(*existing_pid, '\n');

    *status = bool("true")
    if(*existing_pid == "") {
        *status = bool("false")
        *existing_pid = "empty"
    }
    *status;
}

