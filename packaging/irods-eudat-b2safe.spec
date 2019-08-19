Name:		irods-eudat-b2safe
Version:	%{_version}
Release:	%{_release}
#Release:	1%{?dist}
Summary:	b2safe core application for iRODS v4

Group:		Application
License:	open BSD License
URL:		http://www.eudat.eu/b2safe
BuildArch:	noarch
#Source0:	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#BuildRequires:	
#Requires:	irods-icat or irods-server

%define _whoami %(whoami)
%define _b2safehomepackaging %(pwd)
%define _irodsPackage /opt/eudat/b2safe
 
%description
B2SAFE is a robust, safe, and highly available service which allows
community and departmental repositories to implement data management policies
on their research data across multiple administrative domains in a trustworthy
manner.


# get all our source code in the $RPM_SOURCE_DIR
%prep
echo "the spec file directory is %{_b2safehomepackaging}"
echo "The user that built this is %{_whoami}"
# create string where git repo is started..
workingdir=`pwd`
cd %{_b2safehomepackaging}
cd ..
b2safehome=`pwd`
cd $workingdir
# empty source directory and copy new files
rm -rf $RPM_SOURCE_DIR/*
cp -ar $b2safehome/* $RPM_SOURCE_DIR

# build images. We don't have to make them so exit
%build
exit 0


# put images in correct place
%install
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_irodsPackage}/cmd
mkdir -p $RPM_BUILD_ROOT%{_irodsPackage}/conf
mkdir -p $RPM_BUILD_ROOT%{_irodsPackage}/packaging
mkdir -p $RPM_BUILD_ROOT%{_irodsPackage}/rulebase
mkdir -p $RPM_BUILD_ROOT%{_irodsPackage}/testRules

cp $RPM_SOURCE_DIR/*.txt      $RPM_BUILD_ROOT%{_irodsPackage}
cp $RPM_SOURCE_DIR/LICENSE    $RPM_BUILD_ROOT%{_irodsPackage}
cp $RPM_SOURCE_DIR/cmd/*      $RPM_BUILD_ROOT%{_irodsPackage}/cmd
cp $RPM_SOURCE_DIR/conf/*     $RPM_BUILD_ROOT%{_irodsPackage}/conf
cp $RPM_SOURCE_DIR/packaging/install.py $RPM_BUILD_ROOT%{_irodsPackage}/packaging
cp $RPM_SOURCE_DIR/packaging/convert_b2safe_conf_to_json.sh $RPM_BUILD_ROOT%{_irodsPackage}/packaging
cp $RPM_SOURCE_DIR/rulebase/* $RPM_BUILD_ROOT%{_irodsPackage}/rulebase
cp $RPM_SOURCE_DIR/rules/*    $RPM_BUILD_ROOT%{_irodsPackage}/testRules
mkdir -p $RPM_BUILD_ROOT/var/log/irods

touch $RPM_BUILD_ROOT%{_irodsPackage}/cmd/toBeExcludedFile.pyc
touch $RPM_BUILD_ROOT%{_irodsPackage}/cmd/toBeExcludedFile.pyo

# cleanup
%clean
rm -rf %{buildroot}


#provide files to rpm. Set attributes 
%files
# default attributes
%defattr(-,-,-,-)
# files
# exclude .pyc and .pyo files
%exclude %{_irodsPackage}/packaging/*.pyc
%exclude %{_irodsPackage}/packaging/*.pyo
%exclude %{_irodsPackage}/cmd/*.pyc
%exclude %{_irodsPackage}/cmd/*.pyo
%exclude %{_irodsPackage}/cmd/Pipefile
%exclude %{_irodsPackage}/cmd/Pipefile.lock
%exclude %{_irodsPackage}/cmd/logs

#include files
%{_irodsPackage}/cmd
%{_irodsPackage}/conf
%{_irodsPackage}/packaging
%{_irodsPackage}/rulebase
%{_irodsPackage}/testRules
# attributes on files and directory's
%attr(-,-,-)   %{_irodsPackage}
%attr(700,-,-) %{_irodsPackage}/cmd/*.py
%attr(600,-,-) %{_irodsPackage}/conf/*.json
%attr(600,-,-) %{_irodsPackage}/conf/*.conf
%attr(700,-,-) %{_irodsPackage}/packaging/*.sh
%attr(700,-,-) %{_irodsPackage}/packaging/*.py
%attr(-,-,-)   /var/log/irods
%doc
# config files
%config(noreplace) %{_irodsPackage}/conf/*.json
%config(noreplace) %{_irodsPackage}/conf/*.conf


%post
# create configuration file if it does not exist yet
INSTALL_CONF=%{_irodsPackage}/packaging/install.json

if [ ! -e $INSTALL_CONF ]
then

cat > $INSTALL_CONF << EOF
{
  "b2safe_package_dir": "%{_irodsPackage}",
  "irods_conf_dir": "/etc/irods",
  "irods_dir": "/var/lib/irods",
  "irods_default_resource": "demoResc",
  "cred_store_type": "os",
  "cred_file_path": "%{_irodsPackage}/conf/credentials",
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
  "handle_https_verify": "True",
  "handle_users": [ "user0#Zone0", "user1#Zone1" ],
  "handle_groups": [],
  "log_level": "INFO",
  "log_directory": "/var/log/irods",
  "shared_space": "",
  "authz_enabled": true,
  "msg_queue_enabled": false
}
EOF

fi

# show actions to do after installation
cat << EOF

The package b2safe has been installed in %{_irodsPackage}.
To install/configure it in iRODS do following as the user who runs iRODS :

# update install.conf with correct parameters with your favorite editor
sudo vi %{_irodsPackage}/packaging/install.json

# install/configure it as the user who runs iRODS
source /etc/irods/service_account.config 
sudo su - \$IRODS_SERVICE_ACCOUNT_NAME -s "/bin/bash" -c "cd %{_irodsPackage}/packaging/ ; ./install.py"

EOF

# set owner of files to the user who run's iRODS
IRODS_SERVICE_ACCOUNT_CONFIG=/etc/irods/service_account.config
if [ -e $IRODS_SERVICE_ACCOUNT_CONFIG ]
then
    source $IRODS_SERVICE_ACCOUNT_CONFIG
    chown -R $IRODS_SERVICE_ACCOUNT_NAME:$IRODS_SERVICE_GROUP_NAME %{_irodsPackage}
    chown -R $IRODS_SERVICE_ACCOUNT_NAME:$IRODS_SERVICE_GROUP_NAME /var/log/irods
fi


%changelog
* Wed Jul 24 2019  Stefan Wolfsheimer <stefan.wolfsheimer@surfsara.nl> 4.2.1
- exclude python object files, fix install.json
* Tue Mar 26 2019  Robert Verkerk <robert.verkerk@surfsara.nl> 4.2.1
- add python installation/setup script.
* Fri Mar 8 2019  Robert Verkerk <robert.verkerk@surfsara.nl> 4.2.1
- add new parameters. Convert to json input file for configuration.
* Thu Nov 22 2018  Robert Verkerk <robert.verkerk@surfsara.nl> 4.2.0
- add new parameters.
* Wed Nov 22 2017  Robert Verkerk <robert.verkerk@surfsara.nl> 4.0.1
- remove obsolete parameters. Only support epicclient2.py
* Tue Apr 18 2017  Robert Verkerk <robert.verkerk@surfsara.nl> 4.0.0
- update for better info. Remove requires. iRODS can be in 2 different packages.
* Fri Nov 20 2015  Robert Verkerk <robert.verkerk@surfsara.nl> 3.0.0
- set owner of files during installation of rpm.
* Fri Oct 23 2015  Robert Verkerk <robert.verkerk@surfsara.nl> 3.0.0
- remove docs directory.
* Thu Oct 15 2015  Robert Verkerk <robert.verkerk@surfsara.nl> 3.0
- add extra files and create docs directory, specify config files.
* Tue Jul 07 2015  Robert Verkerk <robert.verkerk@surfsara.nl> 3.0
- assign version of package at build time with input parameters 
* Fri Feb 13 2015  Robert Verkerk <robert.verkerk@surfsara.nl> 3.0
- Add files to b2safe package
* Wed Jan 28 2015  Robert Verkerk <robert.verkerk@surfsara.nl> 3.0
- Initial version of b2safe
