#!/bin/bash

workdir=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
YUM_SERVER='software@software.irodspoc-sara.surf-hosted.nl'
SSH_OPTIONS='-oStrictHostKeyChecking=no'

docker build $workdir/centos7_b2handle -t b2handle
docker run -v $workdir/centos7_b2handle/dist:/opt/B2HANDLE/dist b2handle

rpm=$workdir/centos7_b2handle/dist/b2handle-*.noarch.rpm
rpm_file=$( basename $rpm )

for REPO_NAME in irods-4.1.11  irods-4.1.12  irods-4.2.3  irods-4.2.4  irods-4.2.5  irods-4.2.6
do
    ssh $SSH_OPTIONS $YUM_SERVER "mkdir -p /repos/CentOS/7/${REPO_NAME}/Packages/"
    scp $SSH_OPTIONS $rpm $YUM_SERVER:/repos/CentOS/7/${REPO_NAME}/Packages/$rpm_file
    ssh $SSH_OPTIONS $YUM_SERVER createrepo --update /repos/CentOS/7/${REPO_NAME}
done 

