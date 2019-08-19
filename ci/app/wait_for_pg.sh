#!/bin/bash

RETRIES=10
PG_HOST=postgres
PG_USER=irods
PG_DATABASE=ICAT

err=1
while [ $err != 0 ]
do
    echo "attempt to connect to database"
    PGPASSWORD=test psql --user $PG_USER --host=$PG_HOST --command='\q' $PG_DATABASE
    err=$?
    RETRIES=$(( RETRIES - 1 ))
    if [ $err != 0 ];
    then
        if [ $RETRIES == 0 ]
        then
            echo "cannot connect to database"
            exit 8
        fi
        echo "failed: try again ($attempts attempts)"
        sleep 2;
    fi
done


