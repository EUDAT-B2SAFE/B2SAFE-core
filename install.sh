#!/bin/bash
#
# procedure to install the B2SAFE module using a bash script
#
# set tabstop=4
# set expendtab
#
#set -x
#
INSTALL_CONFIG=./install.conf
STATUS=0
EUDAT_RULEFILES=''

# start default parameters for setup
IRODS_DIR=/opt/irods3.3/iRODS
#
# the directory where trunk of B2SAFE is housed
TRUNK_DIR=/home/rods/svn/iRODS-modules/BE2SAFE/trunk
#
B2SAFE_MODULE_DIR=$IRODS_DIR/modules/B2SAFE
#
# the default iRODS resource to use
DEFAULT_RESOURCE=eudat
#
# credentials type and location
CRED_STORE_TYPE=os
CRED_FILE_PATH=$B2SAFE_MODULE_DIR/cmd
#
# credentials for server id
SERVER_ID=
BASE_URI=
USERNAME=
PREFIX=
#
#
USERS=
LOG_LEVEL=
LOG_DIR=
SHARED_SPACE=
# end default parameters for setup



########################
# Functions
########################

read_parameters() {

    if [ -e $INSTALL_CONFIG ]
    then
        . $INSTALL_CONFIG
    else
        echo "ERROR: $INSTALL_CONFIG not present!"
        STATUS=1
    fi

    return $STATUS
}

copy_trunk() {

    if [ -e $IRODS_DIR ]
    then
        if [ -e $TRUNK_DIR ]
        then
            echo "mkdir $B2SAFE_MODULE_DIR"
            mkdir $B2SAFE_MODULE_DIR
            echo "cp -r $TRUNK_DIR $B2SAFE_MODULE_DIR"
            cp -rf $TRUNK_DIR/* $B2SAFE_MODULE_DIR
        else
            echo "ERROR: $TRUNK_DIR not present!"
            STATUS=1
        fi
    else
        echo "ERROR: $IRODS_DIR not present!"
        STATUS=1
    fi

    return $STATUS
}

enable_module() {

    cd $IRODS_DIR ; $IRODS_DIR/scripts/configure --enable-B2SAFE
    if [ $? -eq 0 ]
    then
        echo "make clean"
        cd $IRODS_DIR ; make clean
        echo "make"
        cd $IRODS_DIR ; make
        echo "$IRODS_DIR/irodsctl restart"
        $IRODS_DIR/irodsctl restart
    else
        echo "ERROR: enabling B2SAFE failed!"
        STATUS=1
    fi
    return $STATUS
}

create_links() {

    COUNT=0
    EUDAT_SERVER_CONFIG=$IRODS_DIR/server/config/server.config

    for file in `find $B2SAFE_MODULE_DIR/rulebase/*.re | sort `
    do
        LINK=eudat${COUNT}
        grep "^reRuleSet.*$LINK.*"  $EUDAT_SERVER_CONFIG > /dev/null
        if [ $? -ne 0 ]
        then
            EUDAT_RULEFILES="$EUDAT_RULEFILES,$LINK"
        fi
        EUDAT_LINKFILE=$IRODS_DIR/server/config/reConfigs/$LINK.re
        if [ -e $EUDAT_LINKFILE ]
        then
            echo "rm $EUDAT_LINKFILE"
            rm $EUDAT_LINKFILE
        fi
        echo "ln -s $file $EUDAT_LINKFILE"
        ln -s $file $EUDAT_LINKFILE

        let COUNT=COUNT+1
    done

    return $STATUS
}


update_server_config() {

    EUDAT_SERVER_CONFIG=$IRODS_DIR/server/config/server.config

    if [ -n "$EUDAT_RULEFILES" ]
    then
        cat $EUDAT_SERVER_CONFIG | \
            awk -v EUDAT_RULEFILES=$EUDAT_RULEFILES '{
                if ($1 ~ /reRuleSet/) {
                    $2=$2EUDAT_RULEFILES
                } print $0
            }' > $EUDAT_SERVER_CONFIG.new

            if [ $? -eq 0 ]
            then
                mv $EUDAT_SERVER_CONFIG      $EUDAT_SERVER_CONFIG.org
                mv $EUDAT_SERVER_CONFIG.new  $EUDAT_SERVER_CONFIG
            else
                echo "ERROR: updating $EUDAT_SERVER_CONFIG failed!"
                STATUS=1
            fi
    fi

    return $STATUS
}

configure_irods_hooks() {

    IRODS_COREFILE=$IRODS_DIR/server/config/reConfigs/core.re
    TMP_FILE=/tmp/irodshooks.re

    status=$(awk '/acPostProcForPut/{f=1}/(\*\.replicate)|(\*\.pid\.create)/{g=1;exit}END{print g&&f ?1:0}' $IRODS_COREFILE)

    if [ $status -eq 0 ]
    then

        cat > $TMP_FILE << EOF

acPostProcForPut {
    ON(\$objPath like "\*.replicate") {
        processReplicationCommandFile();
    }
}
acPostProcForPut {
    ON(\$objPath like "\*.pid.create") {
        processPIDCommandFile();
    }
}

EOF

       if [ $? -eq 0 ]
       then
            cat $TMP_FILE $IRODS_COREFILE > $IRODS_COREFILE.new
            if [ $? -eq 0 ]
            then
                mv $IRODS_COREFILE      $IRODS_COREFILE.org
                mv $IRODS_COREFILE.new  $IRODS_COREFILE
            else
                echo "ERROR: creating $IRODS_COREFILE.new failed!"
                STATUS=1
            fi
       else
            echo "ERROR: creating $TMP_FILE failed!"
            STATUS=1
       fi
    fi

    return $STATUS
}

update_irods_core_resource() {

    IRODS_COREFILE=$IRODS_DIR/server/config/reConfigs/core.re
    cat $IRODS_COREFILE | \
        awk -v DEFAULT_RESOURCE=$DEFAULT_RESOURCE '{
            if ( $1 ~ /acSetRescSchemeForCreate|acSetRescSchemeForRepl/ ) {
                $2="{msiSetDefaultResc(\""DEFAULT_RESOURCE"\",\"null\");}"
                $0=$1" "$2
            } print $0
        }' >  $IRODS_COREFILE.new
        if [ $? -eq 0 ]
        then
            mv $IRODS_COREFILE      $IRODS_COREFILE.org
            mv $IRODS_COREFILE.new  $IRODS_COREFILE
        else
            echo "ERROR: updating $IRODS_COREFILE failed!"
            STATUS=1
        fi

    return $STATUS
}

install_python_scripts() {

    for file in `find $B2SAFE_MODULE_DIR/cmd/*  | grep -v ".new" | grep -v ".org" | sort `
    do
        SHORTFILE="${file##*/}"
        EXTENSION="${file##*.}"
        PYTHON_LINKFILE=$IRODS_DIR/server/bin/cmd/$SHORTFILE
        if [ -e $PYTHON_LINKFILE ]
        then
            echo "rm $PYTHON_LINKFILE"
            rm $PYTHON_LINKFILE
        fi
        echo "ln -s $file $PYTHON_LINKFILE"
        ln -s $file $PYTHON_LINKFILE

        # make the file executable
        if [ "$EXTENSION" == "py" ]
        then
            chmod +x $file
        fi

    done

    return $STATUS
}

update_get_epic_api_parameters() {

    B2SAFE_LOCALFILE=$B2SAFE_MODULE_DIR/rulebase/local.re
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
        mv $B2SAFE_LOCALFILE      $B2SAFE_LOCALFILE.org
        mv $B2SAFE_LOCALFILE.new  $B2SAFE_LOCALFILE
    else
        echo "ERROR: updating $B2SAFE_LOCALFILE failed!"
        STATUS=1
    fi

    return $STATUS
}

update_credentials() {

    echo -n "enter the password belonging to the credentals of username: $USERNAME for prefix: $PREFIX :"
    read -s PASSWORD

    CRED_FILE_PATH_EXAMPLE=$B2SAFE_MODULE_DIR/cmd/credentials_example
    cat $CRED_FILE_PATH_EXAMPLE | \
        awk -v BASE_URI=$BASE_URI -v USERNAME=$USERNAME -v PREFIX=$PREFIX -v PASSWORD=$PASSWORD '{
            if ( $1 ~ /baseuri/ ) {
                $0="    \"baseuri\": \""BASE_URI"\","
            }
            if ( $1 ~ /"username/ ) {
                $0="    \"username\": \""USERNAME"\","
            }
            if ( $1 ~ /prefix/ ) {
                $0="    \"prefix\": \""PREFIX"\","
            }
            if ( $1 ~ /password/ ) {
                $0="    \"password\": \""PASSWORD"\","
            } print $0
        }' >  $CRED_FILE_PATH.new
    if [ $? -eq 0 ]
    then
        mv $CRED_FILE_PATH       $CRED_FILE_PATH.org
        mv $CRED_FILE_PATH.new   $CRED_FILE_PATH
    else
        echo "ERROR: updating $CRED_FILE_PATH failed!"
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

#
# copy trunk to modules dir in irods
#
if [ $? -eq 0 ]
then
    echo "copy_trunk"
    copy_trunk
fi

#
# enable module
#
if [ $? -eq 0 ]
then
    echo "enable_module"
    enable_module
fi

#
# create symbolic links to the eudat rulebase
#
if [ $? -eq 0 ]
then
    echo "create_links"
    create_links
fi

#
# edit <irods>/server/config/server.config
# append ",eudat,replication,pid-service,catchError,eudat-authZ-filters,local" to reRuleSet
# (make sure to include the comma and no spaces)
#
if [ $? -eq 0 ]
then
    echo "update_server_config"
    update_server_config
fi

#
# configure iRODS hooks
#
if [ $? -eq 0 ]
then
    echo "configure_irods_hooks"
    configure_irods_hooks
fi

#
# properly configure the default resource in <irods>/server/config/reConfigs/core.re
#
if [ $? -eq 0 ]
then
    echo "update_irods_core_resource"
    update_irods_core_resource
fi

#
# install python scripts
#
if [ $? -eq 0 ]
then
    echo "install_python_scripts"
    install_python_scripts
fi

#
# update the 'getEpicApiParameters' rule in './server/config/reConfigs/local.re'
#
if [ $? -eq 0 ]
then
    echo "update_get_epic_api_parameters"
    update_get_epic_api_parameters
fi

#
# Set the proper values in the credentials file
#
if [ $? -eq 0 ]
then
    echo "update_credentials"
    update_credentials
fi

#
# update the 'getAuthZParameters' rule in './server/config/reConfigs/local.re'
#

#
# update the "getLogParameters" rule in "./server/config/reConfigs/local.re"
#

#
# create a shared space in all zones as configured in the eudat.re rulebase getSharedCollection function.
#


