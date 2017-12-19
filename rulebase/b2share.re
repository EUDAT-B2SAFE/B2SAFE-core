################################################################################
#                                                                              #
# EUDAT B2SHARE management rule set                                            #
#                                                                              #
################################################################################


#EUDATListB2shareCommunities(*user) {
#    getConfParameters(*authzEnabled, *b2shareConf);
#    logDebug("[EUDATListB2shareCommunities] Listing b2share communities");
#    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' list communities",
#               "null", "null", "null", *outB2shcl);
#    msiGetStdoutInExecCmdOut(*outB2shcl, *response);
#TODO format the response as a string of community names separated by ","
#    *response;
#}


#EUDATListB2shareDrafts(*user) {
#    getConfParameters(*authzEnabled, *b2shareConf);
#    logDebug("[EUDATListB2shareDraft] Listing b2share drafts");
#    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' list drafts",
#               "null", "null", "null", *outB2shcl);
#    msiGetStdoutInExecCmdOut(*outB2shcl, *response);
#TODO format the response as a string od record ids separated by ","
#    *response;
#}


#EUDATB2shareCommunityToCommunityID(*communityName) {
#}


EUDATCollectionToDraft(*user, *communityName, *title, *path, *adminUser) {

    if (*adminUser == "" || *adminUser == "None") { *adminUser = $userName }
    getConfParameters(*authzEnabled, *b2shareConf);
    logDebug("[EUDATCollectionToDraft] Creating b2share draft");
    logVerbose("[EUDATCollectionToDraft] b2shareclient.py --confpath "
               ++ "'*b2shareConf' -u '*user' draft -c '*communityName' -ti '*title'");

#    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' draft -c '*communityName' -ti '*title'",
#               "null", "null", "null", *outB2shcl);
#    msiGetStdoutInExecCmdOut(*outB2shcl, *recordId);
#    mockup:
    *recordId = "f77de1f5ff5c434d97a54c116737e7d7";

    logVerbose("[EUDATCollectionToDraft] got recordId = *recordId");
    #adding metadata to the collection (overwrite the existing one)
    logVerbose("[EUDATCollectionToDraft] msiSetACL admin:write for '*adminUser' on '*path'");
    msiSetACL("default", "admin:write", *adminUser, *path);
    EUDATCreateAVU("EUDAT_B2SHARE_RECORD_ID", *recordId, *path);
    logVerbose("[EUDATCollectionToDraft] msiSetACL admin:null for '*adminUser' on '*path'");
    msiSetACL("default", "admin:null", *adminUser, *path);
#TODO adding the PIDs of the files inside the collection to the draft    
#    msiExecCmd("b2shareclient.py", "--confpath '*b2shareConf' -u '*user' addFilePIDs -pi '*recordId' -cn '*path'",
#               "null", "null", "null", *outB2shcl);
#    msiGetStdoutInExecCmdOut(*outB2shcl, *response);    
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
EUDATScanForB2shareDrafts(*adminUser) {

     logDebug("[EUDATScanForB2shareDrafts] searching for collection to draft");
     foreach (*Row in SELECT COLL_NAME,META_COLL_ATTR_VALUE WHERE META_COLL_ATTR_NAME = 'EUDAT_B2SHARE_DRAFT') {
         logVerbose("[EUDATScanForB2shareDrafts] found collection '" ++ *Row.COLL_NAME
                                           ++ "' and community '" ++ *Row.META_COLL_ATTR_VALUE  ++ "'");
         *communityName = *Row.META_COLL_ATTR_VALUE;
         *recordId = "recordId";
         EUDATgetLastAVU(*Row.COLL_NAME, 'EUDAT_B2SHARE_RECORD_ID', *recordId);
         logVerbose("[EUDATScanForB2shareDrafts] found recordId = '*recordId'");
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
             *recordId = EUDATCollectionToDraft(*user, *communityName, *title, *path, *adminUser); 
#             *metadataPath = "*path/b2share_metadata.json";
#             EUDATUpdateDraftMetadata(*user, *recordId, *metadataPath);
         }
    }
}

# run as irods admin
EUDATScanForPublishingOnB2share(*publishingPath, *adminUser) {

    if (*adminUser == "" || *adminUser == "None") { *adminUser = $userName }
    logDebug("[EUDATScanForPublishingOnB2share] archive area: '*publishingPath'");
    foreach (*Row in SELECT COLL_NAME,META_COLL_ATTR_VALUE WHERE META_COLL_ATTR_NAME = 'EUDAT_B2SHARE_PUBLISHME') {
        *recordId = "recordId";
        EUDATgetLastAVU(*Row.COLL_NAME, 'EUDAT_B2SHARE_RECORD_ID', *recordId);
        logVerbose("[EUDATScanForPublishingOnB2share] got EUDAT_B2SHARE_RECORD_ID = *recordId");
        if (*recordId != "recordId") {
            
#            msiSetACL("default", "admin:read", *adminUser, *Row.COLL_NAME);
            setRecursiveACL(*Row.COLL_NAME, "admin:write", *adminUser);
            # *publishingPath = /cinecaDMPZone2/publishing
            *destination = *publishingPath ++ triml(*Row.COLL_NAME, "home");
            msiCollCreate(*destination, 1, *status);
            *resource = "";
            EUDATCollCopy(*Row.COLL_NAME, *destination, *resource);
#            msiSetACL("default", "admin:null", *adminUser, *Row.COLL_NAME);
            setRecursiveACL(*Row.COLL_NAME, "admin:null", *adminUser);
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
            setRecursiveACL(*destination, "admin:read", *user);
#            EUDATUpdateDraftPids(*user, *recordId, *destination);
#            EUDATPublishCollection(*user, *recordId);
        }
    }
}

EUDATCollCopy(*src, *dest, *destRes) {

    logDebug("[EUDATCollCopy] copying *src to *dest on the resource '*destRes'");
    *Len = strlen(*src);
    *Query = select DATA_NAME, DATA_CHECKSUM, COLL_NAME where COLL_NAME = '*src';
    foreach(*Row in *Query) {
      *File = *Row.DATA_NAME;
      *Check = *Row.DATA_CHECKSUM;
      *Coll = *Row.COLL_NAME;
      *L1 = strlen(*Coll);
      *Src1 = *Coll ++ "/" ++ *File;
      if (strlen(*Check) < 1) {
          msiDataObjChksum(*Src1, "forceChksum=", *Check);
      }
      *C1 = substr(*Coll,*Len,*L1);
      if (strlen(*C1)==0) {
         *DestColl = *dest;
         *Dest1 = *dest ++ "/" ++ *File;
      } else {
         *DestColl = *dest ++ *C1;
         *Dest1 = *dest ++ *C1 ++ "/" ++ *File;
      }
      isColl(*DestColl, "serverLog", *Status1);
      if (*Status1 == 0) {
        isData(*DestColl, *File, *Status);
        if (*Status == "0") {
          writeLine("serverLog", "msiDataObjCopy(*Src1,*Dest1,destRescName=*destRes++++forceFlag=, *Status)");
          msiDataObjCopy(*Src1,*Dest1,"destRescName=*destRes++++forceFlag=++++verifyChksum=", *Status3);
          writeLine("serverLog", "copied");
          msiSetACL("default","own",$userNameClient, *Dest1);
          writeLine("serverLog", "changed ACL");
          msiDataObjChksum(*Dest1, "forceChksum=", *Chksum);
          writeLine("serverLog", "calculated checksum: *Chksum");
          writeLine("serverLog", "original checksum: *Check");
          if (*Check != *Chksum) {
            writeLine("serverLog", "Bad checksum for file *Dest1");
          }
          else {
            writeLine("serverLog", "Moved file *Src1 to *Dest1");
          }
        }
      }
    }

}

isColl (*LPath, *Lfile, *Status) {
  *Status = 0;
  *Query0 = select count(COLL_ID) where COLL_NAME = '*LPath';
  foreach(*Row0 in *Query0) {*Result = *Row0.COLL_ID;}
  writeLine("*Lfile","Found collection: *Result");
  if(*Result == "0" ) {
    msiCollCreate(*LPath, "1", *Status);
    if(*Status < 0) {
      writeLine("*Lfile","Could not create *LPath collection");
    }
  }
}

isData (*Coll, *File, *Status) {
  *Status = "0";
  *Q = select count(DATA_ID) where COLL_NAME = '*Coll' and DATA_NAME = '*File';
  foreach (*R in *Q) {
    writeLine("serverLog", "Data ID: " ++ *R.DATA_ID);
    *Status = *R.DATA_ID;
  }
  *Status;
}

setRecursiveACL(*Coll, *acl, *user) {
    *Q = select DATA_NAME, COLL_NAME where COLL_NAME = '*Coll' || like '*Coll/%';
    foreach (*R in *Q) {
        *path = *R.COLL_NAME ++ "/" ++ *R.DATA_NAME;
        msiSetACL("default", *acl, *user, *R.COLL_NAME);
        msiSetACL("default", *acl, *user, *path);
    }
}
