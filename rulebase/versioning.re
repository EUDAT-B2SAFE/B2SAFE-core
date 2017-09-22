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
# EUDATVersioning(*source, *destination, *registered, *recursive, *versionPatternStr, *lastUpdateOn, *response)
# EUDATCreateVerionWithPID(*source, *destination, *recursive, *versionPatternStr, *lastUpdateOn, *response)
# EUDATCreateVerionNoPID(*source, *destination, *recursive, *versionPatternStr, *response)
# EUDATCreateVersionOfDataObjRegPID(*source, *destination, *versionNumbPrefixStr, *lastUpdateOn, *status)
# EUDATCreateVersionOfDataObj(*source, *destination, *versionNumbPrefixStr, *status)
# EUDATGetAllVersionsOfDataObj(*source, *destination, *versionNumbPrefixStr, *ListOfAllVersions)
# EUDATListAllVersionsOfDataObj(*source, *destination, *versionNumbPrefixStr)
# MY_EUDATSearchAndCreatePID(*path, *pid)
# MY_EUDATPIDRegistration(*parentPID, *source, *destination, *notification, *do_version, *lastUpdateOn, *prevVersionPath, *prevVersionPID, *registration_response)
# MY_EUDATCreatePID(*parent_pid, *path, *ror, *fio, *fixed, *do_version, *lastUpdateOn, *newPID)
# MY_EUDATePIDremove(*path, *force)
# MY_EUDATUpdatePIDWithNewChild(*parentPID, *childPID, *field)



#------------------------------------------------------------------------------------------
# Data set versioning
#
# Parameters:
#    *source            [IN] path of the source data set in iRODS
#    *destination       [IN] destination of versioning in iRODS
#    *registered        [IN] boolean value: "true" for registered data, "false" otherwise
#    *recursive         [IN] boolean value: "true" to enable the recursive versioning
#                            of registered data, "false" otherwise
#    *versionPatternStr [IN] a version number prefix (e.g., "__v") located at the end 
#                            of a file extension and before the version number;
#                            example: "my_file.txt__v3" 
#    *lastUpdateOn      [IN] date of last update of data object 
#    *response          [OUT]the result of the versioning
# 
# Author: Alexander Atamas, DANS
#------------------------------------------------------------------------------------------

EUDATVersioning(*source, *destination, *registered, *recursive, *versionPatternStr, *lastUpdateOn, *response){

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

            *status = EUDATCreateVerionWithPID(*source, *destination, EUDATtoBoolean(*recursive), *versionPatternStr, *lastUpdateOn, *response);
      } else {
            logDebug("Versioning data without PID registration");
            *status = EUDATCreateVerionNoPID(*source, *destination, EUDATtoBoolean(*recursive), *versionPatternStr, *response);
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
# Creates, WITH pid registration, a version of either:
#         - all files of collection, if source type is a collection 
#         - all files of collection and subcollections recursively, if source type is a collection 
#         - one file, if source type is a data object and not a collection
#
# Parameters:
#    *source            [IN] path of the source data set in iRODS
#    *destination       [IN] destination of versioning in iRODS
#    *recursive         [IN] boolean value: "true" to enable the recursive versioning
#                            of registered data, "false" otherwise
#    *versionPatternStr [IN] a version number prefix (e.g., "__v") located at the end 
#                            of a file extension and before the version number;
#                            example: "my_file.txt__v3" 
#    *lastUpdateOn      [IN] date of last update of data object 
#    *response          [OUT]the result of the versioning
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATCreateVerionWithPID(*source, *destination, *recursive, *versionPatternStr, *lastUpdateOn, *response){
  
      *status = bool("true");
      *responses = "";
      msiGetObjType(*source, *source_type);

      if (*source_type == '-c'){

        foreach(*SrcRow in SELECT DATA_NAME WHERE COLL_NAME = '*source') {
          *ScrDataObjName = *SrcRow.DATA_NAME;
          *Source = *source ++ "/" ++ *ScrDataObjName;
          *dataCopyStatus = EUDATCreateVersionOfDataObjRegPID(*Source, *destination, *versionPatternStr, *lastUpdateOn, *dataCopyStatus);
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
             *dataCopyStatus = EUDATCreateVersionOfDataObjRegPID(*Source, *Dest, *versionPatternStr, *lastUpdateOn, *dataCopyStatus);
             if ( *dataCopyStatus != 0 ){
                 *contents = *Source ++ '::*destination::false::*dataCopyStatus';
                 *responses = *responses ++ *contents ++ ",";
             }
             *status = (*dataCopyStatus == 0) && *status;
           }
         }
        }

      } else if (*source_type == '-d'){
           *dataCopyStatus = EUDATCreateVersionOfDataObjRegPID(*source, *destination, *versionPatternStr, *lastUpdateOn, *dataCopyStatus);
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
# Creates, WITHOUT pid registration, a version of either:
#         - all files of collection, if source type is a collection 
#         - all files of collection and subcollections recursively, if source type is a collection 
#         - one file, if source type is a data object and not a collection
#
# Parameters:
#    *source            [IN] path of the source data set in iRODS
#    *destination       [IN] destination of versioning in iRODS
#    *recursive         [IN] boolean value: "true" to enable the recursive versioning
#                            of registered data, "false" otherwise
#    *versionPatternStr [IN] a version number prefix (e.g., "__v") located at the end 
#                            of a file extension and before the version number;
#                            example: "my_file.txt__v3"  
#    *response          [OUT]the result of the versioning
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATCreateVerionNoPID(*source, *destination, *recursive, *versionPatternStr, *response){

      *status = bool("true");
      *responses = "";
      msiGetObjType(*source, *source_type);

      if (*source_type == '-c'){

        foreach(*SrcRow in SELECT DATA_NAME WHERE COLL_NAME = '*source') {
          *ScrDataObjName = *SrcRow.DATA_NAME;
          *Source = *source ++ "/" ++ *ScrDataObjName;
          *dataCopyStatus = EUDATCreateVersionOfDataObj(*Source, *destination, *versionPatternStr, *dataCopyStatus);
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
             *dataCopyStatus = EUDATCreateVersionOfDataObj(*Source, *Dest, *versionPatternStr, *dataCopyStatus);
             if ( *dataCopyStatus != 0 ){
                 *contents = *Source ++ '::*destination::false::*dataCopyStatus';
                 *responses = *responses ++ *contents ++ ",";
             }
             *status = (*dataCopyStatus == 0) && *status;
           }
         }
        }

      } else if (*source_type == '-d'){
           *dataCopyStatus = EUDATCreateVersionOfDataObj(*source, *destination, *versionPatternStr, *dataCopyStatus);
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
#    *versionPatternStr  [IN] a version number prefix (e.g., "__v") located at the end 
#                             of a file extension and before the version number;
#                             example: "my_file.txt__v3" 
#    *lastUpdateOn       [IN] date of last update of data object 
#    *status            [OUT] the result of data object copying and registration performed
#                             by microservice "msiDataObjCopy" and function "MY_EUDATPIDRegistration",
#                             respectively
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATCreateVersionOfDataObjRegPID(*source, *destination, *versionNumbPrefixStr, *lastUpdateOn, *status){

  *ListOfVersions = list();
  EUDATGetAllVersionsOfDataObj(*source, *destination, *versionNumbPrefixStr, *ListOfVersions);
  
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
  *LatestVers = *ScrDataObjName ++ *versionNumbPrefixStr ++ "*NewVers";
  *destinationVers = *destination ++ "/" ++ *LatestVers;

  *status = -1;
  *statusPID = bool("true");
  # initial value of parentPID
  *parentPID = "None";

  # search and create pid related to the source of the versioning
  MY_EUDATSearchAndCreatePID(*source, *parentPID);

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
            MY_EUDATSearchAndCreatePID(*prevVersion, *prevVersionPID);
          }

          *notification = 0;
          *versionPID = MY_EUDATPIDRegistration(*parentPID, *source, *destinationVers, *notification, str(*NewVers), *lastUpdateOn, *prevVersion, *prevVersionPID, *singleResponse);
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
#    *versionPatternStr  [IN] a version number prefix (e.g., "__v") located at the end 
#                             of a file extension and before the version number;
#                             example: "my_file.txt__v3"  
#    *status            [OUT] the result of data object copying performed by microservice "msiDataObjCopy"  
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATCreateVersionOfDataObj(*source, *destination, *versionNumbPrefixStr, *status){

  *ListOfVersions = list();
  EUDATGetAllVersionsOfDataObj(*source, *destination, *versionNumbPrefixStr, *ListOfVersions);
  
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
  *LatestVers = *ScrDataObjName ++ *versionNumbPrefixStr ++ "*NewVers";
  *destinationVers = *destination ++ "/" ++ *LatestVers;

   msiDataObjCopy(*source, *destinationVers, "", *status);

   if ( *status == 0 ){
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
#    *versionPatternStr  [IN] a version number prefix (e.g., "__v") located at the end 
#                             of a file extension and before the version number;
#                             example: "my_file.txt__v3"  
#    *ListOfAllVersions  [OUT] list of all versions existing in *destionation for a given data object  
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATGetAllVersionsOfDataObj(*source, *destination, *versionNumbPrefixStr, *ListOfAllVersions){

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
# Lists all existing versions of a given data object and prints them out on screen 
# The found versions are ordered by version number
# The ordering is carried out by the Bubble sort argorithm: https://en.wikipedia.org/wiki/Bubble_sort
#
# Parameters:
#    *source             [IN] path of the source data object to find existing versions of 
#    *destination        [IN] destination where to look for existing versions
#    *versionPatternStr  [IN] a version number prefix (e.g., "__v") located at the end 
#                             of a file extension and before the version number;
#                             example: "my_file.txt__v3"   
# 
# Author: Alexander Atamas, DANS
#--------------------------------------------------------------------------------------------------

EUDATListAllVersionsOfDataObj(*source, *destination, *versionNumbPrefixStr){

  msiGetObjType(*source, *source_type);
  if (*source_type == '-d'){

     msiStrlen(*versionNumbPrefixStr,*versionNumbPrefixStrLen);
     msiSplitPath(*source, *path, *File);
     msiStrlen(*path, *pathLength);
     msiSubstr(*source, str(int(*pathLength)+1), "null", *ScrDataObjName);

     *UnsortedListOfVersions = list();
     EUDATGetAllVersionsOfDataObj(*source, *destination, *versionNumbPrefixStr, *UnsortedListOfVersions);

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
    writeLine ("stdout", "*SortedListOfVersions");
  }

}


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################


#-------------------------------------------------------------------------------
# Search PID for a given path and in case it is not found, 
# it creates a new PID.
#
# Parameters:
# *path    [IN] iRODS path
# *pid     [OUT] the related PID
#
# Author: Claudio, Cineca
# Modified by: Alexander Atamas, DANS
#-----------------------------------------------------------------------------
MY_EUDATSearchAndCreatePID(*path, *pid) {

    logDebug("[EUDATSearchAndCreateVersionPID] query PID of path *path");
    EUDATiFieldVALUEretrieve(*path, "PID", *pid);
    logDebug("[EUDATSearchAndCreateVersionPID] retrieved the iCAT PID value *pid for path *path");
    # if there is no entry for the PID in ICAT, get it from EPIC
    if (*pid == "None") {
        MY_EUDATCreatePID("None", *path, "None", "None", "True", "None", "None", "None", *pid);
        EUDATiPIDcreate(*path, *pid);
    }
}


#-------------------------------------------------------------------------------
# Verify that a PID exist for a given path and optionally create it 
# if not found.
#
# Parameters:
# *parentPID             [IN]  PID of parent 
# *source                [IN]  source iRODS path
# *destination           [IN]  target iRODS path
# *notification          [IN]  enable messaging for async call [0|1]
# *do_version            [IN]  version number of data object
# *lastUpdateOn          [IN]  date of last update of data object
# *prevVersionPath       [IN]  path of previous version of data object
# *prevVersionPID        [IN]  PID of previous version of data object
# *registration_response [OUT] a message containing the reason of the failure
# *childPID              [OUT] PID of created version 
#
# Author: Claudio, Cineca
# Modified by: Alexander Atamas, DANS
#-----------------------------------------------------------------------------
MY_EUDATPIDRegistration(*parentPID, *source, *destination, *notification, *do_version, *lastUpdateOn, *prevVersionPath, *prevVersionPID, *registration_response) {

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
            MY_EUDATCreatePID(*parentPID, *destination, *parentROR, *fio, *fixed, *do_version, *lastUpdateOn, *prevVersionPID, *childPID);
        }
        # update parent PID with a child one 
        # if the child exists in ICAT on the remote server
        if (*childPID != "None") {
            *field = "EUDAT/VERSION";
            *version = MY_EUDATUpdatePIDWithNewChild(*parentPID, *childPID, *field);
            if (*version != "None") {
                EUDATCreateAVU("EUDAT/VERSION", *version, *source);
            }
            else {
                *registration_response = "VERSION attribute of source *source is None";
                logDebug(*registration_response);
                EUDATUpdateLogging(bool("false"),*source,*destination,*registration_response);
            }
        }
        else {
            *registration_response = "PID of destination *destination is None";
            logDebug(*registration_response);
            EUDATUpdateLogging(bool("false"),*source,*destination,*registration_response);
        }

        if (*childPID != "None") {
            *field = "EUDAT/LATEST_VERSION";
            *latestVersion = MY_EUDATUpdatePIDWithNewChild(*parentPID, *childPID, *field);
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
            *field = "EUDAT/NEXT_REVISION";
            *nextVersion = MY_EUDATUpdatePIDWithNewChild(*parentPID, *childPID, *field);
            if (*nextVersion != "None") {
                EUDATCreateAVU("EUDAT/NEXT_REVISION", *nextVersion, *source);
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
            *field = "EUDAT/NEXT_REVISION";
            *nextVersion = MY_EUDATUpdatePIDWithNewChild(*prevVersionPID, *childPID, *field);
            if (*nextVersion != "None") {
                EUDATCreateAVU("EUDAT/NEXT_REVISION", *nextVersion, *prevVersionPath);
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


#-------------------------------------------------------------------------------
# Generate a new PID for a digital object.
# Fields stored in the PID record: URL, ROR and CHECKSUM
# adds a ROR field if (*ror != "None")
#
# Parameters:
#   *parent_pid     [IN]    the PID of the digital object whose version was created (not necessarily the ROR)
#   *path           [IN]    the path of the object to store with the PID record
#   *ror            [IN]    the ROR PID of the digital object that we want to store.
#   *fio            [IN]    the FIO PID of the digital object that we want to store.
#   *fixed          [IN]    the boolean flag to define that the object related to this PID cannot change
#   *do_version     [IN]    version number of data object
#   *lastUpdateOn   [IN]    date of last update of data object
#   *prevVersionPID [IN]    PID of previous version of data object
#   *newPID         [OUT]   the pid generated for this object 
#
# Author: Willem Elbers, MPI-TLA
# Edited by Elena Erastova, RZG; Long Phan, JSC; Robert Verkerk, SURFsara, Javier Quinteros, GFZ; Alexander Atamas, DANS
#-------------------------------------------------------------------------------
MY_EUDATCreatePID(*parent_pid, *path, *ror, *fio, *fixed, *do_version, *lastUpdateOn, *prevVersionPID, *newPID) {

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
                      *extraType = "*extraType"++";EUDAT/VERSION_SOURCE=*parent_pid";
                } else {
                      *extraType = "EUDAT/VERSION_SOURCE=*parent_pid";
                }
                EUDATCreateAVU("EUDAT/VERSION_SOURCE", *parent_pid, *path);
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


##########################################################################################

            if (*do_version != "None" && *do_version != "") {

                # add do_version (i.e., data object version) as extratype parameter
            
                if (*extraType != "empty") {
                      *extraType = "*extraType"++";EUDAT/DO_VERSION_NUMBER=*do_version";
                } else {
                      *extraType = "EUDAT/DO_VERSION_NUMBER=*do_version";
                }
                EUDATCreateAVU("EUDAT/DO_VERSION_NUMBER", *do_version, *path);
            }

            if (*lastUpdateOn != "None" && *lastUpdateOn != "") {

                # add lastUpdateOn (date of last updated of data object ) as extratype parameter
            
                if (*extraType != "empty") {
                      *extraType = "*extraType"++";EUDAT/LAST_UPDATE_ON=*lastUpdateOn";
                } else {
                      *extraType = "EUDAT/LAST_UPDATE_ON=*lastUpdateOn";
                }
                EUDATCreateAVU("EUDAT/LAST_UPDATE_ON", *lastUpdateOn, *path);
            }

            if (*prevVersionPID != "None" && *prevVersionPID != "") {

                # add prevVersionPID (PID of previous version of data object ) as extratype parameter
            
                if (*extraType != "empty") {
                      *extraType = "*extraType"++";EUDAT/REVISION_OF=*prevVersionPID";
                } else {
                      *extraType = "EUDAT/REVISION_OF=*prevVersionPID";
                }
                EUDATCreateAVU("EUDAT/REVISION_OF", *prevVersionPID, *path);
            }
            else {

                if ( *parent_pid != "None" && *parent_pid != "" ){
                   if (*extraType != "empty" ) {
                        *extraType = "*extraType"++";EUDAT/REVISION_OF=*parent_pid";
                   } else {
                        *extraType = "EUDAT/REVISION_OF=*parent_pid";
                   }
                   EUDATCreateAVU("EUDAT/REVISION_OF", *parent_pid, *path);
                }                
            }

##########################################################################################
            

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




#-------------------------------------------------------------------------------
# This function remove an ePID... even if its EUDAT/VERSION field is not empty!
# To be improved.       
#
# Arguments:
#   *path           [IN]    The path of the object to be removed
#
# Author: Giacomo Mariani, CINECA
# Modified by: Alexander Atamas, DANS
#-------------------------------------------------------------------------------
MY_EUDATePIDremove(*path, *force) {
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug) 
    logInfo("[EUDATeVersPIDremove] removing PID associated to: $userNameClient, *path");

    if (EUDATSearchPID(*path, *pid)) {
        msiExecCmd("epicclient.py","*credStoreType *credStorePath read --key EUDAT/VERSION *pid", "null", "null", "null", *outEPR);
        msiGetStdoutInExecCmdOut(*outEPR, *version);
        getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
        if (*msiFreeEnabled) {
            msifree_microservice_out(*outEPR);
        }
        logDebug("[EUDATeVersPIDremove] EUDAT/VERSION = *version");
        if (("*version" like "Error*")||("*version" == "")||("*version" like "None*")) {
            logDebug("[EUDATeVersPIDremove] No versions found: PID *pid will be deleted");
            msiExecCmd("epicclient.py","*credStoreType *credStorePath delete *pid",
                       "null", "null", "null", *outEPR1);
            msiGetStdoutInExecCmdOut(*outEPR1, *response3);
            getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
            if (*msiFreeEnabled) {
                msifree_microservice_out(*outEPR1);
            }
            logInfo("[EUDATeVersPIDremove] removing completed, response = *response3");
        }
        else if (EUDATtoBoolean(*force) == bool("true")){
            logDebug("[EUDAVersTePIDremove] Found versions: PID *pid will be deleted");
            msiExecCmd("epicclient.py","*credStoreType *credStorePath delete *pid",
                       "null", "null", "null", *outEPR2);
            msiGetStdoutInExecCmdOut(*outEPR2, *response3);
            getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
            if (*msiFreeEnabled) {
                msifree_microservice_out(*outEPR2);
            }
            logInfo("[EUDATeVersPIDremove] removing completed, response = *response3");
        }
        else {
            # The PID record contains pointers to other DO copies.
            # What should we do?
            # Maybe all the copies should be deleted together with the master copy.
            logDebug("[EUDATeVersPIDremove] Found versions related to PID *pid");
            logInfo("[EUDATeVersPIDremove] nothing has been deleted");
        }
    }
    else {
        logInfo("[EUDATeVersPIDremove] no PID associated to *path found");
    }
}  


#-------------------------------------------------------------------------------
# Update a PID record with a new child.
#
# Parameters:
#       *parentPID  [IN]    PID of the record that will be updated
#       *childPID   [IN]    PID to store as one of the child locations
#
# Author: Willem Elbers, MPI-TLA
# Modified by: Claudio Cacciari, CINECA; Alexander Atamas, DANS
#-------------------------------------------------------------------------------
MY_EUDATUpdatePIDWithNewChild(*parentPID, *childPID, *field) {
    *versionNew = "None"
    logInfo("[EUDATUpdatePIDWithNewVersionChild] update parent pid (*parentPID) with new child (*childPID)");
    getEpicApiParameters(*credStoreType, *credStorePath, *epicApi, *serverID, *epicDebug);
    *version = EUDATGeteValPid(*parentPID, *field);
    if ((*version == "") || (*version == "None")) {
        *versionNew = *childPID;
    }
    else {
        if ( *field == "EUDAT/VERSION" ){
           *versionNew = *version ++ "," ++ *childPID;
        }
        else{
           *versionNew = *childPID;
        }
    }
    logDebug("[EUDATUpdatePIDWithNewVersionChild] epicclient.py *credStoreType *credStorePath modify *parentPID *field *versionNew");
    msiExecCmd("epicclient.py", "*credStoreType *credStorePath modify *parentPID *field *versionNew",
               "null", "null", "null", *outUPwNC);
    msiGetStdoutInExecCmdOut(*outUPwNC, *response);
    getConfParameters(*msiFreeEnabled, *msiCurlEnabled, *authzEnabled);
    if (*msiFreeEnabled) {
        msifree_microservice_out(*outUPwNC);
    }
    logDebug("[EUDATUpdatePIDWithNewVersionChild] update handle version response = *response");
    if (*response != "True") { *versionNew = "None" }

    *versionNew;
}



