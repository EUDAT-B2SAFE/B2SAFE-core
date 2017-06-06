#!/bin/bash

if [[ -z "$1" ]]
then
    echo "missing input path"
    exit 1
fi

irods_default_resource=`ienv | grep irods_default_resource | cut -d '-' -f 2 | tr -d '[[:space:]]'`

syncMeta () {
  rule="{EUDATSearchPID(*path, *existing_pid)}"
  input="*path=${sourcePath}"
  output="*existing_pid"

  echo "############ PID search ############"
  echo "Rule: irule ${rule} ${input} ${output}"

  pid_raw=`irule "${rule}" "${input}" "${output}"`
  echo "PID RAW: ${pid_raw}"
  pid=`echo ${pid_raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
  echo "PID: ${pid}"
  pid_source=${pid}

  if [[ ${pid} = "empty" ]]; then
      echo "PID is empty"
      return 0
  fi

  echo "Rule: irule {EUDATCreateAVU(*key, *value, *path)} ${sourcePath} PID ${pid}"
  irule "{EUDATCreateAVU(*key, *value, *path)}" "*key=PID%*value=${pid}%*path=${sourcePath}" ""

  echo "        ############ PID record key/value pairs: ############"
  for k in "EUDAT/REPLICA" "EUDAT/ROR" "EUDAT/FIO" "EUDAT/FIXED_CONTENT" "EUDAT/PARENT"
  do
      raw=`irule "{*res=EUDATGeteValPid(*pid, *key)}" "*pid=${pid}%*key=$k" "*res"`
      val=`echo ${raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
      echo "        $k: ${val}"
      if [[ -n "${val}" ]] && [[ ${val} != "None" ]]
      then
          echo "        Rule: irule {EUDATCreateAVU(*key, *value, *path)} *path=${sourcePath}%*key=$k%*value=${val}"
          irule "{EUDATCreateAVU(*key, *value, *path)}" "*path=${sourcePath}%*key=$k%*value=${val}" ""
      fi
  done

  raw=`irule "{*res=EUDATGeteValPid(*pid, *key)}" "*pid=${pid}%*key=EUDAT/CHECKSUM_TIMESTAMP" "*res"`
  val=`echo ${raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
  echo "        EUDAT/CHECKSUM_TIMESTAMP: ${val}"
  irule "{EUDATCreateAVU(*key, *value, *path)}" "*path=${sourcePath}%*key=eudat_dpm_checksum_date:${irods_default_resource}%*value=${val}" ""
  
  echo "        ############ iCAT key/value pairs: ############"
  for k in "PID" "EUDAT/ROR" "EUDAT/FIO" "EUDAT/PARENT" "EUDAT/FIXED_CONTENT" "eudat_dpm_checksum_date:${irods_default_resource}" "EUDAT/REPLICA"
  do
      raw=`irule "{EUDATgetLastAVU(*path, *key, *value)}" "*path=${sourcePath}%*key=$k" "*value"`
      val=`echo ${raw} | cut -d '=' -f 2 | tr -d '[[:space:]]'`
      echo "        $k: ${val}"
  done
}

input_path=`echo $1 | tr -d '[[:space:]]'`

listing () {

  echo "ils ${input_path}"
  IN=`ils ${input_path}`
  while IFS='\n' read -ra ADDR; do
      for i in "${ADDR[@]}"; do
          collection="false"
          item=$i
          if [[ $i =~ ^"  C- ".* ]]
          then
              item=${i//  C- /}
              collection="true"
          fi
          path=`echo ${item} | sed -e 's/^[[:space:]]*//' | tr -d ':'`
          if [[ "$path" = "$input_path" ]] || [[ "$path/" = "$input_path" ]]
          then
             continue 
          fi
          echo "path:$path"
          if [[ $collection = "true" ]]
          then
              sourcePath="$path"
              syncMeta
              input_path=$path
              listing
          else
              echo "${input_path}/$path"
              sourcePath="${input_path}/$path"
              syncMeta
              continue
          fi
      done
  done <<< "$IN"
}

listing

exit 0
