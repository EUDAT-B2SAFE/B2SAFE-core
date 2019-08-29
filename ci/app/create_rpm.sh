#!/bin/bash
set -x
set -e
BUILD=$1

if [[ -z "$BUILD" ]]
then
    BUILD=0
fi

chown irods /var/lib/irods
sudo -u irods cp -r /build /src/B2SAFE-core
cd /src/B2SAFE-core/packaging
sudo -u irods ./create_rpm_package.sh $BUILD
chmod a+w /var/lib/irods/rpmbuild/RPMS/noarch/*.rpm



