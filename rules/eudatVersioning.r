eudatVersion{

    *home="/$rodsZoneClient/home/$userNameClient";

    *collDestName = "test_versioning_dest_30";

    *collName = "test_versioning_30";
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

  
  if ( *case == 1 ) {

#  This rule is executed with the following terminal command:    irule -F eudatVersioning.r 1

#  A version of test_file_a.txt file is created WITHOUT a PID assigned to the version
#  *source is a path and a file name of the file which version we want to create
#  *destination is a directory where a version of the file is created
#  *recursive = "false" specifies that versions of files located in subcollections are not created 
#  *registered = "false" indicates that no PID is generated and assigned to the created version
#  *response returns stutus of the executed EUDATVersioning with the above defined parameters  

    *source = "*home/*collName/test_file_a.txt";
    *destination = "*home/*collDestName";
    *recursive = "false";
    *registered = "false";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for one file WITHOUT pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *response);
  
  }
  else if ( *case == 2 ) {

#  This rule is executed with the following terminal command:    irule -F eudatVersioning.r 2

#  A version of test_file_a.txt file is created WITH a PID assigned to the version
#  *source is a path and a file name of the file which version we want to create
#  *destination is a directory where a version of the file is created
#  *recursive = "false" specifies that versions of files located in subcollections are not created
#  *registered = "true" indicates that a new PID is generated and then assigned to the created version
#  *response returns stutus of the executed EUDATVersioning with the above defined parameters  

    *source = "*home/*collName/test_file_a.txt";
    *destination = "*home/*collDestName";
    *recursive = "false";
    *registered = "true";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for one file WITH pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *response);

  }
  else if ( *case == 3 ) {

#  This rule is executed with the following terminal command:    irule -F eudatVersioning.r 3

#  Versions of the entire collection *source, i.e. versions of all files located in the collection, 
#     are created WITHOUT a PID assigned to any version file
#  *source is a path to the collection
#  *destination is a directory where the versions of all files of the collection are created
#  *recursive = "false" specifies that versions of files located in subcollections are not created
#  *registered = "false" indicates that no PID is generated and assigned to any created version
#  *response returns stutus of the executed EUDATVersioning with the above defined parameters 

    *source = *coll;
    *destination = "*home/*collDestName";
    *recursive = "false";
    *registered = "false";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for collection WITHOUT pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *response);

  }
  else if ( *case == 4 ) {

#  This rule is executed with the following terminal command:    irule -F eudatVersioning.r 4

#  Versions of the entire collection *source, i.e. versions of all files located in the collection, 
#     and versions of all files contained in all subcollections of the collection *source are 
#     created WITHOUT a PID assigned to any version file
#  *source is a path to the collection
#  *destination is a directory where the versions of all files of the collection and its subcollections are created
#  *recursive = "true" specifies that versions of all files located in subcollections to be created
#  *registered = "false" indicates that no PID is generated and assigned to any created version
#  *response returns stutus of the executed EUDATVersioning with the above defined parameters 

    *source = *coll;
    *destination = "*home/*collDestName";
    *recursive = "true";
    *registered = "false";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for collection and also recursively for all subcollections WITHOUT pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *response);

  }
  else if ( *case == 5 ) {

#  This rule is executed with the following terminal command:    irule -F eudatVersioning.r 5

#  Versions of the entire collection *source, i.e. versions of all files located in the collection, 
#     are created WITH a PID assigned to each version file
#  *source is a path to the collection
#  *destination is a directory where the versions of all files of the collection are created
#  *recursive = "false" specifies that versions of files located in subcollections are not created
#  *registered = "true" indicates that a new PID is generated and then assigned to the created version
#  *response returns stutus of the executed EUDATVersioning with the above defined parameters 

    *source = *coll;
    *destination = "*home/*collDestName";
    *recursive = "false";
    *registered = "true";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for collection WITH pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *response);

 }
 else if ( *case == 6 ) {

#  This rule is executed with the following terminal command:    irule -F eudatVersioning.r 6

#  Versions of the entire collection *source, i.e. versions of all files located in the collection, 
#     and versions of all files contained in all subcollections of the collection *source are 
#     created WITH a PID assigned to each version file
#  *source is a path to the collection
#  *destination is a directory where the versions of all files of the collection and its subcollections are created
#  *recursive = "true" specifies that versions of all files located in subcollections to be created
#  *registered = "false" indicates that no PID is generated and assigned to any created version
#  *response returns stutus of the executed EUDATVersioning with the above defined parameters 

    *source = *coll;
    *destination = "*home/*collDestName";
    *recursive = "true";
    *registered = "true";
    *response = "";
    writeLine("stdout", "\n(*case) Versioning for collection and also recursively for all subcollections WITH pid registration:");
    EUDATVersioning(*source, *destination, *registered, *recursive, *response);

 }
  else if ( *case == 7 ) {

#  This rule is executed with the following terminal command:    irule -F eudatVersioning.r 7

#  This lists all versions of an origin file specified by *source. 
#  This list of paths to all versions and their names is obtained using only file name of the origin file. 
#  The origin file DOESN'T HAVE to have a PID. 
#  *source specifies name of origin file whose versions and paths to be found
#  *destination is a directory where all versions are stored 


    *source = "*home/*collName/test_file_a.txt";
    *destination = "*home/*collDestName";
    writeLine("stdout", "\n(*case) List of all versions of a given file nicely ordered by version number:");
    EUDATListAllVersionsOfDataObjNoPID(*source, *destination);

 }
  else if ( *case == 8 ) {

#  This rule is executed with the following terminal command:    irule -F eudatVersioning.r 8

#  Writes a version of the *source file to *destination directory
#  *versNumb indicates which version to be pulled
#  If the first parameter *versNumb of the function EUDATPullVersionNoPID is "latest", then 
#     the latest version of *source is written to *destination. Alternatively, to get the latest version, its integer number 
#     should be specified as *versNumb.  
#  To retrieve an older version, its number should be passed as the first parameter *versNumb to EUDATPullVersionNoPID
#  *source specifies an origin file whose version to be retrieved
#  *versPath refers to a path to directory where versions of the *source file are kept
#  *destination defines a directory where the version to be written 

#  EUDATPullVersionNoPID retrieves the *versNumb version of the *source file using the *source name. 
#  Therefore, the source file and its versions DO NOT have to have a PID.

    *source = "*home/*collName/test_file_a.txt";
#    *versNumb = "latest";
    *versNumb = 3;
    *versPath = "*home/*collDestName";
    *destination = "*home/*collName";
    writeLine("stdout", "\n(*case) Pull back version:");
    EUDATPullVersionNoPID(*versNumb, *source, *versPath, *destination, *response)
 }
  else if ( *case == 9 ) {

#  This rule is executed with the following terminal command:    irule -F eudatVersioning.r 9

#  This lists all versions of an origin file specified by *source. 
#  This list of paths to all versions and their names is obtained using only PID of the origin file and PIDs of its versions. 
#  Therefore, both the origin file and all its versions HAVE TO have registered PIDs. 
#  *source specifies name of origin file whose versions and paths to be found

    *source = "*home/*collName/test_file_a.txt";
    writeLine("stdout", "\n(*case) List of all versions of a given file nicely ordered by version number:");
    EUDATListAllVersionsOfDataObjWithPID(*source);

 }
  else if ( *case == 10 ) {

#  This rule is executed with the following terminal command:    irule -F eudatVersioning.r 10

#  Writes a version of the *source file to *destination directory
#  *versNumb indicates which version to be pulled
#  If the first parameter *versNumb of the function EUDATPullVersionWithPID is "latest", then 
#     the latest version of *source is written to *destination. Alternatively, to get the latest version, its integer number 
#     should be specified as *versNumb.  
#  To retrieve an older version, its number should be passed as the first parameter *versNumb to EUDATPullVersionWithPID
#  *source specifies an origin file whose version to be retrieved
#  *destination defines a directory where the version to be written 

#  EUDATPullVersionWithPID retrieves the *versNumb version of the *source file using PID the *source file and PIDs of its versions. 
#  Therefore, both the source file and all its versions HAVE TO have registered PIDs.

    *source = "*home/*collName/test_file_a.txt";
#    *versNumb = "latest";
    *versNumb = 4;
    *destination = "*home/*collName";
    writeLine("stdout", "\n(*case) Pull back version:");
    EUDATPullVersionWithPID(*versNumb, *source, *destination, *response)
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
