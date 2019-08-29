#!/bin/bash
#
set -e
set -x

BUILD=$1
if [[ -z "$BUILD" ]]
then
    BUILD=0
fi

USERNAME=`whoami`

if [ "$USERNAME" = "root" ]
then
	echo "We are NOT allowed to run as root, exit"
        echo "Run this script/procedure as any user except root"
	exit 1
fi

# check existence of rpmbuild
which rpmbuild > /dev/null 2>&1
STATUS=$?

if [ $STATUS -gt 0 ]
then
	echo "Please install rpmbuild. It is not present at the machine"
	exit 1
fi 



# create build directory's
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# create rpm macro's if they do not exist
if [ -e ~/.rpmmacros ]
then
	echo "~/.rpmmacros already exist. NOT overwritten"
else
	echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros
fi

# find directory where we are executing:
ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)

#extract major_version, minor_version and subversion from local.re in tree
MAJOR_VERS=`grep "^\s*\*major_version" $ABSOLUTE_PATH/../rulebase/local.re | awk -F\" '{print $2}'`
MINOR_VERS=`grep "^\s*\*minor_version" $ABSOLUTE_PATH/../rulebase/local.re | awk -F\" '{print $2}'`
SUB_VERS=`grep "^\s*\*sub_version" $ABSOLUTE_PATH/../rulebase/local.re | awk -F\" '{print $2}'`
VERSION="${MAJOR_VERS}.${MINOR_VERS}.${SUB_VERS}"

# build rpm
rpmbuild -ba --define "_version $VERSION" --define "_release $BUILD" irods-eudat-b2safe.spec

# done..
