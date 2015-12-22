B2SAFE user attributes synchronization
===========

The objective of the scripts included here is the synchronization of the user attributes and accounts between the EUDAT B2ACCESS (https://b2access.eudat.eu:8443/home/home) service and the B2SAFE service.
The process is performed in two steps:

1. the script *remote_users_sync.py* downloads the user attributes from B2ACCESS admin interface and store them into two separate json documents which represents the local cache.
2. the script *user_sync.py* synchronize the local cache (two json files) with the iCAT DB (B2SAFE).

---------------
Deployment
---------------
Just download the directory and run the scripts as the B2SAFE admin user.

1. remote_users_sync.py conf/remote.users.sync.conf syncto EUDAT
2. user_sync.py conf/user.sync.conf sync 

---------------
Documentation
---------------
There are two configuration files:

1. $ cat conf/remote.users.sync.conf:
```
# section containing the common options
[Common]
logfile=remote.sync.log
# possible values: INFO, DEBUG, ERROR, WARNING
loglevel=INFO
usersfile=irods.remote.users
dnsfile=irods.DNs.map

[EUDAT]
host=https://unity.eudat-aai.fz-juelich.de:8443/rest-admin/v1/
username=
password=
carootdn= /C=DE/L=Juelich/O=FZJ/OU=JSC
ns_prefix=eudat_
```
Just add username/password of the unity REST admin interface

2. $ cat conf/user.sync.conf_example: 
```
# section containing the logging options
[Logging]
# possible values: INFO, DEBUG, ERROR, WARNING, CRITICAL
log_level=INFO
log_file=user.sync.log

# section containing the sources for users and projects/groups'information
[Sources]
project_file=irods.local.users
external_file=irods.remote.users
dn_map_file=irods.DNs.map
# set to "False" to define it false, set to "True" to set it to true
local_authoritative=False
# condition to filter the projects/groups to be added.
# Only triplets are allowed: (attribute, operator, value).
# Operators allowed are <,>,==,!=,<=,>=
# Only numeric attributes and values are supported
# Example: DiskQuota > 0
condition=

# section containing options for the notification system
[Notification]
# set to "False" to define it false, set to "True" to set it to true
notification_active=True
notification_sender=rodsmaster
notification_receiver=admin@email

# section containing options for iRODS operations
[iRODS]
internal_project_list=public,rodsadmin
irods_home_dir=/iRODSZoneName/home/
# if "False" the home directories for the sub-groups are not created.
irods_subgroup_home=False
# if "False" the home directory for the main group "EUDAT" is not created.
irods_group_home=True
irods_debug=False
```
The mechanism add new users and groups automatically, but does not delete them. 
Instead it notifies via email the *notification_receiver* that a user or a group should be removed.

---------------
FAQ
---------------
1. What if I want to download user attributes related to only few EUDAT groups?
 * remote_users_sync.py conf/remote.users.sync.conf syncto EUDAT -s group1,group2,group3
2. What if I want to merge my local users with those coming from the EUDAT B2ACCESS?
 * Just create the file *irods.local.users* which has the same syntax of the file *irods.remote.users*:
 ```
 $ cat irods.local.users
 {
    "EUDAT": {
        "groups": {
            "eudat_EUDAT-Staff": [
                "eudat_ultra-user",
                "eudat_75",
                "eudat_57"
            ]
        }
    }
 }
 ```
and set the parameter *local_authoritative*=**True**. In this way you are merging together user attributes defined locally with those defined remotely.
3. What if there are conflicts between EUDAT user names and local user names?
 * the *ns_prefix* parameter in the remote.users.sync.conf allow you to define a prefix to minimize the risk of conflicts.
