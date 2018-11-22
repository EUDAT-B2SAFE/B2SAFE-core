#!/bin/bash
#
# procedure to install the B2SAFE module using a bash script
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
STATUS=0
EUDAT_RULEFILES=''
JSON_CONFIG="false"
DATE_TODAY=`date +%Y%m%d`
#
# end set default parameters for installation

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
#
#
#============================================
# end default parameters for setup
#
#
IRODS_LINK_DIR="${IRODS_DIR}/iRODS/server/bin/cmd"


########################
# Functions
########################

read_parameters() {

    if [ -e $INSTALL_CONFIG ] 
    then
        source $INSTALL_CONFIG
    else
        echo "ERROR: $INSTALL_CONFIG not present!"
        STATUS=1
    fi

    if [ $STATUS -eq 0 ]
    then
        IRODS_SERVICE_ACCOUNT_CONFIG="${IRODS_CONF_DIR}/service_account.config"
        if [ -e $IRODS_SERVICE_ACCOUNT_CONFIG ]
        then
            source $IRODS_SERVICE_ACCOUNT_CONFIG
        else
            echo "ERROR: $IRODS_SERVICE_ACCOUNT_CONFIG not present!"
            echo "At the moment the file ownership of the b2safe package is wrong!"
            echo "Is iRODS configured?"
            echo "Remove the b2safe package and re-install after configuring iRODS"
            STATUS=1
        fi
    fi

    return $STATUS
}

check_username() {

    username=`whoami`

    if ! [ "$username" == "$IRODS_SERVICE_ACCOUNT_NAME" ]
    then
        echo "ERROR: username: $username is different from the user who runs iRODS: $IRODS_SERVICE_ACCOUNT_NAME"
        echo ""
        echo "please run the script under the correct user:"
        echo "sudo su - $IRODS_SERVICE_ACCOUNT_NAME -s "/bin/bash" -c \"cd ${B2SAFE_PACKAGE_DIR}/package ; ./install.sh\" "
        echo ""
        STATUS=1
    fi

    return $STATUS
}

check_epicclient2_config() {

    COUNTER=0
    PARAMETERS_PRESENT=0

    # check which of the epicclient2 parameters are set
    for parameter in HANDLE_SERVER_URL PRIVATE_KEY CERTIFICATE_ONLY PREFIX HANDLEOWNER REVERSELOOKUP_USERNAME HTTPS_VERIFY 
    do
        let COUNTER=COUNTER+1
        eval processed_parameter=\$$parameter
        if ! [ "${processed_parameter}X" == "X"  ]
        then
           let PARAMETERS_PRESENT=PARAMETERS_PRESENT+1
        fi
    done

    if [ "$COUNTER" -eq "$PARAMETERS_PRESENT" ]
    then
        echo "epicclient2 parameters set. We will use epicclient2"
    else
        BASENAME=$(basename $INSTALL_CONFIG)
        echo "Please add the following parameters to the file: \"${B2SAFE_PACKAGE_DIR}/packaging/${BASENAME}\""
        echo "Update where necessary and rerun the procedure"
        echo ""
        echo "HANDLE_SERVER_URL=\"https://epic3.storage.surfsara.nl:8001\""
        echo "PRIVATE_KEY=\"/path/prefix_suffix_index_privkey.pem\""
        echo "CERTIFICATE_ONLY=\"/path/prefix_suffix_index_certificate_only.pem\""
        echo "PREFIX=\"ZZZ\""
        echo "HANDLEOWNER=\"0.NA/ZZZ\""
        echo "REVERSELOOKUP_USERNAME=\"ZZZ\""
        echo "HTTPS_VERIFY=\"True\""
        echo ""
        STATUS=1
    fi

    return $STATUS

}

check_http_api_config() {

    COUNTER=0
    PARAMETERS_PRESENT=0

    # check which of the http api parameters are set
    for parameter in SERVERAPIREG SERVERAPIPUB
    do
        let COUNTER=COUNTER+1
        eval processed_parameter=\$$parameter
        if ! [ "${processed_parameter}X" == "X"  ]
        then
           let PARAMETERS_PRESENT=PARAMETERS_PRESENT+1
        fi
    done

    if [ "$COUNTER" -eq "$PARAMETERS_PRESENT" ]
    then
        echo "http api parameters set. We will use the http api parameters"
    else
        BASENAME=$(basename $INSTALL_CONFIG)
        echo "Please add the following parameters to the file: \"${B2SAFE_PACKAGE_DIR}/packaging/${BASENAME}\""
        echo "Update where necessary and rerun the procedure"
        echo ""
        echo "SERVERAPIREG=\"https://<hostnameWithFullDomain>/api/registered\""
        echo "SERVERAPIPUB=\"https://<hostnameWithFullDomain>/api/pub\""
        echo ""
        echo "or if no http api is present"
        echo ""
        echo "SERVERAPIREG=\"irods://<hostnameWithFullDomain>:1247\""
        echo "SERVERAPIPUB=\"irods://<hostnameWithFullDomain>:1247\""
        echo ""
        STATUS=1
    fi

    return $STATUS

}

create_links() {

    COUNT=0
    EUDAT_SERVER_CONFIG=$IRODS_CONF_DIR/server.config
    if [ "$JSON_CONFIG" == "true" ]
    then
       EUDAT_SERVER_CONFIG=$IRODS_CONF_DIR/server_config.json
       EUDAT_SERVER_CONFIG_JSON_STRING=`awk 1 ORS=' ' ${EUDAT_SERVER_CONFIG} | sed 's/ //g'`
    fi

    #delete old symbolic links
    for file in $IRODS_CONF_DIR/eudat*.re
    do
        if [ -h $file ]
        then
            rm -v $file
        fi
    done

    # create new symbolic links
    for file in $B2SAFE_PACKAGE_DIR/rulebase/*.re
    do
        LINK=eudat${COUNT}
        if [ "$JSON_CONFIG" == "true" ]
        then
	    echo $EUDAT_SERVER_CONFIG_JSON_STRING | grep -e "re_rulebase_set.*$LINK.*" > /dev/null
        else
            cat $EUDAT_SERVER_CONFIG | grep -e "^reRuleSet.*$LINK.*" > /dev/null
        fi
        if [ $? -ne 0 ]
        then
            EUDAT_RULEFILES="$EUDAT_RULEFILES,$LINK"
        fi
        EUDAT_LINKFILE=$IRODS_CONF_DIR/$LINK.re
        if [ -e $EUDAT_LINKFILE ]
        then
            echo "rm $EUDAT_LINKFILE"
            rm $EUDAT_LINKFILE
        fi
        echo "ln -sf $file $EUDAT_LINKFILE"
        ln -sf $file $EUDAT_LINKFILE

        let COUNT=COUNT+1
    done

    return $STATUS
}


update_server_config() {

    EUDAT_SERVER_CONFIG=$IRODS_CONF_DIR/server.config

    if [ -n "$EUDAT_RULEFILES" ]
    then
       if [ ! -e ${EUDAT_SERVER_CONFIG}.org.${DATE_TODAY} ]
       then
           cp ${EUDAT_SERVER_CONFIG} ${EUDAT_SERVER_CONFIG}.org.${DATE_TODAY} 
       fi
        cat $EUDAT_SERVER_CONFIG | \
            awk -v EUDAT_RULEFILES=$EUDAT_RULEFILES '{
                if ($1 ~ /reRuleSet/) {
                    $2=$2""EUDAT_RULEFILES
                } print $0
            }' > $EUDAT_SERVER_CONFIG.new
            if [ $? -eq 0 ]
            then
                mv $EUDAT_SERVER_CONFIG.new  $EUDAT_SERVER_CONFIG
            else
                echo "ERROR: updating $EUDAT_SERVER_CONFIG failed!"
                STATUS=1
            fi
    fi

    echo "*********************************************************************"
    echo ""
    echo "Please check the file: ${EUDAT_SERVER_CONFIG} by hand                "
    echo "    grep ^reRuleSet ${EUDAT_SERVER_CONFIG}                           "
    echo ""
    echo "It should only have the following eudat{n}.re files mentioned:       "
    echo "    `cd $IRODS_CONF_DIR ; ls -C eudat*.re`       "
    echo ""
    echo "*********************************************************************"


    return $STATUS
}

update_server_config_json() {

    EUDAT_SERVER_CONFIG=$IRODS_CONF_DIR/server_config.json

    if [ -n "$EUDAT_RULEFILES" ]
    then
       if [ ! -e ${EUDAT_SERVER_CONFIG}.org.${DATE_TODAY} ]
       then
           cp ${EUDAT_SERVER_CONFIG} ${EUDAT_SERVER_CONFIG}.org.${DATE_TODAY} 
       fi
       # put json file in a single string so it easier to process.
       EUDAT_SERVER_CONFIG_JSON_STRING=`awk 1 ORS=' ' ${EUDAT_SERVER_CONFIG} | sed 's/ //g'`
       JSON_RULESET=`echo $EUDAT_SERVER_CONFIG_JSON_STRING | sed 's/.*re_rulebase_set":/re_rulebase_set":/ ; s/].*$/]/'` 
       # check for iRODS 4.2.1 and higher because of new format.
       IRODS_SERVER_JSON_CONFIG_FORMAT_2='false'
       echo $JSON_RULESET | grep -e "\"filename\"" > /dev/null
       if [ $? -eq 1 ]
       then
            IRODS_SERVER_JSON_CONFIG_FORMAT_2='true'
       fi
       # create a rule working set..
       JSON_RULESET_WORK=`echo $JSON_RULESET | sed 's/]//'`
       EUDAT_RULEFILES=`echo $EUDAT_RULEFILES | sed 's/,/ /g'`
       for file in $EUDAT_RULEFILES
       do
            if [ "${IRODS_SERVER_JSON_CONFIG_FORMAT_2}" == "false" ]
            then
                 JSON_RULESET_WORK+=",{\"filename\":\"$file\"}"
            else
                 JSON_RULESET_WORK+=",\"$file\""
            fi
       done
       JSON_RULESET_WORK+="]"
       # substitute the new string for the old string
       perl -pi -e "undef $/; s/re_rulebase_set[^\]]*\]/$JSON_RULESET_WORK/" $EUDAT_SERVER_CONFIG
       if [ $? -eq 0 ]
       then
            echo "The file $EUDAT_SERVER_CONFIG has been updated!"
       else
            echo "ERROR: updating $EUDAT_SERVER_CONFIG failed!"
            STATUS=1
       fi
    fi

    echo "*********************************************************************"
    echo ""
    echo "Please check the file: ${EUDAT_SERVER_CONFIG} by hand                "
    echo "    grep -A5 re_rulebase_set ${EUDAT_SERVER_CONFIG}                  "
    echo ""
    echo "It should only have the following eudat{n}.re files mentioned:       "
    echo "    `cd $IRODS_CONF_DIR ; ls -C eudat*.re`       "
    echo ""
    echo "*********************************************************************"


    return $STATUS
}

update_irods_core_resource() {

    IRODS_COREFILE=$IRODS_CONF_DIR/core.re
    if [ ! -e ${IRODS_COREFILE}.org.${DATE_TODAY} ]
    then
        cp $IRODS_COREFILE ${IRODS_COREFILE}.org.${DATE_TODAY} 
    fi
    cat $IRODS_COREFILE | \
        awk -v DEFAULT_RESOURCE=$DEFAULT_RESOURCE '{
            if ( $1 ~ /acSetRescSchemeForCreate|acSetRescSchemeForRepl/ ) {
                $2="{msiSetDefaultResc(\""DEFAULT_RESOURCE"\",\"null\"); }"
                $0=$1" "$2
            } print $0
        }' >  $IRODS_COREFILE.new
        if [ $? -eq 0 ]
        then
            mv $IRODS_COREFILE.new  $IRODS_COREFILE
        else
            echo "ERROR: updating $IRODS_COREFILE failed!"
            STATUS=1
        fi

    return $STATUS
}

install_python_scripts() {

    # link all files except epicclient*.py
    for file in `find $B2SAFE_PACKAGE_DIR/cmd/* | egrep -v ".new|.org|.~|epicclient" | sort `
    do
        SHORTFILE="${file##*/}"
        EXTENSION="${file##*.}"
        PYTHON_LINKFILE=$IRODS_LINK_DIR/$SHORTFILE
        if [ -e $PYTHON_LINKFILE ]
        then
            echo "rm $PYTHON_LINKFILE"
            rm $PYTHON_LINKFILE
        fi
        echo "ln -sf $file $PYTHON_LINKFILE"
        ln -sf $file $PYTHON_LINKFILE

        # make the file executable
        if [ "$EXTENSION" == "py" ]
        then
            chmod u+x $file
        fi
    done

    # link the correct epicclient
    SHORTFILE=epicclient.py
    PYTHON_LINKFILE=$IRODS_LINK_DIR/$SHORTFILE
    file=`find $B2SAFE_PACKAGE_DIR/cmd/epicclient2.py` 
    if [ -e $PYTHON_LINKFILE ]
    then
        echo "rm $PYTHON_LINKFILE"
        rm $PYTHON_LINKFILE
    fi
    # link the correct file
    echo "ln -sf $file $PYTHON_LINKFILE"
    ln -sf $file $PYTHON_LINKFILE
    # make the file executable
    chmod u+x $file

    return $STATUS
}

update_get_epic_api_parameters() {

    B2SAFE_LOCALFILE=$B2SAFE_PACKAGE_DIR/rulebase/local.re
    if [ ! -e ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} ]
    then
        cp $B2SAFE_LOCALFILE ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} 
    fi
    cat $B2SAFE_LOCALFILE | \
        awk -F= -v CRED_STORE_TYPE=$CRED_STORE_TYPE -v CRED_FILE_PATH=$CRED_FILE_PATH -v SERVER_ID=$SERVER_ID '{
            if ( $1 ~ /^ +\*credStoreType/ ) {
                $1=$1"=\""CRED_STORE_TYPE"\";"
                $2=""
            }
            if ( $1 ~ /^ +\*credStorePath/ ) {
                $1=$1"=\""CRED_FILE_PATH"\";"
                $2=""
            }
            if ( $1 ~ /^ +\*serverID/ ) {
                $1=$1"=\""SERVER_ID"\";"
                $2=""
            } print $0
        }' >  $B2SAFE_LOCALFILE.new
    if [ $? -eq 0 ]
    then
        mv $B2SAFE_LOCALFILE.new  $B2SAFE_LOCALFILE
    else
        echo "ERROR: updating $B2SAFE_LOCALFILE failed!"
        STATUS=1
    fi

    return $STATUS
}

update_epicclient2_credentials() {

    echo -n "enter the password belonging to the credentals of reverse lookup username: $REVERSELOOKUP_USERNAME for prefix: $PREFIX :"
    read -s REVERSELOOKUP_PASSWORD
    echo ""

    if [ ! -e ${CRED_FILE_PATH}.org.${DATE_TODAY} ]
    then
        if [ -e $CRED_FILE_PATH ]
        then
           cp $CRED_FILE_PATH ${CRED_FILE_PATH}.org.${DATE_TODAY} 
           # set access mode to file
           chmod 600 ${CRED_FILE_PATH}.org.${DATE_TODAY}
        fi
    fi

    CRED_FILE_PATH_EXAMPLE=$B2SAFE_PACKAGE_DIR/conf/credentials_epicclient2_example
    cat $CRED_FILE_PATH_EXAMPLE | \
        awk -v HANDLE_SERVER_URL=$HANDLE_SERVER_URL -v PRIVATE_KEY=$PRIVATE_KEY -v CERTIFICATE_ONLY=$CERTIFICATE_ONLY -v PREFIX=$PREFIX -v HANDLEOWNER=$HANDLEOWNER -v REVERSELOOKUP_USERNAME=$REVERSELOOKUP_USERNAME -v REVERSELOOKUP_PASSWORD=$REVERSELOOKUP_PASSWORD  -v HTTPS_VERIFY=$HTTPS_VERIFY '{
            if ( $1 ~ /handle_server_url/ ) {
                $0="    \"handle_server_url\": \""HANDLE_SERVER_URL"\","
            }
            if ( $1 ~ /private_key/ ) {
                $0="    \"private_key\": \""PRIVATE_KEY"\","
            }
            if ( $1 ~ /certificate_only/ ) {
                $0="    \"certificate_only\": \""CERTIFICATE_ONLY"\","
            }
            if ( $1 ~ /prefix/ ) {
                $0="    \"prefix\": \""PREFIX"\","
            }
            if ( $1 ~ /handleowner/ ) {
                $0="    \"handleowner\": \""HANDLEOWNER"\","
            }
            if ( $1 ~ /"reverselookup_username/ ) {
                $0="    \"reverselookup_username\": \""REVERSELOOKUP_USERNAME"\","
            }
            if ( $1 ~ /reverselookup_password/ ) {
                $0="    \"reverselookup_password\": \""REVERSELOOKUP_PASSWORD"\","
            }
            if ( $1 ~ /HTTPS_verify/ ) {
                $0="    \"HTTPS_verify\": \""HTTPS_VERIFY"\""
            } print $0
        }' >  $CRED_FILE_PATH.new
    if [ $? -eq 0 ]
    then
        mv $CRED_FILE_PATH.new   $CRED_FILE_PATH
    else
        echo "ERROR: updating $CRED_FILE_PATH failed!"
        STATUS=1
    fi

    # set access mode to file
    chmod 600 $CRED_FILE_PATH

    return $STATUS
}

update_get_auth_parameters() {

    AUTH_MAP_PATH=$B2SAFE_PACKAGE_DIR/conf/authz.map.json
    B2SAFE_LOCALFILE=$B2SAFE_PACKAGE_DIR/rulebase/local.re
    if [ ! -e ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} ]
    then
        cp $B2SAFE_LOCALFILE ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} 
    fi
    cat $B2SAFE_LOCALFILE | \
        awk -F= -v AUTH_MAP_PATH=$AUTH_MAP_PATH '{
            if ( $1 ~ /^ +\*authZMapPath/ ) {
                $1=$1"=\""AUTH_MAP_PATH"\";"
                $2=""
            } print $0
        }' >  $B2SAFE_LOCALFILE.new
    if [ $? -eq 0 ]
    then
        mv $B2SAFE_LOCALFILE.new  $B2SAFE_LOCALFILE
    else
        echo "ERROR: updating $B2SAFE_LOCALFILE failed!"
        STATUS=1
    fi

    return $STATUS
}

update_authz_map_json() {
    AUTH_MAP_PATH=$B2SAFE_PACKAGE_DIR/conf/authz.map.json
    TMP_FILE=/tmp/authz.map.json
    if [ ! -e ${AUTH_MAP_PATH}.org.${DATE_TODAY} ]
    then
        cp $AUTH_MAP_PATH ${AUTH_MAP_PATH}.org.${DATE_TODAY} 
    fi

    # constrict a list of users to fill in the userlist
    let count=0
    for user in $USERS 
    do
        if [ "$count" -lt "1" ]
        then
            userlist=$user
        else
            userlist+="\",\"$user"
        fi
    let count=$count+1
    done

    cat > $TMP_FILE << EOF
{
"assertion 1":
	{ "subject":
		[ "$userlist" ],
	  "action":
		[ "read" ],
	  "target":
		[ "${IRODS_LINK_DIR}/*","${B2SAFE_PACKAGE_DIR}/conf/*" ]
	}
}

EOF
    if [ $? -eq 0 ]
    then
        mv $TMP_FILE $AUTH_MAP_PATH
        if [ ! $? -eq 0 ]
        then
            echo "ERROR: moving $AUTH_MAP_PATH failed!"
            STATUS=1
        fi
    else
        echo "ERROR: creating $TMP_FILE failed!"
        STATUS=1
    fi

    # set access mode to file
    chmod 600 $AUTH_MAP_PATH

    return $STATUS
}

update_get_log_parameters() {

    LOG_MANAGER_CONF=$B2SAFE_PACKAGE_DIR/conf/log.manager.conf
    B2SAFE_LOCALFILE=$B2SAFE_PACKAGE_DIR/rulebase/local.re
    if [ ! -e ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} ]
    then
        cp $B2SAFE_LOCALFILE ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} 
    fi
    cat $B2SAFE_LOCALFILE | \
        awk -F= -v LOG_MANAGER_CONF=$LOG_MANAGER_CONF '{
            if ( $1 ~ /^ +\*logConfPath/ ) {
                $1=$1"=\""LOG_MANAGER_CONF"\";"
                $2=""
            } print $0
        }' >  $B2SAFE_LOCALFILE.new
    if [ $? -eq 0 ]
    then
        mv $B2SAFE_LOCALFILE.new  $B2SAFE_LOCALFILE
    else
        echo "ERROR: updating $B2SAFE_LOCALFILE failed!"
        STATUS=1
    fi

    return $STATUS
}

update_log_manager_conf() {

    LOG_MANAGER_CONF=$B2SAFE_PACKAGE_DIR/conf/log.manager.conf

    if [ ! -e ${LOG_MANAGER_CONF}.org.${DATE_TODAY} ]
    then
        cp $LOG_MANAGER_CONF ${LOG_MANAGER_CONF}.org.${DATE_TODAY} 
    fi

    cat $LOG_MANAGER_CONF | \
        awk -v LOG_LEVEL=$LOG_LEVEL -v LOG_DIR=$LOG_DIR '{
            if ( $1 ~ /log_level/ ) {
                $0="\"log_level\": \""LOG_LEVEL"\","
            }
            if ( $1 ~ /log_dir/ ) {
                $0="\"log_dir\": \""LOG_DIR"\","
            } print $0
        }' >  $LOG_MANAGER_CONF.new
    if [ $? -eq 0 ]
    then
        mv $LOG_MANAGER_CONF.new   $LOG_MANAGER_CONF
    else
        echo "ERROR: updating $LOG_MANAGER_CONF failed!"
        STATUS=1
    fi

    return $STATUS
}

update_get_metadata_parameters() {

    METADATA_MANAGER_CONF=$B2SAFE_PACKAGE_DIR/conf/metadataManager.conf
    B2SAFE_LOCALFILE=$B2SAFE_PACKAGE_DIR/rulebase/local.re
    if [ ! -e ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} ]
    then
        cp $B2SAFE_LOCALFILE ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} 
    fi
    cat $B2SAFE_LOCALFILE | \
        awk -F= -v METADATA_MANAGER_CONF=$METADATA_MANAGER_CONF '{
            if ( $1 ~ /^ +\*metaConfPath/ ) {
                $1=$1"=\""METADATA_MANAGER_CONF"\";"
                $2=""
            } print $0
        }' >  $B2SAFE_LOCALFILE.new
    if [ $? -eq 0 ]
    then
        mv $B2SAFE_LOCALFILE.new  $B2SAFE_LOCALFILE
    else
        echo "ERROR: updating $B2SAFE_LOCALFILE failed!"
        STATUS=1
    fi

    return $STATUS
}

update_get_conf_parameters() {

    B2SAFE_LOCALFILE=$B2SAFE_PACKAGE_DIR/rulebase/local.re
    if [ ! -e ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} ]
    then
        cp $B2SAFE_LOCALFILE ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} 
    fi
    cat $B2SAFE_LOCALFILE | \
        awk -F= -v AUTHZ_ENABLED=$AUTHZ_ENABLED -v MSG_QUEUE_ENABLED=$MSG_QUEUE_ENABLED '{
            if ( $1 ~ /^ +\*authzEnabled/ ) {
                $1=$1"=bool(\""AUTHZ_ENABLED"\");"
                $2=""
            } 
            if ( $1 ~ /^ +\*messageQueueEnabled/ ) {
                $1=$1"=\""MSG_QUEUE_ENABLED"\";"
                $2=""
            } print $0
        }' >  $B2SAFE_LOCALFILE.new
    if [ $? -eq 0 ]
    then
        mv $B2SAFE_LOCALFILE.new  $B2SAFE_LOCALFILE
    else
        echo "ERROR: updating $B2SAFE_LOCALFILE failed!"
        STATUS=1
    fi

    return $STATUS
}

update_get_http_api_parameters() {

    B2SAFE_LOCALFILE=$B2SAFE_PACKAGE_DIR/rulebase/local.re
    if [ ! -e ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} ]
    then
        cp $B2SAFE_LOCALFILE ${B2SAFE_LOCALFILE}.org.${DATE_TODAY} 
    fi
    cat $B2SAFE_LOCALFILE | \
        awk -F= -v SERVERAPIREG=$SERVERAPIREG -v SERVERAPIPUB=$SERVERAPIPUB '{
            if ( $1 ~ /^ +\*serverApireg/ ) {
                $1=$1"=\""SERVERAPIREG"\";"
                $2=""
            } 
            if ( $1 ~ /^ +\*serverApipub/ ) {
                $1=$1"=\""SERVERAPIPUB"\";"
                $2=""
            } print $0
        }' >  $B2SAFE_LOCALFILE.new
    if [ $? -eq 0 ]
    then
        mv $B2SAFE_LOCALFILE.new  $B2SAFE_LOCALFILE
    else
        echo "ERROR: updating $B2SAFE_LOCALFILE failed!"
        STATUS=1
    fi

    return $STATUS
}


########################
# main program
########################


#
# read parameter file
#
echo "read_parameters"
read_parameters
STATUS=$?
#
# check user doing actions. It should be the user from:
# /etc/irods/service_account.config
#
if [ $STATUS -eq 0 ]
then
    echo "check username"
    check_username
    STATUS=$?
fi

#
# check for json or normal config files
# irods 4.1 and higher use json config files
#
if [ $STATUS -eq 0 ]
then
    echo "check iRODS config files"
    if [ "${IRODS_DIR}" == "/var/lib/irods/iRODS" ]
    then
        IRODS_DIR="/var/lib/irods"
    fi
    if [ -e "${IRODS_DIR}/VERSION.json" ]
    then
        JSON_CONFIG="true"
        echo "We have iRODS 4.1 or higher. The config files are in json format"
    fi
    if [ -e "${IRODS_DIR}/msiExecCmd_bin" ]
    then
        IRODS_LINK_DIR=${IRODS_DIR}/msiExecCmd_bin
        echo "We have iRODS 4.2 or higher. The \"msiExecCmd_bin\" is present"
    else
        IRODS_LINK_DIR="${IRODS_DIR}/iRODS/server/bin/cmd"
    fi 
fi

#
# check if credentials for epicclient2 are set. Default we want to use epicclient2
# if they are NOT set ask if the user is really sure to use the old epicclient 
#
if [ $STATUS -eq 0 ]
then
    echo "check epicclient2 config in install.conf"
    check_epicclient2_config
    STATUS=$?
fi

#
# check if parameters for http api are set.
# if they are NOT set ask the user to add them
#
if [ $STATUS -eq 0 ]
then
    echo "check http api config in install.conf"
    check_http_api_config
    STATUS=$?
fi

#
# create symbolic links to the eudat rulebase
#
if [ $STATUS -eq 0 ]
then
    echo "create_links"
    create_links
    STATUS=$?
fi

#
# edit /etc/irods/server.config or /etc/irods/server_config.json
# append eudat specific rules to to reRuleSet.
# we use links in the type of eudatxy.re.
# (make sure to include the comma and no spaces)
#
if [ $STATUS -eq 0 ]
then
    echo "update_server_config"
    if [ "$JSON_CONFIG" == "false" ]
    then
        update_server_config
        STATUS=$?
    else
        update_server_config_json
        STATUS=$?
    fi
fi

#
# properly configure the default resource in /etc/irods/core.re
#
if [ $STATUS -eq 0 ]
then
    echo "update_irods_core_resource"
    update_irods_core_resource
    STATUS=$?
fi

#
# install python scripts
#
if [ $STATUS -eq 0 ]
then
    echo "install_python_scripts"
    install_python_scripts
    STATUS=$?
fi

#
# update the 'getEpicApiParameters' rule in '/opt/eudat/b2safe/rulebase/local.re'
#
if [ $STATUS -eq 0 ]
then
    echo "update_get_epic_api_parameters"
    update_get_epic_api_parameters
    STATUS=$?
fi

#
# Set the proper values in the credentials file
#
if [ $STATUS -eq 0 ]
then
    echo "update_epicclient2_credentials"
    update_epicclient2_credentials
    STATUS=$?
fi

#
# update the 'getAuthZParameters' rule in '/opt/eudat/b2safe/rulebase/local.re'
# update authz.map.json
#
if [ $STATUS -eq 0 ]
then
    echo "update_authz_map_json"
    update_get_auth_parameters
    STATUS=$?
fi

#
# update the "getLogParameters" rule in "/opt/eudat/b2safe/rulebase/local.re"
# update log.manager.conf
#
if [ $STATUS -eq 0 ]
then
    echo "update_log_manager_conf"
    update_get_log_parameters
    update_log_manager_conf
    STATUS=$?
fi

#
# update the "getMetaParameters" rule in "/opt/eudat/b2safe/rulebase/local.re"
#
if [ $STATUS -eq 0 ]
then
    echo "update_metadata_manager"
    update_get_metadata_parameters
    STATUS=$?
fi

#
# update the "getConfParameters" rule in "/opt/eudat/b2safe/rulebase/local.re"
#
if [ $STATUS -eq 0 ]
then
    echo "update_conf_parameters"
    update_get_conf_parameters
    STATUS=$?
fi

#
# update the "getConfParameters" rule in "/opt/eudat/b2safe/rulebase/local.re"
#
if [ $STATUS -eq 0 ]
then
    echo "update_http_api_parameters"
    update_get_http_api_parameters
    STATUS=$?
fi
