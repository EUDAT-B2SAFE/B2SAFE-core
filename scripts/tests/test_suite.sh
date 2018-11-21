#!/bin/bash

# If no param given: Fail:
if [ -z $1 ]
then
    echo "Please provide args (1) remote zone for replication and (2) default resource. The latter is optional. (If not provided, it's taken from the ienv command)."
    exit 1
fi

# Get remote zone from command line arg:
REMOTE_ZONE=$1

# If a second arg is given, it's the resource:
if [ ! -z $2 ]
then
    DEFAULT_RESC=$2
else
    DEFAULT_RESC=
fi

# Define test file name
testFileName="test_data.txt"
testFileNameRemote="test_data2.txt"
testCollName="test_coll_root"
testCollNameSub="test_coll_sub"

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
# If not provided via command line, get default resc from in ienv output
if [ -z $DEFAULT_RESC ]
then
    irods_default_resource=`ienv | grep irods_default_resource | cut -d '-' -f 2 | tr -d '[[:space:]]'`
else
    irods_default_resource=$DEFAULT_RESC
fi
# If it's neither provided nor found in ienv, exit!
if [ -z $irods_default_resource ]
then
    echo "No irods_default_resource found in ienv output nor passed as argument. Exiting. Please provide it as command line argument"
    exit
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

# Define collection
collPath="${irods_home}/${testCollName}"
# If exists, ask whether replace or exit
exists=`ils ${irods_home} | grep ${testCollName}`
if [ ! -z $exists ]
then
    echo "The collection $collPath already exists. Remove it before continuing (y or n)? Otherwise, script will exit."
    read shouldRemove
    echo "You entered $shouldRemove"
    if [ $shouldRemove == "y" ]
    then
        echo "Will be removed"
        irm -rf $collPath
    else
        echo "Exiting..."
        exit 1
    fi
fi

imkdir ${testCollName}
imkdir "${testCollName}/${testCollNameSub}"
echo "Hello World!" > ${testFileName}
iput ${testFileName} ${testCollName}
iput ${testFileName} "${testCollName}/${testCollNameSub}"
rm ${testFileName}
echo "############ Collection ############"
ils -rl ${testCollName}
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
  if [ "${REMOTE_ZONE}" == "${irods_zone_name}" ]
  then
    destPath="${irods_home}/${testFileNameRemote}"
  else
    destPath="/${REMOTE_ZONE}/home/${irods_user_name}#${irods_zone_name}/${testFileNameRemote}"
  fi
  echo "Replica path: ${destPath}"
  rule="{*status = EUDATReplication(*source, *destination, *dest_res, *registered, *recursive, *response); 
        if (*status) {
            writeLine('stdout', 'Success!');
        }
        else {
            writeLine('stdout', 'Failed: *response');
        }}"
  input="*source=${sourcePath}%*destination=${destPath}%*dest_res=${irods_default_resource}%*registered=true%*recursive=true"
  
  echo "Rule: irule ${rule} ${input} ruleExecOut"
  rep_raw=`irule "${rule}" "${input}" ruleExecOut`
  echo "Replication response: ${rep_raw}"

  echo "        ############ PID record key/value pairs: ############"
  rule="{EUDATgetLastAVU(*path, *FNAME, *FVALUE)}"
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

moveCollection () {
  rule="{EUDATPidsForColl(*collPath, *fixed)}"
  input="*collPath=${collPath}%*fixed=true"

  echo ""
  echo "############ Collection PID creation ############"
  echo "Rule: irule ${rule} ${input} null"

  irule "${rule}" "${input}" null
  rule="{EUDATSearchPID(*path, *existing_pid)}"
  input="*path=${collPath}"
  output="*existing_pid"
  pid_raw=`irule "${rule}" "${input}" "${output}"`
  pid=`echo ${pid_raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
  echo "ROOT Collection PID: ${pid}"
  root_coll_pid=${pid}
  root_coll_url_raw=`irule "{EUDATGeteValPid(*pid, *key)}" "*pid=${root_coll_pid}%*key='URL'" ruleExecOut`
  root_coll_url=`echo ${root_coll_url_raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
  echo "ROOT Collection URL: ${root_coll_url}"
  new_collPath="${irods_home}/${testCollName}_new"

  echo ""
  echo "############ Moving collection ############"
  imv ${collPath} ${new_collPath}

  echo ""
  echo "############ Updating collection PID ############"
  http_url_raw=`irule "{getHttpApiParameters(*serverApireg, *serverApipub)}" null "*serverApireg"`
  http_url=`echo ${http_url_raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
  newURL="${http_url}${new_collPath}"
  irule "{EUDATeURLupdateColl(*pid, *newURL)}" "*pid=${pid}%*newURL=${newURL}" null
  new_root_coll_url_raw=`irule "{EUDATGeteValPid(*pid, *key)}" "*pid=${root_coll_pid}%*key='URL'" ruleExecOut`
  new_root_coll_url=`echo ${new_root_coll_url_raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
  echo "NEW ROOT Collection URL: ${new_root_coll_url}"
  irule "{EUDATePIDremove(*path, *force)}" "*path=${new_collPath}%*force=true" null
  irule "{EUDATePIDremove(*path, *force)}" "*path=${new_collPath}/${testFileName}%*force=true" null
  irule "{EUDATePIDremove(*path, *force)}" "*path=${new_collPath}/${testCollNameSub}%*force=true" null
  irule "{EUDATePIDremove(*path, *force)}" "*path=${new_collPath}/${testCollNameSub}/${testFileName}%*force=true" null
  irm -rf ${new_collPath}
}

createPID
if [ -n "$REMOTE_ZONE" ]; then
  replication
fi
moveCollection

irule "{EUDATePIDremove(*path, *force)}" "*path=${sourcePath}%*force=true" null
irm ${sourcePath}
#irm -rf ${collPath}
