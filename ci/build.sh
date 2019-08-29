#!/bin/bash

VERSION=centos7_4_2_6
CLEANUP="yes"
BUILD=0
GIT_BRANCH=""
GIT_URL=""

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

cleanup () {
    exit_code=$?
    docker-compose -f ci/${VERSION}/docker-compose.yml down -v
    exit $exit_code
}

set -x
set -e

trap cleanup EXIT ERR INT TERM

source $(cd `dirname "${BASH_SOURCE[0]}"` && pwd)/version.sh
RPM_PACKAGE=`rpm_package $BUILD `
IRODS_VERSION=`irods_version $VERSION`
REPO_NAME=`repo_name $VERSION $GIT_URL $GIT_BRANCH `


mkdir -p ci/RPMS/Centos/7/${REPO_NAME}

docker-compose -f ci/${VERSION}/docker-compose.yml build
docker-compose -f ci/${VERSION}/docker-compose.yml up -d

docker exec ${VERSION}_icat_1 /app/create_rpm.sh $BUILD

docker exec ${VERSION}_icat_1 bash -c "set -x; set -e; cp /var/lib/irods/rpmbuild/RPMS/noarch/${RPM_PACKAGE} /build/ci/RPMS/Centos/7/${REPO_NAME};" 
