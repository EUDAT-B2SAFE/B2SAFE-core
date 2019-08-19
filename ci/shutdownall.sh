#!/bin/bash

set -x

for VERSION in centos7_4_2_6 centos7_4_1_12
do
    docker-compose -f ci/${VERSION}/docker-compose.yml down -v
done
