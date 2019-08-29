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

source $(cd `dirname "${BASH_SOURCE[0]}"` && pwd)/version.sh
RPM_PACKAGE=`rpm_package $BUILD `
IRODS_VERSION=`irods_version $VERSION`
REPO_NAME=`repo_name $VERSION $GIT_URL $GIT_BRANCH `

set -e
set -x

ssh $SSH_OPTIONS $YUM_SERVER "mkdir -p /repos/CentOS/7/${REPO_NAME}/Packages/"
scp $SSH_OPTIONS ./ci/RPMS/Centos/7/${REPO_NAME}/${RPM_PACKAGE} $YUM_SERVER:/repos/CentOS/7/${REPO_NAME}/Packages/
ssh $SSH_OPTIONS $YUM_SERVER createrepo --update /repos/CentOS/7/${REPO_NAME}
