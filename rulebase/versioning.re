###############################################################################################
#                                                                                             #
#  Module Versioning:                                                                         #
#    - enable creation of version of single file WITHOUT pid registration                     # 
#    - enable creation of version of single file WITH pid registration                        #  
#    - enable creation of versions of all files of collection WITHOUT pid registration        #
#    - enable creation of versions of all files of collection and its subcollections          # 
#      recusively WITHOUT pid registration                                                    #
#    - enable creation of versions of all files of collection WITH pid registration           #
#    - enable creation of versions of all files of collection and its subcollections          # 
#      recusively WITH pid registration                                                       #
#    - display list of all versions of a given file nicely ordered by version number          #
#                                                                                             #
###############################################################################################

# List of the functions:
# 
# EUDATVersioning(*source, *destination, *registered, *recursive, *response)
# EUDATCreateVersion(*withPID, *source, *destination, *recursive, *response)
# EUDATCreateVersionOfDataObjRegPID(*source, *destination, *status)
# EUDATCreateVersionOfDataObj(*source, *destination, *status)
# EUDATGetAllVersionsOfDataObj(*source, *destination, *ListOfAllVersions)
# EUDATListAllVersionsOfDataObjNoPID(*source, *destination)
# EUDATListAllVersionsOfDataObjWithPID(*source)
# EUDATPullVersionWithPID(*versNumber, *source, *destination, *status)
# EUDATPullVersionNoPID(*versNumber, *source, *versPath, *destination, *status)
# EUDATVersioningSearchAndCreatePID(*path, *pid)
# EUDATVersioningPIDRegistration(*parentPID, *source, *destination, *notification, *do_version, *prevVersionPath, *prevVersionPID, *registration_response)


VERSION_SUFFIX = "__v"
MAX_NUM_OF_VERSIONS = 5

#------------------------------------------------------------------------------------------
# Data set versioning
#
# Parameters:
#    *source            [IN] path of the source data set in iRODS
#    *destination       [IN] destination of versioning in iRODS
#    *registered        [IN] boolean value: "true" for registered data, "false" otherwise
#    *recursive         [IN] boolean value: "true" to enable the recursive versioning
#                            of registered data, "false" otherwise
#    *response          [OUT]the result of the versioning
# 
# Author: Alexander Atamas, DANS
#------------------------------------------------------------------------------------------

EUDATVersioning(*source, *destination, *registered, *recursive, *response){

  logInfo("[EUDATVersioning] from *source to *destination"); 
  *status = bool("true");
  *response = "";

  # Catch Error CAT_NO_ACCESS_PERMISSION before versioning
  if (errormsg(EUDATCatchErrorDataOwner(*source,*msg), *errmsg) < 0) {

      logDebug("*errmsg");
      *status = bool("false");
      *response = "no access permission to the path *source for user $userNameClient";
      EUDATUpdateLogging(*status,*source,*destination,*response);

  } else {
      
      logInfo("[EUDATVersioning] *msg");

      if (EUDATtoBoolean(*registered)) {
            logDebug("Versioning data with PID registration");
            *withPID = "true"; 
            *status = EUDATCreateVersion(*withPID, *source, *destination, EUDATtoBoolean(*recursive), *response);
      } else {
            *withPID = "false";
            logDebug("Versioning data without PID registration");
            *status = EUDATCreateVersion(*withPID, *source, *destination, EUDATtoBoolean(*recursive), *response);
      }
  }

  if (*status) { *response = "*source::*destination::registered=*registered::recursive=*recursive" }
  EUDATGetZoneNameFromPath(*source, *zone);
  *queue = *zone ++ "_" ++ $userNameClient;
  *message = "status:*status;response:*response"
  EUDATMessage(*queue, *message);
  
  *status;

}


#--------------------------------------------------------------------------------------------------
# Creates(WITH pid registration, if the parameter *withPID == "true", 
#          WITHOUT pid registration, if the parameter *withPID == "false")
#   a version of either:
#         - all files of collection, if source type is a collection 
#         - all files of collection and subcollections recursively, if source type is a collection 
#         - one file, if source type is a data object and not a collection
#
# Parameters:
#    *source            [IN] path of the source data set in iRODS
#    *destination       [IN] destination of versioning in iRODS
#    *recursive         [IN] boolean value: "true" to enable the recursive versioning
#                            of registered data, "false" otherwise
#    *response          [OUT]the result of the versioning
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATCreateVersion(*withPID, *source, *destination, *recursive, *response){
  
      *status = bool("true");
      *responses = "";
      msiGetObjType(*source, *source_type);

      if (*source_type == '-c'){

        foreach(*SrcRow in SELECT DATA_NAME WHERE COLL_NAME = '*source') {
          *ScrDataObjName = *SrcRow.DATA_NAME;
          *Source = *source ++ "/" ++ *ScrDataObjName;
          if (*withPID == "true"){
              *dataCopyStatus = EUDATCreateVersionOfDataObjRegPID(*Source, *destination, *dataCopyStatus);
          }else if (*withPID == "false"){
              *dataCopyStatus = EUDATCreateVersionOfDataObj(*Source, *destination, *dataCopyStatus);
          }
          if ( *dataCopyStatus != 0 ){
              *contents = *Source ++ '::*destination::false::*dataCopyStatus';
              *responses = *responses ++ *contents ++ ",";
          }
          *status = (*dataCopyStatus == 0) && *status;
        }
   
        if ( *status && *recursive ){
         foreach (*RowSrcSubColl in SELECT COLL_NAME WHERE COLL_NAME LIKE '*source/%' ){
           *RowSrcSubCollPath = *RowSrcSubColl.COLL_NAME;
           foreach (*Row in SELECT DATA_NAME WHERE COLL_NAME LIKE '*RowSrcSubCollPath' ){
             *ScrSubCollDataObjName = *Row.DATA_NAME;
             *Source = *RowSrcSubCollPath ++ "/" ++ *ScrSubCollDataObjName;
             msiStrlen(*source, *pathLength);
             msiSubstr(*RowSrcSubCollPath, str(int(*pathLength)+1), "null", *subCollection);
             *Dest = *destination ++"/" ++ *subCollection; 
             if (*withPID == "true"){
                 *dataCopyStatus = EUDATCreateVersionOfDataObjRegPID(*Source, *Dest, *dataCopyStatus);
             }else if (*withPID == "false"){
                 *dataCopyStatus = EUDATCreateVersionOfDataObj(*Source, *Dest, *dataCopyStatus);
             }
             if ( *dataCopyStatus != 0 ){
                 *contents = *Source ++ '::*destination::false::*dataCopyStatus';
                 *responses = *responses ++ *contents ++ ",";
             }
             *status = (*dataCopyStatus == 0) && *status;
           }
         }
        }

      } else if (*source_type == '-d'){
           if (*withPID == "true"){
               *dataCopyStatus = EUDATCreateVersionOfDataObjRegPID(*source, *destination, *dataCopyStatus);
           }else if (*withPID == "false"){
               *dataCopyStatus = EUDATCreateVersionOfDataObj(*source, *destination, *dataCopyStatus);
           }
           if ( *dataCopyStatus != 0 ){
               *contents = *Source ++ '::*destination::false::*dataCopyStatus';
               *responses = *responses ++ *contents ++ ",";
               *status = bool("false");
           }
      }
      *response = trimr(*responses, ",");

      *status;

}


#--------------------------------------------------------------------------------------------------
# Creates a copy of one data object WITH pid registration
#
# Parameters:
#    *source             [IN] path of the source data object to make version of 
#    *destination        [IN] destination of the version created
#    *status            [OUT] the result of data object copying and registration performed
#                             by microservice "msiDataObjCopy" and function "EUDATVersioningPIDRegistration",
#                             respectively
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATCreateVersionOfDataObjRegPID(*source, *destination, *status){

  *versionNumbPrefixStr = VERSION_SUFFIX;
  *ListOfVersions = list();
  EUDATGetAllVersionsOfDataObj(*source, *destination, *ListOfVersions);
  
  *ExistingVersNum = 0;
  msiStrlen(*versionNumbPrefixStr,*versionNumbPrefixStrLen);
  msiSplitPath(*source, *path, *File);
  msiStrlen(*path, *pathLength);
  msiSubstr(*source, str(int(*pathLength)+1), "null", *ScrDataObjName);

  *prevVersion = "None";

  foreach (*DestRow in *ListOfVersions) {
    *DestDataObjName = *DestRow;
    msiStrlen(*ScrDataObjName,*ScrDataObjNameStrLen); 
    msiStrlen(*DestDataObjName,*DestDataObjNameStrLen);
    *offset = int(*ScrDataObjNameStrLen) + int(*versionNumbPrefixStrLen);
    msiSubstr(*DestDataObjName, str(*offset), "null", *vers);
    *vers = int(*vers);
    if (*vers > *ExistingVersNum) {
          *ExistingVersNum = *vers;
          *prevVersion = *DestRow;
    }	
  }

  *NewVers = *ExistingVersNum + 1;

  *max_num_vers = MAX_NUM_OF_VERSIONS;
  if ( *NewVers > *max_num_vers){
	writeLine("stdout","Cannot create a version number *NewVers of \"*ScrDataObjName\".\nMaximum number of versions allowed is *max_num_vers");
	fail;
  }

  *LatestVers = *ScrDataObjName ++ *versionNumbPrefixStr ++ "*NewVers";
  *destinationVers = *destination ++ "/" ++ *LatestVers;

  *status = -1;
  *statusPID = bool("true");
  # initial value of parentPID
  *parentPID = "None";

  # search and create pid related to the source of the versioning
  EUDATVersioningSearchAndCreatePID(*source, *parentPID);

  if (*parentPID == "empty" || (*parentPID == "None")) {
    *statusPID = bool("false");
    # check to skip metadata special path
    if (!EUDATisMetadata(*source)) {
        *response = "PID is empty, no versioning will be executed for *source";
        EUDATUpdateLogging(*statusPID,*source,*destination,"empty PID");
    }
    else {
        *response = "the path '*source' is a special metadata path: it cannot be registered";
        EUDATUpdateLogging(*statusPID,*source,*destination,"reserved metadata path");
    }
    logDebug(*response);
  }
  else {
      logDebug("PID exist for *source");

      msiDataObjCopy(*source, *destinationVers, "", *status);

      if ( *status == 0 ){

          *prevVersionPID = "None";
          if ( *ExistingVersNum != 0 ) {
            *prevVersion = *destination ++ "/" ++ *prevVersion;
            EUDATVersioningSearchAndCreatePID(*prevVersion, *prevVersionPID);
          }

          *notification = 0;
          *versionPID = EUDATVersioningPIDRegistration(*parentPID, *source, *destinationVers, *notification, str(*NewVers), *prevVersion, *prevVersionPID, *singleResponse);
          if (*singleResponse != "None") { *status = -1 }

          writeLine("stdout","Version \"*LatestVers\" is created with PID = *versionPID\n         in *destination\nof source file \"*File\" with PID = *parentPID");

      }
      else if (*status != 0) {
          logDebug("perform a further verification about checksum and size");
          *logEnabled = bool("true");
          *notification = 0;
          *status = EUDATCheckIntegrity(*source,*destinationVers,*logEnabled,*notification,*response);
      }

  }

  *status;
}

#--------------------------------------------------------------------------------------------------
# Creates a copy of one data object WITHOUT pid registration
#
# Parameters:
#    *source             [IN] path of the source data object to make version of 
#    *destination        [IN] destination of the version created 
#    *status             [OUT] the result of data object copying performed by microservice "msiDataObjCopy"  
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATCreateVersionOfDataObj(*source, *destination, *status){
   
  *versionNumbPrefixStr = VERSION_SUFFIX;
  *ListOfVersions = list();
  EUDATGetAllVersionsOfDataObj(*source, *destination, *ListOfVersions);
  
  *ExistingVersNum = 0;
  msiStrlen(*versionNumbPrefixStr,*versionNumbPrefixStrLen);
  msiSplitPath(*source, *path, *File);
  msiStrlen(*path, *pathLength);
  msiSubstr(*source, str(int(*pathLength)+1), "null", *ScrDataObjName);

  foreach (*DestRow in *ListOfVersions) {
    *DestDataObjName = *DestRow;
    msiStrlen(*ScrDataObjName,*ScrDataObjNameStrLen); 
    msiStrlen(*DestDataObjName,*DestDataObjNameStrLen);
    *offset = int(*ScrDataObjNameStrLen) + int(*versionNumbPrefixStrLen);
    msiSubstr(*DestDataObjName, str(*offset), "null", *vers);
    *vers = int(*vers);
    if (*vers > *ExistingVersNum) {
          *ExistingVersNum = *vers;
    }	
  }

  *NewVers = *ExistingVersNum + 1;

  *max_num_vers = MAX_NUM_OF_VERSIONS;
  if ( *NewVers > *max_num_vers){
	writeLine("stdout","Cannot create a version number *NewVers of \"*ScrDataObjName\".\nMaximum number of versions allowed is *max_num_vers");
	fail;
  }

  *LatestVers = *ScrDataObjName ++ *versionNumbPrefixStr ++ "*NewVers";
  *destinationVers = *destination ++ "/" ++ *LatestVers;

   msiDataObjCopy(*source, *destinationVers, "", *status);

   if ( *status == 0 ){

       EUDATiCHECKSUMget(*destinationVers, *checksum, *modtime);

       EUDATCreateAVU("EUDAT/DO_VERSION_NUMBER", str(*NewVers), *destinationVers);
       EUDATCreateAVU("EUDAT/FIXED_CONTENT", "True", *destinationVers);
       EUDATCreateAVU("EUDAT/CHECKSUM", *checksum, *destinationVers);

       *execCmd=" epoch_to_iso8601  *modtime";
       msiExecCmd("timeconvert.py","*execCmd","null", "null", "null", *outGRP9);
       msiGetStdoutInExecCmdOut(*outGRP9, *modtime_iso8601);
       *modtime_iso8601 = trimr(*modtime_iso8601, "\n");
       getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
       if (*msiFreeEnabled) {
              msifree_microservice_out(*outGRP9);
       }
       EUDATCreateAVU("EUDAT/CHECKSUM_TIMESTAMP", *modtime_iso8601, *destinationVers);

       writeLine("stdout","Version \"*LatestVers\" is created in *destination");
   }
   else if (*status != 0) {
       logDebug("perform a further verification about checksum and size");
       *logEnabled = bool("true");
       *notification = 0;
       *status = EUDATCheckIntegrity(*source,*destinationVers,*logEnabled,*notification,*response);
   }

  *status;
}

#--------------------------------------------------------------------------------------------------
# Looks for existing versions of a given data object and returns a list of all versions found
#
# Parameters:
#    *source             [IN] path of the source data object to find existing versions of 
#    *destination        [IN] destination where to look for existing versions
#    *ListOfAllVersions  [OUT] list of all versions existing in *destionation for a given data object  
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATGetAllVersionsOfDataObj(*source, *destination, *ListOfAllVersions){

  *versionNumbPrefixStr = VERSION_SUFFIX;
  msiStrlen(*versionNumbPrefixStr,*versionNumbPrefixStrLen);
  msiSplitPath(*source, *path, *File);
  msiStrlen(*path, *pathLength);
  msiSubstr(*source, str(int(*pathLength)+1), "null", *ScrDataObjName);
  *strQueryLike = *ScrDataObjName ++ *versionNumbPrefixStr ++ "%";
  *AllDestRows = SELECT DATA_NAME WHERE COLL_NAME = '*destination' and DATA_NAME like '*strQueryLike';

  foreach (*DestRow in *AllDestRows) {
    *ListOfAllVersions = cons(*DestRow.DATA_NAME, *ListOfAllVersions);
  }

}

#--------------------------------------------------------------------------------------------------
# Pulls back a version of a file without PID
#
# Parameters:
#    *versNumber         [IN] a number of version to be pulled to *destination, if *versNumber = "latest" than the latest version is pulled
#    *source             [IN] path of the source data object 
#    *versPath           [IN] path to directory where versions stored 
#    *destination        [IN] destination where to pull a specified version
#    *status             [OUT] status of the pull function
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATPullVersionNoPID(*versNumber, *source, *versPath, *destination, *status){

     *status = -1;
     *listOfVersions = list();
     EUDATGetAllVersionsOfDataObj(*source, *versPath, *listOfVersions);
     *totalNumbOfVersions = size(*listOfVersions);

     *latestVersNum = *totalNumbOfVersions;
     *firstVersNum  = 1;

       *versString = str(*versNumber);

       if ( *versString == "latest" ){
           *versToPull = *latestVersNum;
       } else {
           *vers = int(*versNumber);
           *versToPull = *vers;
       }

       *max_num_vers = MAX_NUM_OF_VERSIONS;
       if ( *versToPull > *max_num_vers){
	    writeLine("stdout","Cannot pull a version number *versToPull. The latest version is *max_num_vers");
	    fail;
       }

       if ( *versToPull >= *firstVersNum && *versToPull <= *latestVersNum ){

            msiSplitPath(*source, *sourcePath, *sourceFile);
            *versName = *sourceFile ++ VERSION_SUFFIX ++ str(*versToPull)
            *destPath = *destination ++ "/" ++ *versName;
            *scrPath = *versPath ++ "/" ++ *versName;

            msiDataObjCopy(*scrPath, *destPath, "", *status);

            if ( *status == 0 ){

              writeLine("stdout", "Version \"*versName\" of \"*sourceFile\" is pulled to *destination");

              EUDATCreateAVU("EUDAT/FIXED_CONTENT", "false", *destPath);
              EUDATiCHECKSUMget(*destPath, *checksum, *modtime);
              EUDATCreateAVU("EUDAT/CHECKSUM", *checksum, *destPath);

              *execCmd=" epoch_to_iso8601  *modtime";
              msiExecCmd("timeconvert.py","*execCmd","null", "null", "null", *outGRP9);
              msiGetStdoutInExecCmdOut(*outGRP9, *modtime_iso8601);
              *modtime_iso8601 = trimr(*modtime_iso8601, "\n");
              getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
              if (*msiFreeEnabled) {
                msifree_microservice_out(*outGRP9);
              }
              EUDATCreateAVU("EUDAT/CHECKSUM_TIMESTAMP", *modtime_iso8601, *destPath);
            }
       }

  *status;
}

#--------------------------------------------------------------------------------------------------
# Pulls back a version of a registered file with PID
#
# Parameters:
#    *versNumber         [IN] a number of version to be pulled to *destination, if *versNumber = "latest" than the latest version is pulled
#    *source             [IN] path of the source data object 
#    *destination        [IN] destination where to pull a specified version 
#    *status             [OUT] status of the pull function
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATPullVersionWithPID(*versNumber, *source, *destination, *status){

  *status = -1;
  getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
  getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);

  if (*msiCurlEnabled) {
      EUDATSearchPIDCurl("*source", *sourcePID);
  } else {
      EUDATSearchPID("*source", *sourcePID);
  }

  if (*sourcePID != "empty" && *sourcePID != "None") {

       *latestVersPID = EUDATGeteValPid(*sourcePID, "EUDAT/LATEST_VERSION");
       *firstVersPID  = EUDATGeteValPid(*sourcePID, "EUDAT/WAS_DERIVED_FROM");
       *latestVersNum = int(EUDATGeteValPid(*latestVersPID, "EUDAT/DO_VERSION_NUMBER"));
       *firstVersNum  = int(EUDATGeteValPid(*firstVersPID, "EUDAT/DO_VERSION_NUMBER"));

       *versString = str(*versNumber);

       if ( *versString == "latest" ){
           *versPID = *latestVersPID;
       } else {
           *vers = int(*versNumber);

           *max_num_vers = MAX_NUM_OF_VERSIONS;
           if ( *vers > *max_num_vers){
	      writeLine("stdout","Cannot pull a version number *vers. The latest version is *max_num_vers");
	      fail;
           }

          if ( *vers == *latestVersNum ){
            *versPID = *latestVersPID;
          } 
          if ( *vers == *firstVersNum ){
            *versPID = *firstVersPID;
          }
          if ( *vers > *firstVersNum && *vers < *latestVersNum ){

             *diffWithLast   = abs(*vers - *latestVersNum);
             *diffWithFirst  = abs(*vers - *firstVersNum);

             if ( *diffWithLast < *diffWithFirst ){
                 *field = "EUDAT/REVISION_OF";
                 *versPID = *latestVersPID;
                 *n = *diffWithLast;
             } else {
                 *field = "EUDAT/WAS_DERIVED_FROM";
                 *versPID = *firstVersPID;
                 *n = *diffWithFirst;
             }
             *versPID = EUDATGeteValPid(*versPID, *field);

             for (*i=1; *i<=(*n-1); *i=*i+1) {
                 *versPID = EUDATGeteValPid(*versPID, *field);
             }

          }
       }

       *versURL = EUDATGeteValPid(*versPID, "URL");

       *versPath = triml(*versURL, "//");
       *versPath = "/" ++ triml(*versPath, "/");
       msiSplitPath(*versPath, *path, *versFile);
       *dest = *destination ++ "/" ++ *versFile;
       msiSplitPath(*source, *sourcePath, *sourceFile);

       msiDataObjCopy(*source, *dest, "", *status);

       if ( *status == 0 ){

          writeLine("stdout", "Version \"*versFile\" of \"*sourceFile\" is pulled to *sourcePath");

          *ror = EUDATGeteValPid(*versPID, "EUDAT/ROR");
          *fio = EUDATGeteValPid(*versPID, "EUDAT/FIO");

          EUDATCreatePID(*sourcePID, *dest, *ror, *fio, "false", *newPID);
          writeLine("stdout", "Its new PID is *newPID");

          EUDATCreateAVU("EUDAT/ROR", *ror, *dest);
          EUDATCreateAVU("EUDAT/FIO", *fio, *dest);
          EUDATCreateAVU("PID", *newPID, *dest);
          EUDATCreateAVU("EUDAT/FIXED_CONTENT", "false", *dest);
          EUDATiCHECKSUMget(*dest, *checksum, *modtime);
          EUDATCreateAVU("EUDAT/CHECKSUM", *checksum, *dest);

          *execCmd=" epoch_to_iso8601  *modtime";
          msiExecCmd("timeconvert.py","*execCmd","null", "null", "null", *outGRP9);
          msiGetStdoutInExecCmdOut(*outGRP9, *modtime_iso8601);
          *modtime_iso8601 = trimr(*modtime_iso8601, "\n");
          getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
          if (*msiFreeEnabled) {
              msifree_microservice_out(*outGRP9);
          }
          EUDATCreateAVU("EUDAT/CHECKSUM_TIMESTAMP", *modtime_iso8601, *dest);
       }
  }

  *status;

}


#--------------------------------------------------------------------------------------------------
# Lists all existing versions of a given data object with PID and prints them out on screen 
#
# Parameters:
#    *source             [IN] path of the source data object which versions we want to list
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATListAllVersionsOfDataObjWithPID(*source){

  getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
  getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);

  if (*msiCurlEnabled) {
      EUDATSearchPIDCurl("*source", *sourcePID);
  } else {
      EUDATSearchPID("*source", *sourcePID);
  }

  if (*sourcePID != "empty" && *sourcePID != "None") {

       *latestVersPID = EUDATGeteValPid(*sourcePID, "EUDAT/LATEST_VERSION");
       *firstVersPID  = EUDATGeteValPid(*sourcePID, "EUDAT/WAS_DERIVED_FROM");
       *latestVersNum = int(EUDATGeteValPid(*latestVersPID, "EUDAT/DO_VERSION_NUMBER"));
       *firstVersNum  = int(EUDATGeteValPid(*firstVersPID, "EUDAT/DO_VERSION_NUMBER"));

       *versPID = *firstVersPID;

       for (*i=1; *i<=*latestVersNum; *i=*i+1) {
           *versURL = EUDATGeteValPid(*versPID, "URL");

           *versPath = triml(*versURL, "//");
           *versPath = "/" ++ triml(*versPath, "/");
           msiSplitPath(*versPath, *path, *versFile);
           writeLine ("stdout", "*versPath");
           if ( *i < *latestVersNum ){
               *versPID = EUDATGeteValPid(*versPID, "EUDAT/WAS_DERIVED_FROM");
           }else{
               *versPID = *latestVersPID;      
           }
       }       
  }
}

#--------------------------------------------------------------------------------------------------
# Lists all existing versions of a given data object and prints them out on screen 
# The found versions are ordered by version number
# The ordering is carried out by the Bubble sort argorithm: https://en.wikipedia.org/wiki/Bubble_sort
#
# Parameters:
#    *source             [IN] path of the source data object which versions we want to list 
#    *destination        [IN] destination where to look for existing versions
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATListAllVersionsOfDataObjNoPID(*source, *destination){

  *versionNumbPrefixStr = VERSION_SUFFIX;
  msiGetObjType(*source, *source_type);
  if (*source_type == '-d'){

     msiStrlen(*versionNumbPrefixStr,*versionNumbPrefixStrLen);
     msiSplitPath(*source, *path, *File);
     msiStrlen(*path, *pathLength);
     msiSubstr(*source, str(int(*pathLength)+1), "null", *ScrDataObjName);

     *UnsortedListOfVersions = list();
     EUDATGetAllVersionsOfDataObj(*source, *destination, *UnsortedListOfVersions);

     *ListOfVersions = list();

     foreach (*R in *UnsortedListOfVersions) {
       *ver = triml(*R, *versionNumbPrefixStr);
       *ListOfVersions = cons(*ver, *ListOfVersions);
     }

############### Bubble sort argorithm: https://en.wikipedia.org/wiki/Bubble_sort ##############################

    *n = size(*ListOfVersions);
    *newn = 1;

    while (*n > 0) {
     *newn = 0;
     for (*I=1; *I<=(*n-1); *I=*I+1) {
        *ai =  int( elem(*ListOfVersions,*I) );
        *aip = int( elem(*ListOfVersions,*I-1) );
        if (*aip > *ai){
            *temp = elem(*ListOfVersions,*I-1);
            *ListOfVersions = setelem(*ListOfVersions,*I-1,elem(*ListOfVersions,*I));
            *ListOfVersions = setelem(*ListOfVersions,*I,*temp);
            *newn = *I;
        }
     }
     *n = *newn;
    }
  }

###############################################################################################################

  *SortedListOfVersions = list();
  *S = size(*ListOfVersions);
  for (*I=*S; *I>0; *I=*I-1) {
    *NameOfDO = *ScrDataObjName ++ *versionNumbPrefixStr ++ str(elem(*ListOfVersions,*I-1));
    *SortedListOfVersions = cons (*NameOfDO,*SortedListOfVersions);       
  }

  foreach (*SortedListOfVersions) {
    writeLine ("stdout", "*destination/*SortedListOfVersions");
  }

}


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################


#-------------------------------------------------------------------------------
# Versioning search PID for a given path and in case it is not found, 
# it creates a new PID.
#
# Parameters:
# *path    [IN] iRODS path
# *pid     [OUT] the related PID
#
# Author: Alexander Atamas, DANS
#-----------------------------------------------------------------------------
EUDATVersioningSearchAndCreatePID(*path, *pid) {

    logDebug("[EUDATSearchAndCreateVersionPID] query PID of path *path");
    EUDATiFieldVALUEretrieve(*path, "PID", *pid);
    logDebug("[EUDATSearchAndCreateVersionPID] retrieved the iCAT PID value *pid for path *path");
    # if there is no entry for the PID in ICAT, get it from EPIC
    if (*pid == "None") {
        EUDATVersioningCreatePID("None", *path, "None", "None", "True", "None", "None", *pid);
        EUDATiPIDcreate(*path, *pid);
    }
}


#-------------------------------------------------------------------------------
# Verify that a PID of version exists for a given path and optionally create it 
# if not found.
#
# Parameters:
# *parentPID             [IN]  PID of parent 
# *source                [IN]  source iRODS path
# *destination           [IN]  target iRODS path
# *notification          [IN]  enable messaging for async call [0|1]
# *do_version            [IN]  version number of data object
# *prevVersionPath       [IN]  path of previous version of data object
# *prevVersionPID        [IN]  PID of previous version of data object
# *registration_response [OUT] a message containing the reason of the failure
# *childPID              [OUT] PID of created version 
#
# Author: Alexander Atamas, DANS
#-----------------------------------------------------------------------------
EUDATVersioningPIDRegistration(*parentPID, *source, *destination, *notification, *do_version, *prevVersionPath, *prevVersionPID, *registration_response) {

    logInfo("[EUDATVersPIDRegistration] registration of PIDs for versioning from *source to *destination");

    *registration_response = "None";
    *parentROR = "None";
    *childPID = "None";
    *fio = "None";
    *fixed = "False";

    EUDATGetZoneNameFromPath(*destination, *zoneName);
    EUDATGetZoneHostFromZoneName(*zoneName, *zoneConn);
    logDebug("[EUDATVersPIDRegistration] remote zone name: *zoneName, connection contact: *zoneConn");

    if (*parentPID == "empty" || (*parentPID == "None")) {
        *registration_response = "PID of source *source is None";
        logDebug(*registration_response);
        # Update Logging (Statistic File and Failed Files)
        EUDATUpdateLogging(bool("false"),*source,*destination,*registration_response);
    }
    else {
        *parentROR = EUDATSearchAndDefineField(*source, *parentPID, "EUDAT/ROR");
        if (*parentROR == "None") {
            logDebug("EUDAT/ROR was empty, using parent PID");
            *parentROR = *parentPID;
        }
        *fio = EUDATSearchAndDefineField(*source, *parentPID, "EUDAT/FIO");
        if (*fio == "None") {
            logDebug("EUDAT/FIO was empty, using parent PID");
            *fio = *parentPID;
        }
        *fixed = EUDATSearchAndDefineField(*source, *parentPID, "EUDAT/FIXED_CONTENT");
        logDebug("[EUDATVersPIDRegistration] the path *destination has EUDAT/PARENT=*parentPID, "
                 ++ "EUDAT/ROR=*parentROR, EUDAT/FIO=*fio, EUDAT/FIXED_CONTENT=*fixed");
        # create a PID for the version which is done on the remote server
        # using remote execution
        remote(*zoneConn,"null") {
            EUDATVersioningCreatePID(*parentPID, *destination, *parentROR, *fio, *fixed, *do_version, *prevVersionPID, *childPID);
        }

        if (*childPID != "None") {
            *field = "EUDAT/LATEST_VERSION";
            *latestVersion = EUDATVersioningUpdatePIDWithNewChild(*parentPID, *childPID, *field);
            if (*latestVersion != "None") {
                EUDATCreateAVU("EUDAT/LATEST_VERSION", *latestVersion, *source);
            }
            else {
                *registration_response = "LATEST VERSION attribute of source *source is None";
                logDebug(*registration_response);
                EUDATUpdateLogging(bool("false"),*source,*destination,*registration_response);
            }
        }
        else {
            *registration_response = "PID of destination *destination is None";
            logDebug(*registration_response);
            EUDATUpdateLogging(bool("false"),*source,*destination,*registration_response);
        }

        if (int(*do_version) == 1) {
          if (*childPID != "None") {
            *field = "EUDAT/WAS_DERIVED_FROM";
            *nextVersion = EUDATVersioningUpdatePIDWithNewChild(*parentPID, *childPID, *field);
            if (*nextVersion != "None") {
                EUDATCreateAVU("EUDAT/WAS_DERIVED_FROM", *nextVersion, *source);
            }
            else {
                *registration_response = "NEXT VERSION attribute of source *source is None";
                logDebug(*registration_response);
                EUDATUpdateLogging(bool("false"),*source,*destination,*registration_response);
            }
          }
          else {
            *registration_response = "Next PID of destination *destination is None";
            logDebug(*registration_response);
            EUDATUpdateLogging(bool("false"),*source,*destination,*registration_response);
          }
        }

        if (int(*do_version) > 1) {
          if (*childPID != "None") {
            *field = "EUDAT/WAS_DERIVED_FROM";
            *nextVersion = EUDATVersioningUpdatePIDWithNewChild(*prevVersionPID, *childPID, *field);
            if (*nextVersion != "None") {
                EUDATCreateAVU("EUDAT/WAS_DERIVED_FROM", *nextVersion, *prevVersionPath);
            }
            else {
                *registration_response = "PREVIOUS VERSION attribute of source *prevVersionPath is None";
                logDebug(*registration_response);
                EUDATUpdateLogging(bool("false"),*prevVersionPath,*destination,*registration_response);
            }
          }
          else {
            *registration_response = "Previous PID of destination *destination is None";
            logDebug(*registration_response);
            EUDATUpdateLogging(bool("false"),*prevVersionPath,*destination,*registration_response);
          }
        }

    }
   
    if (*notification == 1) { 
        if (*registration_response == "None") { *statusMsg = "true"; }
        else { *statusMsg = "false"; }
        EUDATGetZoneNameFromPath(*source, *zone);
        *queue = *zone ++ "_" ++ $userNameClient;
        *message = "status:*statusMsg;response:*source::*destination::*registration_response";
        EUDATMessage(*queue, *message);
    }

    *childPID;
}


