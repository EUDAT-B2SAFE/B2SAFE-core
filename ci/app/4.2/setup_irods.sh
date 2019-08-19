#!/bin/bash
/app/wait_for_pg.sh

set -x

if [ -e  /var/lib/irods/iRODS/Vault/home ]
then
    echo "irods already installed"
    /etc/init.d/irods start
else
    cat /app/setup_answers.txt | python /var/lib/irods/scripts/setup_irods.py
fi

/app/sleep.sh
