#!/bin/bash

REMOTE_ZONE=cinecaDMPZone1

echo "Hello World!" > test_data.txt
iput test_data.txt
rm test_data.txt
echo "############ Data Object ############"
ils -l test_data.txt
echo ""

irods_home=`ienv | grep irods_home | cut -d '-' -f 2 | tr -d '[[:space:]]'`
irods_user_name=`ienv | grep irods_user_name | cut -d '-' -f 2 | tr -d '[[:space:]]'`
irods_zone_name=`ienv | grep irods_zone_name | cut -d '-' -f 2 | tr -d '[[:space:]]'`
irods_default_resource=`ienv | grep irods_default_resource | cut -d '-' -f 2 | tr -d '[[:space:]]'`
sourcePath="${irods_home}/test_data.txt"

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
  destPath="/${REMOTE_ZONE}/home/${irods_user_name}#${irods_zone_name}/test_data2.txt"
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
  echo "        PID: ${pid}"
  
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
