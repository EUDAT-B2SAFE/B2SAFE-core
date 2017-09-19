eudatVersion{

    *home="/$rodsZoneClient/home/$userNameClient";

    *collDestName = "test_versioning_dest_15";

    *collName = "test_versioning_15";
    *coll = "*home/*collName";

    *res = int(checkCollInput(*coll)); 
    if (*res == 0) { 

      msiCollCreate("*coll","",*status); 

      msiDataObjCreate("*home/*collName/test_file_a.txt", "forceFlag=", *fd);
      msiDataObjWrite(*fd, "Hello World! (test_file_a.txt)", "");
      msiDataObjClose(*fd, *status);

      msiDataObjCreate("*home/*collName/test_file_b.txt", "forceFlag=", *fd);
      msiDataObjWrite(*fd, "Hello World! test_file_b.txt", "");
      msiDataObjClose(*fd, *status);

      msiDataObjCreate("*home/*collName/test_file_c.txt", "forceFlag=", *fd);
      msiDataObjWrite(*fd, "Hello World! test_file_c.txt", "");
      msiDataObjClose(*fd, *status);
    }
    



    *subcoll = "*home/*collName/subcollection_a";
    *res = int(checkCollInput(*subcoll)); 
    if (*res == 0) {

      msiCollCreate("*home/*collName/subcollection_a","",*status); 

      msiDataObjCreate("*home/*collName/subcollection_a/subcoll_a_file_a.txt", "forceFlag=", *fd);
      msiDataObjWrite(*fd, "Hello World! (subcoll_a_file_a.txt)", "");
      msiDataObjClose(*fd, *status);

      msiDataObjCreate("*home/*collName/subcollection_a/subcoll_a_file_b.txt", "forceFlag=", *fd);
      msiDataObjWrite(*fd, "Hello World! subcoll_a_file_b.txt", "");
      msiDataObjClose(*fd, *status);
    }




    *subcoll = "*home/*collName/subcollection_b";
    *res = int(checkCollInput(*subcoll)); 
    if (*res == 0) { 

      msiCollCreate("*home/*collName/subcollection_b","",*status); 

      msiDataObjCreate("*home/*collName/subcollection_b/subcoll_b_file_a.txt", "forceFlag=", *fd);
      msiDataObjWrite(*fd, "Hello World! (subcoll_b_file_a.txt)", "");
      msiDataObjClose(*fd, *status);
    }

  
  *versionPatternStr = "__v";
  
  if ( *case == 1 ) {

    *lastUpdateOn = "None";
    *source = "*home/*collName/test_file_a.txt";
    *destination = "*home/*collDestName";
    *recursive = "false";
    *registered = "false";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for one file WITHOUT pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *versionPatternStr, *lastUpdateOn, *response);
  
  }
  else if ( *case == 2 ) {

    *lastUpdateOn = "2013-08-23T16:00:00Z";
    *source = "*home/*collName/test_file_a.txt";
#    *source = "*home/*collDestName/test_file_a.txt__v12";
    *destination = "*home/*collDestName";
    *recursive = "false";
    *registered = "true";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for one file WITH pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *versionPatternStr, *lastUpdateOn, *response);

  }
  else if ( *case == 3 ) {

    *lastUpdateOn = "None";
    *source = *coll;
    *destination = "*home/*collDestName";
    *recursive = "false";
    *registered = "false";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for collection WITHOUT pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *versionPatternStr, *lastUpdateOn, *response);

  }
  else if ( *case == 4 ) {

    *lastUpdateOn = "None";
    *source = *coll;
    *destination = "*home/*collDestName";
    *recursive = "true";
    *registered = "false";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for collection and also recursively for all subcollections WITHOUT pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *versionPatternStr, *lastUpdateOn, *response);

  }
  else if ( *case == 5 ) {

    *lastUpdateOn = "2013-08-23T16:00:00Z";
    *source = *coll;
    *destination = "*home/*collDestName";
    *recursive = "false";
    *registered = "true";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for collection WITH pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *versionPatternStr, *lastUpdateOn, *response);

 }
 else if ( *case == 6 ) {

    *lastUpdateOn = "2013-08-23T16:00:00Z";
    *source = *coll;
    *destination = "*home/*collDestName";
    *recursive = "true";
    *registered = "true";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for collection and also recursively for all subcollections WITH pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *versionPatternStr, *lastUpdateOn, *response);

 }
  else if ( *case == 7 ) {

    *source = "*home/*collName/test_file_a.txt";
    *destination = "*home/*collDestName";
    writeLine("stdout", "\n(*case) List of all versions of a given file nicely ordered by version number:");
    EUDATListAllVersionsOfDataObj(*source, *destination, *versionPatternStr);

 }

}

checkCollInput(*Coll) {
# check whether *Coll exists
# *Coll doesn exist, if *Result == 0
  *Q = select count(COLL_ID) where COLL_NAME = '*Coll';
  foreach (*R in *Q) {*Result = *R.COLL_ID;}
  
  *Result;
}


INPUT *case = "$1"
OUTPUT ruleExecOut 
