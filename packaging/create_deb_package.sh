#!/bin/bash
#
#set -x

USERNAME=`whoami`
B2SAFEHOMEPACKAGING="$(cd $(dirname "$0"); pwd)"
B2SAFEHOME=`dirname $B2SAFEHOMEPACKAGING`
RPM_BUILD_ROOT="${HOME}/debbuild/"
RPM_SOURCE_DIR=$B2SAFEHOME
PRODUCT="irods-eudat-b2safe"
IRODS_PACKAGE_DIR=`grep -i _irodsPackage ${PRODUCT}.spec | head -n 1 | awk '{print $3}'`
# retrieve parameters from spec file. So we only have to update the spec file.
VERSION=`grep -i "^Version:" ${PRODUCT}.spec  | awk '{print $2}'`
RELEASE=`grep -i "^Release:" ${PRODUCT}.spec  | awk '{print $2}'`
PACKAGE="${PRODUCT}_${VERSION}-${RELEASE}"

if [ "$USERNAME" = "root" ]
then
	echo "We are NOT allowed to run as root, exit"
        echo "Run this script/procedure as the user who run's iRODS"
	exit 1
fi

# check existence of rpmbuild
which dpkg-deb > /dev/null 2>&1
STATUS=$?

if [ $STATUS -gt 0 ]
then
	echo "Please install dpkg-deb. It is not present at the machine"
	exit 1
fi 


# create build directory's
mkdir -p $RPM_BUILD_ROOT${PACKAGE}
rm -rf   $RPM_BUILD_ROOT${PACKAGE}/*

# create package directory's
mkdir -p $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/cmd
mkdir -p $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/conf
mkdir -p $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/packaging
mkdir -p $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/rulebase

# copy files and images
cp $RPM_SOURCE_DIR/cmd/*          $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/cmd
cp $RPM_SOURCE_DIR/conf/*         $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/conf
cp $RPM_SOURCE_DIR/packaging/install.sh $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/packaging
cp $RPM_SOURCE_DIR/rulebase/*     $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/rulebase
mkdir -p                          $RPM_BUILD_ROOT${PACKAGE}/var/log/irods

# set mode of specific files
chmod 700 $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/cmd/*.py
chmod 600 $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/conf/*.json
chmod 600 $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/conf/*.conf
chmod 700 $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/packaging/*.sh

# create packaging directory
mkdir -p  $RPM_BUILD_ROOT${PACKAGE}/DEBIAN

cat > $RPM_BUILD_ROOT${PACKAGE}/DEBIAN/control << EOF

Package: $PRODUCT
Version: ${VERSION}-${RELEASE}
Section: base
Priority: optional
Architecture: noarch
Depends: irods-icat (>= 4.0.0)
Maintainer: Robert Verkerk <robert.verkerk@surfsara.nl>
Description: B2SAFE for iRODS package
 B2SAFE is a robust, safe, and highly available service which allows
 community and departmental repositories to implement data management policies
 on their research data across multiple administrative domains in a trustworthy
 manner.

EOF


# build rpm
dpkg-deb --build $RPM_BUILD_ROOT${PACKAGE}

# done..
