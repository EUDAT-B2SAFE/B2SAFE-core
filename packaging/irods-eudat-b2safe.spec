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
%define _irodsPackage /opt/eudat-b2safe
 
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
%{_irodsPackage}/rulebase
# attributes on files and directory's
%attr(-,%{_irodsUID},%{_irodsGID})   %{_irodsPackage}
%attr(700,%{_irodsUID},%{_irodsGID}) %{_irodsPackage}/cmd/*.py
%attr(600,%{_irodsUID},%{_irodsGID}) %{_irodsPackage}/conf/*.json
%attr(600,%{_irodsUID},%{_irodsGID}) %{_irodsPackage}/conf/*.conf
%attr(-,%{_irodsUID},%{_irodsGID}) /var/log/irods
%doc



%changelog
* Fri Feb 13 2015  Robert Verkerk <robert.verkerk@surfsara.nl> 3.0
- Add files to b2safe package
* Wed Jan 28 2015  Robert Verkerk <robert.verkerk@surfsara.nl> 3.0
- Initial version of b2safe
