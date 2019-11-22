#
# procedure to convert the B2SAFE parameters to json using a bash script
#
# set tabstop=4
# set expandtab
#
#set -x
#
#
#
# set default parameters for installation
INSTALL_CONFIG=./install.conf

# start default parameters for setup
#===================================
IRODS_CONF_DIR=/etc/irods
#
IRODS_DIR=/var/lib/irods
#
B2SAFE_PACKAGE_DIR=/opt/eudat/b2safe
#
# the default iRODS resource to use
DEFAULT_RESOURCE=eudat
#
# credentials type and location
CRED_STORE_TYPE=os
CRED_FILE_PATH=$B2SAFE_PACKAGE_DIR/conf
SERVER_ID=
SERVERAPIREG=
SERVERAPIPUB=

#
# credentials for epicclient2
HANDLE_SERVER_URL=
PRIVATE_KEY=
CERTIFICATE_ONLY=
PREFIX=
HANDLEOWNER=
REVERSELOOKUP_USERNAME=
HTTPS_VERIFY=
#
USERS=
LOG_LEVEL=
LOG_DIR=
SHARED_SPACE=
#
# EUDAT iRODS rules behavioral parameters. Because these are later added
# sensible defaults are chosen. They can be overridden by adding them to
# the configuration in install.conf
AUTHZ_ENABLED=true
MSG_QUEUE_ENABLED=false


if [ -e $INSTALL_CONFIG ]
then
  source $INSTALL_CONFIG
else
  echo "ERROR: $INSTALL_CONFIG not present!"
  STATUS=1
fi

# remove trailing /iRODS or /iRODS/ from IRODS_DIR
IRODS_DIR=${IRODS_DIR%/iRODS}
IRODS_DIR=${IRODS_DIR%/iRODS/}

# empty server_api_reg
if [ "x" == "x${SERVERAPIREG}"  ]
then
  echo "WARNING: server_api_reg is empty in install.json. Please give it a reasonable value."
  echo "         if the http api is not implemented make it the same as the server_id."
  echo ""
fi

# empty server_api_pub
if [ "x" == "x${SERVERAPIPUB}"  ]
then
  echo "WARNING: server_api_pub is empty in install.json. Please give it a reasonable value."
  echo "         if the http api is not implemented make it the same as the server_id."
  echo ""
fi

#empty handle_reverse_lookup_password
echo "WARNING: handle_reverse_lookup_password is empty in install.json. Please give it a reasonable value."
echo "         It can be retrieved from /opt/eudat/b2safe/conf/credentials"
echo ""

# set handle_https_verify
string=$(echo "$HTTPS_VERIFY" | tr '[:upper:]' '[:lower:]')
if [[ $string =~ .*true.* ]]
then
  HTTPS_VERIFY_STRING=true
elif [[ $string =~ .*false.* ]]
then
  HTTPS_VERIFY_STRING=false
else
  HTTPS_VERIFY_STRING="\"${HTTPS_VERIFY}\""
fi

# set handle_users
let count=0
handle_users_array=(`echo ${USERS} | sed 's/[\t ]+/\n/g'`)
handle_users_string=
for each in ${handle_users_array[@]}
do
  if [[ $each =~ .*user0#Zone0.* || $each =~ .*user1#Zone1.* ]]
  then
    echo "WARNING: handle_users has a default value: \"$each\" in install.json. Please give it a reasonable value."
    echo "         This will be enforced with the msi_pid uService."
    echo ""
  fi
  if [ $count -eq 0 ]
  then
    handle_users_string=$(echo -n "\"$each\"")
  else
    handle_users_string=$handle_users_string$(echo -n ", \"$each\"")
  fi
  let count=$count+1
done

cat > install.json << EOT
{
  "b2safe_package_dir": "${B2SAFE_PACKAGE_DIR}",
  "irods_conf_dir": "${IRODS_CONF_DIR}",
  "irods_dir": "${IRODS_DIR}",
  "irods_default_resource": "${DEFAULT_RESOURCE}",
  "cred_store_type": "${CRED_STORE_TYPE}",
  "cred_file_path": "${CRED_FILE_PATH}",
  "server_id": "${SERVER_ID}",
  "server_api_reg": "${SERVERAPIREG}",
  "server_api_pub": "${SERVERAPIPUB}",
  "handle_server_url": "${HANDLE_SERVER_URL}",
  "handle_private_key": "${PRIVATE_KEY}",
  "handle_certificate_only": "${CERTIFICATE_ONLY}",
  "handle_prefix": "${PREFIX}",
  "handle_owner": "${HANDLEOWNER}",
  "handle_reverse_lookup_name": "${REVERSELOOKUP_USERNAME}",
  "handle_reverse_lookup_password": "",
  "handle_https_verify": ${HTTPS_VERIFY_STRING},
  "handle_users": [ ${handle_users_string} ],
  "handle_groups": [  ],
  "log_level": "${LOG_LEVEL}",
  "log_directory": "${LOG_DIR}",
  "shared_space": "${SHARED_SPACE}",
  "authz_enabled": ${AUTHZ_ENABLED},
  "msg_queue_enabled": ${MSG_QUEUE_ENABLED}
}
EOT

chmod 600 install.json
