#!/bin/bash
/app/wait_for_pg.sh
set -x
set -e

if [ -f /etc/irods/service_account.config ]
then
    echo 'setup without service account'
    cat /app/setup_answers.txt | /var/lib/irods/packaging/setup_irods.sh
else
    ( echo irods
      echo irods
      cat /app/setup_answers.txt
    ) | /var/lib/irods/packaging/setup_irods.sh
fi

/app/sleep.sh
