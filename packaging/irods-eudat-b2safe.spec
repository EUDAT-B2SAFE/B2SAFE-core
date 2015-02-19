Name:		irods-eudat-b2safe
Version:	3.0
Release:	0
#Release:	1%{?dist}
Summary:	b2safe core application for iRODS v4

Group:		Application
License:	open BSD License
URL:		http://www.eudat.eu/b2safe
BuildArch:	noarch
#Source0:	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#BuildRequires:	
Requires:	irods-icat

%define _whoami %(whoami)
%define _irodsUID %(id -un `whoami`)
%define _irodsGID %(id -gn `whoami`)
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

cp $RPM_SOURCE_DIR/cmd/* $RPM_BUILD_ROOT%{_irodsPackage}/cmd
cp $RPM_SOURCE_DIR/conf/* $RPM_BUILD_ROOT%{_irodsPackage}/conf
cp $RPM_SOURCE_DIR/packaging/install.sh $RPM_BUILD_ROOT%{_irodsPackage}/packaging
cp $RPM_SOURCE_DIR/rulebase/* $RPM_BUILD_ROOT%{_irodsPackage}/rulebase
mkdir -p $RPM_BUILD_ROOT/var/log/irods

# cleanup
%clean
rm -rf %{buildroot}


#provide files to rpm. Set attributes 
%files
# default attributes
%defattr(-,%{_irodsUID},%{_irodsUID},-)
# files
%{_irodsPackage}/cmd
%{_irodsPackage}/conf
%{_irodsPackage}/packaging
%{_irodsPackage}/rulebase
# attributes on files and directory's
%attr(-,%{_irodsUID},%{_irodsGID})   %{_irodsPackage}
%attr(700,%{_irodsUID},%{_irodsGID}) %{_irodsPackage}/cmd/*.py
%attr(600,%{_irodsUID},%{_irodsGID}) %{_irodsPackage}/conf/*.json
%attr(600,%{_irodsUID},%{_irodsGID}) %{_irodsPackage}/conf/*.conf
%attr(700,%{_irodsUID},%{_irodsGID}) %{_irodsPackage}/packaging/*.sh
%attr(-,%{_irodsUID},%{_irodsGID}) /var/log/irods
%doc

%post
# create configuration file if it does not exist yet
INSTALL_CONF=%{_irodsPackage}/packaging/install.conf

if [ ! -e $INSTALL_CONF ]
then

cat > $INSTALL_CONF << EOF
#
# parameters for installation of irods module B2SAFE
#
# the absolute directory where the irods config is installed
IRODS_CONF_DIR=/etc/irods
#
# the absolute directory where irods is installed
IRODS_DIR=/var/lib/irods/iRODS
#
# the directory where B2SAFE will be stored as a package
B2SAFE_PACKAGE_DIR=%{_irodsPackage}
#
# the default iRODS resource to use. Will be set in core.re
DEFAULT_RESOURCE=demoResc
#
# credentials type and location
CRED_STORE_TYPE=os
CRED_FILE_PATH=\$B2SAFE_PACKAGE_DIR/conf/credentials
SERVER_ID="irods://<fully_qualified_hostname>:1247"
#
# epic usage parameters
BASE_URI="https://<fully_qualified_hostname_epic_server>/<instance>/handles/"
USERNAME=<username_for_prefix>
PREFIX=<prefix>
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
SHARED_SPACE=/Zone0/replicate

EOF

chown %{_irodsUID}:%{_irodsGID} $INSTALL_CONF

fi

# show actions to do after installation
cat << EOF

The package b2safe has been installed in %{_irodsPackage}.
To install/configure it in iRODS do following as the user %{_irodsUID} : 

su - %{_irodsUID}
cd %{_irodsPackage}/packaging
# update install.conf with correct parameters with your favorite editor
./install.sh

EOF

%changelog
* Fri Feb 13 2015  Robert Verkerk <robert.verkerk@surfsara.nl> 3.0
- Add files to b2safe package
* Wed Jan 28 2015  Robert Verkerk <robert.verkerk@surfsara.nl> 3.0
- Initial version of b2safe
