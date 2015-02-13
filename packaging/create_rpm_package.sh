#!/bin/bash
#
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
