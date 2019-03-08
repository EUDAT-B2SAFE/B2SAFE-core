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
INSTALL_CONF=${IRODS_PACKAGE_DIR}/packaging/install.json

if [ ! -e \$INSTALL_CONF ]
then

cat > \$INSTALL_CONF << EOF2
{
  "b2safe_package_dir": "${IRODS_PACKAGE_DIR}",
  "irods_conf_dir": "/etc/irods",
  "irods_dir": "/var/lib/irods/iRODS",
  "irods_default_resource": "demoResc",
  "cred_store_type": "os",
  "cred_file_path": "${IRODS_PACKAGE_DIR}/conf/credentials",
  "server_id": "irods://<fully_qualified_hostname>:1247",
  "server_api_reg": "irods://<fully_qualified_hostname>:1247",
  "server_api_pub": "irods://<fully_qualified_hostname>:1247",
  "handle_server_url": "https://epic6.storage.surfsara.nl:8003",
  "handle_private_key": "</path/prefix_suffix_index_privkey.pem>",
  "handle_certificate_only": "</path/prefix_suffix_index_certificate_only.pem>",
  "handle_prefix": "<ZZZ>",
  "handle_owner": "200:0.NA/<ZZZ>",
  "handle_reverse_lookup_name": "<ZZZ>",
  "handle_reverse_lookup_password": "<reverse_lookup_password>",
  "handle_https_verify": True,
  "handle_users": [ "user0#Zone0", "user1#Zone1" ],
  "log_level": "INFO",
  "log_directory": "/var/log/irods",
  "shared_space": "",
  "authz_enabled": true,
  "msg_queue_enabled": false
}
EOF2

fi


# show package installation/configuration info 
cat << EOF1

The package b2safe has been installed in ${IRODS_PACKAGE_DIR}.
To install/configure it in iRODS do following as the user who runs iRODS :

# update install.conf with correct parameters with your favorite editor
sudo vi ${IRODS_PACKAGE_DIR}/packaging/install.json

# install/configure it as the user who runs iRODS
source /etc/irods/service_account.config 
sudo su - \\\$IRODS_SERVICE_ACCOUNT_NAME -s "/bin/bash" -c "cd ${IRODS_PACKAGE_DIR}/packaging/ ; ./install.py"

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
