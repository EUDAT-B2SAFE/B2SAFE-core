#!/bin/bash

# Get command line args:
DEFAULT_RESC=$1
REMOTE_ZONE=$2
if [ -z $REMOTE_ZONE ] || [ -z $DEFAULT_RESC ]
then
    echo "Please provide args (1) default resource and (2) remote zone to be used for replication."
    exit 1
fi

# Define test file name
testFileName="test_data.txt"
testFileNameRemote="test_data2.txt"

# Get user name and zone name from ienv
irods_user_name=`ienv | grep irods_user_name | cut -d '-' -f 2 | tr -d '[[:space:]]'`
irods_zone_name=`ienv | grep irods_zone_name | cut -d '-' -f 2 | tr -d '[[:space:]]'`
# Get home dir (not in ienv output)
irods_home=`ienv | grep irods_home | cut -d '-' -f 2 | tr -d '[[:space:]]'`
if [ -z $irods_home  ]
then
    echo "No irods_home found in ienv output. Constructing irods_home from zone name and user name."
    irods_home="/${irods_zone_name}/home/${irods_user_name}"
fi
# Get default resc (not in ienv output)
irods_default_resource=`ienv | grep irods_default_resource | cut -d '-' -f 2 | tr -d '[[:space:]]'`
if [ -z $irods_default_resource ]
then
    echo "No irods_default_resource found in ienv output. Using the one from command line."
    irods_default_resource=$DEFAULT_RESC
fi

# Define test file
sourcePath="${irods_home}/${testFileName}"
# If exists, ask whether replace or exit
exists=`ils ${irods_home} | grep ${testFileName}`
if [ ! -z $exists ]
then
    echo "The file $sourcePath already exists. Remove it before continuing (y or n)? Otherwise, script will exit."
    read shouldRemove
    echo "You entered $shouldRemove"
    if [ $shouldRemove == "y" ]
    then
        echo "Will be removed"
        irm $sourcePath
    else
        echo "Exiting..."
        exit 1
    fi
fi

echo "Hello World!" > ${testFileName}
iput ${testFileName}
rm ${testFileName}
echo "############ Data Object ############"
ils -l ${testFileName}
echo ""


createPID () {
  rule="{EUDATCreatePID(*parent_pid, *path, *ror, *fio, *fixed, *newPID)}"
  input="*parent_pid=%*path=${sourcePath}%*ror=%*fio=%*fixed=true"
  output="*newPID"

  echo "############ PID creation ############"
  echo "Rule: irule ${rule} ${input} ${output}"

  pid_raw=`irule "${rule}" "${input}" "${output}"`
  pid=`echo ${pid_raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
  echo "PID: ${pid}"
  pid_source=${pid}

  echo "        ############ PID record key/value pairs: ############"
  for k in "URL" "CHECKSUM" "EUDAT/CHECKSUM" "EUDAT/CHECKSUM_TIMESTAMP" "EUDAT/ROR" "EUDAT/FIO" "EUDAT/FIXED_CONTENT"
  do
      raw=`irule "{*res=EUDATGeteValPid(*pid, *key)}" "*pid=${pid}%*key=$k" "*res"`
      val=`echo ${raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
      echo "        $k: ${val}"
  done
  echo "        ############ iCAT key/value pairs: ############"
  for k in "PID" "EUDAT/ROR" "EUDAT/FIO" "EUDAT/FIXED_CONTENT" "eudat_dpm_checksum_date:${irods_default_resource}"
  do
      raw=`irule "{EUDATgetLastAVU(*path, *key, *value)}" "*path=${sourcePath}%*key=$k" "*value"`
      val=`echo ${raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
      echo "        $k: ${val}"
  done
}

replication () {
  echo ""
  echo "############ REPLICATION ############"
#  destPath="${irods_home}/test_data2.txt"
  destPath="/${REMOTE_ZONE}/home/${irods_user_name}#${irods_zone_name}/${testFileNameRemote}"
  echo "Replica path: ${destPath}"
  rule="{*status = EUDATReplication(*source, *destination, *registered, *recursive, *response); 
        if (*status) {
            writeLine('stdout', 'Success!');
        }
        else {
            writeLine('stdout', 'Failed: *response');
        }}"
  input="*source=${sourcePath}%*destination=${destPath}%*registered=true%*recursive=true"
  
  echo "Rule: irule ${rule} ${input} ruleExecOut"
  rep_raw=`irule "${rule}" "${input}" ruleExecOut`
  echo "Replication response: ${rep_raw}"

  echo "        ############ PID record key/value pairs: ############"
  rule="{EUDATiFieldVALUEretrieve(*path, *FNAME, *FVALUE)}"
  input="*path=${destPath}%*FNAME=PID"
  output="*FVALUE"
  pid_raw=`irule "${rule}" "${input}" "${output}"`
  pid=`echo ${pid_raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
  if [ -z $pid ]
  then
    echo "        ERROR! Did not find PID in irods metadata for ${destPath}! Cannot retrieve values from the PID record. Please check what went wrong."
  fi
  echo "        PID: ${pid}"
  
  # The following loop could be places in an else clause, but then the user might not notice the failures, so let it fail...
  for k in "URL" "CHECKSUM" "EUDAT/CHECKSUM" "EUDAT/CHECKSUM_TIMESTAMP" "EUDAT/ROR" "EUDAT/FIO" "EUDAT/FIXED_CONTENT" "EUDAT/PARENT"
  do
      raw=`irule "{*res=EUDATGeteValPid(*pid, *key)}" "*pid=${pid}%*key=$k" "*res"`
      val=`echo ${raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
      echo "        $k: ${val}"
  done
  
  echo "        ############ iCAT key/value pairs: ############"
  for k in "PID" "EUDAT/ROR" "EUDAT/FIO" "EUDAT/PARENT" "EUDAT/FIXED_CONTENT" "eudat_dpm_checksum_date:${irods_default_resource}"
  do
      raw=`irule "{EUDATgetLastAVU(*path, *key, *value)}" "*path=${destPath}%*key=$k" "*value"`
      val=`echo ${raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
      echo "        $k: ${val}"
  done
  echo "        ############ iCAT Parent replica value ############"
  raw=`irule "{EUDATgetLastAVU(*path, *key, *value)}" "*path=${sourcePath}%*key=EUDAT/REPLICA" "*value"`
  val=`echo ${raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
  echo "        EUDAT/REPLICA: ${val}"
  echo "        ############ PID record Parent replica value ############" 
  raw=`irule "{*res=EUDATGeteValPid(*pid, *key)}" "*pid=${pid_source}%*key=EUDAT/REPLICA" "*res"`
  val=`echo ${raw:7}`
  echo "        EUDAT/REPLICA: ${val}"  

  irule "{EUDATePIDremove(*path, *force)}" "*path=${destPath}%*force=true" null
  irm ${destPath}
}

createPID
if [ -n "$REMOTE_ZONE" ]; then
  replication
fi

irule "{EUDATePIDremove(*path, *force)}" "*path=${sourcePath}%*force=true" null
irm ${sourcePath}
