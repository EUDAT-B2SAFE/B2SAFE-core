#!/bin/bash
#
USERNAME=`whoami`

if [ "$USERNAME" = "root" ]
then
	echo "We are NOT allowed to run as root, exit"
        echo "Run this script/procedure as the user who run's iRODS"
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

# build rpm
rpmbuild -ba irods-eudat-b2safe.spec

# done..
