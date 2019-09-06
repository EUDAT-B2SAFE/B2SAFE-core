#!/bin/bash

# default version
VERSION=centos7_4_2_6
CLEANUP="yes"
BUILD=0

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        "--nocleanup")
            CLEANUP="no"
            shift
            ;;
        "--url")
            shift
            GIT_URL=$1
            shift
            ;;
        "--branch")
            shift
            GIT_BRANCH=$1
            shift
            ;;
        "--build")
            shift
            BUILD=$1
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

set +x
source $(cd `dirname "${BASH_SOURCE[0]}"` && pwd)/version.sh
RPM_PACKAGE=`rpm_package $BUILD `
IRODS_VERSION=`irods_version $VERSION`
REPO_NAME=`repo_name $VERSION $GIT_URL $GIT_BRANCH `
EXEC="docker exec ${VERSION}_icat_1"
EXEC_IRODS="docker exec -u irods ${VERSION}_icat_1 "
set -x

# copy source tree
$EXEC cp -r /build /src/B2SAFE-core

# install RPM
$EXEC rpm -i /build/ci/RPMS/Centos/7/${REPO_NAME}/${RPM_PACKAGE}

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



