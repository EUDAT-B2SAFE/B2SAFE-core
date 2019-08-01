#!/bin/bash

# default version
VERSION=centos7_4_2_6
CLEANUP="yes"

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        "--nocleanup")
            CLEANUP="no"
            shift
            ;;
        *)
            VERSION=$1
            shift
            ;;
    esac
done

set -x
set -e

IRODS_VERSION=$( echo $VERSION | awk 'BEGIN{ FS="_"; }{ print $2"."$3"."$4; }' )

cleanup () {
    exit_code=$?
    if [ "$CLEANUP" = "yes" ]
    then
        docker-compose -f ci/${VERSION}/docker-compose.yml down -v
    fi
    exit $exit_code
}

trap cleanup EXIT ERR INT TERM

docker-compose -f ci/${VERSION}/docker-compose.yml build
docker-compose -f ci/${VERSION}/docker-compose.yml up -d

# find directory where we are executing:
ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
MAJOR_VERS=`grep "^\s*\*major_version" $ABSOLUTE_PATH/../rulebase/local.re | awk -F\" '{print $2}'`
MINOR_VERS=`grep "^\s*\*minor_version" $ABSOLUTE_PATH/../rulebase/local.re | awk -F\" '{print $2}'`
SUB_VERS=`grep "^\s*\*sub_version" $ABSOLUTE_PATH/../rulebase/local.re | awk -F\" '{print $2}'`
RPM_VERSION="${MAJOR_VERS}.${MINOR_VERS}-${SUB_VERS}"


EXEC="docker exec ${VERSION}_icat_1"
EXEC_IRODS="docker exec -u irods ${VERSION}_icat_1 "
# copy source tree
$EXEC cp -r /build /src/B2SAFE-core

# install RPM
$EXEC rpm -i /build/ci/RPMS/Centos/7/irods-${IRODS_VERSION}/irods-eudat-b2safe-${RPM_VERSION}.noarch.rpm

# copy configuration
if [ -e ~/secret ]
then
    cp ~/secret/* ci/secret
fi

$EXEC cp /build/ci/secret/308_21.T12995_TRAINING_certificate_only.pem  /etc/irods/308_21.T12995_TRAINING_certificate_only.pem
$EXEC cp /build/ci/secret/308_21.T12995_TRAINING_privkey.pem  /etc/irods/308_21.T12995_TRAINING_privkey.pem
$EXEC cp /build/ci/secret/epic2_credentials /src/B2SAFE-core/scripts/tests/resources
$EXEC /app/update_install.py /opt/eudat/b2safe/packaging/install.json /build/ci/secret/install.json
$EXEC_IRODS bash -c "cd /opt/eudat/b2safe/packaging/ ; python install.py;"

# execute tests
for t in epic2 irods b2safe
do
    echo "------ TEST -----"
    echo " $t "
    echo "-----------------"
    TEST_DIR="/src/B2SAFE-core/scripts/tests/"
    SET_ENV="set -x; set -e; export url_prefix_in_profile='true'; export prefix=21.T12996"
    $EXEC_IRODS bash -c "$SET_ENV; cd $TEST_DIR; python testB2SafeCmd.py -test $t;"
done



