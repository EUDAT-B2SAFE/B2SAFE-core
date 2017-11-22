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
# retrieve parameters from local.re in tree
MAJOR_VERS=`grep "^\s*\*major_version" $B2SAFEHOME/rulebase/local.re | awk -F\" '{print $2}'`
MINOR_VERS=`grep "^\s*\*minor_version" $B2SAFEHOME/rulebase/local.re | awk -F\" '{print $2}'`
VERSION="${MAJOR_VERS}.${MINOR_VERS}"
RELEASE=`grep "^\s*\*sub_version" $B2SAFEHOME/rulebase/local.re | awk -F\" '{print $2}'`
PACKAGE="${PRODUCT}_${VERSION}-${RELEASE}"

if [ "$USERNAME" = "root" ]
then
	echo "We are NOT allowed to run as root, exit"
        echo "Run this script/procedure as any user except root"
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
mkdir -p $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/testRules

# copy files and images
cp $RPM_SOURCE_DIR/*.txt          $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}
cp $RPM_SOURCE_DIR/LICENSE        $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}
cp $RPM_SOURCE_DIR/cmd/*          $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/cmd
cp $RPM_SOURCE_DIR/conf/*         $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/conf
cp $RPM_SOURCE_DIR/packaging/install.sh $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/packaging
cp $RPM_SOURCE_DIR/rulebase/*     $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/rulebase
cp $RPM_SOURCE_DIR/rules/*        $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/testRules
mkdir -p                          $RPM_BUILD_ROOT${PACKAGE}/var/log/irods

# set mode of specific files
chmod 700 $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/cmd/*.py
chmod 600 $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/conf/*.json
chmod 600 $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/conf/*.conf
chmod 700 $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/packaging/*.sh

# create packaging directory
mkdir -p  $RPM_BUILD_ROOT${PACKAGE}/DEBIAN

# create control file
cat > $RPM_BUILD_ROOT${PACKAGE}/DEBIAN/control << EOF

Package: $PRODUCT
Version: ${VERSION}-${RELEASE}
Section: unknown
Priority: optional
Architecture: all
Depends: irods-icat (>= 4.0.0) | irods-server (>= 4.2.0)
Maintainer: Robert Verkerk <robert.verkerk@surfsara.nl>
Description: B2SAFE for iRODS package
 B2SAFE is a robust, safe, and highly available service which allows
 community and departmental repositories to implement data management policies
 on their research data across multiple administrative domains in a trustworthy
 manner.

EOF

# create config file to point to the config files
touch $RPM_BUILD_ROOT${PACKAGE}/DEBIAN/conffiles
for file in `find $RPM_BUILD_ROOT${PACKAGE}${IRODS_PACKAGE_DIR}/conf/  \( -name *.conf -o -name *.json \) -printf "%f "`
do
	echo "${IRODS_PACKAGE_DIR}/conf/$file" >> $RPM_BUILD_ROOT${PACKAGE}/DEBIAN/conffiles
done


# create postinstall scripts
cat > $RPM_BUILD_ROOT${PACKAGE}/DEBIAN/postinst << EOF
#!/bin/bash
# script for postinstall actions

# create configuration file if it does not exist yet
INSTALL_CONF=${IRODS_PACKAGE_DIR}/packaging/install.conf

if [ ! -e \$INSTALL_CONF ]
then

cat > \$INSTALL_CONF << EOF2
#
# parameters for installation of irods module B2SAFE
#
# the absolute directory where the irods config is installed
IRODS_CONF_DIR=/etc/irods
#
# the absolute directory where irods is installed
IRODS_DIR=/var/lib/irods
#
# the directory where B2SAFE is installed as a package
B2SAFE_PACKAGE_DIR=${IRODS_PACKAGE_DIR}
#
# the default iRODS resource to use. Will be set in core.re
DEFAULT_RESOURCE=demoResc
#
# epic credentials type and location
CRED_STORE_TYPE=os
CRED_FILE_PATH=\\\$B2SAFE_PACKAGE_DIR/conf/credentials
SERVER_ID="irods://<fully_qualified_hostname>:1247"
#
# epic credentials file usage parameters
#
# epicclient2 parameters
HANDLE_SERVER_URL=<https://epic3.storage.surfsara.nl:8001>
PRIVATE_KEY=</path/prefix_suffix_index_privkey.pem>
CERTIFICATE_ONLY=</path/prefix_suffix_index_certificate_only.pem>
PREFIX=<ZZZ>
HANDLEOWNER="200:0.NA/\\\$PREFIX"
REVERSELOOKUP_USERNAME=<ZZZ>
HTTPS_VERIFY="True"
#
# users for msiexec command
USERS="user0#Zone0 user1#Zone1"
#
# loglevel and log directory
# possible log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=DEBUG
LOG_DIR=/var/log/irods
#
#
# iRODS behavioral parameters
#
# check if user is authorized to perform several functions
AUTHZ_ENABLED=true
#
# check if message queue is enabled
MSG_QUEUE_ENABLED=false
#
EOF2

fi


# show package installation/configuration info 
cat << EOF1

The package b2safe has been installed in ${IRODS_PACKAGE_DIR}.
To install/configure it in iRODS do following as the user who runs iRODS :

# update install.conf with correct parameters with your favorite editor
sudo vi ${IRODS_PACKAGE_DIR}/packaging/install.conf

# install/configure it as the user who runs iRODS
source /etc/irods/service_account.config 
sudo su - \\\$IRODS_SERVICE_ACCOUNT_NAME -s "/bin/bash" -c "cd ${IRODS_PACKAGE_DIR}/packaging/ ; ./install.sh"

EOF1

# set owner of files to the user who run's iRODS
IRODS_SERVICE_ACCOUNT_CONFIG=/etc/irods/service_account.config
if [ -e \$IRODS_SERVICE_ACCOUNT_CONFIG ]
then
    source \$IRODS_SERVICE_ACCOUNT_CONFIG
    chown -R \$IRODS_SERVICE_ACCOUNT_NAME:\$IRODS_SERVICE_GROUP_NAME ${IRODS_PACKAGE_DIR} 
    chown -R \$IRODS_SERVICE_ACCOUNT_NAME:\$IRODS_SERVICE_GROUP_NAME /var/log/irods
fi

EOF

#make sure the file is executable
chmod +x  $RPM_BUILD_ROOT${PACKAGE}/DEBIAN/postinst


# build rpm
dpkg-deb --build $RPM_BUILD_ROOT${PACKAGE}

# done..
