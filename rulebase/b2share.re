################################################################################
#                                                                              #
# EUDAT B2SHARE management rule set                                            #
#                                                                              #
################################################################################


EUDATListB2shareCommunities(*user) {
    getConfParameters(*authzEnabled, *b2shareConf);
    logDebug("[EUDATListB2shareCommunities] Listing b2share communities");
    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' list communities",
               "null", "null", "null", *outB2shcl);
    msiGetStdoutInExecCmdOut(*outB2shcl, *response);
#TODO format the response as a string of community names separated by ","
    *response;
}


EUDATListB2shareDrafts(*user) {
    getConfParameters(*authzEnabled, *b2shareConf);
    logDebug("[EUDATListB2shareDraft] Listing b2share drafts");
    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' list drafts",
               "null", "null", "null", *outB2shcl);
    msiGetStdoutInExecCmdOut(*outB2shcl, *response);
#TODO format the response as a string od record ids separated by ","
    *response;
}


#EUDATB2shareCommunityToCommunityID(*communityName) {
#}


EUDATCollectionToDraft(*user, *communityName, *title, *path) {
    getConfParameters(*authzEnabled, *b2shareConf);
    logDebug("[EUDATCollectionToDraft] Creating b2share draft");
    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' draft -c '*communityName' -ti '*title'",
               "null", "null", "null", *outB2shcl);
    msiGetStdoutInExecCmdOut(*outB2shcl, *recordId);
    #adding metadata to the collection (overwrite the existing one)
    EUDATCreateAVU("EUDAT_B2SHARE_RECORD_ID", *recordId, *path);
#TODO adding the PIDs of the files inside the collection to the draft    
    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' addFilePIDs -pi '*recordId' -cn '*path'",
               "null", "null", "null", *outB2shcl);
    msiGetStdoutInExecCmdOut(*outB2shcl, *response);    
    *recordId;
}


#EUDATRemoveDraft() {
#}


EUDATUpdateDraftMetadata(*user, *recordId, *metadataPath) {
    getConfParameters(*authzEnabled, *b2shareConf);
    logDebug("[EUDATUpdateDraftMetadata] Updating b2share draft metadata");
    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' meta -id '*recordId' -md '*metadataPath'",
               "null", "null", "null", *outB2shcl);
    msiGetStdoutInExecCmdOut(*outB2shcl, *response);
}


EUDATUpdateDraftPids(*user, *recordId, *path) {
    getConfParameters(*authzEnabled, *b2shareConf);
    logDebug("[EUDATUpdateDraftPids] Updating b2share draft pids");
    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' updateFilePIDs -pi '*recordId' -cn '*path'", "null", "null", "null", *outB2shcl);
    msiGetStdoutInExecCmdOut(*outB2shcl, *response);
}


EUDATPublishCollection(*user, *recordId) {
    getConfParameters(*authzEnabled, *b2shareConf);
    logDebug("[EUDATPublishCollection] Publishing b2share draft");
    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' pub -pi '*recordId'",
               "null", "null", "null", *outB2shcl);
    msiGetStdoutInExecCmdOut(*outB2shcl, *response);
}

# run as irods admin
EUDATScanForB2shareDrafts() {

     foreach (*Row in SELECT COLL_NAME,META_COLL_ATTR_VALUE WHERE META_COLL_ATTR_NAME = 'EUDAT_B2SHARE_DRAFT') {
        *communityName = "*Row.META_COLL_ATTR_VALUE";
        *recordId = "recordId";
        EUDATgetLastAVU(*Row.COLL_NAME, 'EUDAT_B2SHARE_RECORD_ID', *recordId);
        if (*communityName != "" && *recordId != "recordId") {
            *title = *Row.COLL_NAME;
            *path = *Row.COLL_NAME;
            *owners = list();
            foreach ( *R in SELECT COLL_OWNER_NAME WHERE COLL_NAME = '*path' ) {
                *owners = cons(*R.COLL_OWNER_NAME, *owners);
            }
            *user = "";
            if (size(*owners) > 0) {
                *user = hd(*owners);
            }
            *recordId = EUDATCollectionToDraft(*user, *communityName, *title, *path); 
            *metadataPath = "*path/b2share_metadata.json";
            EUDATUpdateDraftMetadata(*user, *recordId, *metadataPath);
        }
    }
}

# runa as irods admin
EUDATScanForPublishingOnB2share(*publishingPath) {

    foreach (*Row in SELECT COLL_NAME,META_COLL_ATTR_VALUE WHERE META_COLL_ATTR_NAME = 'EUDAT_B2SHARE_PUBLISHME') {
        *recordId = "recordId";
        EUDATgetLastAVU(*Row.COLL_NAME, 'EUDAT_B2SHARE_RECORD_ID', *recordId);
        if (*recordId != "recordId") {
            msiSetACL("recursive", "read", $userName, *Row.COLL_NAME);
            # *publishingPath = /cinecaDMPZone2/publishing
            *destination = *publishingPath ++ triml(*Row.COLL_NAME, "home");
            msiCollCreate(*destination, 1, *status);
#TODO verify if it works: msiCollRsync from local to local
            msiCollRsync(*Row.COLL_NAME, *destination);
            *fixed = "true";
            EUDATPidsForColl(*destination, *fixed);
            *owners = list();
            *path = *Row.COLL_NAME;
            foreach ( *R in SELECT COLL_OWNER_NAME WHERE COLL_NAME = '*path' ) {
                *owners = cons(*R.COLL_OWNER_NAME, *owners);
            }
            *user = "";
            if (size(*owners) > 0) {
                *user = hd(*owners);
            }
            EUDATUpdateDraftPids(*user, *recordId, *destination);
            EUDATPublishCollection(*user, *recordId);
        }
    }
}

