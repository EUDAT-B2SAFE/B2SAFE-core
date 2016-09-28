Name:		nagios-plugins-eudat-b2safe
Version:	%{_version}
Release:	%{_release}
#Release:	1%{?dist}
Summary:	nagios probe for b2safe

Group:		Application
License:	open BSD License
URL:		http://www.eudat.eu/b2safe
BuildArch:	noarch
#Source0:	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#BuildRequires:	
Requires:	irods-icommands

%define _whoami %(whoami)
%define _b2safehomepackaging %(pwd)
%define _b2safeNagiosPackage /usr/libexec/argo-monitoring/probes/eudat-b2safe
%define _b2safeNagiosTmp     /var/lib/argo-monitoring/eudat-b2safe
%define _b2safeNagiosConfig  /etc/nagios/plugins/eudat-b2safe

%description
This nagios plugin provides the nessecary scripts and config files to test
 b2safe/iRODS.


# get all our source code in the $RPM_SOURCE_DIR
%prep
echo "the spec file directory is %{_b2safehomepackaging}"
echo "The user that built this is %{_whoami}"
# create string where git repo is started..
workingdir=`pwd`
cd %{_b2safehomepackaging}
cd ../irods
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
mkdir -p $RPM_BUILD_ROOT%{_b2safeNagiosPackage}
mkdir -p $RPM_BUILD_ROOT%{_b2safeNagiosTmp}
mkdir -p $RPM_BUILD_ROOT%{_b2safeNagiosConfig}

cp $RPM_SOURCE_DIR/*.sh         $RPM_BUILD_ROOT%{_b2safeNagiosPackage}
cp $RPM_SOURCE_DIR/*.json       $RPM_BUILD_ROOT%{_b2safeNagiosConfig}
cp $RPM_SOURCE_DIR/irods_passwd $RPM_BUILD_ROOT%{_b2safeNagiosConfig}


# cleanup
%clean
rm -rf %{buildroot}

#provide files to rpm. Set attributes 
%files
# default attributes
%defattr(-,-,-,-)
# files
#include files
%{_b2safeNagiosPackage}
%{_b2safeNagiosTmp}
%{_b2safeNagiosConfig}
# attributes on files and directory's
%attr(-,nagios,nagios)   %{_b2safeNagiosPackage}
%attr(-,nagios,nagios)   %{_b2safeNagiosTmp}
%attr(-,nagios,nagios)   %{_b2safeNagiosConfig}
%attr(750,nagios,nagios) %{_b2safeNagiosPackage}/*.sh
%attr(600,nagios,nagios) %{_b2safeNagiosConfig}/*.json
%attr(600,nagios,nagios) %{_b2safeNagiosConfig}/irods_passwd
%doc
# config files
%config(noreplace) %{_b2safeNagiosConfig}/*.json
%config(noreplace) %{_b2safeNagiosConfig}/irods_passwd


%post
%changelog
* Tue Jul 26 2016  Robert Verkerk <robert.verkerk@surfsara.nl> 1.0
- Initial version of b2safe nagios plugin
